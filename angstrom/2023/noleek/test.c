#include <stdio.h>

int main() {
    char s[40];
    fgets(s, 32, stdin);
    fprintf(stdout, s);
}