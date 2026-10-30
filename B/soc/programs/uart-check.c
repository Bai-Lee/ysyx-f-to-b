#include <am.h>
#include <stdint.h>
#define UART ((volatile uint8_t*)0x10000000u)
int main(const char *args) {
  if(UART[3]!=3)halt(21);
  UART[3]=0x83;
  uint8_t low=UART[0],high=UART[1];
  if(low!=(SOC_UART_DIV&255)||high!=((SOC_UART_DIV>>8)&255))halt(22);
  UART[3]=3;
  unsigned count=0;
  for(const char *p=args;*p;p++){if(*p<'0'||*p>'9')halt(23);count=count*10+(*p-'0');}
  if(count>4096)halt(24);
  for(unsigned i=0;i<count;i++)putch((char)(i&255));
  while((UART[5]&0x40)==0){}
  return 0;
}
