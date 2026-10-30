#include <am.h>
#include <klib.h>
#include <klib-macros.h>
#include <stdint.h>
int main(const char *args){
  (void)args;ioe_init();volatile uint32_t *gpio=(volatile uint32_t *)0x10002000u;
  unsigned project;__asm__ volatile("csrr %0,marchid":"=r"(project));gpio[2]=project;
  printf("C5 ID=%08x\nLOCKED: set switches to A55A\n",project);
  while(gpio[1]!=0xa55a){}
  printf("UNLOCKED\n");
  for(unsigned i=0;i<16;i++){
    gpio[0]=1u<<i;
    uint64_t start=io_read(AM_TIMER_UPTIME).us;
    while(io_read(AM_TIMER_UPTIME).us-start<10000){}
  }
  gpio[0]=0xa55a;printf("C5_GPIO_DONE\n");
  for(;;)__asm__ volatile("nop");
}
