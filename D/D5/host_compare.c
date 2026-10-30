#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdarg.h>
#include <stddef.h>
#include <limits.h>
#include <assert.h>
extern size_t d_strlen(const char *);
extern char *d_strcpy(char *,const char *),*d_strncpy(char *,const char *,size_t),*d_strcat(char *,const char *);
extern int d_strcmp(const char *,const char *),d_strncmp(const char *,const char *,size_t),d_memcmp(const void *,const void *,size_t);
extern void *d_memcpy(void *,const void *,size_t),*d_memmove(void *,const void *,size_t),*d_memset(void *,int,size_t);
extern char *d_strchr(const char *,int),*d_strrchr(const char *,int);
extern int d_vsnprintf(char *,size_t,const char *,va_list),d_vsprintf(char *,const char *,va_list),d_printf(const char *,...);
static char serial[2048];static size_t serial_n;static unsigned checks;
void putch(char c){assert(serial_n+1<sizeof(serial));serial[serial_n++]=c;serial[serial_n]=0;}
static int sign(int x){return (x>0)-(x<0);}
static void pattern(unsigned char *b,size_t n){for(size_t i=0;i<n;i++)b[i]=(unsigned char)(i*17+3);}
static void formatting(const char *fmt,...){
 for(size_t cap=0;cap<48;cap++){
  unsigned char a[160],b[160];memset(a,0xa5,sizeof(a));memset(b,0xa5,sizeof(b));
  va_list ap,bp;va_start(ap,fmt);va_copy(bp,ap);
  int expected=vsnprintf(cap?(char *)a+4:NULL,cap,fmt,ap);int got=d_vsnprintf(cap?(char *)b+4:NULL,cap,fmt,bp);
  va_end(bp);va_end(ap);
  if(expected!=got||memcmp(a,b,sizeof(a))){fprintf(stderr,"FORMAT_MISMATCH fmt=%s cap=%zu want=%d got=%d\n",fmt,cap,expected,got);abort();}checks++;
 }
 char a[512],b[512];va_list ap,bp;va_start(ap,fmt);va_copy(bp,ap);int x=vsprintf(a,fmt,ap),y=d_vsprintf(b,fmt,bp);va_end(bp);va_end(ap);assert(x==y&&!strcmp(a,b));checks++;
}
int main(void){
 unsigned char a[96],b[96],source[96];pattern(source,sizeof(source));
 for(size_t l=0;l<=32;l++)for(size_t n=0;n<=32-l;n++){
  pattern(a,sizeof(a));pattern(b,sizeof(b));assert(d_memset(b+l,0x180,n)==b+l);memset(a+l,0x180,n);assert(!memcmp(a,b,sizeof(a)));checks++;
  pattern(a,sizeof(a));pattern(b,sizeof(b));assert(d_memcpy(b+l,source+3,n)==b+l);memcpy(a+l,source+3,n);assert(!memcmp(a,b,sizeof(a)));checks++;
  assert(sign(d_memcmp(source,a,n))==sign(memcmp(source,a,n)));checks++;
 }
 for(size_t dst=0;dst<24;dst++)for(size_t src=0;src<24;src++)for(size_t n=0;n<24;n++){
  pattern(a,sizeof(a));pattern(b,sizeof(b));assert(d_memmove(b+dst,b+src,n)==b+dst);memmove(a+dst,a+src,n);assert(!memcmp(a,b,sizeof(a)));checks++;
 }
 for(size_t n=0;n<32;n++){
  char text[40];for(size_t i=0;i<n;i++)text[i]=(char)('a'+i%5);text[n]=0;
  assert(d_strlen(text)==strlen(text));checks++;
  pattern(a,sizeof(a));pattern(b,sizeof(b));strcpy((char *)a+7,text);assert(d_strcpy((char *)b+7,text)==(char *)b+7);assert(!memcmp(a,b,sizeof(a)));checks++;
  for(size_t count=0;count<40;count++){
   pattern(a,sizeof(a));pattern(b,sizeof(b));strncpy((char *)a+5,text,count);assert(d_strncpy((char *)b+5,text,count)==(char *)b+5);assert(!memcmp(a,b,sizeof(a)));checks++;
   assert(sign(d_strncmp(text,"abcdeabcde",count))==sign(strncmp(text,"abcdeabcde",count)));checks++;
  }
  strcpy((char *)a,"PRE");strcpy((char *)b,"PRE");strcat((char *)a,text);assert(d_strcat((char *)b,text)==(char *)b);assert(!strcmp((char *)a,(char *)b));checks++;
  for(int ch=0;ch<256;ch+=17){char *x=strchr(text,ch),*y=d_strchr(text,ch);assert((x?x-text:-1)==(y?y-text:-1));x=strrchr(text,ch);y=d_strrchr(text,ch);assert((x?x-text:-1)==(y?y-text:-1));checks+=2;}
 }
 assert(d_strcmp("\xff","\x01")>0);assert(d_strncmp("\x80","\x7f",1)>0);checks+=2;
 int ints[]={0,1,-1,INT_MIN,INT_MAX,INT_MIN+1,INT_MAX/17};
 for(size_t i=0;i<sizeof(ints)/sizeof(ints[0]);i++){
  formatting("%d",ints[i]);formatting("%+015d",ints[i]);formatting("% -15.10d",ints[i]);formatting("%.0d",ints[i]);
  formatting("%u %#012x %#o",(unsigned)ints[i],(unsigned)ints[i],(unsigned)ints[i]);
 }
 formatting("%lld %llu %llx",LLONG_MIN,ULLONG_MAX,ULLONG_MAX);
 formatting("%ld %lu %zu %td %jd",LONG_MIN,ULONG_MAX,(size_t)123,(ptrdiff_t)-123,(intmax_t)INTMAX_MIN);
 formatting("%hhd %hd %hhu %hu",250,65530,260u,65538u);
 formatting("%*.*s|%-10s|%c|%%",12,3,"abcdef","str",'A');
 formatting("%08.4x|%#.0o|%#.0x|%#.0o",15u,0u,0u,15u);
 formatting("%p",(void *)(uintptr_t)0x1234);
 serial_n=0;int n=d_printf("%s %d %08x", "stream",INT_MIN,0xdeadbeefu);assert(n==(int)strlen(serial));assert(!strcmp(serial,"stream -2147483648 deadbeef"));checks++;
 printf("KLIB_HOST_DIFFERENTIAL_PASS checks=%u\n",checks);return 0;
}
