#include <am.h>
#include <stdint.h>
#include <klib.h>
#ifndef MEMORY_CAPACITY
#define MEMORY_CAPACITY 33554432u
#endif
static unsigned offsets[128],count;
static void add(unsigned offset){
  if(offset>=MEMORY_CAPACITY||(offset&3))return;
  for(unsigned i=0;i<count;i++)if(offsets[i]==offset)return;
  if(count==128)halt(85);
  offsets[count++]=offset;
}
static uint32_t value(unsigned offset){return 0x81629374u^(offset*0x10203u);}
int main(const char *args){
  add(0);add(MEMORY_CAPACITY-4);add(MEMORY_CAPACITY/2-4);add(MEMORY_CAPACITY/2);add(MEMORY_CAPACITY/2+4);
  for(unsigned bit=2;(1u<<bit)<MEMORY_CAPACITY;bit++){
    add((1u<<bit)-4);add(1u<<bit);add((1u<<bit)+4);
  }
  for(unsigned i=0;i<count;i++)*(volatile uint32_t *)(0xa0000000u+offsets[i])=value(offsets[i]);
  if(args[0]=='x')*(volatile uint32_t *)(0xa0000000u+MEMORY_CAPACITY-4)^=1;
  for(unsigned i=count;i>0;i--)if(*(volatile uint32_t *)(0xa0000000u+offsets[i-1])!=value(offsets[i-1]))halt(86);
  for(unsigned i=0;i<count;i++){
    uintptr_t address=0xa0000000u+offsets[i];
    *(volatile uint8_t *)(address+1)=0x5a;*(volatile uint16_t *)(address+2)=0xc33c;
    if(*(volatile uint32_t *)address!=((value(offsets[i])&255)|0xc33c5a00u))halt(87);
  }
  printf("C5_MEMORY_BOUNDARIES_PASS points=%u bytes=%u\n",count,MEMORY_CAPACITY);return 0;
}
