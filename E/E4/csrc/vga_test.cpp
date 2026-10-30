#include "Vvga.h"
#include "verilated.h"
#include <cstdio>
#include <cstdlib>
static unsigned long long checks=0;
static void eq(unsigned a,unsigned b,const char*s,int h,int v){++checks;if(a!=b){fprintf(stderr,"FAIL %s h=%d v=%d actual=%u expected=%u\n",s,h,v,a,b);exit(1);}}
static unsigned color(int x,int y){unsigned r=x%256,g=y%256,b=((x/8)^(y/8))*17%256;return ((r>>4)<<20)|((g>>4)<<12)|((b>>4)<<4);}
int main(int argc,char**argv){
  VerilatedContext ctx;ctx.commandArgs(argc,argv);Vvga d{&ctx};d.vx=3;d.vy=2;d.moving=0;
  auto tick=[&](){d.clk=0;ctx.timeInc(20);d.eval();d.clk=1;ctx.timeInc(20);d.eval();};d.reset=1;tick();d.reset=0;
  FILE*f=fopen("static_frame.ppm","wb");if(!f)return 2;fprintf(f,"P6\n640 480\n255\n");
  unsigned valid=0,hlow=0,vlow=0;
  for(int frame=0;frame<2;frame++)for(int v=0;v<525;v++)for(int h=0;h<800;h++){
    tick();eq(d.sample_h,h,"horizontal coordinate",h,v);eq(d.sample_v,v,"vertical coordinate",h,v);
    eq(d.hsync,h>=96,"hsync",h,v);eq(d.vsync,v>=2,"vsync",h,v);bool active=h>=144&&h<784&&v>=35&&v<515;
    eq(d.valid,active,"blank",h,v);unsigned got=(d.red<<16)|(d.green<<8)|d.blue;
    eq(got,active?color(h-144,v-35):0,"pixel",h,v);
    if(frame==0){valid+=d.valid;hlow+=!d.hsync;vlow+=!d.vsync;
      if(active){unsigned char bytes[]={d.red,d.green,d.blue};fwrite(bytes,1,3,f);}}
  }
  fclose(f);eq(valid,640*480,"active count",0,0);eq(hlow,96*525,"hsync count",0,0);eq(vlow,2*800,"vsync count",0,0);
  d.reset=1;tick();d.reset=0;d.moving=1;
  for(int frame=0;frame<3;frame++)for(int v=0;v<525;v++)for(int h=0;h<800;h++){
    tick();bool active=h>=144&&h<784&&v>=35&&v<515;int x=h-144,y=v-35;
    bool inside=x>=frame*3&&x<frame*3+64&&y>=frame*2&&y<frame*2+48;
    unsigned wanted=!active?0:inside?color(x-frame*3,y-frame*2):16;
    eq((d.red<<16)|(d.green<<8)|d.blue,wanted,"moving pixel",h,v);
    eq(d.valid,active,"moving blank",h,v);
  }
  printf("PASS VGA checks=%llu static_frames=2 moving_frames=3 pixels_per_frame=420000 active=307200 frequency=25MHz refresh=59.5238095Hz\n",checks);d.final();return 0;
}
