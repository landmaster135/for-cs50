#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int asciiShift(int asciiNum, int key, int occation);

int main(int argc, string argv[])
{
    if (argc != 2) //number of argument is two.
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }
    
    int charlen = strlen(argv[1]);
    int key[charlen]; //number of shifting
    int asciiNum; //convert text to ASCII code
    for (int i = 0; i < charlen; i++) //loop on length of argv[1].
    {
        if (isalpha(argv[1][i])) //argv[1] is alphabet.
        {
            asciiNum = argv[1][i];
            key[i] = asciiShift(asciiNum, 0, 0);; //store as ascii code
        }
        else
        {
            printf("Usage: ./vigenere keyword\n");
            return 1;
        }
    }
    
    string plaintext = get_string("plaintext is: "); //prompt plaintext
    printf("ciphertext: ");
    
    for (int i = 0, textLen = strlen(plaintext); i < textLen; i++) //loop in the length of text
    {
        asciiNum = plaintext[i]; //convert plaintext to ASCII code
        printf("%c", asciiShift(asciiNum, key[i % charlen], 1)); //convert to shifted number array for encrypted message.
    }
    printf("\n");
}

int asciiShift(int asciiNum, int key, int occation)
{
    if (asciiNum >= 'A' && asciiNum <= 'Z') //case of uppercase letter
    {
        asciiNum = (asciiNum + key - 'A') % 26; //convert to key OR shift by key
        if (occation == 0)
        {
            //nothing to do
        }
        else if (occation == 1)
        {
            asciiNum = asciiNum + 'A';
        }
    }
    else if (asciiNum >= 'a' && asciiNum <= 'z') //case of lowercase letter
    {
        asciiNum = (asciiNum + key - 'a') % 26; //convert to key OR shift by key
        if (occation == 0)
        {
            //nothing to do
        }
        else if (occation == 1)
        {
            asciiNum = asciiNum + 'a';
        }
    }
    return asciiNum;
    
}
