#include <am.h>
#include <klib.h>
#include <limits.h>
static unsigned checks;
static void init(unsigned char *a,int n){for(int i=0;i<n;i++)a[i]=(unsigned char)(i+1);}
int main(const char *args){
 (void)args;unsigned char a[80],b[80],original[80];char text[64],copy[80],format[96];
 for(int l=0;l<=32;l++)for(int n=0;n<=32-l;n++){
  init(a,80);assert(memset(a+l,0xab,(size_t)n)==a+l);
  for(int i=0;i<80;i++){assert(a[i]==(i>=l&&i<l+n?0xab:i+1));}checks++;
  init(a,80);init(b,80);assert(memcpy(a+l,b+40,(size_t)n)==a+l);
  for(int i=0;i<80;i++){assert(a[i]==(i>=l&&i<l+n?41+i-l:i+1));}checks++;
 }
 for(int src=0;src<12;src++)for(int dst=0;dst<12;dst++)for(int n=0;n<20;n++){
  init(a,80);init(original,80);assert(memmove(a+dst,a+src,(size_t)n)==a+dst);
  for(int i=0;i<80;i++){assert(a[i]==(i>=dst&&i<dst+n?original[src+i-dst]:original[i]));}checks++;
 }
 for(int n=0;n<30;n++){
  for(int i=0;i<n;i++){text[i]=(char)('a'+i%5);}text[n]=0;assert(strlen(text)==(size_t)n);
  memset(copy,0x7e,sizeof(copy));assert(strcpy(copy+3,text)==copy+3);assert(strcmp(copy+3,text)==0&&copy[3+n]==0&&copy[2]==0x7e&&copy[4+n]==0x7e);checks++;
  for(int count=0;count<32;count++){
   memset(copy,0x7e,sizeof(copy));strncpy(copy+3,text,(size_t)count);
   for(int i=0;i<count;i++){assert(copy[3+i]==(i<n?text[i]:0));}assert(copy[2]==0x7e&&copy[3+count]==0x7e);checks++;
  }
 }
 assert(strcmp("\xff","\x01")>0&&strncmp("\x80","\x7f",1)>0);assert(memcmp("\xff","\x01",1)>0);
 strcpy(text,"abc");strcat(text,"def");assert(!strcmp(text,"abcdef"));assert(strchr(text,'c')==text+2&&strrchr(text,0)==text+6);
 int values[]={0,1,-1,INT_MIN,INT_MAX};const char *expected[]={"0","1","-1","-2147483648","2147483647"};
 for(int i=0;i<5;i++){int n=sprintf(format,"%d",values[i]);assert(n==(int)strlen(expected[i])&&!strcmp(format,expected[i]));checks++;}
 assert(sprintf(format,"%s %d %%","hello",-42)==11&&!strcmp(format,"hello -42 %"));
 for(size_t n=0;n<10;n++){memset(format,0x7e,sizeof(format));int len=snprintf(format+2,n,"%08x",0xabcu);assert(len==8);assert(format[1]==0x7e&&format[2+n]==0x7e);if(n)assert(format[2+(n<9?n-1:8)]==0);checks++;}
 printf("KLIB_PORTABLE_PASS checks=%u\n",checks);return 0;
}
