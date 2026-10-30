#include <stdio.h>
int main(void){char s[100];if(scanf("%50s",s)!=1)return 1;printf("%s|next=%d\n",s,getchar());return 0;}
