"""Extend a private accepted NEMU reference with physical SoC memory regions."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *


def main():
    source=WORK/'nemu-ref';dest=WORK/'c5/nemu-ref';local=ROOT/'C/C5/ref'
    if not dest.exists():shutil.copytree(source,dest,ignore=shutil.ignore_patterns('.git','build','__pycache__'))
    header=(source/'src/memory/paddr.c').read_text().split('#include',1)[0]
    paddr=header+r'''
#include <memory/paddr.h>
#include <isa.h>
typedef struct {paddr_t base;size_t size;bool readonly;const char *name;uint8_t *data;} Region;
static Region regions[]={
 {0x0f000000,0x2000,false,"SRAM",NULL},
 {0x20000000,0x1000,true,"MROM",NULL},
 {0x30000000,0x1000000,true,"FLASH",NULL},
 {0x80000000,0x400000,false,"PSRAM",NULL},
 {0xa0000000,0x8000000,false,"SDRAM",NULL},
 {0xc0000000,0x1000,false,"CHIPLINK_TEST",NULL}
};
static Region *find_region(paddr_t addr,size_t n){
 for(size_t i=0;i<ARRLEN(regions);i++){
  Region *r=&regions[i];
  if((uint64_t)addr>=r->base&&n<=r->size&&(uint64_t)addr-r->base<=r->size-n)return r;
 }
 return NULL;
}
bool c5_memory_span(paddr_t addr,size_t n){return find_region(addr,n)!=NULL;}
uint8_t *guest_to_host(paddr_t addr){
 Region *r=find_region(addr,1);Assert(r&&r->data,"C5_REF_ADDRESS %08x",addr);
 return r->data+(addr-r->base);
}
paddr_t host_to_guest(uint8_t *host){
 uintptr_t h=(uintptr_t)host;
 for(size_t i=0;i<ARRLEN(regions);i++){
  uintptr_t start=(uintptr_t)regions[i].data;
  if(h>=start&&h-start<regions[i].size)return regions[i].base+(h-start);
 }
 panic("C5_REF_HOST_ADDRESS");return 0;
}
void init_mem(void){
 for(size_t i=0;i<ARRLEN(regions);i++){
  Region *r=&regions[i];if(!r->data)r->data=malloc(r->size);
  Assert(r->data,"C5_REF_ALLOC %s",r->name);memset(r->data,0,r->size);
 }
}
word_t paddr_read(paddr_t addr,int len){
 Assert((len==1||len==2||len==4)&&c5_memory_span(addr,(size_t)len),"C5_REF_READ_SPAN addr=%08x len=%d",addr,len);
 word_t data=0;memcpy(&data,guest_to_host(addr),(size_t)len);return data;
}
void paddr_write(paddr_t addr,int len,word_t value){
 Region *r=find_region(addr,(size_t)len);
 Assert((len==1||len==2||len==4)&&r,"C5_REF_WRITE_SPAN addr=%08x len=%d",addr,len);
 Assert(!r->readonly,"C5_READONLY_REGION addr=%08x region=%s",addr,r->name);
 memcpy(guest_to_host(addr),&value,(size_t)len);
}
'''
    ref=(source/'src/cpu/difftest/ref.c').read_text()
    start=ref.index('static void check_span(');end=ref.index('__EXPORT void difftest_memcpy',start)
    ref=ref[:start]+'''extern bool c5_memory_span(paddr_t address,size_t n);
static void check_span(paddr_t address,size_t n){
 Assert(c5_memory_span(address,n),"REF_MEMORY_RANGE address=%08x size=%zu",address,n);
}
'''+ref[end:]
    ref=ref.replace('memset(guest_to_host(CONFIG_MBASE),0,CONFIG_MSIZE);','')
    for name,relative,data in [('paddr.c','src/memory/paddr.c',paddr),('ref.c','src/cpu/difftest/ref.c',ref)]:
        saved=local/name
        # Once created, the versioned project source is authoritative.
        if not saved.exists():saved.write_text(data)
        shutil.copyfile(saved,dest/relative)
    if (local/'inst.c').exists():shutil.copyfile(local/'inst.c',dest/'src/isa/riscv32/inst.c')
    exe=dest/'build/riscv32-nemu-interpreter-so'
    inputs=[dest/'.config',local/'paddr.c',local/'ref.c',dest/'src/isa/riscv32/inst.c']
    fixdep=dest/'tools/fixdep'
    run('C5/reference/fixdep',['make','-j1'],cwd=fixdep,env={'NEMU_HOME':str(dest)},inputs=[fixdep/'Makefile',fixdep/'fixdep.c'],outputs=[fixdep/'build/fixdep'])
    run('C5/reference/build',['make','-j1','LIBS=-lreadline -ldl'],cwd=dest,env={'NEMU_HOME':str(dest)},inputs=inputs,outputs=[exe],timeout=300)
    dump(ROOT/'reports/C5_reference_build.json',{'status':'BUILT_NOT_ACCEPTED','source_origin':str(source),'workspace':str(dest),'binary':str(exe),'sha256':sha(exe),
         'inputs':[{'path':str(p),'sha256':sha(p)} for p in inputs],
         'scope':'Original independent RV32IM interpreter, private SoC address regions and strict ROM protection. Existing33-word GPR/PC DiffTest ABI unchanged. Machine-mode CSR/trap code has a separate dedicated acceptance; these memory controls alone do not qualify RT-Thread.'})
    print('C5_SOC_REFERENCE_BUILT',flush=True)


if __name__=='__main__':main()
