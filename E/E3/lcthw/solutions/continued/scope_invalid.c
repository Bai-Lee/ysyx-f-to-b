#include <stdio.h>
static const int immutable=3;
int main(void){*(volatile int *)&immutable=4;printf("%d\n",immutable);return 0;}
