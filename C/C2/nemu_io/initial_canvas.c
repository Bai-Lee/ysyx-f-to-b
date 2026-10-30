#include <am.h>
#include <klib.h>
#include <klib-macros.h>
#include <nemu.h>

/* A separate teaching variant of the initial GPU exercise. Link wrapping
 * leaves the final general-purpose AM driver byte-identical. */
void __wrap___am_gpu_init(void) {
  uint32_t size=inl(VGACTL_ADDR);
  unsigned w=size>>16,h=size&0xffff;
  assert(w==400 && h==300);
  volatile uint32_t *fb=(volatile uint32_t *)(uintptr_t)FB_ADDR;
  for(unsigned i=0;i<w*h;i++)fb[i]=i;
  outl(VGACTL_ADDR+4,1);
  printf("INITIAL_CANVAS %u %u\n",w,h);
}
int main(void) {
  ioe_init();
  while(1) { (void)io_read(AM_TIMER_UPTIME); }
  return 0;
}
