import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    rows_users = db.execute("SELECT * FROM users WHERE id = :userid",
                            userid=session["user_id"]) # usersの行
    rows_stock = db.execute("SELECT * FROM :stockinfo",
                            stockinfo="stockinfo{}".format(str(session["user_id"])))
    for i in range(len(rows_stock)):
        quote = lookup(rows_stock[i]["stocksymbol"]) # 株式情報を取得
        rows_stock[i]["price"] = quote["price"] # 現在価格を格納

    if len(rows_stock) != 0: # 記録があったら、
        return render_template("index.html", username=rows_users[0]["username"], cash=rows_users[0]["cash"], stocks=rows_stock)
    else:
        return render_template("index.html", username=rows_users[0]["username"], cash=rows_users[0]["cash"])


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    rows_users = db.execute("SELECT * FROM users WHERE id = :userid",
                                userid=session["user_id"]) # 入力者のデータベースを選択
    if request.method == "POST":
        if not request.form.get("stocksymbol"): # 銘柄記号が入力されていない場合、
            return apology("Missing Symbol!")
        elif not request.form.get("numstock"): # 株式数が入力されていない場合、
            return apology("Missing numstock!")
        elif not str(request.form.get("numstock")).isdigit(): # 株式数が数字でない場合、
            return apology("numstock is numerical!")

        cash_added  = int(rows_users[0]["cash"]) + int(request.form["addcash"]) # 入力されたキャッシュを足しておく
        quote       = lookup(request.form["stocksymbol"]) # 株式情報を取得
        price_buy   = int(request.form["numstock"]) * int(quote["price"]) # 購入額を計算
        cash_bought = cash_added - price_buy # 購入後のキャッシュを計算

        if int(request.form["numstock"]) <= 0 or int(request.form["addcash"]) < 0:
            return apology("Numstock or Addcash is negative")
        if cash_added < price_buy: # キャッシュが購入額より少なかったら、
            return apology("Cash is lack")
        db.execute("INSERT INTO :stockinfo (stocksymbol, stockname, numstock, curprice, totalamount) VALUES(:symbol, :name, :numstock, :curprice, :totalprice);",
                    stockinfo="stockinfo{}".format(str(session["user_id"])),
                    symbol=request.form["stocksymbol"], name=quote["name"], numstock=request.form["numstock"],
                    curprice=quote["price"], totalprice=price_buy) # 所有株式DBに追加
        db.execute("INSERT INTO :history (tradingcategory, stocksymbol, stockname, numstock, price, totalamount, date_time) VALUES('BUY', :symbol, :name, :numstock, :price, :totalprice, :date_time);",
                    history="history{}".format(str(session["user_id"])),
                    symbol=request.form["stocksymbol"], name=quote["name"], numstock=request.form["numstock"],
                    price=quote["price"], totalprice=price_buy,
                    date_time=str(datetime.datetime.now(datetime.timezone.utc))) # 売買履歴DBに追加
        db.execute("UPDATE users SET cash = :cash WHERE id = :userid;",
                    cash=cash_bought, userid=str(session["user_id"])) # 足したキャッシュと購入額をDBに反映

        return redirect("/")
    else: # POST送信ではない場合、
        return render_template("buy.html", cash=rows_users[0]["cash"])


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    username     = request.form["username"]
    password     = request.form["password"]
    confirmation = request.form["confirmation"]
    checkname    = db.execute("SELECT * FROM users WHERE username = :username", username=username)
    if len(username) == 0: # ユーザー名が入力されていない場合、
        # return apology("must provide username")
        return jsonify(False)
    if len(password) == 0: # パスワードが入力されていない場合、
        # return apology("must provide password")
        return jsonify(False)
    if str(password) != str(confirmation): # パスワードが一致しない場合、
        # return apology("passwords in disagreement")
        return jsonify(False)
    if len(checkname) > 0: # 既に登録済みだったら
        return jsonify(False) # Falseを返す。

    return jsonify(True)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows_users   = db.execute("SELECT * FROM users WHERE id = :userid",
                            userid=session["user_id"]) # usersの行
    rows_history = db.execute("SELECT * FROM :history",
                              history="history{}".format(str(session["user_id"])))
    return render_template("history.html", username=rows_users[0]["username"], histories=rows_history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        quote = lookup(request.form["stocksymbol"])
        # dict_stock = {"name":1, "price":2, "symbol":3} # テスト
        # return render_template("quote.html", name=dict_stock["name"], price=dict_stock["price"], symbol=dict_stock["symbol"])
        return render_template("quote.html", symbol=quote["symbol"], name=quote["name"], price=quote["price"])
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    return render_template("register.html") # 登録画面に進む

@app.route("/registered", methods=["GET", "POST"])
def registered():
    """Registered user"""
    if request.method == "POST":
        username     = request.form.get("username")
        password     = request.form.get("password")
        confirmation = request.form.get("confirmation")
        checkname    = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        if len(username) == 0:
            return apology("must provide username")
        if len(password) == 0:
            return apology("must provide password")
        if str(password) != str(confirmation):
            return apology("passwords in disagreement")
        if len(checkname) > 0:
            return apology("Username is taken")

        db.execute("INSERT INTO users(username, hash, cash) VALUES(:t_username, :t_hash, 0)",
                    t_username=request.form.get("username"), t_hash=generate_password_hash(request.form.get("password"))) # 入力値をDBに格納する。
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        db.execute("CREATE TABLE :stockinfo ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'stocksymbol' TEXT NOT NULL, 'stockname' TEXT NOT NULL, 'numstock' INTEGER NOT NULL, 'curprice' INTEGER NOT NULL, 'totalamount' INTEGER NOT NULL);",
                    stockinfo="stockinfo{}".format(str(rows[0]["id"])))
        db.execute("CREATE TABLE :history ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'tradingcategory' TEXT NOT NULL, 'stocksymbol' TEXT NOT NULL, 'stockname' TEXT NOT NULL, 'numstock' INTEGER NOT NULL, 'price' INTEGER NOT NULL, 'totalamount' INTEGER NOT NULL, 'date_time' TEXT NOT NULL);",
                    history="history{}".format(str(rows[0]["id"])))
        return render_template("registered.html") # 登録済画面に進む
    else: # POST送信ではない場合、
        return render_template("login.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    rows_users = db.execute("SELECT * FROM users WHERE id = :userid",
                                userid=session["user_id"]) # 入力者のデータベースを選択
    rows_stock = db.execute("SELECT * FROM :stockinfo",
                            stockinfo="stockinfo{}".format(str(session["user_id"])))
    if request.method == "POST":
        if not request.form.get("stocksymbol"): # 銘柄記号が入力されていない場合、
            return apology("Missing Symbol!")
        elif not request.form.get("numstock"): # 株式数が入力されていない場合、
            return apology("Missing numstock!")
        elif not str(request.form.get("numstock")).isdigit(): # 株式数が数字でない場合、
            return apology("numstock is numerical!")

        quote      = lookup(request.form["stocksymbol"]) # 株式情報を取得
        price_sell = int(request.form["numstock"]) * int(quote["price"]) # 売却額を計算
        cash_sold  = int(rows_users[0]["cash"]) + price_sell # 売却後のキャッシュを計算

        if int(request.form["numstock"]) <= 0: # 株式数が0の場合、
            return apology("Numstock is negative")
        i = 0
        while(i < len(rows_stock)): # 保有株式リストを走査、
            if str(rows_stock[i]["stocksymbol"]) == str(request.form["stocksymbol"]): # 銘柄記号がDBにあったら、
                break
            if i == len(rows_stock): # 選択した株式を持っていなかったら、
                return apology("You have no that stock")
            i += 1

        numstock_sold = int(rows_stock[i]["numstock"]) - int(request.form["numstock"]) # 保有株式数 - 売却株式数
        if numstock_sold == 0: # 残保有株式が0になったら、
            db.execute("DELETE FROM :stockinfo WHERE stocksymbol = :symbol;",
                        stockinfo="stockinfo{}".format(str(session["user_id"])),
                        symbol=request.form["stocksymbol"]) # 所有株式DBから削除
        else: # 残っていたら、
            db.execute("UPDATE :stockinfo SET numstock = :numstock WHERE stocksymbol = :symbol;",
                        stockinfo="stockinfo{}".format(str(session["user_id"])),
                        numstock=numstock_sold,
                        symbol=request.form["stocksymbol"]) # 保有株式数を減らす
        db.execute("INSERT INTO :history (tradingcategory, stocksymbol, stockname, numstock, price, totalamount, date_time) VALUES('SELL',:symbol, :name, :numstock, :price, :totalprice, :date_time);",
                    history="history{}".format(str(session["user_id"])),
                    symbol=request.form["stocksymbol"], name=quote["name"], numstock=request.form["numstock"],
                    price=quote["price"], totalprice=price_sell,
                    date_time=str(datetime.datetime.now(datetime.timezone.utc))) # 売買履歴DBに追加
        db.execute("UPDATE users SET cash = :cash WHERE id = :userid;",
                    cash=cash_sold, userid=str(session["user_id"])) # 売却額をDBに反映

        return redirect("/")
    else: # POST送信ではない場合、
        list_symbols = []
        for i in rows_stock:
            list_symbols.append(i["stocksymbol"])
        return render_template("sell.html", symbols=list_symbols, cash=rows_users[0]["cash"])


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
