#include "ref.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef struct {uint8_t *bytes;size_t n;uint32_t base;} Ram;
static unsigned diagnostic_fetches;
static int readmem(void*p,uint32_t addr,unsigned size,int kind,uint32_t*out){
    Ram*m=p;(void)kind;if(addr<m->base||(uint64_t)addr-m->base+size>m->n)return -1;
    if(!kind)diagnostic_fetches++;
    *out=0;for(unsigned i=0;i<size;i++)*out|=(uint32_t)m->bytes[addr-m->base+i]<<(8*i);
    if(getenv("E5_TRACE_DEBUG")&&kind&&addr==0x40080)fprintf(stderr,"READ_PROBE fetch=%u addr=%08x data=%08x\n",diagnostic_fetches,addr,*out);
    return 0;
}
static int writemem(void*p,uint32_t addr,unsigned size,uint32_t v){
    Ram*m=p;if(addr<m->base||(uint64_t)addr-m->base+size>m->n)return -1;
    if(getenv("E5_TRACE_DEBUG")&&diagnostic_fetches<40)fprintf(stderr,"WRITE_PROBE fetch=%u addr=%08x size=%u data=%08x\n",diagnostic_fetches,addr,size,v);
    for(unsigned i=0;i<size;i++)m->bytes[addr-m->base+i]=(uint8_t)(v>>(8*i));
    return 0;
}
int main(int argc,char**argv){
    if(argc!=6){fprintf(stderr,"usage: minirvEMU image base steps expected trace\n");return 2;}
    Ram mem={calloc(1,1024*1024),1024*1024,(uint32_t)strtoul(argv[2],0,0)};if(!mem.bytes)return 2;
    if(getenv("E5_TRACE_DEBUG"))fprintf(stderr,"ALLOC_PROBE data40080=%02x%02x%02x%02x\n",mem.bytes[0x40083],mem.bytes[0x40082],mem.bytes[0x40081],mem.bytes[0x40080]);
    FILE*f=fopen(argv[1],"rb");if(!f)return 2;
    if(fseek(f,0,SEEK_END))return 2;
    long length=ftell(f);if(length<0||(uint64_t)length>mem.n)return 2;
    rewind(f);size_t n=fread(mem.bytes,1,(size_t)length,f);if(n!=(size_t)length||ferror(f))return 2;
    /* Only the returned image bytes are input; explicitly initialize the rest. */
    memset(mem.bytes+n,0,mem.n-n);
    if(getenv("E5_TRACE_DEBUG"))fprintf(stderr,"READFILE_PROBE data40080=%02x%02x%02x%02x\n",mem.bytes[0x40083],mem.bytes[0x40082],mem.bytes[0x40081],mem.bytes[0x40080]);
    fclose(f);
    if(getenv("E5_TRACE_DEBUG"))fprintf(stderr,"LOAD_PROBE bytes=%zu data40080=%02x%02x%02x%02x\n",n,mem.bytes[0x40083],mem.bytes[0x40082],mem.bytes[0x40081],mem.bytes[0x40080]);
    unsigned long steps=strtoul(argv[3],0,0);uint32_t expected=(uint32_t)strtoul(argv[4],0,0);
    FILE*trace=fopen(argv[5],"w");if(!trace)return 2;
    MiniState state;minirv_reset(&state,mem.base);MiniBus bus={&mem,readmem,writemem};unsigned long i=0;int rc=0;
    for(;i<(steps?steps:1000000ul);i++){
        MiniEvent ev;if(minirv_step(&state,&bus,&ev)){fprintf(stderr,"EMU_FAULT pc=%08x code=%u\n",state.pc,state.fault);rc=3;break;}
        fprintf(trace,"%lu,%08x,%08x,%08x",i+1,ev.pc,ev.inst,state.pc);for(unsigned j=0;j<16;j++)fprintf(trace,",%08x",state.r[j]);fputc('\n',trace);
        if(state.halted){i++;break;}
    }
    if(!steps&&!state.halted&&!rc)rc=124;
    if(!rc&&state.r[10]!=expected)rc=1;
    printf("EMU_RESULT instructions=%lu pc=%08x a0=%u expected=%u halted=%u fault=%u\n",i,state.pc,state.r[10],expected,state.halted,state.fault);
    fclose(trace);free(mem.bytes);return rc;
}
