#include <common.h>
#include <errno.h>
#include "trace_core.h"
#include "dtrace.h"
static dtrace_context *context;
static uint64_t legacy_limit,legacy_lines;
void dtrace_finish(void){dtrace_destroy(context);context=NULL;}
void dtrace_start(void){
  const char *path=getenv("D_TRACE_FILE"),*elf=getenv("D_TRACE_ELF"),*m=getenv("D_TRACE_MODES"),*limit=getenv("D_TRACE_LIMIT");
  unsigned modes=0;char error[256];uint64_t count=10000;
  if(m)for(;*m;m++){if(*m=='i')modes|=1;else if(*m=='m')modes|=2;else if(*m=='f')modes|=4;else if(*m!=','){fprintf(stderr,"TRACE_CONFIG invalid mode\n");exit(2);}}
  if(limit){char *end;errno=0;count=strtoull(limit,&end,10);if(errno||*end||*limit=='-'||end==limit){fprintf(stderr,"TRACE_CONFIG invalid limit\n");exit(2);}}
  const char *legacy=getenv("D_LEGACY_ITRACE_LIMIT");legacy_limit=legacy?strtoull(legacy,NULL,10):0;
  context=dtrace_create(path,elf,modes,count,error,sizeof error);
  if(!context){fprintf(stderr,"TRACE_CONFIG %s\n",error);exit(2);}
  atexit(dtrace_finish);
  printf("D_TRACE modes=%u limit=%"PRIu64" symbols=%zu\n",modes,count,dtrace_symbol_count(context));
}
int dtrace_legacy_allow(void){return legacy_lines++<legacy_limit;}
void dtrace_before(uint32_t pc,uint32_t inst){
  char assembly[144]="";
#ifdef CONFIG_ITRACE
  void disassemble(char*,int,uint64_t,uint8_t*,int);
  if(context)disassemble(assembly,sizeof assembly,pc,(uint8_t*)&inst,4);
#endif
  dtrace_instruction(context,pc,inst,assembly);
}
void dtrace_after(uint32_t pc,uint32_t inst,uint32_t npc){dtrace_commit(context,pc,inst,npc);}
void dtrace_access(uint32_t pc,char op,uint32_t addr,unsigned len,uint32_t data){dtrace_memory(context,pc,op,addr,len,data);}
void dtrace_error(void){dtrace_dump_ring(context,stderr);}
