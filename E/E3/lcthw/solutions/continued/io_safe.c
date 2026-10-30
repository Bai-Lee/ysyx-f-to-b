#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <errno.h>
#include <limits.h>
#include <math.h>
static int line(char *out,size_t cap){
    size_t n=0;int c,invalid=0;if(!cap)return -1;
    while((c=fgetc(stdin))!=EOF&&c!='\n'){if(c==0)invalid=1;if(n+1<cap)out[n++]=(char)c;else invalid=1;}
    out[n]=0;return invalid?-1:(c==EOF&&n==0)?-1:0;
}
static int integer(const char *s,int *out){char *end;errno=0;long n=strtol(s,&end,10);if(end==s||errno||n<INT_MIN||n>INT_MAX)return -1;while(isspace((unsigned char)*end))end++;if(*end)return -1;*out=(int)n;return 0;}
static void strip_space(char *s){char *p=s;for(char *q=s;*q;q++)if(!isspace((unsigned char)*q))*p++=*q;*p=0;}
int main(void){
    char first[100],last[100],text[100];int age,eye;float income;char *end;
    if(line(first,sizeof first)||line(last,sizeof last)||line(text,sizeof text)||integer(text,&age))goto error;
    strip_space(first);strip_space(last);
    if(line(text,sizeof text)||integer(text,&eye)||eye<1||eye>5)goto error;
    if(line(text,sizeof text))goto error;
    errno=0;income=strtof(text,&end);if(end==text||errno||!isfinite(income))goto error;
    while(isspace((unsigned char)*end)){end++;}
    if(*end)goto error;
    const char *colors[]={"Blue","Green","Brown","Black","Other"};
    printf("%s|%s|%d|%s|%.6f\n",first,last,age,colors[eye-1],(double)income);return 0;
error:fputs("invalid input\n",stderr);return 1;
}
