// gcc source.c -o vuln -no-pie -fno-stack-protector -z execstack -m32

#include <stdio.h>

void main() {
    int num = 0;
    char buf[20];
    puts("Overflow me: ");
    gets(buf);
    if(num == 1337) {
        puts("You win!");
    }
    else if(num != 0) {
        puts("Almost there!");
    }
    else {
        puts("Try harder!");
    }
}