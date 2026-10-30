#define UART_BASE 0x10000000u
#define UART_TX 0
void _start(void) {
  *(volatile unsigned char *)(UART_BASE + UART_TX) = 'A';
#ifdef INCLUDE_NEWLINE
  *(volatile unsigned char *)(UART_BASE + UART_TX) = '\n';
#endif
#ifdef FINISH_TRAP
  __asm__ volatile("li a0, 0; ebreak" : : : "a0", "memory");
#endif
  for (;;) {}
}
