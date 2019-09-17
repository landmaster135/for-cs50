import sys

args = sys.argv
argc = len(args)


def asciiShift(asciiNum, key, occation):
    if (asciiNum >= ord('A') and asciiNum <= ord('Z')):  # case of uppercase letter
        asciiNum = (asciiNum + key - ord('A')) % 26  # shift by key
        if (occation == 0):
            pass  # nothing to do
        elif(occation == 1):
            asciiNum += ord('A')
    elif (asciiNum >= ord('a') and asciiNum <= ord('z')):  # case of lowercase letter
        asciiNum = (asciiNum + key - ord('a')) % 26  # shift by key
        if (occation == 0):
            pass  # nothing to do
        elif(occation == 1):
            asciiNum += ord('a')
    return asciiNum


def main():
    if (argc != 2):  # number of argument is two.
        print("number of argument is two.\n")
        sys.exit()

    charlen = len(args[1])
    key = []
    asciiNum = 0
    for i in args[1]:  # loop on length of args[1]
        if (str.isalpha(i)):  # args[1] is integer.
            asciiNum = ord(i)
            key += [asciiShift(asciiNum, 0, 0)]  # store as ascii code
        else:
            print("argc is integer.\n")
            sys.exit()

    plaintext = None
    ciphertext = ''
    while (plaintext == None or plaintext == ''):
        plaintext = input('plaintext is...  ')

    j = 0
    for i in plaintext:  # loop in the length of text
        asciiNum = ord(i)  # convert plaintext to ASCII code
        # convert shifted number array for encrypted message.
        ciphertext += chr(asciiShift(asciiNum, key[plaintext.index(i) % charlen], 1))

    print('ciphertext: ' + ciphertext + '\n')  # print encrypted message.


main()
