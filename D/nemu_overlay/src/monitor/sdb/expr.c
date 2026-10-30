#include <isa.h>
#include <memory/paddr.h>
#include "sdb.h"
#include <debug_core.h>

static bool read_reg(void *opaque,const char *name,uint32_t *value){
  (void)opaque;bool ok=false;*value=isa_reg_str2val(name,&ok);return ok;
}
bool sdb_read_word(uint32_t addr,uint32_t *value){
  if(addr<CONFIG_MBASE||(uint64_t)addr+4>(uint64_t)CONFIG_MBASE+CONFIG_MSIZE)return false;
  /* Debugger reads are restricted to RAM and have no MMIO side effects. */
  memcpy(value,guest_to_host(addr),4);return true;
}
static bool read_mem(void *opaque,uint32_t addr,uint32_t *value){(void)opaque;return sdb_read_word(addr,value);}
DExprContext sdb_expr_context={read_reg,read_mem,NULL};
void init_regex(void){}
word_t expr(char *text,bool *success){
  uint32_t result=0;char error[160];*success=d_expr(text,&sdb_expr_context,&result,error,sizeof(error));
  if(!*success){printf("EXPR_ERROR %s\n",error);}
  return result;
}
