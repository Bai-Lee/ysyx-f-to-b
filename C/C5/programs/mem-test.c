#include <am.h>
#include <klib-macros.h>
#include <stdint.h>
#define check(condition) do { if(!(condition)) halt(1); } while(0)
#define TEST_TYPE(type) do { \
  for(unsigned pass=0;pass<2;pass++){ \
    for(volatile type *p=(volatile type*)heap.start;(uintptr_t)p<(uintptr_t)heap.end;p++){ \
      uint64_t value=(uintptr_t)p; *p=(type)(pass?~value:value); \
    } \
    if(corrupt){volatile type *first=(volatile type*)heap.start;*first^=(type)1;} \
    for(volatile type *p=(volatile type*)heap.start;(uintptr_t)p<(uintptr_t)heap.end;p++){ \
      uint64_t value=(uintptr_t)p;check(*p==(type)(pass?~value:value)); \
    } \
  } \
} while(0)
int main(const char *args) {
  int corrupt=args[0]=='x';
#ifdef MEMTEST_BASE
  heap=(Area){(void*)(uintptr_t)MEMTEST_BASE,(void*)(uintptr_t)(MEMTEST_BASE+MEMTEST_BYTES)};
#endif
  check((uintptr_t)heap.end>(uintptr_t)heap.start);
  check(((uintptr_t)heap.start&7)==0&&((uintptr_t)heap.end&7)==0);
  TEST_TYPE(uint8_t);TEST_TYPE(uint16_t);TEST_TYPE(uint32_t);TEST_TYPE(uint64_t);
  return 0;
}
