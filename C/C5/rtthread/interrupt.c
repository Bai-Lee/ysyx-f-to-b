#include <am.h>
#include <rthw.h>
rt_base_t rt_hw_interrupt_disable(void) {
  rt_base_t previous=ienabled();iset(false);return previous;
}
void rt_hw_interrupt_enable(rt_base_t previous) { iset(previous!=0); }
