from cs50 import get_string
from sys import argv


def main():

    argc = len(argv)

    if argc != 2:  # number of argument is two.
        print("number of argument is two without 'python'.\n")  # ERROR message.
        exit(1)

    if argv[1][-4:] != ".txt":
        print('third argument is type of ".txt".\n')  # ERROR message.
        exit(1)

    inp = input('What message would you like to censor?\n')  # Prompt message.


    inp_list = inp.split(' ')  # seperate message.

    file_name = argv[1]  # for reading file.
    ban_lines = ''  # for replace banned.txt.

    with open(file_name, encoding="cp932") as f:  # read file.
        ban_lines = f.read()

    ban_list = ban_lines.split('\n')  # seperate text from banned.txt.

    for i1 in inp_list:  # for all input words.
        i2 = i1 # (replace input word to other variable)
        if i1.islower() == False: # (transfer upper to lower)
            i1 = i1.lower()
        if i1 in ban_list:  # if input word is banned word,
            inp_list[inp_list.index(i2)] = '*' * len(i2)  # tokenize message.
        else:
            pass


    print(' '.join(inp_list))   # print tokenized message.


if __name__ == "__main__":
    main()
