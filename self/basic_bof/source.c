// gcc source.c -o vuln -no-pie -fno-stack-protector -z execstack -m32

#include <stdio.h>

void main() {
    int num = 0;
    char buf[20];
    puts("Overflow me: ");
    gets(buf);
    if(num != 0) {
        puts("You win!");
    }
    else {
        puts("Try harder!");
    }
}