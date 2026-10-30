#include <am.h>
#include <stdint.h>
#ifndef MEMTEST_BASE
#define MEMTEST_BASE 0xa0000000u
#endif
#ifndef MEMTEST_BYTES
#define MEMTEST_BYTES 4096u
#endif
extern int c5_sweep8(uintptr_t,uintptr_t,unsigned,unsigned);
extern int c5_sweep16(uintptr_t,uintptr_t,unsigned,unsigned);
extern int c5_sweep32(uintptr_t,uintptr_t,unsigned,unsigned);
extern int c5_sweep64(uintptr_t,uintptr_t,unsigned,unsigned);
int main(const char *args){
  uintptr_t begin=MEMTEST_BASE,end=MEMTEST_BASE+MEMTEST_BYTES;
  if(end<=begin||(begin&63)||(end&63))halt(72);
  int (*const sweeps[])(uintptr_t,uintptr_t,unsigned,unsigned)={c5_sweep8,c5_sweep16,c5_sweep32,c5_sweep64};
  const char tags[]="BHWQ";
  for(unsigned type=0;type<4;type++)for(unsigned inverse=0;inverse<2;inverse++){
    if(sweeps[type](begin,end,inverse,args[0]=='x'))halt(71);
    putch(tags[type]+(inverse?32:0));putch('\n');
  }
  return 0;
}
