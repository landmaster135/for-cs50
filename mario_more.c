#include <cs50.h> 
#include <stdio.h>
 
int main(void) 
{ 
    int h;
    int between = 1; //half of distance among pyramids
    int p = 0;
    do
    {
        h = get_int("Height: "); //prompt height.
    }
    while (h < 1 || h > 8); //Height is between 1 and 8.
    
    for (int i = 1; i < h + 1; i++) //loop by Height.
    {
        for (int j = 1; j < (h + between) * 2 + 1; j++) //loop by horizontally.
        {
            if (j != h + between * 2 + i) 
            {
                if (j <= h - i) //x number Height from over owns (Height - x) * 2 spaces and x * 2 blocks.
                {
                    printf(" ");
                }
                else if (j > h && j < h + between * 2 + 1) //In addition, it owns (between * 2) spaces too.
                {
                    printf(" ");
                }
                else
                {
                    printf("#");
                }               
            }
            else //if a block's number is same as height.
            {
                printf("#\n");
                break; //creating a block at right edge in right side, a loop finishes.
            } 
        }       
    }
}
