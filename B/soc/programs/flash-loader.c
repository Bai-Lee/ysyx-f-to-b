#include <am.h>
#include <stdint.h>
#include "spi_io.h"
#include "payload.h"
int main(const char *args) {
  (void)args;
#ifdef COPY_TO_SRAM
  volatile uint32_t *destination=(volatile uint32_t*)PAYLOAD_ENTRY;
  for(unsigned i=0;i<PAYLOAD_WORDS;i++){
    uint32_t value=flash_read(PAYLOAD_OFFSET+i*4);
    if(value!=payload_words[i])halt(41);
    destination[i]=value;
  }
#ifdef CORRUPT_COPY
  destination[0]^=1;
#endif
  for(unsigned i=0;i<PAYLOAD_WORDS;i++)if(destination[i]!=payload_words[i])halt(42);
#endif
  ((void(*)(void))PAYLOAD_ENTRY)();
  halt(43);
  return 0;
}
