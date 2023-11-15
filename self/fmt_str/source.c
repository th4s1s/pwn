// gcc source.c -o vuln -z -m32

#include <stdio.h>
#include <stdlib.h>

void win()
{
    puts("You win!");
}

void vuln()
{
    char buf[200];
    scanf("%200s", buf);
    printf(buf);
    exit(0);
}


void main() {
    puts("Hello ");
    puts("World!\n");
    vuln();
}