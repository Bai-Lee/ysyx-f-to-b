#include "Vmotion.h"
#include "verilated.h"
#include <cstdio>
#include <cstdlib>
static unsigned checks=0;
static void eq(unsigned a,unsigned b,const char*s){++checks;if(a!=b){fprintf(stderr,"FAIL %s actual=%u expected=%u\n",s,a,b);exit(1);}}
static void reflect(int&x,int&d,int v,int lim){int next=x+(d?v:-v);if(next>=lim){next=2*lim-next;d=0;}else if(next<=0){next=-next;d=1;}x=next;}
int main(int argc,char**argv){VerilatedContext ctx;ctx.commandArgs(argc,argv);Vmotion m{&ctx};
 auto tick=[&](){m.clk=0;m.eval();m.clk=1;m.eval();};m.reset=1;tick();m.reset=0;
 unsigned seed=260708;
 for(int trial=0;trial<1000;trial++){
   seed=seed*1664525u+1013904223u;int x=trial<4?(trial&1?576:0):seed%577;
   seed=seed*1664525u+1013904223u;int y=trial<4?(trial&2?432:0):seed%433;
   int dx=(seed>>7)&1,dy=(seed>>13)&1,vx=1+trial%15,vy=1+(trial*7)%15;
   m.load=1;m.seed_x=x;m.seed_y=y;m.seed_dx=dx;m.seed_dy=dy;m.vx=vx;m.vy=vy;tick();m.load=0;m.frame=1;
   for(int frame=0;frame<1000;frame++){reflect(x,dx,vx,576);reflect(y,dy,vy,432);tick();eq(m.x,x,"x");eq(m.y,y,"y");eq(m.dx,dx,"dx");eq(m.dy,dy,"dy");if(m.x>576||m.y>432)return 2;}
 }
 printf("PASS motion checks=%u trials=1000 frames_each=1000 seed=260708 edges_and_corners=covered\n",checks);m.final();return 0;}
