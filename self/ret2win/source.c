// gcc source.c -o vuln -no-pie -fno-stack-protector -z execstack -m32

#include <stdio.h>


void win(int a1, int a2) {
    puts("You win!");
}

void vuln() {
}

void main() {
    char c;
    int num;
    char padding[30];
    char buf[20];
    puts("Overflow me: ");
    gets(buf);
    puts("Try harder!");
}