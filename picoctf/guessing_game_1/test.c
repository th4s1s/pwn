#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>

int main(int argc, char **argv){
	int i;
    for(i = 0; i < 10; i++)
    {
        int d = rand()%100 + 1;
        printf("%d ", d);
    }
	
	return 0;
}