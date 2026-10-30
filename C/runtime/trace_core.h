#ifndef D_TRACE_CORE_H
#define D_TRACE_CORE_H
#include <stdint.h>
#include <stdio.h>
#include <stddef.h>
#ifdef __cplusplus
extern "C" {
#endif
typedef struct dtrace_context dtrace_context;
/* modes: bit 0 instruction, bit 1 data memory, bit 2 function control flow. */
dtrace_context *dtrace_create(const char *path,const char *elf,unsigned modes,uint64_t limit,char *error,size_t error_size);
void dtrace_destroy(dtrace_context *t);
void dtrace_instruction(dtrace_context *t,uint32_t pc,uint32_t instruction,const char *assembly);
void dtrace_commit(dtrace_context *t,uint32_t pc,uint32_t instruction,uint32_t next_pc);
void dtrace_memory(dtrace_context *t,uint32_t pc,char operation,uint32_t address,unsigned size,uint32_t value);
void dtrace_dump_ring(dtrace_context *t,FILE *out);
size_t dtrace_symbol_count(const dtrace_context *t);
#ifdef __cplusplus
}
#endif
#endif
