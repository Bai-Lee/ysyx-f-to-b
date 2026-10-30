/* Machine-mode teaching subset, independently executed by NEMU.
 * Adapted from the project's accepted C5 NEMU CSR implementation.
 * Timer ticks are driven by instruction execution for standalone NEMU and by
 * the simulated CPU clock for DiffTest. No DUT register value feeds this model.
 */
#include <isa.h>
#include <difftest-def.h>
#include "b_csr.h"
#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
static uint32_t mstatus, mtvec, mscratch, mepc, mcause;
static uint64_t mcycle;
static bool cycle_written;
static bool fault_reference_clock;
static FILE *etrace;
static uint64_t events;
void c5_csr_reset(void) {
  mstatus=0x1800; mtvec=mscratch=mepc=mcause=0;
  mcycle=0; cycle_written=false; events=0;
  fault_reference_clock=getenv("B_FAULT_REFERENCE_CLOCK")!=NULL;
  if(etrace){fclose(etrace);etrace=NULL;}
  const char *path=getenv("B_ETRACE");
  if(path && *path){etrace=fopen(path,"w");Assert(etrace,"Cannot open B_ETRACE");}
}
static void trace(const char *kind,uint32_t pc,uint32_t target) {
  if(etrace) {
    fprintf(etrace,"{\"event\":\"%s\",\"seq\":%" PRIu64 ",\"pc\":%u,\"target\":%u,\"mcause\":%u,\"mepc\":%u,\"mstatus\":%u}\n",kind,events++,pc,target,mcause,mepc,mstatus);
    fflush(etrace);
  }
}
static uint32_t *storage(unsigned number) {
  switch(number){case 0x300:return &mstatus;case 0x305:return &mtvec;
    case 0x340:return &mscratch;case 0x341:return &mepc;case 0x342:return &mcause;
    default:return NULL;}
}
bool b_csr_read(unsigned number,uint32_t *value,bool *readonly) {
  uint32_t *p=storage(number);*readonly=false;
  if(p){*value=*p;return true;}
  if(number==0xb00){*value=(uint32_t)mcycle;return true;}
  if(number==0xb80){*value=(uint32_t)(mcycle>>32);return true;}
  *readonly=true;
  switch(number){case 0xf11:*value=0x79737978;return true;
    case 0xf12:*value=0x26070001;return true;case 0xf13:*value=1;return true;
    case 0xf14:*value=0;return true;default:return false;}
}
void b_csr_write(unsigned number,uint32_t value) {
  if(number==0xb00){mcycle=(mcycle&UINT64_C(0xffffffff00000000))|value;cycle_written=true;return;}
  if(number==0xb80){mcycle=((uint64_t)value<<32)|(uint32_t)mcycle;cycle_written=true;return;}
  uint32_t *p=storage(number);Assert(p,"CSR_STORAGE");
  if(number==0x300)value=0x1800|(value&0x88);
  if(number==0x305)value=(value&~3u)|((value&3u)==1?1u:0u);
  if(number==0x341)value&=~3u;
  *p=value;
}
word_t isa_raise_intr(word_t no,vaddr_t epc) {
  mepc=epc&~3u;mcause=no;mstatus=0x1800|((mstatus&8)<<4);
  uint32_t target=mtvec&~3u;trace("ECALL",epc,target);return target;
}
uint32_t b_mret(uint32_t pc) {
  mstatus=0x1880|((mstatus&0x80)>>4);trace("MRET",pc,mepc);return mepc;
}
word_t isa_query_intr(void){return INTR_EMPTY;}
void b_clock_tick(void){if(!cycle_written)mcycle++;cycle_written=false;}
__EXPORT void b_reference_clock(int reset) {
  if(reset){mcycle=0;cycle_written=false;}else if(!fault_reference_clock)b_clock_tick();
}
