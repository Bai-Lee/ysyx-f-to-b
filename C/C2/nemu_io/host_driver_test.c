#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <am.h>
#include <nemu.h>

uint32_t c2_framebuffer[400 * 300 + 2];
static uint32_t keyboard_value, sync_value;
static uint64_t clock_value, clock_snapshot;
static unsigned timer_reads, sync_writes;

uint32_t inl(uintptr_t address) {
  if (address == VGACTL_ADDR) return (400u << 16) | 300u;
  if (address == KBD_ADDR) return keyboard_value;
  if (address == RTC_ADDR + 4) {
    clock_snapshot=clock_value;
    clock_value+=0x100000001ull; /* Cross a low-half boundary between bus reads. */
    timer_reads++;
    return clock_snapshot >> 32;
  }
  if (address == RTC_ADDR) { timer_reads++; return (uint32_t)clock_snapshot; }
  assert(!"unexpected MMIO read"); return 0;
}
void outl(uintptr_t address,uint32_t value) {
  assert(address==VGACTL_ADDR+4);sync_value=value;sync_writes++;
}
void __am_gpu_config(AM_GPU_CONFIG_T *);
void __am_gpu_status(AM_GPU_STATUS_T *);
void __am_gpu_fbdraw(AM_GPU_FBDRAW_T *);
void __am_timer_init(void);
void __am_timer_uptime(AM_TIMER_UPTIME_T *);
void __am_input_keybrd(AM_INPUT_KEYBRD_T *);

int main(int argc,char **argv) {
  (void)argv;
  if(argc>1) {
    AM_GPU_FBDRAW_T bad={.x=0,.y=0,.w=-1,.h=1,.pixels=NULL,.sync=false};
    __am_gpu_fbdraw(&bad);return 2;
  }
  AM_GPU_CONFIG_T cfg;__am_gpu_config(&cfg);
  assert(cfg.present && !cfg.has_accel && cfg.width==400 && cfg.height==300 && cfg.vmemsz==480000);
  AM_GPU_STATUS_T stat;__am_gpu_status(&stat);assert(stat.ready);
  uint32_t *expected=calloc(400*300,sizeof *expected),pixels[49];assert(expected);
  unsigned cases=0;
  c2_framebuffer[0]=c2_framebuffer[400*300+1]=0xdeadbeefu;
  for (int k=0;k<160;k++) {
    int x=(k*131)%414-7,y=(k*97)%314-7,w=k%7+1,h=(k*3)%7+1;
    for(int i=0;i<w*h;i++)pixels[i]=0x110000u+k*123u+i;
    AM_GPU_FBDRAW_T draw={.x=x,.y=y,.w=w,.h=h,.pixels=pixels,.sync=(k%5)==0};
    unsigned before=sync_writes;__am_gpu_fbdraw(&draw);
    for(int row=0;row<h;row++)for(int col=0;col<w;col++)
      if(x+col>=0&&x+col<400&&y+row>=0&&y+row<300)expected[(y+row)*400+x+col]=pixels[row*w+col];
    assert(memcmp(expected,c2_framebuffer+1,480000)==0);
    assert(c2_framebuffer[0]==0xdeadbeefu&&c2_framebuffer[120001]==0xdeadbeefu);
    assert(sync_writes==before+(unsigned)draw.sync);cases++;
  }
  AM_GPU_FBDRAW_T flush={.w=0,.h=0,.pixels=NULL,.sync=true};__am_gpu_fbdraw(&flush);assert(sync_value==1);
  clock_value=0xfffffffdull;__am_timer_init();assert(timer_reads==2);
  for(unsigned i=0;i<300;i++) {
    uint64_t now=0xfffffffdull+(uint64_t)i*0x1000000a3ull;
    clock_value=now;AM_TIMER_UPTIME_T time;__am_timer_uptime(&time);
    assert(time.us==now-0xfffffffdull);cases++;
  }
  uint32_t events[]={0,0x8031u,0x31u,0x804bu,0x4bu,0x801bu,0x1bu};
  for(unsigned i=0;i<sizeof events/sizeof events[0];i++) {
    keyboard_value=events[i];AM_INPUT_KEYBRD_T key;__am_input_keybrd(&key);
    assert(key.keydown==((events[i]&0x8000u)!=0)&&key.keycode==(int)(events[i]&0x7fffu));cases++;
  }
  free(expected);printf("C2_DRIVER_PASS cases=%u timer_reads=%u sync_writes=%u\n",cases,timer_reads,sync_writes);return 0;
}
