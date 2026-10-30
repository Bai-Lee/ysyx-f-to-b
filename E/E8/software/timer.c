#include <am.h>
#include "e7_config.h"
static uint64_t boot_cycles;
static uint64_t read_cycles(void) {
  uint32_t hi,lo,again;
  /* A high-low-high retry also works when the 64-bit counter crosses a boundary. */
  do {
    asm volatile("csrr %0, mcycleh":"=r"(hi));
    asm volatile("csrr %0, mcycle":"=r"(lo));
    asm volatile("csrr %0, mcycleh":"=r"(again));
  } while (hi!=again);
  return ((uint64_t)hi<<32)|lo;
}
void __am_timer_init() { boot_cycles=read_cycles(); }
void __am_timer_uptime(AM_TIMER_UPTIME_T *uptime) {
#ifdef __PLATFORM_YSYXSOC__
  const uint32_t hz=SOC_CPU_HZ;
#else
  const uint32_t hz=NPC_CPU_HZ;
#endif
  uptime->us=(read_cycles()-boot_cycles)/(hz/1000000u);
}
void __am_timer_rtc(AM_TIMER_RTC_T *rtc) {
  *rtc=(AM_TIMER_RTC_T){.year=1900};
}
