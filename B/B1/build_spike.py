"""Align Spike's ISA/privilege environment with the B machine-mode contract."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    nemu=BENCH/'nemu';adapter=nemu/'tools/spike-diff';repo=adapter/'repo'
    baseline=json.loads((ROOT/'reports/D_spike_build.json').read_text())
    libraries=[Path(row['path']) for row in baseline['libraries']]
    for row in baseline['libraries']:assert sha(row['path'])==row['sha256'],row['path']
    source=Path('/home/USER/c-stage/workbench/nemu/tools/spike-diff/difftest.cc')
    text=source.read_text().replace('const char *isa = "RV" MUXDEF(CONFIG_RV64, "64", "32") MUXDEF(CONFIG_RVE, "E", "I") "MAFDC";', 'const char *isa = "RV32IM"; // B: no floating point/compressed ISA')
    text=text.replace('/*default_priv=*/DEFAULT_PRIV','/*default_priv=*/"M"')
    text=text.replace('  s->diff_init(port);','  s->diff_init(port);\n  p->put_csr(CSR_MSTATUS, 0x1800); // Explicit shared initial environment')
    dest=adapter/'b1-difftest.cc';dest.write_text(text)
    includes=[repo,*[repo/x for x in ['fesvr','riscv','disasm','customext','fdt','softfloat','spike_main','spike_dasm']],libraries[0].parent,nemu/'include']
    exe=adapter/'build/riscv32-spike-so'
    run('B1/spike/machine-adapter',['g++','-std=c++17','-O2','-shared','-fPIC','-fvisibility=hidden',*['-I'+str(p) for p in includes],dest,*libraries,'-o',exe],inputs=[dest,nemu/'include/generated/autoconf.h',*libraries],outputs=[exe],timeout=120,resume=True)
    dump(ROOT/'reports/B1_spike_environment.json',{'status':'BUILT_PENDING_CONTEXT_VALIDATION','source_commit':baseline['commit'],'source_adapter_sha256':sha(source),'adapter':str(dest),'adapter_sha256':sha(dest),'executable':str(exe),'sha256':sha(exe),'libraries':baseline['libraries'],'ISA':'RV32IM with privileged CSR instructions','privilege_modes':'M only','initial_mstatus':'0x1800','reason':'The accepted older adapter default enabled U/S modes, whose MPP reset/MRET behavior differs from a machine-only processor. Align the explicit environment without changing Spike instruction semantics or skipping CSR comparisons.','specification':'https://docs.riscv.org/reference/isa/priv/machine.html'})
    print('B1_SPIKE_MACHINE_ENVIRONMENT_BUILT')

if __name__=='__main__':main()
