#include <am.h>
#include <klib.h>
#include <stdint.h>
#ifndef C4_CLINT_HZ
#define C4_CLINT_HZ 100000000u
#endif
static uint32_t ticks_hz=C4_CLINT_HZ;
void c4_timer_set_frequency(uint32_t hz) { assert(hz>0);ticks_hz=hz; }
void __am_timer_init(void) {}
void __am_timer_uptime(AM_TIMER_UPTIME_T *uptime) {
  uint32_t lo=*(volatile uint32_t *)0x20000000u;
  uint32_t hi=*(volatile uint32_t *)0x20000004u;
  uint64_t value=((uint64_t)hi<<32)|lo;
#ifdef C4_RTL_TIMER
  uptime->us=(value/ticks_hz)*1000000u+((value%ticks_hz)*1000000u)/ticks_hz;
#else
  uptime->us=value;
#endif
}
void __am_timer_rtc(AM_TIMER_RTC_T *rtc) {
  *rtc=(AM_TIMER_RTC_T){.year=1900,.month=0,.day=0,.hour=0,.minute=0,.second=0};
}
