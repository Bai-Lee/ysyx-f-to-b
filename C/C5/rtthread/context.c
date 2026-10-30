#include <am.h>
#include <klib.h>
#include <rtthread.h>

/* Single CPU, synchronous traps only. No asynchronous interrupt source is enabled. */
static Context **switch_from, **switch_to;
volatile unsigned c5_context_switches, c5_thread_returns;
struct thread_start { void (*entry)(void *); void *parameter; void (*exit)(void); };
static void start_thread(void *argument) {
  struct thread_start start=*(struct thread_start *)argument;
  start.entry(start.parameter);
  c5_thread_returns++;
  start.exit();
  halt(78);
}
static Context *ev_handler(Event event,Context *context) {
  assert(event.event==EVENT_YIELD && switch_to!=NULL);
  Context *next=*switch_to;
  if(switch_from) *switch_from=context;
  switch_from=switch_to=NULL;
  c5_context_switches++;
  assert(next!=NULL);
  return next;
}
void __am_cte_init(void) { cte_init(ev_handler); }
void rt_hw_context_switch_to(rt_ubase_t to) {
  assert(switch_to==NULL);switch_from=NULL;switch_to=(Context **)to;
  yield();
  halt(79);
}
void rt_hw_context_switch(rt_ubase_t from,rt_ubase_t to) {
  assert(switch_to==NULL);switch_from=(Context **)from;switch_to=(Context **)to;
  yield();
}
void rt_hw_context_switch_interrupt(rt_ubase_t from,rt_ubase_t to,rt_thread_t from_thread,rt_thread_t to_thread) {
  (void)from;(void)to;(void)from_thread;(void)to_thread;
  /* The current SoC/AM profile has no asynchronous interrupt delivery. */
  halt(80);
}
rt_uint8_t *rt_hw_stack_init(void *entry,void *parameter,rt_uint8_t *stack_addr,void *exit) {
  uintptr_t top=((uintptr_t)stack_addr+sizeof(rt_ubase_t))&~(uintptr_t)15;
  top=(top-sizeof(struct thread_start))&~(uintptr_t)15;
  struct thread_start *start=(struct thread_start *)top;
  *start=(struct thread_start){entry,parameter,exit};
  return (rt_uint8_t *)kcontext((Area){(void *)(top-sizeof(Context)),(void *)top},start_thread,start);
}
