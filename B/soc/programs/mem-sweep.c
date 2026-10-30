#include <am.h>
#include <stdint.h>
#ifndef MEMTEST_BASE
#define MEMTEST_BASE 0x80000000u
#endif
#ifndef MEMTEST_BYTES
#define MEMTEST_BYTES 0x400000u
#endif
// Bounds are local constants: volatile target writes must not force reloading
// the unrelated global heap descriptor on every iteration.
#define SWEEP(type,tag) do { \
 for(unsigned inverse=0;inverse<2;inverse++){ \
  for(volatile type *p=(volatile type*)begin;(uintptr_t)p<end;p++){ \
   uint64_t value=(uintptr_t)p;*p=(type)(inverse?~value:value); \
  } \
  if(corrupt){volatile type *p=(volatile type*)begin;*p^=(type)1;} \
  for(volatile type *p=(volatile type*)begin;(uintptr_t)p<end;p++){ \
   uint64_t value=(uintptr_t)p;if(*p!=(type)(inverse?~value:value))halt(71); \
  } \
  putch(inverse?(tag)+32:(tag));putch('\n'); \
 } \
} while(0)
int main(const char *args){
 const uintptr_t begin=MEMTEST_BASE,end=MEMTEST_BASE+MEMTEST_BYTES;
 const int corrupt=args[0]=='x';
 if(end<=begin||(begin&7)||(end&7))halt(72);
 SWEEP(uint8_t,'B');SWEEP(uint16_t,'H');SWEEP(uint32_t,'W');SWEEP(uint64_t,'Q');
 return 0;
}
