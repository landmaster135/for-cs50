#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int hundred_check(int number);

int ma#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{    
    if (argc != 4)
    {
        printf("Usage: ./resize n infile outfile\n");
        return 1;
    }
    
    //remember number to multiplying
    int multi = atoi(argv[1]);
    if (multi < 1 || multi > 100)
    {
        printf("Scale must be between 1 and 100\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        printf("Could not open %s.\n", infile);
        return 2;
    }    
    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        printf("Could not create %s.\n", outfile);
        return 3;
    }
    
    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    
    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        printf("Unsupported file format.\n");
        return 4;
    }

    // create outfile's BITMAPFILEHEADER and BITMAPINFOHEADER
    BITMAPFILEHEADER obf = bf;
    BITMAPINFOHEADER obi = bi;

    // rescale outfile's dimension
    obi.biWidth *= multi;
    obi.biHeight *= multi;
    
    // determine padding for scanlines of both infile and outfile
    int in_padding =  (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int out_padding = (4 - (obi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    
    // determine the outfile's biSizeImage
    obi.biSizeImage = abs(obi.biHeight) * (obi.biWidth * sizeof(RGBTRIPLE) + out_padding);
    // determine the outfile's bfSize (biSizeImage + 54 bytes header files)
    obf.bfSize = (obi.biSizeImage + 54);
    
    // write outfile's BITMAPFILEHEADER
    fwrite(&obf, sizeof(BITMAPFILEHEADER), 1, outptr);
    // write outfile's BITMAPINFOHEADER
    fwrite(&obi, sizeof(BITMAPINFOHEADER), 1, outptr);
    
    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // iterate over infile's pixels in a scanline
        for (int j = 0; j < multi; j++)
        {
            // set pointer to start of line(infile's stride)
            fseek(inptr, 54 + (bi.biWidth * sizeof(RGBTRIPLE) + in_padding) * i, SEEK_SET); // fseek(file, offset ,whence)

            // iterate over pixels in scanline
            for (int k = 0; k < bi.biWidth; k++)
            {
                // temporary storage
                RGBTRIPLE triple;
            
                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
                
                // write RGB triple to outfile multi times
                for (int l = 0; l < multi; l++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }
            // then add it back
            for (int k = 0; k < out_padding; k++)
            {
                fputc(0x00, outptr);
            }
        }
    }

    // close infile
    fclose(inptr);
    // close outfile
    fclose(outptr);

    // success
    return 0;
}
in(int argc, char *argv[])
{
    //argv[1]は、100以下の正の整数でなければなりません。
    //argv[2]は、サイズ変更するBMPの名前でなければなりません。
    //argv[3]は、書き込まれるサイズ変更されたバージョンの名前でなければなりません。
    
    if (argc != 4)
    {
        printf("Usage: ./resize n infile outfile\n");
        return 1;
    }
    
    //remember number of multiply
    int m = atoi(argv[1]);
    if (m < 1 || m > 100)
    {
        printf("Scale must be between 1 and 100\n");
        return 1;
    }
    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        printf("Could not open %s.\n", infile);
        return 2;
    }    
    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        printf("Could not create %s.\n", outfile);
        return 3;
    }
    
    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    
    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        printf("Unsupported file format.\n");
        return 4;
    }
    
    // create outfile's BITMAPFILEHEADER and BITMAPINFOHEADER
    BITMAPFILEHEADER obf = bf;
    BITMAPINFOHEADER obi = bi;
    
    // rescale outfile's dimension
    out_bi.biWidth *= m;
    out_bi.biHeight *= m;
    
    
    
    bi.biSize = 54 + (bi.biSize - 54) * m;
    bi.biHeight = bi.biHeight * m;
    bi.biWidth = bi.biWidth * m;
    
    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);
    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);
    
    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    
    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {

        // iterate over pixels in scanline
        for (int j = 0; j < bi.biWidth; j++)
        {
            // temporary storage
            RGBTRIPLE triple;
            
            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
            // multiple write RGB triple to outfile
            //for (int k = 0; k < bi.biWidth * m; k++)
            //{
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
            //}
        }

        // skip over padding, if any
        fseek(inptr, padding, SEEK_CUR);

        // then add it back (to demonstrate how)
        for (int k = 0; k < padding; k++)
        {
            fputc(0x00, outptr);
        }
    }

    // close infile
    fclose(inptr);
    // close outfile
    fclose(outptr);

    // success
    return 0;

}


/*
int hundred_check(int num)
{
    if (!((int)argv[0][i] = num))
    {
        
    }
    else
    {
        printf("Usage: ./resize n infile outfile\n");
        return 1;
    }
}
*/
