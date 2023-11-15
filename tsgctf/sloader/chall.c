#include <stdio.h>

int main(void) {
    char buf[16];
    read(0, buf, 100);
    puts(buf);
    return 0;
}
