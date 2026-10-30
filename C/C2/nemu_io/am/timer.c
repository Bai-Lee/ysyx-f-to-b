#include <am.h>
#include <nemu.h>

static uint64_t start_us;
static uint64_t snapshot_us(void) {
  /* The NEMU RTC callback snapshots both words when the high word is read. */
  uint32_t hi = inl(RTC_ADDR + 4);
  uint32_t lo = inl(RTC_ADDR);
  return ((uint64_t)hi << 32) | lo;
}

void __am_timer_init(void) { start_us = snapshot_us(); }
void __am_timer_uptime(AM_TIMER_UPTIME_T *uptime) { uptime->us = snapshot_us() - start_us; }
void __am_timer_rtc(AM_TIMER_RTC_T *rtc) {
  *rtc = (AM_TIMER_RTC_T) { .year=1900, .month=0, .day=0, .hour=0, .minute=0, .second=0 };
}
