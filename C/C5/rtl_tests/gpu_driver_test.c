#include <stdint.h>
#include <stdlib.h>
#include <limits.h>
static volatile uint32_t storage[640*480+16];
static uint32_t expected[640*480],pixels[64];
#define C5_GPU_FRAMEBUFFER (storage+8)
#include "ioe.c"
void putch(char c){(void)c;}
void halt(int code){exit(code?code:99);}
int main(void){
  const int cases[][4]={{4,5,3,2},{0,0,2,2},{639,479,2,2},{-1,-1,3,3},{-3,2,3,2},{5,-2,2,4},{640,0,2,2},{0,480,2,2},{INT_MIN,0,2,2},{0,INT_MIN,2,2},{0,0,0,2},{0,0,2,0},{637,478,4,4}};
  for(unsigned i=0;i<64;i++)pixels[i]=0x81726300+i;
  for(unsigned test=0;test<sizeof cases/sizeof cases[0];test++){
    for(unsigned i=0;i<640*480+16;i++)storage[i]=0xdeadbeef;
    for(unsigned i=0;i<640*480;i++)storage[i+8]=expected[i]=0x10203040;
    int x=cases[test][0],y=cases[test][1],w=cases[test][2],h=cases[test][3];
    for(int sy=0;sy<h;sy++)for(int sx=0;sx<w;sx++){
      int64_t dx=(int64_t)x+sx,dy=(int64_t)y+sy;
      if(dx>=0&&dx<640&&dy>=0&&dy<480)expected[dy*640+dx]=pixels[sy*w+sx];
    }
    AM_GPU_FBDRAW_T draw={.x=x,.y=y,.pixels=pixels,.w=w,.h=h,.sync=true};ioe_write(AM_GPU_FBDRAW,&draw);
    for(unsigned i=0;i<640*480;i++)if(storage[i+8]!=expected[i])return 1;
    for(unsigned i=0;i<8;i++)if(storage[i]!=0xdeadbeef||storage[640*480+8+i]!=0xdeadbeef)return 2;
  }
  AM_GPU_FBDRAW_T sync={.pixels=NULL,.w=0,.h=0,.sync=true};ioe_write(AM_GPU_FBDRAW,&sync);
  return 0;
}
