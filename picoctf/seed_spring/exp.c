#include <stdio.h> 
#include <time.h>
#include <stdlib.h> 
  
int main () 
{ 
    int i;
      
    srand(time(0)); 
    
    for (i = 0; i < 30; i++)
    {
        printf("%d\n", rand() & 0xf); 
    }
      
    return 0; 
} 