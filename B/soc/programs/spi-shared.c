#include <am.h>
#include <klib.h>
#include <stdint.h>
#define SPI ((volatile uint32_t *)0x10001000u)
__attribute__((noinline)) static uint32_t software_flash_read(unsigned offset){
  unsigned poll;
  for(poll=0;poll<10000;poll++)if(!(SPI[4]&0x100))break;
  if(poll==10000)halt(89);
  const uint32_t config=(1u<<13)|(1u<<10)|64;
  SPI[4]=config;SPI[0]=0;SPI[1]=0x03000000u|offset;SPI[5]=0;SPI[6]=1;SPI[4]=config|0x100;
  for(poll=0;poll<10000;poll++)if(!(SPI[4]&0x100))break;
  if(poll==10000)halt(89);
  uint32_t value=SPI[0];
  return ((value&255)<<24)|((value&0xff00)<<8)|((value>>8)&0xff00)|((value>>24)&255);
}
int main(const char *args){
  (void)args;uint32_t value=software_flash_read(0x80000);
  printf("C5_SHARED_SPI value=%08x expected=51c0ffee\n",value);
  if(value!=0x51c0ffee)halt(88);
  return 0;
}
