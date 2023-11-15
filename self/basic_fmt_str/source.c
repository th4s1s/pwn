// gcc source.c -o vuln -no-pie -fno-stack-protector -z execstack -m32

#include <stdio.h>
#include <stdlib.h>


void main() {
    char flag[64];
    char buf[64];

    FILE *f = fopen("flag.txt", "r");
    if(f == NULL)
    {
        puts("Where is my file? :)))");
        exit(0);
    }
    fgets(flag, 64, f);
    fflush(stdout);
    printf("Give me something to print!\n");
    scanf("%64s", buf);
    printf(buf);
    printf("\n");
}