import sys

args = sys.argv
argc = len(args)


def main():

    if (argc != 2):  # number of argument is two.
        print("number of argument is two.\n")
        sys.exit()

    for i in args[1]:  # loop on length of args[1]
        if not(str.isdigit(i)):  # args[1] is integer.
            print("argc is integer.\n")
            sys.exit()

    k = int(args[1])
    plaintext = None
    ciphertext = ''
    while (plaintext == None or plaintext == ''):
        plaintext = input('plaintext is...  ')

    for j in plaintext:   # loop in the length of text
        asciiNum = ord(j)   # convert plaintext to ASCII code
        if (asciiNum >= ord('A') and asciiNum <= ord('Z')):  # case of uppercase letter
            asciiNum = (asciiNum + k - ord('A')) % 26 + ord('A')  # shift by k
        elif (asciiNum >= ord('a') and asciiNum <= ord('z')):  # case of lowercase letter
            asciiNum = (asciiNum + k - ord('a')) % 26 + ord('a')  # shift by k
        ciphertext += chr(asciiNum)

    print('ciphertext: ' + ciphertext + '\n')  # convert shifted number array for encrypted message.

    return 0


main()
