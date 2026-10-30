#include <am.h>
#include <klib.h>
#include <klib-macros.h>
static unsigned char stacks[2][1536] __attribute__((aligned(16)));
static Context *workers[2],*parent;
static int active=-1,target;
static volatile unsigned progress[2];
static const unsigned cookies[2]={0x51826374,0xe7d6c5b4};
extern int context_probe(void);
int probe_check(const unsigned *saved) {
  for(unsigned i=1;i<16;i++) {
    unsigned expected=i==2?(uintptr_t)saved:i==3?saved[19]:i==15?~0u:0x10000000u+i;
    if(saved[i]!=expected)return i;
  }
  return 0;
}
static Context *handler(Event event,Context *context) {
  assert(event.event==EVENT_YIELD && context->mcause==11);
  assert((context->mstatus&8)==0 && (context->mstatus&0x1800)==0x1800);
  if(active<0) {parent=context;active=target;return workers[target];}
  workers[active]=context;active=-1;return parent;
}
static void worker(void *argument) {
  unsigned id=argument==&cookies[0]?0:1;
  assert(argument==&cookies[id] && *(unsigned *)argument==cookies[id]);
  volatile unsigned local[8];for(unsigned i=0;i<8;i++)local[i]=cookies[id]^i;
  for(unsigned round=0;round<12;round++) {
    int result=context_probe();if(result)halt(90+result);
    for(unsigned i=0;i<8;i++)assert(local[i]==(cookies[id]^i));
    progress[id]++;
  }
  yield();halt(81);
}
int main(const char *args) {
  (void)args;cte_init(handler);
  for(unsigned i=0;i<2;i++) {
    workers[i]=kcontext(RANGE(stacks[i],stacks[i]+sizeof stacks[i]),worker,(void *)&cookies[i]);
    assert(workers[i]->gpr[10]==(uintptr_t)&cookies[i] && workers[i]->gpr[2]%16==0);
  }
  iset(true);assert(ienabled());iset(false);assert(!ienabled());iset(true);
  for(unsigned round=0;round<13;round++)for(target=0;target<2;target++)yield();
  assert(progress[0]==12&&progress[1]==12);
  printf("C5_CTE_PASS a=%u b=%u\n",progress[0],progress[1]);return 0;
}
