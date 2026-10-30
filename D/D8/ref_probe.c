#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <dlfcn.h>
#include <assert.h>
typedef struct {uint32_t r[32],pc;} state;
int main(int argc,char **argv){
  assert(argc>=2);void *h=dlopen(argv[1],RTLD_NOW|RTLD_LOCAL);if(!h){fprintf(stderr,"%s\n",dlerror());return 2;}
  void (*init)(int)=dlsym(h,"difftest_init");
  void (*copy)(uint32_t,void*,size_t,bool)=dlsym(h,"difftest_memcpy");
  void (*regs)(void*,bool)=dlsym(h,"difftest_regcpy");
  void (*step)(uint64_t)=dlsym(h,"difftest_exec");
  void (*intr)(uint32_t)=dlsym(h,"difftest_raise_intr");
  assert(init&&copy&&regs&&step&&intr);init(0);
  uint8_t input[256],output[256];uint32_t rng=0x2607d8;
  if(argc==3){if(strcmp(argv[2],"range")==0)copy(0x87ffffff,input,4,true);else intr(7);return 3;}
  for(unsigned k=0;k<1000;k++){
    for(unsigned j=0;j<sizeof input;j++){rng^=rng<<13;rng^=rng>>17;rng^=rng<<5;input[j]=(uint8_t)rng;}
    uint32_t address=0x80001000+(k%32)*256;copy(address,input,sizeof input,true);memset(output,0,sizeof output);copy(address,output,sizeof output,false);assert(memcmp(input,output,sizeof input)==0);
  }
  copy(0x88000000,NULL,0,true);
  state s={0},got={0};s.pc=0x80000000;s.r[0]=17;s.r[3]=0x80000100;regs(&s,true);regs(&got,false);assert(got.r[0]==0&&got.r[3]==s.r[3]&&got.pc==s.pc);
  uint32_t program[]={0x00500093,0x00108113,0x0021a023,0x0001a203};copy(0x80000000,program,sizeof program,true);
  step(1);regs(&got,false);assert(got.pc==0x80000004&&got.r[1]==5&&got.r[2]==0);
  step(2);regs(&got,false);assert(got.pc==0x8000000c&&got.r[2]==6);uint32_t memory=0;copy(0x80000100,&memory,4,false);assert(memory==6);
  step(1);regs(&got,false);assert(got.pc==0x80000010&&got.r[4]==6);
  init(0);regs(&got,false);assert(got.pc==0x80000000);for(unsigned i=0;i<32;i++)assert(got.r[i]==0);copy(0x80000100,&memory,4,false);assert(memory==0);
  puts("REF_API_PASS copies=1000 instructions=4 reinit=clean");dlclose(h);return 0;
}
