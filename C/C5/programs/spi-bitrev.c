#include <am.h>
#include "spi_io.h"
int main(const char *args) {
  (void)args;
  for(unsigned value=0;value<256;value++){
    unsigned reverse=0;
    for(unsigned i=0;i<8;i++)reverse=(reverse<<1)|((value>>i)&1);
    unsigned actual=spi_transfer(7,16,value<<8,0)&255;
    if(actual!=reverse)halt(31);
  }
  return 0;
}
