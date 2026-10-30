#include <am.h>
#include <stdint.h>
#include "spi_io.h"
static uint8_t pattern(uint32_t address){return (uint8_t)((address^(address>>8)^(address>>16)^0xa7u)&255);}
static uint32_t expected(uint32_t address){uint32_t value=0;for(unsigned i=0;i<4;i++)value|=(uint32_t)pattern(address+i)<<(8*i);return value;}
int main(const char *args) {
  (void)args;
  const uint32_t addresses[]={0,4,0x1fc,0x1000,0x12344,0x7ffffc,0xfffffc};
  for(unsigned i=0;i<sizeof(addresses)/sizeof(addresses[0]);i++){
    uint32_t offset=addresses[i];
#ifdef SERIAL_READ
    uint32_t value=flash_read(offset);
#else
    uint32_t value=*(volatile uint32_t*)(0x30000000u+offset);
#endif
    if(value!=expected(offset))halt(32);
  }
#ifndef SERIAL_READ
  const uint32_t bytes[]={1,2,3,0x7fffff,0xffffff};
  for(unsigned i=0;i<sizeof(bytes)/sizeof(bytes[0]);i++)if(*(volatile uint8_t*)(0x30000000u+bytes[i])!=pattern(bytes[i]))halt(33);
  if(*(volatile uint16_t*)0x30fffffeu!=((uint16_t)pattern(0xfffffe)|((uint16_t)pattern(0xffffff)<<8)))halt(34);
#endif
  return 0;
}
