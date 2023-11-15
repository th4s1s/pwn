#include <stdio.h>
#include <stdlib.h>

int* genRand(char* str)
{
    long long int* x = str;
    srand(*x);
    int i;
    static int ret[8];
    int y = 0;
    for ( i = 10; i <= 999999999; i *= 10 )
    {
        ret[y] = rand() % i + 1;
        y++;
    }
    return ret;
}