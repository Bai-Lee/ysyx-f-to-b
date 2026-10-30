#include "Vkeyboard.h"
#include "verilated.h"
#include <cstdio>
#include <cstdlib>
static unsigned checks=0;
static void eq(unsigned a,unsigned b,const char*s){++checks;if(a!=b){fprintf(stderr,"FAIL %s actual=%u expected=%u\n",s,a,b);exit(1);}}
int main(int argc,char**argv){
  VerilatedContext ctx;ctx.commandArgs(argc,argv);Vkeyboard d{&ctx};unsigned received=0,errors=0,last=0;
  auto tick=[&](){d.clk=0;d.eval();d.clk=1;d.eval();if(d.valid){received++;last=d.code;}if(d.frame_error)errors++;};
  auto wait=[&](int n){for(int i=0;i<n;i++)tick();};
  auto reset=[&](){d.ps2_clk=1;d.ps2_data=1;d.reset=1;wait(5);d.reset=0;wait(5);received=errors=0;};reset();
  auto send=[&](unsigned code,int bad){unsigned parity=1;for(int i=0;i<8;i++)parity^=(code>>i)&1;
    unsigned frame=(code<<1)|(parity<<9)|(1<<10);if(bad==1)frame^=1<<9;if(bad==2)frame&=~(1<<10);
    for(int i=0;i<11;i++){d.ps2_data=(frame>>i)&1;d.ps2_clk=1;wait(5);d.ps2_clk=0;wait(5);d.ps2_clk=1;wait(5);}d.ps2_data=1;wait(8);
  };
  auto release=[&](unsigned code){send(0xf0,0);send(code,0);};
  const unsigned codes[]={0x1c,0x32,0x21,0x23,0x24,0x2b,0x34,0x33,0x43,0x3b,0x42,0x4b,0x3a,0x31,0x44,0x4d,0x15,0x2d,0x1b,0x2c,0x3c,0x2a,0x1d,0x22,0x35,0x1a,0x45,0x16,0x1e,0x26,0x25,0x2e,0x36,0x3d,0x3e,0x46};
  const char chars[]="abcdefghijklmnopqrstuvwxyz0123456789";
  for(unsigned i=0;i<36;i++){
    send(codes[i],0);eq(last,codes[i],"LSB-first frame");eq(d.keycode,codes[i],"keycode");eq(d.ascii,chars[i],"ASCII");eq(d.active,1,"pressed");eq(d.press_count,i+1,"new press");
    for(int k=0;k<3;k++)send(codes[i],0);eq(d.press_count,i+1,"typematic not counted");
    release(codes[i]);eq(d.active,0,"release blank");eq(d.keycode,0,"release code cleared");eq(d.ascii,0,"release ASCII cleared");
  }
  unsigned n=d.press_count,prior=received;send(0x1c,1);eq(received,prior,"bad parity rejected");eq(d.press_count,n,"bad parity no key");
  send(0x1c,2);eq(received,prior,"bad stop rejected");eq(errors,2,"two invalid frames");send(0x1c,0);eq(d.ascii,'a',"recovery");release(0x1c);
  reset();send(0x12,0);send(0x59,0);eq(d.shift,1,"both shifts");release(0x12);eq(d.shift,1,"right shift retained");
  send(0x1d,0);eq(d.ascii,'W',"shift W");eq(d.press_count,1,"modifiers not characters");release(0x1d);
  send(0x16,0);eq(d.ascii,'!',"shift digit");release(0x16);release(0x59);eq(d.shift,0,"shift release");
  send(0x14,0);eq(d.ctrl,1,"left control");send(0xe0,0);send(0x14,0);release(0x14);eq(d.ctrl,1,"right control retained");
  send(0xe0,0);send(0xf0,0);send(0x14,0);eq(d.ctrl,0,"right control release");
  send(0x52,0);eq(d.ascii,39,"apostrophe");release(0x52);
  for(int i=0;i<260;i++){send(0x1c,0);release(0x1c);}eq(d.press_count,(3+260)%256,"counter wrap");
  printf("PASS keyboard checks=%u received_frames=%u errors=%u letters_digits=36 modifiers=Shift/CTRL\n",checks,received,errors);d.final();return 0;
}
