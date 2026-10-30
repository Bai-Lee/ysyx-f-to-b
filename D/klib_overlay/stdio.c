#ifdef D_KLIB_HOST_TEST
#include <stddef.h>
#include <stdint.h>
#include <stdarg.h>
#include <stdbool.h>
extern void putch(char);
#else
#include <klib.h>
#endif
#include <limits.h>
#if !defined(__ISA_NATIVE__) || defined(__NATIVE_USE_KLIB__) || defined(D_KLIB_HOST_TEST)
typedef struct {char *dst;size_t cap,count;int stream;} Output;
static void emit(Output *o,char c){if(o->stream)putch(c);else if(o->dst&&o->count<o->cap&&o->cap-o->count>1)o->dst[o->count]=c;o->count++;}
static void repeat(Output *o,char c,int n){while(n-->0)emit(o,c);}
static size_t length(const char *s,int max){size_t n=0;while(s[n]&&(max<0||n<(size_t)max))n++;return n;}
static int format(Output *out,const char *fmt,va_list source){
 va_list args;va_copy(args,source);int failure=0;
 while(*fmt){
  if(*fmt!='%'){emit(out,*fmt++);continue;}
  fmt++;bool left=false,zero=false,plus=false,space=false,alternate=false;
  for(;;){if(*fmt=='-')left=true;else if(*fmt=='0')zero=true;else if(*fmt=='+')plus=true;else if(*fmt==' ')space=true;else if(*fmt=='#')alternate=true;else break;fmt++;}
  int width=0,precision=-1;
  if(*fmt=='*'){width=va_arg(args,int);fmt++;if(width<0){left=true;width=width==INT_MIN?INT_MAX:-width;}}
  else while(*fmt>='0'&&*fmt<='9'){if(width>100000)failure=1;else width=width*10+(*fmt-'0');fmt++;}
  if(*fmt=='.'){
   fmt++;precision=0;
   if(*fmt=='*'){precision=va_arg(args,int);fmt++;if(precision<0)precision=-1;}
   else while(*fmt>='0'&&*fmt<='9'){if(precision>100000)failure=1;else precision=precision*10+(*fmt-'0');fmt++;}
  }
  if(width>1000000||precision>1000000||failure){failure=1;break;}
  enum {NORMAL,HH,H,L,LL,Z,T,J} len=NORMAL;
  if(*fmt=='h'){fmt++;len=H;if(*fmt=='h'){fmt++;len=HH;}}
  else if(*fmt=='l'){fmt++;len=L;if(*fmt=='l'){fmt++;len=LL;}}
  else if(*fmt=='z'){fmt++;len=Z;}else if(*fmt=='t'){fmt++;len=T;}else if(*fmt=='j'){fmt++;len=J;}
  char spec=*fmt;if(!spec){failure=1;break;}fmt++;
  if(spec=='%'||spec=='c'||spec=='s'){
   char ch=spec=='%'?'%':spec=='c'?(char)va_arg(args,int):0;const char *str=spec=='s'?va_arg(args,const char *):&ch;
   if(!str)str="(null)";
   size_t n=spec=='s'?length(str,precision):1;int pad=width>(int)n?width-(int)n:0;
   if(!left){repeat(out,' ',pad);}
   for(size_t i=0;i<n;i++){emit(out,str[i]);}
   if(left){repeat(out,' ',pad);}
   continue;
  }
  bool sign=spec=='d'||spec=='i',pointer=spec=='p';unsigned base=(spec=='x'||spec=='X'||pointer)?16:spec=='o'?8:10;
  if(!sign&&!pointer&&spec!='u'&&spec!='x'&&spec!='X'&&spec!='o'){failure=1;break;}
  uint64_t number=0;char prefix[3];unsigned prefix_n=0;
  if(pointer){number=(uintptr_t)va_arg(args,void *);prefix[prefix_n++]='0';prefix[prefix_n++]='x';}
  else if(sign){
   int64_t value;
   if(len==LL)value=va_arg(args,long long);else if(len==L)value=va_arg(args,long);else if(len==Z||len==T)value=va_arg(args,ptrdiff_t);else if(len==J)value=va_arg(args,intmax_t);
   else{int x=va_arg(args,int);value=len==HH?(signed char)x:len==H?(short)x:x;}
   number=(uint64_t)value;
   if(value<0){prefix[prefix_n++]='-';number=0-number;}else if(plus)prefix[prefix_n++]='+';else if(space)prefix[prefix_n++]=' ';
  }else{
   if(len==LL)number=va_arg(args,unsigned long long);else if(len==L)number=va_arg(args,unsigned long);else if(len==Z||len==T)number=va_arg(args,size_t);else if(len==J)number=va_arg(args,uintmax_t);
   else{unsigned x=va_arg(args,unsigned);number=len==HH?(unsigned char)x:len==H?(unsigned short)x:x;}
   if(alternate&&number&&base==16){prefix[prefix_n++]='0';prefix[prefix_n++]=spec=='X'?'X':'x';}
  }
  char digits[65];unsigned digits_n=0;const char *alphabet=spec=='X'?"0123456789ABCDEF":"0123456789abcdef";
  if(number||precision!=0){do{digits[digits_n++]=alphabet[number%base];number/=base;}while(number);}
  if(alternate&&base==8&&(digits_n==0||digits[digits_n-1]!='0')&&precision<=(int)digits_n)precision=(int)digits_n+1;
  int zero_n=precision>(int)digits_n?precision-(int)digits_n:0;
  int total=(int)(prefix_n+digits_n)+zero_n,pad=width>total?width-total:0;
  if(zero&&!left&&precision<0){zero_n+=pad;pad=0;}
  if(!left)repeat(out,' ',pad);
  for(unsigned i=0;i<prefix_n;i++){emit(out,prefix[i]);}
  repeat(out,'0',zero_n);
  while(digits_n){emit(out,digits[--digits_n]);}
  if(left){repeat(out,' ',pad);}
 }
 va_end(args);
 if(!out->stream&&out->dst&&out->cap)out->dst[out->count<out->cap?out->count:out->cap-1]=0;
 return failure||out->count>INT_MAX?-1:(int)out->count;
}
int vsnprintf(char *dst,size_t n,const char *fmt,va_list args){Output out={dst,n,0,0};return format(&out,fmt,args);}
int snprintf(char *dst,size_t n,const char *fmt,...){va_list args;va_start(args,fmt);int count=vsnprintf(dst,n,fmt,args);va_end(args);return count;}
int vsprintf(char *dst,const char *fmt,va_list args){return vsnprintf(dst,SIZE_MAX,fmt,args);}
int sprintf(char *dst,const char *fmt,...){va_list args;va_start(args,fmt);int count=vsprintf(dst,fmt,args);va_end(args);return count;}
int vprintf(const char *fmt,va_list args){Output out={NULL,0,0,1};return format(&out,fmt,args);}
int printf(const char *fmt,...){va_list args;va_start(args,fmt);int count=vprintf(fmt,args);va_end(args);return count;}
#endif
