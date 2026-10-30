#include <klib.h>
#include <rtthread.h>
__attribute__((weak)) char *strchr(const char *s,int c) {
  for(;;s++){if(*s==(char)c)return (char *)s;if(!*s)return NULL;}
}
__attribute__((weak)) char *strrchr(const char *s,int c) {
  const char *last=NULL;do{if(*s==(char)c)last=s;}while(*s++);return (char *)last;
}
__attribute__((weak)) char *strstr(const char *s,const char *n) { return rt_strstr(s,n); }
__attribute__((weak)) char *strncat(char *dst,const char *src,size_t n) {
  char *out=dst+strlen(dst);while(n--&&*src)*out++=*src++;*out=0;return dst;
}
