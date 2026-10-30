/* One complete address range and one pattern per independently reset run.
 * The assembly bodies are the exact accepted mem-sweep-asm.S bodies.
 */
#include <am.h>
#include <stdint.h>
#ifndef MEMTEST_BYTES
#define MEMTEST_BYTES 4096u
#endif
#ifndef MEMTEST_PHASE
#define MEMTEST_PHASE 0
#endif
extern int c5_sweep8(uintptr_t,uintptr_t,unsigned,unsigned);
extern int c5_sweep16(uintptr_t,uintptr_t,unsigned,unsigned);
extern int c5_sweep32(uintptr_t,uintptr_t,unsigned,unsigned);
extern int c5_sweep64(uintptr_t,uintptr_t,unsigned,unsigned);
int main(const char *args) {
  const uintptr_t begin=0xa0000000u,end=begin+MEMTEST_BYTES;
  if (end<=begin || (begin&63) || (end&63) || MEMTEST_PHASE<0 || MEMTEST_PHASE>7) halt(72);
  int (*const sweeps[])(uintptr_t,uintptr_t,unsigned,unsigned)={c5_sweep8,c5_sweep16,c5_sweep32,c5_sweep64};
  const char tags[]="BHWQ";
  const unsigned type=MEMTEST_PHASE/2,inverse=MEMTEST_PHASE%2;
  if (sweeps[type](begin,end,inverse,args[0]=='x')) halt(71);
  putch(tags[type]+(inverse?32:0));putch('\n');
  return 0;
}
