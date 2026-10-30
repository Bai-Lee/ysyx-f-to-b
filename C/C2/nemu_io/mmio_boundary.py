from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *
d=ROOT/'C/C2/nemu_io/results';d.mkdir(exist_ok=True)
source=d/'mmio-cross-end.S';source.write_text('.section .text\n.globl _start\n_start:\n lui t0,0xa1075\n addi t0,t0,0x2fe\n lw a0,0(t0)\n ebreak\n')
ld=ROOT/'D/D7/baremetal.ld';elf=d/'mmio-cross-end.elf';binary=d/'mmio-cross-end.bin'
run('C2/pa2/mmio-span/build',['riscv64-linux-gnu-gcc','-march=rv32im','-mabi=ilp32','-nostdlib','-nostartfiles','-static','-Wl,--build-id=none','-T',ld,source,'-o',elf],inputs=[source,ld],outputs=[elf])
run('C2/pa2/mmio-span/image',['riscv64-linux-gnu-objcopy','-O','binary',elf,binary],inputs=[elf],outputs=[binary])
build=json.loads((ROOT/'reports/C2_nemu_build.json').read_text());exe=Path(next(r['executable'] for r in build['variants'] if r['mode']=='feature'))
o,e,r=run('C2/pa2/mmio-span/reject',[exe,'-b','--diff=none',binary],cwd=BENCH/'nemu',inputs=[exe,binary],env={'SDL_VIDEODRIVER':'dummy'},expected=(-6,))
assert 'out of bound {vmem}' in o+e and '0xa10752fe' in o+e
dump(ROOT/'reports/C2_nemu_mmio_boundary.json',{'status':'PASS_NEGATIVE_CONTROL','address':'0xa10752fe','length':4,'device_high':'0xa10752ff','exit_code':r['exit_code'],'scope':'Actual RV32IM load whose first byte is mapped but complete span is not; NEMU rejects before host access. No independent REF comparison needed for an intentional invalid MMIO access.'})
