#include <stdio.h>
static int left(void){puts("LEFT");return 1;}
static int right(void){puts("RIGHT");return 2;}
static void f(int x,int y){printf("%d %d\n",x,y);}
int main(void){f(left(),right());return 0;}
