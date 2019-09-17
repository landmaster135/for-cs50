#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define jpeg_signsize 3

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        // ensure proper usage.
        printf("Usage: ./recover image");
        return 1;
    }
    char *infile = argv[1];
    // open memory card file.
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        printf("%s is not existing.\n", "card.raw");
        return 1;
    }
    
    FILE *outptr = NULL;
    
    // create 512 byte buffer array.
    unsigned char buffer[512];
    
    // the first 3 bytes of a jpg file.
    unsigned char jpg_sign[jpeg_signsize] = {0xff, 0xd8, 0xff};
    
    int jpg_num = 0; // keep track of jpg numbers.
    char jpg_name[9]; // jpg filenames.
    
    // read a buffer from card.raw until EOF
    while (fread(&buffer, sizeof(buffer), 1, inptr) > 0)
    {	
        // if jpg signature is found
        if (memcmp(buffer, jpg_sign, sizeof(jpg_sign)) == 0)
        {
            if (outptr == NULL) //jpeg is none yet.
            {
                //open a new jpeg file.
                sprintf(jpg_name, "%04d.jpg", jpg_num);
                outptr = fopen(jpg_name, "a");
                fwrite(&buffer, sizeof(buffer), 1, outptr);
            }
            // a jpg is already open.
            else
            {
                fclose(outptr);
                jpg_num++;
                sprintf(jpg_name, "%04d.jpg", jpg_num);
                outptr = fopen(jpg_name, "a");
                fwrite(&buffer, sizeof(buffer), 1, outptr);
            }
        }
        
        else
        {
            // a jpg is already open.
            if (outptr != NULL)
            {
                fwrite(&buffer, sizeof(buffer), 1, outptr);
            }
        }
    }
    
    // close files and exit cleanly
    fclose(inptr);
    fclose(outptr);
    return 0;
}
