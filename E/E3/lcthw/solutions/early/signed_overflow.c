#include <stdio.h>
#include <limits.h>
int main(void){volatile long two=2;long x=LONG_MAX;printf("%ld\n",x*two);return 0;}
