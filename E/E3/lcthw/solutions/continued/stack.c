#include <stdio.h>
int main(void){int a[8],n=0,v;char op;while(scanf(" %c",&op)==1){if(op=='+'){if(scanf("%d",&v)!=1)return 2;if(n==8)puts("FULL");else{a[n++]=v;puts("OK");}}else if(op=='-'){if(!n)puts("EMPTY");else printf("%d\n",a[--n]);}else return 2;}return 0;}
