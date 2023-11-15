// gcc source.c -o vuln -no-pie -fno-stack-protector -z execstack -m32

#include <stdio.h>



void win(int a1, int a2) {
    // Đọc file flag
    if(a1 == 0x1337C0DE && a2 == 0xD34DB33F) {
        puts("You win!");
    }
    else {
        puts("Almost there!");
    }
}

void vuln(int a, int b) {
    char c;
    int num;
    char padding[30];
    char buf[20];
    puts("Overflow me: ");
    gets(buf);
}

void main() {
    vuln(1, 2);
    puts("Try harder!");
}