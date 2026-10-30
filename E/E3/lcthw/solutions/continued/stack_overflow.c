#include <stdio.h>
volatile unsigned depth=0;
__attribute__((noinline)) void recurse(void){volatile char block[1024];block[0]=(char)depth++;recurse();if(block[0]==123)puts("unreachable");}
int main(void){recurse();return 0;}
