#include <am.h>
#include <klib.h>
#include <klib-macros.h>
static unsigned yields;
static Context *trap(Event event,Context *context) {
  assert(event.event==EVENT_YIELD && context->mcause==11);
  assert(context->GPR1==(uintptr_t)-1 && context->mepc%4==0);
  yields++;putch('y');return context;
}
int main(const char *args) {
  (void)args;cte_init(trap);
  for(unsigned i=0;i<16;i++)yield();
  assert(yields==16);printf("\nB1_YIELD_PASS count=%u\n",yields);return 0;
}
