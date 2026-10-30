#define main original_main
#include "ex27_book.c"
#undef main
int main(void){char from[3]={'a','b','c'},to[8];safercopy(3,from,8,to);puts(to);return 0;}
