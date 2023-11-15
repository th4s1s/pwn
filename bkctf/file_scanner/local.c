#include <stdio.h>

void main() {
    int seed = time(0);
    srand(seed);
    for(int i = 0; i < 16; i++) {
        printf("%d ", rand() % 16);
    }
}