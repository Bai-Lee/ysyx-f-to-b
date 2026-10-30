#include <am.h>
#include <klib-macros.h>
#include <klib.h>
extern char _heap_start,_heap_end;
Area heap=RANGE(&_heap_start,&_heap_end);
static const char mainargs[MAINARGS_MAX_LEN]=TOSTRING(MAINARGS_PLACEHOLDER);
#define UART ((volatile unsigned char *)0x10000000u)
#if SOC_UART_MODE >= 1
static void uart_init(void) {
  UART[3]=0x83;
  UART[1]=(SOC_UART_DIV>>8)&255;
  UART[0]=SOC_UART_DIV&255;
  UART[3]=0x03;
  UART[2]=0x07;
}
#endif
void putch(char c) {
#if SOC_UART_MODE >= 2
  while((UART[5]&0x20)==0){}
#endif
  UART[0]=(unsigned char)c;
}
void halt(int code) {
#if SOC_UART_MODE >= 1
  while((UART[5]&0x40)==0){}
#endif
  __asm__ volatile("mv a0,%0; ebreak" : : "r"(code) : "a0","memory");
  for(;;){}
}
int main(const char *args);
void _trm_init(void) {
#if SOC_UART_MODE >= 1
  uart_init();
#endif
#if SOC_PRINT_ID
  unsigned vendor,project;
  __asm__ volatile("csrr %0,mvendorid":"=r"(vendor));
  __asm__ volatile("csrr %0,marchid":"=r"(project));
  printf("C5 ID vendor=%08x project=%08x\n",vendor,project);
#endif
  halt(main(mainargs));
}
