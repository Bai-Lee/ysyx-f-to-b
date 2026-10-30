#include <am.h>
#include <klib.h>
#include <stdint.h>
#define read_csr(name) ({uint32_t value;__asm__ volatile("csrr %0," #name:"=r"(value));value;})
#define write_csr(name,value) __asm__ volatile("csrw " #name ",%0"::"r"((uint32_t)(value)):"memory")
#define check(test) do{if(!(test))halt(61);}while(0)
static uint64_t cycles(void) {
  uint32_t hi,lo,again;
  do{hi=read_csr(mcycleh);lo=read_csr(mcycle);again=read_csr(mcycleh);}while(hi!=again);
  return ((uint64_t)hi<<32)|lo;
}
int main(const char *args) {
  (void)args;
  check(read_csr(mvendorid)==0x79737978u&&read_csr(marchid)==0x26070001u);
  uint64_t before=cycles();
  for(unsigned i=0;i<32;i++) {
    __asm__ volatile("nop; nop; nop; nop":::"memory");
    uint64_t after=cycles();check(after>before);before=after;
  }
  write_csr(mcycleh,0);write_csr(mcycle,0xffffff00u);
  for(unsigned i=0;i<1024;i++)__asm__ volatile("nop":::"memory");
  check(read_csr(mcycleh)==1);
  uint32_t old;
  write_csr(mcycleh,3);
  __asm__ volatile("csrrs %0,mcycleh,zero":"=r"(old)::"memory");check(old==3);
  __asm__ volatile("csrrci %0,mcycleh,1":"=r"(old)::"memory");check(old==3&&read_csr(mcycleh)==2);
  __asm__ volatile("csrrsi %0,mcycleh,4":"=r"(old)::"memory");check(old==2&&read_csr(mcycleh)==6);
  printf("B1_MCYCLE_PASS vendor=%08x project=%08x\n",read_csr(mvendorid),read_csr(marchid));
  return 0;
}
