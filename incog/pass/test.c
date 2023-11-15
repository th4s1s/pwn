// gcc source.c -o vuln -no-pie -fno-stack-protector -z execstack -m32

#include <stdio.h>

void convert() //gets the float input from user and turns it into hexadecimal
{
    float f;
    printf("Enter float: ");
    scanf("%f", &f);
    printf("hex is %x", *(unsigned int*)&f);
}

void main() {
    convert();
}