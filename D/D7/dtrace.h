#ifndef D_NEMU_TRACE_H
#define D_NEMU_TRACE_H
#include <stdint.h>
void dtrace_start(void);
void dtrace_finish(void);
int dtrace_legacy_allow(void);
void dtrace_before(uint32_t pc,uint32_t inst);
void dtrace_after(uint32_t pc,uint32_t inst,uint32_t npc);
void dtrace_access(uint32_t pc,char op,uint32_t addr,unsigned len,uint32_t data);
void dtrace_error(void);
#endif
