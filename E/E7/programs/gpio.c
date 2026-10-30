#include <am.h>
#include <klib.h>
#include <klib-macros.h>
#define LED (*(volatile uint32_t *)0x20001000u)
#define SWITCH (*(volatile uint32_t *)0x20001004u)
#define DIGITS (*(volatile uint32_t *)0x20001008u)
int main(const char *args){
 (void)args;uint32_t vendor,id;
 asm volatile("csrr %0, mvendorid":"=r"(vendor));
 asm volatile("csrr %0, marchid":"=r"(id));
 assert(vendor==0x79737978u&&id==26070001u);
 printf("CSR vendor=%x project=%u\n",vendor,id);DIGITS=id;
 uint32_t first,last,hi;
 asm volatile("csrr %0, mcycle":"=r"(first));
 for(volatile int i=0;i<100;i++){}
 asm volatile("csrr %0, mcycle":"=r"(last));
 asm volatile("csrr %0, mcycleh":"=r"(hi));
 assert(last>first&&hi==0);printf("MCYCLE delta=%u\n",last-first);
 putstr("LOCKED: set switches to A55A\n");LED=0;
 while((SWITCH&0xffffu)!=0xa55au){}
 putstr("UNLOCKED\n");
 for(unsigned i=0;i<16;i++){
  LED=1u<<i;
  uint64_t start=io_read(AM_TIMER_UPTIME).us;
  while(io_read(AM_TIMER_UPTIME).us-start<20000){}
 }
 LED=0xa55a;putstr("GPIO_SEQUENCE_PASS\n");return 0;
}
