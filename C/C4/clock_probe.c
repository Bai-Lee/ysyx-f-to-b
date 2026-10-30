#include <am.h>
#include <klib.h>
#include <klib-macros.h>
void c4_timer_set_frequency(uint32_t hz);
int main(const char *args) {
  unsigned hz=(unsigned)atoi(args);if(hz)c4_timer_set_frequency(hz);ioe_init();
  uint64_t start=io_read(AM_TIMER_UPTIME).us;
  for(unsigned second=1;second<=3;second++) {
    while(io_read(AM_TIMER_UPTIME).us-start<(uint64_t)second*1000000u){}
    printf("C4_CLOCK %u\n",second);
  }
  return 0;
}
