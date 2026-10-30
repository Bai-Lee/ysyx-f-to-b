#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <assert.h>
#include <device/map.h>
#include <utils.h>

static uint32_t storage[2];
static io_callback_t callback;
static uint64_t current_time;
uint8_t *new_space(int size) { assert(size==8);return (uint8_t *)storage; }
void add_mmio_map(const char *name,uint32_t address,void *space,uint32_t size,io_callback_t cb) {
  assert(name && address==CONFIG_RTC_MMIO && space==storage && size==8);callback=cb;
}
uint64_t get_time(void) { return current_time; }
void init_timer(void);

int main(int argc,char **argv) {
  (void)argv;init_timer();assert(callback);
  if(argc>1){callback(2,4,false);return 2;}
  uint64_t values[]={0,0xfffffff0ull,0x100000005ull,0x200000003ull,0xfffffffffffffffeull};
  unsigned differences=0;
  for(unsigned i=0;i<sizeof(values)/sizeof(values[0]);i++) {
    current_time=values[i];uint32_t oldlo=storage[0];
    callback(4,4,false);uint32_t hi=storage[1];
    callback(0,4,false);uint32_t lo=storage[0];
    assert((((uint64_t)hi<<32)|lo)==values[i]);
    if(oldlo!=lo){assert((((uint64_t)hi<<32)|oldlo)!=values[i]);differences++;}
  }
  assert(differences==4);
  printf("C2_RTC_MODEL_PASS high_low=5 stale_low_high_detected=%u\n",differences);
  return 0;
}
