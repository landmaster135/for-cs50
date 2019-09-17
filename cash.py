import sys
import math


coins = [25, 10, 5, 1]  # kind of usable coins
counts = [0, 0, 0, 0]  # count coins


def now_coin(rest):  # max coin of cash owed currently.
    for i in coins:
        if (rest >= i):  # rest is larger than coin
            return int(i)
        else:  # rest is smaller than coin
            pass


cash = float(input('Change owed: '))  # prompt Change owed.
if not (isinstance(cash, float)):  # cash owed is float type.
    print("prompt by float type.\n")
    sys.exit()  # ERROR

cash = cash * 100 % 100  # extract only sum of coin.
max_coin = 0  # largest coin currently
sum = 0  # sum of coins

while (int(cash) != 0):  # while cash owed is 0.
    max_coin = now_coin(cash)
    cash -= max_coin  # decrease cash owed.
    counts[coins.index(max_coin)] += 1  # increase coin count.

for i in counts:  # count all coins.
    sum += i
print('number of coin is {}'.format(sum))
