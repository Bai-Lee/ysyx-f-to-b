#ifdef D_KLIB_HOST_TEST
#include <stddef.h>
#include <stdint.h>
#else
#include <klib.h>
#endif
#if !defined(__ISA_NATIVE__) || defined(__NATIVE_USE_KLIB__) || defined(D_KLIB_HOST_TEST)
size_t strlen(const char *s){size_t n=0;while(s[n])n++;return n;}
char *strcpy(char *dst,const char *src){char *ret=dst;do{*dst++=*src;}while(*src++);return ret;}
char *strncpy(char *dst,const char *src,size_t n){size_t i=0;for(;i<n&&src[i];i++)dst[i]=src[i];for(;i<n;i++)dst[i]=0;return dst;}
char *strcat(char *dst,const char *src){char *ret=dst;while(*dst)dst++;do{*dst++=*src;}while(*src++);return ret;}
int strcmp(const char *a,const char *b){while(*a&&(unsigned char)*a==(unsigned char)*b){a++;b++;}return (unsigned char)*a-(unsigned char)*b;}
int strncmp(const char *a,const char *b,size_t n){for(size_t i=0;i<n;i++){unsigned char x=(unsigned char)a[i],y=(unsigned char)b[i];if(x!=y)return x-y;if(!x)return 0;}return 0;}
void *memset(void *dst,int c,size_t n){unsigned char *d=dst;for(size_t i=0;i<n;i++)d[i]=(unsigned char)c;return dst;}
void *memcpy(void *dst,const void *src,size_t n){unsigned char *d=dst;const unsigned char *s=src;for(size_t i=0;i<n;i++)d[i]=s[i];return dst;}
void *memmove(void *dst,const void *src,size_t n){
 unsigned char *d=dst;const unsigned char *s=src;uintptr_t da=(uintptr_t)d,sa=(uintptr_t)s;
 if(da>sa&&da-sa<n){for(size_t i=n;i>0;i--)d[i-1]=s[i-1];}
 else{for(size_t i=0;i<n;i++)d[i]=s[i];}
 return dst;
}
int memcmp(const void *a,const void *b,size_t n){const unsigned char *x=a,*y=b;for(size_t i=0;i<n;i++)if(x[i]!=y[i])return x[i]-y[i];return 0;}
char *strchr(const char *s,int c){unsigned char ch=(unsigned char)c;do{if((unsigned char)*s==ch)return (char *)s;}while(*s++);return NULL;}
char *strrchr(const char *s,int c){unsigned char ch=(unsigned char)c;const char *last=NULL;do{if((unsigned char)*s==ch)last=s;}while(*s++);return (char *)last;}
#endif
