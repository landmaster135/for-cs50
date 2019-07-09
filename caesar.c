#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    if (argc != 2) //number of argument is two.
    {
        printf("number of argument is two.\n");
        return 1;
    }
    
    
    for (int i = 0, charlen = strlen(argv[1]); i < charlen; i++) //loop on length of argv[1].
    {
        if (!(isdigit(argv[1][i]))) //argv[1] is integer.
        {
            printf("argc is integer.\n");
            return 1;
        }
    }
    
    int k = argc; //number of shifting
    string plaintext = get_string("plaintext is: "); //prompt plaintext
    printf("ciphertext: ");
    
    for (int i = 0, textLen = strlen(plaintext); i < textLen; i++) //loop in the length of text
    {
        int asciiNum = plaintext[i]; //convert plaintext to ASCII code
        if (asciiNum >= 'A' && asciiNum <= 'Z') //case of uppercase letter
        {
            asciiNum = (asciiNum + k - 'A') % 26 + 'A'; //shift by k
        }
        else if (asciiNum >= 'a' && asciiNum <= 'z') //case of lowercase letter
        {
            asciiNum = (asciiNum + k - 'a') % 26 + 'a'; //shift by k
        }
        printf("%c", asciiNum); //convert shifted number array for encrypted message.
    }
    printf("\n");
}
