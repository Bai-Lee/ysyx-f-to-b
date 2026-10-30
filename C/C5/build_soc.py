from pathlib import Path
import sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from resource_policy import POLICY_PATH
from support import variant_name
from sdram_wiring import render
from chiplink_wiring import instrument


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--reset',default='0x20000000');parser.add_argument('--mutant',action='store_true');parser.add_argument('--fast-flash',action='store_true');parser.add_argument('--cycle-sim',action='store_true');parser.add_argument('--psram-qpi',action='store_true');parser.add_argument('--psram-bytes',type=int,choices=[4096,4194304],default=4096)
    parser.add_argument('--sdram-width',type=int,choices=[0,16,32],default=0);parser.add_argument('--sdram-ranks',type=int,choices=[1,2],default=1);parser.add_argument('--optimized',action='store_true');parser.add_argument('--nvboard',action='store_true');parser.add_argument('--ps2-observe',action='store_true');parser.add_argument('--chiplink',action='store_true');parser.add_argument('--chiplink-corrupt',action='store_true');args=parser.parse_args();reset=int(args.reset,0)
    assert args.sdram_ranks==1 or args.sdram_width==32
    assert not args.chiplink_corrupt or args.chiplink
    configuration={'reset_pc':reset,'mutant':args.mutant,'fast_flash':args.fast_flash,'cycle_sim':args.cycle_sim,'psram_qpi':args.psram_qpi,'psram_bytes':args.psram_bytes,'sdram_width':args.sdram_width,'sdram_ranks':args.sdram_ranks,'optimized':args.optimized,'nvboard':args.nvboard,'ps2_observe':args.ps2_observe,'chiplink':args.chiplink,'chiplink_corrupt':args.chiplink_corrupt}
    label=variant_name(configuration)
    base=ROOT/'C/C5';out=WORK/'c5/build'/label;out.mkdir(parents=True,exist_ok=True)
    subprocess.run(['python3',str(base/'make_cpu_wrapper.py')],check=True)
    cpp_extra=[];link_extra=[];cflags=f'-O3 -g -Wall -Wextra -DC5_START_PC=0x{reset:08x}u'
    if args.nvboard:
        subprocess.run(['python3',str(base/'prepare_nvboard.py'),'--build'],check=True)
        nv=WORK/'c5/nvboard';cpp_extra=[WORK/'c5/nvboard_bind.cpp',nv/'build/nvboard.a']
        cflags+=' -DC5_ENABLE_NVBOARD -I'+str(nv/'usr/include')+' '+subprocess.check_output(['sdl2-config','--cflags'],text=True).strip()
        link_extra=['-LDFLAGS','-lSDL2 -lSDL2_image -lSDL2_ttf']
    original=base/('generation/chiplink/ysyxSoCFull.v' if args.chiplink else 'generation/ysyxSoCFull.v');generated=original
    if args.sdram_width==32 or args.chiplink:
        text=render(original.read_text(),args.sdram_width or 16,args.sdram_ranks)
        if args.chiplink:text=instrument(text,args.chiplink_corrupt)
        generated=out/'ysyxSoCFull.v';generated.write_text(text)
    files=[generated,*sorted((base/'rtl').glob('*.sv')),*sorted((base/'rtl').glob('*.v')),*sorted((base/'perip').rglob('*.v'))]
    inputs=list(dict.fromkeys([*files,original,base/'sim/runner.cpp',*sorted((base/'sim').glob('*.hpp')),*cpp_extra,base/'build_soc.py',base/'sdram_wiring.py',base/'chiplink_wiring.py',base/'make_cpu_wrapper.py',ROOT/'C/runtime/budget_exec.py',ROOT/'C/runtime/resource_policy.py',POLICY_PATH]))
    exe=out/'sim';guard=ROOT/'C/runtime/budget_exec.py';tag='C5/build/'+label;budget=ROOT/'artifacts'/tag/'budget.json'
    command=[VERILATOR,'--cc','--exe','--build','--no-timing' if args.cycle_sim else '--timing','--trace','--assert','-j','1','-Wall','-Wno-fatal','--top-module','ysyxSoCFull','--timescale-override','1ns/1ns','--Mdir',out,'-o','sim',f"-DC5_RESET_PC=32'h{reset:08x}",f'-DC5_FAULT_ADDI={int(args.mutant)}','-CFLAGS',cflags,'-LDFLAGS','-ldl',
             '-I'+str(base/'perip/uart16550/rtl'),'-I'+str(base/'perip/spi/rtl'),f'-DC5_PSRAM_QPI={int(args.psram_qpi)}',f'-DC5_PSRAM_BYTES={args.psram_bytes}',
             f'-DC5_SDRAM_DQ={args.sdram_width or 16}',f'-DC5_SDRAM_RANKS={args.sdram_ranks}',*(['-DC5_SDRAM_OBSERVE=1'] if args.sdram_width else []),*(['-DC5_PS2_OBSERVE=1'] if args.ps2_observe else []),
             *(['-MAKEFLAGS','OPT_FAST=-O3 OPT_SLOW=-O3 OPT_GLOBAL=-O3'] if args.optimized else []),*(['-DFAST_FLASH'] if args.fast_flash else []),*files,base/'sim/runner.cpp',*cpp_extra,*link_extra]
    run(tag,['python3',guard,'--report',budget,'--',*command],inputs=inputs,outputs=[exe],timeout=900,resume=True)
    report=ROOT/'reports/C5_soc_build.json';rows=json.loads(report.read_text()).get('variants',[]) if report.exists() else []
    rows=[r for r in rows if variant_name(r)!=label]+[{**configuration,'variant':label,'executable':str(exe),'sha256':sha(exe),'inputs':[{'path':str(p),'sha256':sha(p)} for p in inputs],'budget':json.loads(budget.read_text())}]
    dump(report,{'status':'BUILT_NOT_FUNCTIONALLY_ACCEPTED','variants':rows,'scope':'Full generated SoC and real APB UART/SPI/PSRAM/SDRAM controllers; unimplemented endpoint stubs are not declared functional.16 external reset cycles plus framework CPU reset delay. Timing simulation preserves published #1 UART delays with1ns precision.'})
    print('C5_FULL_SOC_BUILD_PASS',hex(reset),flush=True)


if __name__=='__main__':main()
