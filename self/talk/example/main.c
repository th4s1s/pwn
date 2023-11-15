#include <stdio.h>
#include <stdlib.h>


void main() {
    char flag[64];
    char buf[64];

    setbuf(stdin, 0);
    setbuf(stdout, 0);

    FILE *f = fopen("flag.txt", "r");
    if(f == NULL)
    {
        puts("Where is my file? :)))");
        exit(0);
    }
    
    fgets(flag, 64, f);
    fflush(stdout);
    printf("Give me something to print: ");
    fgets(buf, 64, stdin);
    printf(buf);
    printf("\n");
}