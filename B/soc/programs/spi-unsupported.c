#include <am.h>
#include "spi_io.h"
int main(const char *args) {
  (void)args;
  (void)spi_transfer(0,64,0,0x9f000000u);
  halt(45);
  return 0;
}
