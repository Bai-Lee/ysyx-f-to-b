#include <am.h>
#include <stdint.h>
int main(const char *args) {
  (void)args;
  *(volatile uint32_t*)0x30000000u=0;
  halt(44);
  return 0;
}
