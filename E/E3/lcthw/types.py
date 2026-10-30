from native import *
def main():
    lines=['#include <stdio.h>','#include <stdint.h>','#include <inttypes.h>','#include <stddef.h>','#include <limits.h>','#include <assert.h>','static void nop(void){}','enum Color{RED,GREEN};','int main(void){']
    for family in ('','least','fast'):
        for bits in (8,16,32,64):
            tail=f'_{family}{bits}' if family else str(bits)
            macro=f'_{family.upper()}{bits}' if family else str(bits)
            signed='int'+tail+'_t';unsigned='uint'+tail+'_t'
            lines += [f'printf("{signed} %zu %" PRIdMAX " %" PRIdMAX "\\n",sizeof({signed}),(intmax_t)INT{macro}_MIN,(intmax_t)INT{macro}_MAX);',
                      f'printf("{unsigned} %zu %" PRIuMAX "\\n",sizeof({unsigned}),(uintmax_t)UINT{macro}_MAX);']
    lines += [
      'printf("intptr_t %zu %" PRIdMAX " %" PRIdMAX "\\n",sizeof(intptr_t),(intmax_t)INTPTR_MIN,(intmax_t)INTPTR_MAX);',
      'printf("uintptr_t %zu %" PRIuMAX "\\n",sizeof(uintptr_t),(uintmax_t)UINTPTR_MAX);',
      'printf("intmax_t %zu %" PRIdMAX " %" PRIdMAX "\\n",sizeof(intmax_t),(intmax_t)INTMAX_MIN,(intmax_t)INTMAX_MAX);',
      'printf("uintmax_t %zu %" PRIuMAX "\\n",sizeof(uintmax_t),(uintmax_t)UINTMAX_MAX);',
      'printf("size_t %zu %" PRIuMAX "\\n",sizeof(size_t),(uintmax_t)SIZE_MAX);',
      'printf("ptrdiff_t %zu %" PRIdMAX " %" PRIdMAX "\\n",sizeof(ptrdiff_t),(intmax_t)PTRDIFF_MIN,(intmax_t)PTRDIFF_MAX);',
      '''int x=3;const int *view=&x;x=4;assert(*view==4);
volatile int observed=7;int saved=observed;observed=8;assert(saved==7&&observed==8);
register int hint=9;assert(hint==9);
unsigned u=1;assert((-1 < u)==0);
uint8_t byte=255;assert(byte+1==256);byte=(uint8_t)(byte+1);assert(byte==0);
short small=3;long wide=4;float f=1.25f;double d=2.5;long double ld=3.75L;char c='A';void *p=&x;
assert((void *)(uintptr_t)p==p);nop();enum Color color=GREEN;assert(color==1);
printf("basic %d %ld %.2f %.2f %.2Lf %c %zu\\n",(int)small,wide,(double)f,d,ld,c,sizeof(void*));
unsigned a=5,b=3;assert((a&b)==1&&(a|b)==7&&(a^b)==6&&((a<<1)>>1)==a);
int n=1,old=n++;assert(old==1&&n==2);assert(++n==3);assert(n--==3&&--n==1);
n=3;n+=2;n*=4;n/=2;n-=1;n%=4;assert(n==1);
a=3;a<<=2;a>>=1;a|=1;a&=7;a^=3;assert(a==4);
struct Box{int v;} box={3};struct Box *bp=&box;assert(bp->v==box.v&&*&x==4);
int array[3]={1,2,3};assert(array[1]==*(array+1)&&sizeof array==3*sizeof(int));
int sum=0;for(int i=0;i<5;i++){if(i%2)continue;sum+=i;}assert(sum==6);
int once=0;do{once++;}while(0);assert(once==1);
if(x==4)goto reached;assert(0);reached:assert(x>=4&&x<=4&&x!=3);
assert((x==4?12:13)==12);puts("PASS types operators and control");return 0;}''']
    src=write('types.c','\n'.join(lines)+'\n');exe,_,_=build('types',files=[src])
    o,e,r=execute('types',exe,vg=True);assert 'PASS types' in o and 'ERROR SUMMARY: 0 errors' in e
    table=[]
    for line in o.splitlines():
        parts=line.split()
        if not parts or not parts[0].endswith('_t'):continue
        size=int(parts[1]);values=list(map(int,parts[2:]))
        if len(values)==2:assert values==[-(1<<(size*8-1)),(1<<(size*8-1))-1]
        else:assert values==[(1<<(size*8))-1]
        table.append({'type':parts[0],'bytes':size,'limits':values})
    assert len(table)==30
    o,e,r=run('stdint_macros',['gcc','-E','-dM','-include','stdint.h','-x','c','/dev/null'])
    assert '#define INT8_MAX' in o and '#define UINT_FAST64_MAX' in o and '#define SIZE_MAX' in o
    dump(common.OUT/'types_table.json',{'target':'Linux AMD64 GCC11','table':table,'not_universal':'Exact-width types and intptr_t are conditional; this is the installed target. intmax_t need not cover GNU extended __int128.'})
    verdict(['LCT-21-BASE','LCT-21-X01','LCT-21-X02','LCT-21-X04'],'PASS',['types','stdint_macros','types_table.json'],'All listed type families/limits measured, representative qualifiers/operators/control verified. Volatile does not disable all optimization or provide synchronization; register is not a physical allocation guarantee.')
    verdict(['LCT-21-X03'],'MATERIAL_PREPARED_HUMAN_DURATION',[],'Flashcards included in notes; no claim that a week of daily15-minute human practice has already elapsed.')
    print('TYPE_REFERENCE_DONE',flush=True)
if __name__=='__main__':main()
