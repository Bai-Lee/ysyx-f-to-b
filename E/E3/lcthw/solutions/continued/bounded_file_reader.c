#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
int main(int argc,char **argv){if(argc!=3)return 2;size_t cap=strtoul(argv[2],0,10);if(cap>1000000)return 2;unsigned char *a=malloc(cap+2);if(!a)return 2;a[0]=a[cap+1]=0xcc;if(!cap){free(a);return 1;}unsigned char *s=a+1;s[0]=0;FILE *f=fopen(argv[1],"rb");if(!f){free(a);return 1;}size_t n=0;char ch;while(n+1<cap&&fscanf(f,"%c",&ch)==1)s[n++]=(unsigned char)ch;s[n]=0;if(a[0]!=0xcc||a[cap+1]!=0xcc)return 3;for(size_t i=0;i<n;i++)printf("%02x",(unsigned)s[i]);printf("\n");fclose(f);free(a);return 0;}
