#include <am.h>
#include <stdint.h>
volatile uint32_t initialized=0x1234a5c7u;
volatile uint8_t odd_bytes[3]={3,4,5};
volatile uint64_t wide_initialized=0x1122334455667788ull;
volatile uint32_t zeroed[16];
static __attribute__((noinline)) uint32_t stack_check(unsigned n) {
  volatile uint32_t words[16];
  for(unsigned i=0;i<16;i++)words[i]=0x11220000u+i+n;
  uint32_t result=n?stack_check(n-1):0;
  for(unsigned i=0;i<16;i++)if(words[i]!=0x11220000u+i+n)halt(13);
  return result+n;
}
int main(const char *args) {
  (void)args;
  if(initialized!=0x1234a5c7u||odd_bytes[0]!=3||odd_bytes[1]!=4||odd_bytes[2]!=5||wide_initialized!=0x1122334455667788ull)halt(11);
  for(unsigned i=0;i<16;i++)if(zeroed[i]!=0)halt(12);
  initialized^=0xffffffffu;zeroed[15]=0xa5a55a5au;
  if(initialized!=0xedcb5a38u||zeroed[15]!=0xa5a55a5au)halt(14);
  if(stack_check(5)!=15)halt(15);
  return 0;
}
