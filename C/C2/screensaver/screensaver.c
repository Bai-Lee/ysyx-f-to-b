#include <am.h>
#include <klib.h>
#include <klib-macros.h>
#include "screensaver_core.h"

enum { WIDTH=400, HEIGHT=300, STEPS=120 };
static uint32_t pixels[WIDTH * HEIGHT];
static const uint32_t palette[8] = {
  0x000000, 0xff0000, 0x00ff00, 0x0000ff,
  0xffff00, 0xff00ff, 0x00ffff, 0xffffff
};

void draw(uint32_t color) {
  for (unsigned i=0; i<WIDTH*HEIGHT; i++) pixels[i]=color;
  io_write(AM_GPU_FBDRAW,0,0,pixels,WIDTH,HEIGHT,true);
}

static uint32_t next_color(uint32_t old) {
  uint32_t color;
  do { color=palette[(unsigned)rand()%8]; } while (color==old);
  return color;
}

int main(const char *args) {
  const bool solid=args && (!strcmp(args,"solid") || !strcmp(args,"solid-audit"));
  const bool audit=args && (!strcmp(args,"audit") || !strcmp(args,"solid-audit"));
  ioe_init();
  AM_GPU_CONFIG_T cfg=io_read(AM_GPU_CONFIG);
  assert(cfg.present && cfg.width==WIDTH && cfg.height==HEIGHT);
  srand(260702);
  screen_keys keys={0};
  uint32_t from=0x0000ff, to=next_color(from); unsigned step=0, frames=0;
  uint64_t last=io_read(AM_TIMER_UPTIME).us;
  draw(from);
  if(audit)printf("SCREEN_START width=%d height=%d color=%06x\n",WIDTH,HEIGHT,from);
  for (;;) {
    AM_INPUT_KEYBRD_T event=io_read(AM_INPUT_KEYBRD);
    if (event.keycode==AM_KEY_ESCAPE && event.keydown) {
      if(audit)printf("SCREEN_EXIT frames=%u held=%u\n",frames,keys.held);
      return 0;
    }
    if (event.keycode!=AM_KEY_NONE && event.keycode!=AM_KEY_ESCAPE) {
      screen_key(&keys,(unsigned)event.keycode,event.keydown);
      if(audit)printf("SCREEN_KEY code=%d down=%d held=%u\n",event.keycode,event.keydown,keys.held);
    }
    uint64_t now=io_read(AM_TIMER_UPTIME).us;
    unsigned interval=keys.held ? 8333u : 33333u;
    if (!solid && now-last>=interval) {
      /* Render at most once per loop; a delayed host cannot skip the endpoint. */
      last=now;step++;
      uint32_t color=screen_blend(from,to,step,STEPS);draw(color);frames++;
      if(audit)printf("SCREEN_FRAME us=%llu step=%u color=%06x held=%u interval=%u\n",(unsigned long long)now,step,color,keys.held,interval);
      if(step==STEPS){from=to;to=next_color(from);step=0;}
    }
  }
}
