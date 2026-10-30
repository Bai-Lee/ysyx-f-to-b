#include <am.h>
#include <klib.h>
#include <klib-macros.h>
#include <stddef.h>
_Static_assert(sizeof(Context)==80,"RV32E Context size");
_Static_assert(offsetof(Context,gpr)==0&&offsetof(Context,mcause)==64&&offsetof(Context,mstatus)==68&&offsetof(Context,mepc)==72&&offsetof(Context,pdir)==76,"Context/trap offsets");
static Context *(*user_handler)(Event,Context*);
extern void __am_asm_trap(void);
Context *__am_irq_handle(Context *context) {
  Event event={0};event.cause=context->mcause;
  if(context->mcause==11){
    event.event=context->GPR1==(uintptr_t)-1?EVENT_YIELD:EVENT_SYSCALL;
    context->mepc+=4;
  }else event.event=EVENT_ERROR;
  if(user_handler){context=user_handler(event,context);assert(context!=NULL);}
  return context;
}
bool cte_init(Context *(*handler)(Event,Context*)) {
  user_handler=handler;
  __asm__ volatile("csrw mtvec,%0"::"r"(__am_asm_trap):"memory");
  return true;
}
static void context_returned(void){halt(77);}
Context *kcontext(Area stack,void (*entry)(void*),void *arg) {
  uintptr_t top=(uintptr_t)stack.end&~(uintptr_t)15;
  assert(top>=(uintptr_t)stack.start+sizeof(Context));
  Context *context=(Context*)(top-sizeof(Context));memset(context,0,sizeof(*context));
  uintptr_t gp;__asm__ volatile("mv %0,gp":"=r"(gp));
  context->gpr[1]=(uintptr_t)context_returned;context->gpr[2]=top;context->gpr[3]=gp;
  context->gpr[10]=(uintptr_t)arg;context->mepc=(uintptr_t)entry;context->mstatus=0x1880;
  return context;
}
void yield(void){__asm__ volatile("li a5,-1; ecall":::"a5","memory");}
bool ienabled(void){uintptr_t status;__asm__ volatile("csrr %0,mstatus":"=r"(status));return (status&8)!=0;}
void iset(bool enable){
  if(enable)__asm__ volatile("csrsi mstatus,8":::"memory");
  else __asm__ volatile("csrci mstatus,8":::"memory");
}
