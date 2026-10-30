#include "trace_core.h"
#include <elf.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <inttypes.h>
#include <ctype.h>

enum { MAX_SYMBOLS=8192, MAX_DEPTH=1024, RING_SIZE=16 };
typedef struct {uint32_t address,size;char name[96];} symbol;
typedef struct {uint32_t return_pc;const symbol *function;} frame;
struct dtrace_context {
  FILE *output;unsigned modes;uint64_t limit,lines;int limited;
  symbol symbols[MAX_SYMBOLS];size_t symbol_count;
  frame stack[MAX_DEPTH];size_t depth;unsigned overflow;
  char ring[RING_SIZE][192];unsigned ring_next,ring_count;
};
static int error_text(char *error,size_t n,const char *why){if(n)snprintf(error,n,"%s",why);return 0;}
static int range(size_t total,uint64_t off,uint64_t length){return off<=total&&length<=total-off;}
static int symbol_compare(const void *a,const void *b){const symbol *x=a,*y=b;return x->address<y->address?-1:x->address>y->address;}
static int load_symbols(dtrace_context *t,const char *path,char *error,size_t n){
  FILE *file=fopen(path,"rb");if(!file)return error_text(error,n,"ELF cannot be opened");
  if(fseek(file,0,SEEK_END)!=0){fclose(file);return error_text(error,n,"ELF seek failed");}
  long length=ftell(file);if(length<(long)sizeof(Elf32_Ehdr)||length>64*1024*1024){fclose(file);return error_text(error,n,"ELF size outside 52..64MiB");}
  rewind(file);unsigned char *data=malloc((size_t)length);if(!data){fclose(file);return error_text(error,n,"ELF allocation failed");}
  int ok=0;const char *why="ELF malformed";
  if(fread(data,1,(size_t)length,file)!=(size_t)length){why="ELF short read";goto finish;}
  Elf32_Ehdr h;memcpy(&h,data,sizeof h);
  if(memcmp(h.e_ident,ELFMAG,SELFMAG)||h.e_ident[EI_CLASS]!=ELFCLASS32||h.e_ident[EI_DATA]!=ELFDATA2LSB||h.e_ident[EI_VERSION]!=EV_CURRENT||h.e_machine!=EM_RISCV||h.e_version!=EV_CURRENT){why="ELF requires 32-bit little-endian RISC-V";goto finish;}
  if(h.e_shnum==0){if(h.e_shoff!=0){why="ELF extended section numbering unsupported";goto finish;}ok=1;goto finish;}
  if(h.e_shentsize!=sizeof(Elf32_Shdr)||!range((size_t)length,h.e_shoff,(uint64_t)h.e_shnum*sizeof(Elf32_Shdr))){why="ELF invalid section table";goto finish;}
  for(unsigned i=0;i<h.e_shnum;i++){
    Elf32_Shdr section;memcpy(&section,data+h.e_shoff+(size_t)i*sizeof section,sizeof section);
    if(section.sh_type!=SHT_SYMTAB&&section.sh_type!=SHT_DYNSYM)continue;
    if(section.sh_entsize!=sizeof(Elf32_Sym)||section.sh_size%sizeof(Elf32_Sym)||section.sh_link>=h.e_shnum||!range((size_t)length,section.sh_offset,section.sh_size)){why="ELF invalid symbol table";goto finish;}
    Elf32_Shdr strings;memcpy(&strings,data+h.e_shoff+(size_t)section.sh_link*sizeof strings,sizeof strings);
    if(strings.sh_type!=SHT_STRTAB||!range((size_t)length,strings.sh_offset,strings.sh_size)){why="ELF invalid string table";goto finish;}
    for(size_t j=0;j<section.sh_size/sizeof(Elf32_Sym);j++){
      Elf32_Sym s;memcpy(&s,data+section.sh_offset+j*sizeof s,sizeof s);
      if(ELF32_ST_TYPE(s.st_info)!=STT_FUNC||s.st_shndx==SHN_UNDEF)continue;
      if(s.st_name>=strings.sh_size||(uint64_t)s.st_value+s.st_size>UINT64_C(0x100000000)){why="ELF invalid function range or name";goto finish;}
      const char *name=(const char *)data+strings.sh_offset+s.st_name;
      if(!memchr(name,0,strings.sh_size-s.st_name)){why="ELF unterminated function name";goto finish;}
      if(t->symbol_count==MAX_SYMBOLS){why="ELF symbol budget exceeded";goto finish;}
      symbol *out=&t->symbols[t->symbol_count++];out->address=s.st_value;out->size=s.st_size;snprintf(out->name,sizeof out->name,"%s",name);
      for(char *p=out->name;*p;p++)if(!isprint((unsigned char)*p))*p='?';
    }
  }
  qsort(t->symbols,t->symbol_count,sizeof(symbol),symbol_compare);ok=1;
finish:free(data);fclose(file);return ok?1:error_text(error,n,why);
}
dtrace_context *dtrace_create(const char *path,const char *elf,unsigned modes,uint64_t limit,char *error,size_t n){
  if(modes&~7u){error_text(error,n,"invalid trace mode");return NULL;}
  dtrace_context *t=calloc(1,sizeof *t);if(!t){error_text(error,n,"trace allocation failed");return NULL;}
  t->modes=modes;t->limit=limit;
  if(elf&&*elf&&!load_symbols(t,elf,error,n)){free(t);return NULL;}
  if(path&&*path&&modes){t->output=fopen(path,"w");if(!t->output){free(t);error_text(error,n,"trace output cannot be opened");return NULL;}}
  return t;
}
void dtrace_destroy(dtrace_context *t){if(!t)return;if(t->output)fclose(t->output);free(t);}
size_t dtrace_symbol_count(const dtrace_context *t){return t?t->symbol_count:0;}
static void emit(dtrace_context *t,unsigned mode,const char *format,...){
  if(!t||!t->output||!(t->modes&mode))return;
  if(t->lines>=t->limit){if(!t->limited){fprintf(t->output,"TRACE_LIMIT limit=%"PRIu64"\n",t->limit);t->limited=1;}return;}
  va_list args;va_start(args,format);vfprintf(t->output,format,args);va_end(args);t->lines++;fflush(t->output);
}
void dtrace_instruction(dtrace_context *t,uint32_t pc,uint32_t i,const char *assembly){
  if(!t)return;
  char *line=t->ring[t->ring_next];snprintf(line,192,"0x%08x: %08x  %.144s",pc,i,assembly?assembly:"");
  t->ring_next=(t->ring_next+1)%RING_SIZE;if(t->ring_count<RING_SIZE)t->ring_count++;
  emit(t,1,"I %s\n",line);
}
void dtrace_dump_ring(dtrace_context *t,FILE *out){
  if(!t)return;
  fputs("IRINGBUF oldest-to-newest (last fetched instruction marked -->)\n",out);
  for(unsigned j=0;j<t->ring_count;j++){unsigned k=(t->ring_next+RING_SIZE-t->ring_count+j)%RING_SIZE;fprintf(out,"%s %s\n",j+1==t->ring_count?"-->":"   ",t->ring[k]);}
}
void dtrace_memory(dtrace_context *t,uint32_t pc,char op,uint32_t address,unsigned size,uint32_t value){emit(t,2,"M pc=0x%08x %c addr=0x%08x size=%u value=0x%08x\n",pc,op,address,size,value);}
static const symbol *lookup(dtrace_context *t,uint32_t pc,int exact){
  const symbol *best=NULL;
  for(size_t j=0;j<t->symbol_count;j++){const symbol *s=&t->symbols[j];if(s->address>pc)break;if(s->address==pc||(!exact&&s->size&&(uint64_t)pc<(uint64_t)s->address+s->size))best=s;}
  return best;
}
void dtrace_commit(dtrace_context *t,uint32_t pc,uint32_t i,uint32_t npc){
  if(!t||!(t->modes&4))return;
  unsigned op=i&127,rd=(i>>7)&31,rs1=(i>>15)&31;
  if(op!=0x6f&&op!=0x67)return;
  int call=rd==1||rd==5;int ret=op==0x67&&(rs1==1||rs1==5)&&rd!=rs1;
  const symbol *destination=lookup(t,npc,0),*from=lookup(t,pc,0);
  if(ret){
    if(t->overflow)t->overflow--;else if(t->depth)t->depth--;
    emit(t,4,"F pc=0x%08x depth=%zu ret %s -> 0x%08x\n",pc,t->depth,from?from->name:"?",npc);
  }
  if(call){
    emit(t,4,"F pc=0x%08x depth=%zu call %s@0x%08x return=0x%08x\n",pc,t->depth,destination?destination->name:"?",npc,pc+4);
    if(t->depth<MAX_DEPTH){t->stack[t->depth++]=(frame){pc+4,destination};}else{t->overflow++;emit(t,4,"F stack_overflow max=%u\n",MAX_DEPTH);}
  }else if(!ret&&rd==0){
    const symbol *target=lookup(t,npc,1);
    if(target&&target!=from){emit(t,4,"F pc=0x%08x depth=%zu tail %s -> %s@0x%08x\n",pc,t->depth,from?from->name:"?",target->name,npc);if(t->depth)t->stack[t->depth-1].function=target;}
  }
}
