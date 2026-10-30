from pathlib import Path
import sys,tarfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    n=BENCH/'nemu';d=ROOT/'D/D7';snapshot=d/'before_trace.tar.gz'
    affected=['src/isa/riscv32/inst.c','src/cpu/cpu-exec.c','src/monitor/monitor.c']
    if not snapshot.exists():
        with tarfile.open(snapshot,'w:gz') as t:
            for rel in affected:t.add(n/rel,arcname=rel)
    changed=[]
    for src,rel in [(ROOT/'D/runtime/trace_core.c','src/utils/trace_core.c'),(ROOT/'D/runtime/trace_core.h','include/trace_core.h'),(d/'trace_adapter.c','src/utils/trace_adapter.c'),(d/'dtrace.h','include/dtrace.h')]:
        shutil.copyfile(src,n/rel);changed.append(n/rel)
    for rel in affected:
        p=n/rel;text=p.read_text()
        if '#include "dtrace.h"' not in text:
            text='#include "dtrace.h"\n'+text
            if rel.endswith('inst.c'):
                text=text.replace('static void rejected(','''static uint32_t traced_read(uint32_t pc,uint32_t addr,unsigned len){
  uint32_t value=vaddr_read(addr,len);dtrace_access(pc,'R',addr,len,value);return value;
}
static void traced_write(uint32_t pc,uint32_t addr,unsigned len,uint32_t value){
  vaddr_write(addr,len,value);dtrace_access(pc,'W',addr,len,value & (len==4?UINT32_MAX:((1u<<(len*8))-1)));
}
static void rejected(''')
                # Replace call sites only; wrapper definitions retain the real API.
                i=text.index('int isa_exec_once');head,body=text[:i],text[i:]
                body=body.replace('vaddr_read(addr,','traced_read(s->pc,addr,').replace('vaddr_write(addr,','traced_write(s->pc,addr,')
                body=body.replace('s->isa.inst=i;s->dnpc=s->snpc;','s->isa.inst=i;s->dnpc=s->snpc;dtrace_before(s->pc,i);')
                text=head+body
            elif rel.endswith('cpu-exec.c'):
                text=text.replace('if (ITRACE_COND)', 'if (ITRACE_COND && dtrace_legacy_allow())')
                text=text.replace('cpu.pc = s->dnpc;','cpu.pc = s->dnpc;\n  dtrace_after(s->pc,s->isa.inst,cpu.pc);')
                text=text.replace('void assert_fail_msg() {','void assert_fail_msg() {\n  dtrace_error();')
                text=text.replace('case NEMU_END: case NEMU_ABORT:\n', 'case NEMU_END: case NEMU_ABORT:\n      if(nemu_state.state==NEMU_ABORT || nemu_state.halt_ret!=0) dtrace_error();\n')
            else:
                text=text.replace('{"report", required_argument, NULL, \'r\'},','{"elf", required_argument, NULL, \'e\'},\n    {"report", required_argument, NULL, \'r\'},')
                text=text.replace('"-bhl:d:p:r:"','"-bhl:d:p:r:e:"')
                text=text.replace("case 'r': result_file", "case 'e': setenv(\"D_TRACE_ELF\",optarg,1); break;\n      case 'r': result_file")
                text=text.replace('IFDEF(CONFIG_ITRACE, init_disasm());','IFDEF(CONFIG_ITRACE, init_disasm());\n  dtrace_start();')
            p.write_text(text)
        changed.append(p)
    env={'NEMU_HOME':str(n),**json.loads((ROOT/'reports/D_spike_support.json').read_text())['env']}
    exe=n/'build/riscv32-nemu-interpreter'
    run('D7/nemu/build',['make','-j1'],cwd=n,env=env,inputs=[*changed,n/'.config'],outputs=[exe],timeout=300)
    ref=n/'tools/spike-diff/build/riscv32-spike-so'
    o,_,_=run('D7/nemu/builtin',[exe,'-b','-d',ref],cwd=n,env=env,inputs=[exe,ref]);assert 'HIT GOOD TRAP' in o
    dump(ROOT/'reports/D7_build.json',{'status':'PASS_BUILTIN_ONLY','nemu':str(exe),'spike':str(ref),'environment':env,'sources':[{'path':str(p),'sha256':sha(p)} for p in changed]})

if __name__=='__main__':main()
