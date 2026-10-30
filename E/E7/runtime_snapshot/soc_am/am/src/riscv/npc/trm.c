#include <am.h>
#include <klib-macros.h>
#include "e7_config.h"
extern char _heap_start, _pmem_start;
int main(const char *args);
#ifdef __PLATFORM_YSYXSOC
#define PMEM_SIZE (8 * 1024 * 1024)
#else
#define PMEM_SIZE (128 * 1024 * 1024)
#endif
Area heap = RANGE(&_heap_start, (uintptr_t)&_pmem_start + PMEM_SIZE);
static const char mainargs[MAINARGS_MAX_LEN] = TOSTRING(MAINARGS_PLACEHOLDER);
void putch(char ch) {
#ifdef __PLATFORM_YSYXSOC
  volatile uint8_t *uart=(volatile uint8_t *)0x10000000u;
  while ((uart[5] & 0x20u) == 0) {}
  uart[0]=(uint8_t)ch;
#else
  while (*(volatile uint32_t *)0x10000004u == 0) {}
  *(volatile uint8_t *)0x10000000u = (uint8_t)ch;
#endif
}
void halt(int code) {
  asm volatile("mv a0, %0; ebreak" : : "r"(code) : "a0", "memory");
  while (1) {}
}
void _trm_init() {
#ifdef __PLATFORM_YSYXSOC
  volatile uint8_t *uart=(volatile uint8_t *)0x10000000u;
  uart[3]=0x80; uart[0]=UART_DIVISOR&0xff; uart[1]=(UART_DIVISOR>>8)&0xff;
  uart[3]=0x03; uart[1]=0; uart[2]=0x07;
#endif
  halt(main(mainargs));
}
