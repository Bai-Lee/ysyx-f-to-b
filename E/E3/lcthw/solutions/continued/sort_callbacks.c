#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <limits.h>
typedef int (*Compare)(int,int);
typedef int *(*Sort)(const int *,size_t,Compare);
static int ascending(int a,int b){return (a>b)-(a<b);}
static int descending(int a,int b){return (a<b)-(a>b);}
static int *copy(const int *a,size_t n){int *p=malloc((n?n:1)*sizeof(int));assert(p);if(n)memcpy(p,a,n*sizeof(int));return p;}
static int *bubble(const int *a,size_t n,Compare cmp){
    int *p=copy(a,n);for(size_t i=0;i<n;i++)for(size_t j=1;j<n-i;j++)if(cmp(p[j-1],p[j])>0){int x=p[j];p[j]=p[j-1];p[j-1]=x;}return p;
}
static int *insertion(const int *a,size_t n,Compare cmp){
    int *p=copy(a,n);for(size_t i=1;i<n;i++){int value=p[i];size_t j=i;while(j&&cmp(p[j-1],value)>0){p[j]=p[j-1];--j;}p[j]=value;}return p;
}
static int qcompare(const void *a,const void *b){return ascending(*(const int *)a,*(const int *)b);}
static void test(const int *a,size_t n,Sort sort,Compare cmp,int reverse){
    int *p=sort(a,n,cmp),*reference=copy(a,n);qsort(reference,n,sizeof(int),qcompare);
    for(size_t i=0;i<n;i++)assert(p[i]==reference[reverse?n-i-1:i]);
    free(reference);free(p);
}
int main(void){
    int data[64]={INT_MIN,INT_MAX,0,-1,1,1,0,42};unsigned seed=260718;
    for(size_t n=0;n<=64;n++){
        for(size_t i=8;i<n;i++){seed=1664525u*seed+1013904223u;data[i]=(int)(seed%201)-100;}
        test(data,n,bubble,ascending,0);test(data,n,insertion,ascending,0);
        test(data,n,bubble,descending,1);test(data,n,insertion,descending,1);
    }
    puts("PASS 260 algorithm/comparator/size combinations");return 0;
}
