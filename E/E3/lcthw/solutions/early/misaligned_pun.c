#include <stdio.h>
int main(void){_Alignas(int) unsigned char bytes[8]={1,2,3,4,5,6,7,8};int *p=(int *)(bytes+1);printf("%d\n",*p);return 0;}
