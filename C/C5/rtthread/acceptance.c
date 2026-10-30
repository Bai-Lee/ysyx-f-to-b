#include <am.h>
#include <klib.h>
#include <rtthread.h>
#include <rthw.h>
extern volatile unsigned c5_context_switches,c5_thread_returns;
static volatile unsigned turns[2];
static void worker(void *argument) {
  uintptr_t id=(uintptr_t)argument;
  volatile unsigned sentinel[8];
  for(unsigned i=0;i<8;i++)sentinel[i]=0x12340000u+(id<<8)+i;
  for(unsigned round=0;round<12;round++) {
    for(unsigned i=0;i<8;i++)assert(sentinel[i]==0x12340000u+(id<<8)+i);
    turns[id]++;rt_thread_yield();
  }
}
static int c5_context_test(int argc,char **argv) {
  (void)argc;(void)argv;
  unsigned before=c5_context_switches,returns=c5_thread_returns;
  turns[0]=turns[1]=0;
  rt_base_t first=rt_hw_interrupt_disable(),second=rt_hw_interrupt_disable();
  assert(!ienabled() && second==0);rt_hw_interrupt_enable(second);assert(!ienabled());
  rt_hw_interrupt_enable(first);assert(ienabled()==(first!=0));
  rt_uint8_t priority=rt_thread_self()->current_priority;
  rt_thread_t a=rt_thread_create("c5-a",worker,(void *)0,2048,priority,20);
  rt_thread_t b=rt_thread_create("c5-b",worker,(void *)1,2048,priority,20);
  assert(a&&b);rt_thread_startup(a);rt_thread_startup(b);
  for(unsigned i=0;i<80 && (turns[0]!=12 || turns[1]!=12 || c5_thread_returns<returns+2);i++)rt_thread_yield();
  assert(turns[0]==12 && turns[1]==12 && c5_thread_returns>=returns+2);
  assert(c5_context_switches>=before+24);
  rt_kprintf("C5_CONTEXT_PASS a=%u b=%u switches=%u returns=%u\n",turns[0],turns[1],c5_context_switches-before,c5_thread_returns-returns);
  return 0;
}
MSH_CMD_EXPORT(c5_context_test,C5 real trap context switch and return validation);
static int c5_done(int argc,char **argv) {
  extern unsigned c5_app_failures __attribute__((weak));
  (void)argc;(void)argv;
  if(&c5_app_failures && c5_app_failures)halt(84);
  rt_kprintf("C5_RTTHREAD_PASS\n");halt(0);return 0;
}
MSH_CMD_EXPORT(c5_done,C5 stop after original scripted commands and context checks);
