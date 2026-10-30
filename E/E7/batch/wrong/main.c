#include <am.h>
#include <klib.h>
extern int batch_call(int (*fn)(void));
extern int cpu_wrong__main(void);
struct test_case {const char *name;int (*fn)(void);int assembly;};
static const struct test_case cases[]={
{"cpu:wrong", cpu_wrong__main, 0}};
static uint64_t count(void){uint32_t h,l,h2;do{asm volatile("csrr %0,mcycleh":"=r"(h));asm volatile("csrr %0,mcycle":"=r"(l));asm volatile("csrr %0,mcycleh":"=r"(h2));}while(h!=h2);return ((uint64_t)h<<32)|l;}
int main(const char *args){(void)args;for(unsigned i=0;i<sizeof(cases)/sizeof(cases[0]);i++){
 printf("[CASE] %s BEGIN\n",cases[i].name);uint64_t start=count();
 int code=cases[i].assembly?batch_call(cases[i].fn):cases[i].fn();uint64_t elapsed=count()-start;
 if(code){printf("[CASE] %s FAIL code=%d\n",cases[i].name,code);halt(code);}
 printf("[CASE] %s PASS cycles=%llu\n",cases[i].name,elapsed);
 }printf("BATCH_ALL_PASSED %u\n",(unsigned)(sizeof(cases)/sizeof(cases[0])));return 0;}
