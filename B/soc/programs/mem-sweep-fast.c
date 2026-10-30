#include <am.h>
#include <stdint.h>
#ifndef MEMTEST_BASE
#define MEMTEST_BASE 0xa0000000u
#endif
#ifndef MEMTEST_BYTES
#define MEMTEST_BYTES 4096u
#endif
/* Four explicit volatile accesses reduce loop bookkeeping without changing the
 * address/inverse patterns, access widths, pass ordering, or coverage counts. */
#define VALUE(n) ((type)(uintptr_t)(p+(n)) ^ mask)
#define WRITE(n) p[n]=VALUE(n)
#define CHECK(n) if(p[n]!=VALUE(n))halt(71)
#define SWEEP(T,tag) do { \
 typedef T type; \
 for(unsigned inverse=0;inverse<2;inverse++){ \
  const type mask=inverse?(type)~(type)0:(type)0; \
  for(volatile type *p=(volatile type*)begin;(uintptr_t)p<end;p+=4){WRITE(0);WRITE(1);WRITE(2);WRITE(3);} \
  if(corrupt){volatile type *p=(volatile type*)begin;*p^=(type)1;} \
  for(volatile type *p=(volatile type*)begin;(uintptr_t)p<end;p+=4){CHECK(0);CHECK(1);CHECK(2);CHECK(3);} \
  putch(inverse?(tag)+32:(tag));putch('\n'); \
 } \
} while(0)
int main(const char *args){
 const uintptr_t begin=MEMTEST_BASE,end=MEMTEST_BASE+MEMTEST_BYTES;
 const int corrupt=args[0]=='x';
 if(end<=begin||(begin&31)||(end&31))halt(72);
 SWEEP(uint8_t,'B');SWEEP(uint16_t,'H');SWEEP(uint32_t,'W');SWEEP(uint64_t,'Q');
 return 0;
}
