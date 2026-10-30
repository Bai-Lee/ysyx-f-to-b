#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>
#include <stddef.h>
#include <limits.h>
#include <assert.h>
static void nop(void){}
enum Color{RED,GREEN};
int main(void){
printf("int8_t %zu %" PRIdMAX " %" PRIdMAX "\n",sizeof(int8_t),(intmax_t)INT8_MIN,(intmax_t)INT8_MAX);
printf("uint8_t %zu %" PRIuMAX "\n",sizeof(uint8_t),(uintmax_t)UINT8_MAX);
printf("int16_t %zu %" PRIdMAX " %" PRIdMAX "\n",sizeof(int16_t),(intmax_t)INT16_MIN,(intmax_t)INT16_MAX);
printf("uint16_t %zu %" PRIuMAX "\n",sizeof(uint16_t),(uintmax_t)UINT16_MAX);
printf("int32_t %zu %" PRIdMAX " %" PRIdMAX "\n",sizeof(int32_t),(intmax_t)INT32_MIN,(intmax_t)INT32_MAX);
printf("uint32_t %zu %" PRIuMAX "\n",sizeof(uint32_t),(uintmax_t)UINT32_MAX);
printf("int64_t %zu %" PRIdMAX " %" PRIdMAX "\n",sizeof(int64_t),(intmax_t)INT64_MIN,(intmax_t)INT64_MAX);
printf("uint64_t %zu %" PRIuMAX "\n",sizeof(uint64_t),(uintmax_t)UINT64_MAX);
printf("int_least8_t %zu %" PRIdMAX " %" PRIdMAX "\n",sizeof(int_least8_t),(intmax_t)INT_LEAST8_MIN,(intmax_t)INT_LEAST8_MAX);
printf("uint_least8_t %zu %" PRIuMAX "\n",sizeof(uint_least8_t),(uintmax_t)UINT_LEAST8_MAX);
printf("int_least16_t %zu %" PRIdMAX " %" PRIdMAX "\n",sizeof(int_least16_t),(intmax_t)INT_LEAST16_MIN,(intmax_t)INT_LEAST16_MAX);
printf("uint_least16_t %zu %" PRIuMAX "\n",sizeof(uint_least16_t),(uintmax_t)UINT_LEAST16_MAX);
printf("int_least32_t %zu %" PRIdMAX " %" PRIdMAX "\n",sizeof(int_least32_t),(intmax_t)INT_LEAST32_MIN,(intmax_t)INT_LEAST32_MAX);
printf("uint_least32_t %zu %" PRIuMAX "\n",sizeof(uint_least32_t),(uintmax_t)UINT_LEAST32_MAX);
printf("int_least64_t %zu %" PRIdMAX " %" PRIdMAX "\n",sizeof(int_least64_t),(intmax_t)INT_LEAST64_MIN,(intmax_t)INT_LEAST64_MAX);
printf("uint_least64_t %zu %" PRIuMAX "\n",sizeof(uint_least64_t),(uintmax_t)UINT_LEAST64_MAX);
printf("int_fast8_t %zu %" PRIdMAX " %" PRIdMAX "\n",sizeof(int_fast8_t),(intmax_t)INT_FAST8_MIN,(intmax_t)INT_FAST8_MAX);
printf("uint_fast8_t %zu %" PRIuMAX "\n",sizeof(uint_fast8_t),(uintmax_t)UINT_FAST8_MAX);
printf("int_fast16_t %zu %" PRIdMAX " %" PRIdMAX "\n",sizeof(int_fast16_t),(intmax_t)INT_FAST16_MIN,(intmax_t)INT_FAST16_MAX);
printf("uint_fast16_t %zu %" PRIuMAX "\n",sizeof(uint_fast16_t),(uintmax_t)UINT_FAST16_MAX);
printf("int_fast32_t %zu %" PRIdMAX " %" PRIdMAX "\n",sizeof(int_fast32_t),(intmax_t)INT_FAST32_MIN,(intmax_t)INT_FAST32_MAX);
printf("uint_fast32_t %zu %" PRIuMAX "\n",sizeof(uint_fast32_t),(uintmax_t)UINT_FAST32_MAX);
printf("int_fast64_t %zu %" PRIdMAX " %" PRIdMAX "\n",sizeof(int_fast64_t),(intmax_t)INT_FAST64_MIN,(intmax_t)INT_FAST64_MAX);
printf("uint_fast64_t %zu %" PRIuMAX "\n",sizeof(uint_fast64_t),(uintmax_t)UINT_FAST64_MAX);
printf("intptr_t %zu %" PRIdMAX " %" PRIdMAX "\n",sizeof(intptr_t),(intmax_t)INTPTR_MIN,(intmax_t)INTPTR_MAX);
printf("uintptr_t %zu %" PRIuMAX "\n",sizeof(uintptr_t),(uintmax_t)UINTPTR_MAX);
printf("intmax_t %zu %" PRIdMAX " %" PRIdMAX "\n",sizeof(intmax_t),(intmax_t)INTMAX_MIN,(intmax_t)INTMAX_MAX);
printf("uintmax_t %zu %" PRIuMAX "\n",sizeof(uintmax_t),(uintmax_t)UINTMAX_MAX);
printf("size_t %zu %" PRIuMAX "\n",sizeof(size_t),(uintmax_t)SIZE_MAX);
printf("ptrdiff_t %zu %" PRIdMAX " %" PRIdMAX "\n",sizeof(ptrdiff_t),(intmax_t)PTRDIFF_MIN,(intmax_t)PTRDIFF_MAX);
int x=3;const int *view=&x;x=4;assert(*view==4);
volatile int observed=7;int saved=observed;observed=8;assert(saved==7&&observed==8);
register int hint=9;assert(hint==9);
unsigned u=1;assert((-1 < u)==0);
uint8_t byte=255;assert(byte+1==256);byte=(uint8_t)(byte+1);assert(byte==0);
short small=3;long wide=4;float f=1.25f;double d=2.5;long double ld=3.75L;char c='A';void *p=&x;
assert((void *)(uintptr_t)p==p);nop();enum Color color=GREEN;assert(color==1);
printf("basic %d %ld %.2f %.2f %.2Lf %c %zu\n",(int)small,wide,(double)f,d,ld,c,sizeof(void*));
unsigned a=5,b=3;assert((a&b)==1&&(a|b)==7&&(a^b)==6&&((a<<1)>>1)==a);
int n=1,old=n++;assert(old==1&&n==2);assert(++n==3);assert(n--==3&&--n==1);
n=3;n+=2;n*=4;n/=2;n-=1;n%=4;assert(n==1);
a=3;a<<=2;a>>=1;a|=1;a&=7;a^=3;assert(a==4);
struct Box{int v;} box={3};struct Box *bp=&box;assert(bp->v==box.v&&*&x==4);
int array[3]={1,2,3};assert(array[1]==*(array+1)&&sizeof array==3*sizeof(int));
int sum=0;for(int i=0;i<5;i++){if(i%2)continue;sum+=i;}assert(sum==6);
int once=0;do{once++;}while(0);assert(once==1);
if(x==4)goto reached;assert(0);reached:assert(x>=4&&x<=4&&x!=3);
assert((x==4?12:13)==12);puts("PASS types operators and control");return 0;}
