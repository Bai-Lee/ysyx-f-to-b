#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stddef.h>

static int side_effects;
static int called(void){++side_effects;return 1;}
static char classify_switch(char c,size_t i){
    if(c>='A'&&c<='Z')c=(char)(c+('a'-'A'));
    switch(c){case 'a':case 'e':case 'i':case 'o':case 'u':return c;
        case 'y':return i>2?'y':'-';default:return '-';}
}
static char classify_if(char c,size_t i){
    if(c>='A'&&c<='Z')c=(char)(c+('a'-'A'));
    if(c=='a'||c=='e'||c=='i'||c=='o'||c=='u')return c;
    if(c=='y'&&i>2)return c;
    return '-';
}
static void fixed_length(const unsigned char *s,size_t n){
    for(size_t i=0;i<n;++i)if(isalpha(s[i])||isblank(s[i]))printf("char:%u\n",(unsigned)s[i]);
}
static void indices(const int a[],const char *const names[],size_t n){
    for(size_t i=0;i<n;++i)printf("method0:%s:%d\n",names[i],a[i]);
}
static void pointers(const int *a,const char *const *names,size_t n){
    for(size_t i=0;i<n;++i)printf("method1:%s:%d\n",*(names+i),*(a+i));
}
static void while_indices(const int a[],const char *const names[],size_t n){
    size_t i=0;while(i<n){printf("method2:%s:%d\n",names[i],a[i]);++i;}
}
static void while_pointers(const int *a,const char *const *names,size_t n){
    const int *end=a+n;while(a!=end){printf("method3:%s:%d\n",*names,*a);++a;++names;}
}
struct StackPerson {char name[16];int age,height,weight;};
static struct StackPerson older(struct StackPerson value){value.age+=20;return value;}

int main(int argc,char **argv){
    int i,j,total;
    for(i=0,j=3,total=0;(total+=0,i<3);(++i,--j,total+=i)){}
    assert(i==3&&j==0&&total==6);
    assert(!(0&&called())&&side_effects==0);
    assert((1||called())&&side_effects==0);
    assert((0||called())&&side_effects==1);
    assert((!0)==1 && (!1)==0);
    const char *states[4]={"California","Oregon","Washington","Texas"};
    if(argc>1){char *saved=argv[1];states[0]=argv[1];argv[1]=(char *)states[1];assert(states[0]==saved&&strcmp(argv[1],"Oregon")==0);argv[1]=saved;}
    const char *copied[4]={0};size_t n=0;
    while(n<4&&n<(size_t)argc){copied[n]=argv[n];++n;}
    assert(n<=4);for(size_t k=0;k<n;++k)assert(copied[k]==argv[k]);
    char mutable[4]="abc";char *shallow=mutable;mutable[0]='Z';assert(shallow[0]=='Z');
    for(int k=argc;k>0;){--k;printf("reverse-arg:%d:%s\n",k,argv[k]);}
    for(int k=4;k>0;){--k;printf("reverse-state:%s\n",states[k]);}
    size_t limited=0;for(char **p=argv;p!=argv+argc;++p){if(limited==2)break;++limited;}
    assert(limited==((argc<2)?(size_t)argc:2));
    size_t w=0;while(w<(size_t)argc){if(w==2)break;++w;}assert(w==limited);
    for(int k=1;k<argc;++k){
        char letter;size_t len=strlen(argv[k]);
        for(size_t q=0;(letter=argv[k][q],q<len);++q){assert(classify_switch(letter,q)==classify_if(letter,q));printf("vowel:%d:%zu:%c\n",k,q,classify_switch(letter,q));}
        fixed_length((const unsigned char *)argv[k],len);
    }
    const unsigned char bounded[3]={'A',0,'Z'};fixed_length(bounded,sizeof bounded);
    assert(!isdigit((unsigned char)'a') && isdigit((unsigned char)'7'));
    for(unsigned ch=0;ch<256;++ch){(void)isalpha((unsigned char)ch);(void)isblank((unsigned char)ch);}
    int ages[5]={23,43,12,89,2};const char *names[5]={"Alan","Frank","Mary","John","Lisa"};
    indices(ages,names,5);pointers(ages,names,5);while_indices(ages,names,5);while_pointers(ages,names,5);
    int reversed[5];size_t k=0;
    for(const int *p=ages+5;p!=ages;){--p;reversed[k++]=*p;printf("reverse-age:%d\n",*p);}
    const int expected[5]={2,89,12,43,23};assert(memcmp(reversed,expected,sizeof expected)==0);
    for(size_t q=0;q<5;++q){
        assert(*(ages+q)==ages[q] && &ages[q]==ages+q);
        printf("address:%p:%p\n",(void *)&ages[q],(void *)(ages+q));
    }
    struct StackPerson person={.name="Stack Joe",.age=32,.height=64,.weight=140};
    struct StackPerson changed=older(person);
    assert(person.age==32&&changed.age==52);person.height-=2;
    printf("stack:%s:%d:%d:%d\n",person.name,person.age,person.height,person.weight);
    puts("PASS middle extensions");
    return 0;
}
