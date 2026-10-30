#include "screensaver_core.h"
#include <stdio.h>
#include <stdlib.h>

static void check(bool value,const char *name) {
  if(!value){fprintf(stderr,"SCREEN_ASSERT %s\n",name);exit(1);}
}
int main(void) {
  const uint32_t colors[8]={0,0xff0000,0xff00,0xff,0xffff00,0xff00ff,0xffff,0xffffff};
  unsigned checks=0;
  for(unsigned a=0;a<8;a++)for(unsigned b=0;b<8;b++) {
    check(screen_blend(colors[a],colors[b],0,120)==colors[a],"initial endpoint");
    check(screen_blend(colors[a],colors[b],120,120)==colors[b],"final endpoint");
    uint32_t old=colors[a];
    for(unsigned i=0;i<=120;i++) {
      uint32_t color=screen_blend(colors[a],colors[b],i,120);
      for(unsigned s=0;s<=16;s+=8) {
        unsigned start=(colors[a]>>s)&255,end=(colors[b]>>s)&255,now=(color>>s)&255,prior=(old>>s)&255;
        check(now<256 && (end>=start ? now>=prior : now<=prior),"monotonic channel");
        /* Independent exact dyadic midpoint has no quantization ambiguity. */
        if(i==60)check(now==(start+end)/2,"midpoint");
      }
      check((color&0xff000000u)==0,"RGB only");old=color;checks++;
    }
  }
  screen_keys keys={0};
  screen_key(&keys,10,true);screen_key(&keys,10,true);check(keys.held==1,"repeat is idempotent");
  screen_key(&keys,20,true);check(keys.held==2,"second held key");
  screen_key(&keys,10,false);check(keys.held==1,"one key remains held");
  screen_key(&keys,20,false);screen_key(&keys,20,false);check(keys.held==0,"released and duplicate release");
  screen_key(&keys,0,true);screen_key(&keys,256,true);check(keys.held==0,"invalid keys ignored");
  printf("SCREEN_CORE_PASS transitions=%u\n",checks);
  return 0;
}
