#include <limits.h>
#define main original_main
#include "ex27_book.c"
#undef main
int main(void){char from[3]={1,2,3},to[8];return safercopy(3,from,INT_MIN,to);}
