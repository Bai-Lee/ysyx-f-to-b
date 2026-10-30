#include <assert.h>
#include <stdio.h>
static int hidden=3;
int *expose(void){return &hidden;}
void value(int x){x=8;}
void pointer(int *x){*x=8;}
int main(void){int a=1;value(a);assert(a==1);pointer(&a);assert(a==8);int *p=expose();*p=11;assert(*expose()==11);puts("PASS value, pointer, static lifetime");}
