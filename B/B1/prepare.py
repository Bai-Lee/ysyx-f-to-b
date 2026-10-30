"""Apply B1 changes to independent B NEMU and Abstract Machine copies."""
from pathlib import Path
import sys,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    root=ROOT/'B/B1'
    origin=Path('/home/USER/c-stage/c5/nemu-ref/src/isa/riscv32/inst.c').read_text()
    first=origin.index('/* C5 machine-mode subset;')
    last=origin.index('int isa_exec_once')
    inst=origin[:first]+'#include "b_csr.h"\n\n'+origin[last:]
    inst=inst.replace('csr_read(number,','b_csr_read(number,').replace('csr_write(number,','b_csr_write(number,')
    inst=inst.replace('mepc=s->pc;mcause=11;mstatus=0x1800|((mstatus&8)<<4);next=mtvec&~3u;','next=isa_raise_intr(11,s->pc);')
    inst=inst.replace('next=mepc;mstatus=0x1880|((mstatus&0x80)>>4);','next=b_mret(s->pc);')
    inst=inst.replace('cpu.gpr[0]=0;s->dnpc=next;return 0;', 'cpu.gpr[0]=0;s->dnpc=next;\n#ifndef CONFIG_TARGET_SHARE\n  b_clock_tick();\n#endif\n  return 0;')
    for nemu in [BENCH/'nemu',WORK/'nemu-ref']:
        (nemu/'src/isa/riscv32/inst.c').write_text(inst)
        shutil.copyfile(root/'intr.c',nemu/'src/isa/riscv32/system/intr.c')
        shutil.copyfile(root/'csr.h',nemu/'include/b_csr.h')
        init=nemu/'src/isa/riscv32/init.c';text=init.read_text()
        if 'c5_csr_reset' not in text:text=text.replace('void init_isa() {','extern void c5_csr_reset(void);\nvoid init_isa() {\n  c5_csr_reset();')
        init.write_text(text)
    for am,platform in [(BENCH/'abstract-machine','nemu'),(WORK/'soc/workbench/abstract-machine','ysyxsoc')]:
        header=am/'am/include/arch/riscv.h';text=header.read_text()
        text=re.sub(r'struct Context \{.*?\};', 'struct Context {\n  uintptr_t gpr[NR_REGS],mcause,mstatus,mepc;\n  void *pdir;\n};',text,flags=re.S)
        header.write_text(text)
        dest=am/'am/src/riscv'/platform
        shutil.copyfile(root/'cte.c',dest/'cte.c');shutil.copyfile(root/'trap.S',dest/'trap.S')
    # The upstream riscv32 architecture uses M arithmetic; rv32e remains E+CSR.
    rt=WORK/'rt-thread-am/bsp/abstract-machine'
    text=(rt/'Makefile').read_text().replace('/home/USER/b-stage/soc/workbench/abstract-machine',str(BENCH/'abstract-machine'))
    if 'extra-nemu.ld' not in text:
        text=text.replace('LDFLAGS += -T extra.ld','ifneq ($(findstring -nemu,$(ARCH)),)\nLDFLAGS += -T extra-nemu.ld\nelse\nLDFLAGS += -T extra.ld\nendif')
    shutil.copyfile(ARCHIVE/'repos/NJU-ProjectN__rt-thread-am__master/bsp/abstract-machine/extra.ld',rt/'extra-nemu.ld')
    (rt/'Makefile').write_text(text)
    for p in rt.rglob('*'):
        if p.is_file() and p.suffix in ('.mk','.py','.h','.c') and 'build' not in p.relative_to(rt).parts:
            old=p.read_text();new=old.replace('/home/USER/b-stage/soc/rt-thread-am','/home/USER/b-stage/rt-thread-am')
            if old!=new:p.write_text(new)
    print('B1_NEMU_AND_CTE_PREPARED')

if __name__=='__main__':main()
