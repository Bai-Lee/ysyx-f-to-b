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
    parser.add_argument('--sdram-width',type=int,choices=[0,16,32],default=0);parser.add_argument('--sdram-ranks',type=int,choices=[1,2],default=1);parser.add_argument('--optimized',action='store_true');parser.add_argument('--nvboard',action='store_true');parser.add_argument('--ps2-observe',action='store_true');parser.add_argument('--chiplink',action='store_true');parser.add_argument('--chiplink-corrupt',action='store_true')
    parser.add_argument('--label');parser.add_argument('--rtl-snapshot');parser.add_argument('--apb-ratio-q',type=int,default=256);parser.add_argument('--axi-ratio-q',type=int,default=256);parser.add_argument('--axi-sdram',action='store_true')
    parser.add_argument('--cache-lines',type=int,default=0);parser.add_argument('--cache-words',type=int,default=1);parser.add_argument('--cache-ways',type=int,default=1);parser.add_argument('--cache-burst',action='store_true')
    parser.add_argument('--pipeline',action='store_true');parser.add_argument('--forward',action='store_true');parser.add_argument('--predict',action='store_true');parser.add_argument('--predict-jal',action='store_true');parser.add_argument('--stream-fetch',action='store_true');args=parser.parse_args();reset=int(args.reset,0)
    assert not(args.predict and args.predict_jal)
    assert 256<=args.apb_ratio_q<=65535
    assert 256<=args.axi_ratio_q<=65535 and not(args.axi_sdram and args.chiplink)
    assert args.cache_lines==0 or (args.cache_lines>=2 and not args.cache_lines&(args.cache_lines-1))
    assert args.cache_words in (1,2,4,8) and args.cache_ways in (1,2)
    assert args.sdram_ranks==1 or args.sdram_width==32
    assert not args.chiplink_corrupt or args.chiplink
    configuration={'reset_pc':reset,'mutant':args.mutant,'fast_flash':args.fast_flash,'cycle_sim':args.cycle_sim,'psram_qpi':args.psram_qpi,'psram_bytes':args.psram_bytes,'sdram_width':args.sdram_width,'sdram_ranks':args.sdram_ranks,'optimized':args.optimized,'nvboard':args.nvboard,'ps2_observe':args.ps2_observe,'chiplink':args.chiplink,'chiplink_corrupt':args.chiplink_corrupt}
    label=variant_name(configuration)
    if args.label:
        import re
        assert re.fullmatch('[a-z0-9-]+',args.label)
        label=args.label
    elif args.apb_ratio_q!=256:label+='-apb'+str(args.apb_ratio_q)
    if not args.label:
        if args.cache_lines:label+=f'-cache{args.cache_lines}x{args.cache_words*4}a{args.cache_ways}'+('-burst' if args.cache_burst else '')
        if args.axi_sdram:label+='-axisdram'+str(args.axi_ratio_q)
    configuration['apb_ratio_q']=args.apb_ratio_q
    configuration.update(cache_lines=args.cache_lines,cache_words=args.cache_words,cache_ways=args.cache_ways,cache_burst=args.cache_burst,axi_sdram=args.axi_sdram,axi_ratio_q=args.axi_ratio_q)
    configuration.update(pipeline=args.pipeline,forward=args.forward,predict=args.predict,predict_jal=args.predict_jal,predict_mode=2 if args.predict_jal else int(args.predict),stream_fetch=args.stream_fetch,prediction_policy='early decoded JAL only; interlock branches/JALR' if args.predict_jal else 'early decoded always-taken branches and JAL target; JALR sequential' if args.predict else 'control interlock')
    configuration['rtl_snapshot']=args.rtl_snapshot
    base=ROOT/'B/soc';out=WORK/'soc/build'/label;out.mkdir(parents=True,exist_ok=True)
    cpp_extra=[];link_extra=[];cflags=f'-O3 -g -Wall -Wextra -DC5_START_PC=0x{reset:08x}u'
    if args.nvboard:
        subprocess.run(['python3',str(base/'prepare_nvboard.py'),'--build'],check=True)
        nv=WORK/'soc/nvboard';cpp_extra=[WORK/'soc/nvboard_bind.cpp',nv/'build/nvboard.a']
        cflags+=' -DC5_ENABLE_NVBOARD -I'+str(nv/'usr/include')+' '+subprocess.check_output(['sdl2-config','--cflags'],text=True).strip()
        link_extra=['-LDFLAGS','-lSDL2 -lSDL2_image -lSDL2_ttf']
    original=base/('generation/chiplink/ysyxSoCFull.v' if args.chiplink else 'generation/axi/ysyxSoCFull.v' if args.axi_sdram else 'generation/ysyxSoCFull.v');generated=original
    if args.sdram_width==32 or args.chiplink:
        text=render(original.read_text(),args.sdram_width or 16,args.sdram_ranks)
        if args.chiplink:text=instrument(text,args.chiplink_corrupt)
        generated=out/'ysyxSoCFull.v';generated.write_text(text)
    rtl=(ROOT/args.rtl_snapshot).resolve() if args.rtl_snapshot else base/'rtl'
    assert rtl.resolve().is_relative_to(ROOT.resolve()) and rtl.is_dir()
    files=[generated,*sorted(rtl.glob('*.sv')),*sorted(rtl.glob('*.v')),*sorted((base/'perip').rglob('*.v'))]
    inputs=list(dict.fromkeys([*files,original,base/'sim/runner.cpp',*sorted((base/'sim').glob('*.hpp')),*cpp_extra,base/'build_soc.py',base/'sdram_wiring.py',base/'chiplink_wiring.py',ROOT/'B/runtime/budget_exec.py',ROOT/'B/runtime/resource_policy.py',POLICY_PATH]))
    exe=out/'sim';guard=ROOT/'B/runtime/budget_exec.py';tag='B/soc/build/'+label;budget=ROOT/'artifacts'/tag/'budget.json'
    command=[VERILATOR,'--cc','--exe','--build','--no-timing' if args.cycle_sim else '--timing','--trace','--assert','-j','4','-Wall','-Wno-fatal','--top-module','ysyxSoCFull','--timescale-override','1ns/1ns','--Mdir',out,'-o','sim',f"-DC5_RESET_PC=32'h{reset:08x}",f'-DC5_FAULT_ADDI={int(args.mutant)}','-CFLAGS',cflags,'-LDFLAGS','-ldl',
             '-I'+str(base/'perip/uart16550/rtl'),'-I'+str(base/'perip/spi/rtl'),f'-DC5_PSRAM_QPI={int(args.psram_qpi)}',f'-DC5_PSRAM_BYTES={args.psram_bytes}',
             f'-DB_APB_RATIO_Q={args.apb_ratio_q}',f'-DB_AXI_RATIO_Q={args.axi_ratio_q}',f'-DB_ICACHE_ENABLE={int(args.cache_lines>0)}',f'-DB_ICACHE_LINES={args.cache_lines or 16}',f'-DB_ICACHE_WORDS={args.cache_words}',f'-DB_ICACHE_WAYS={args.cache_ways}',f'-DB_ICACHE_BURST={int(args.cache_burst)}',f'-DB_PIPELINE={int(args.pipeline)}',f'-DB_FORWARD={int(args.forward)}',f'-DB_PREDICT={int(args.predict)}',f'-DC5_SDRAM_DQ={args.sdram_width or 16}',f'-DC5_SDRAM_RANKS={args.sdram_ranks}',*(['-DC5_SDRAM_OBSERVE=1'] if args.sdram_width else []),*(['-DC5_PS2_OBSERVE=1'] if args.ps2_observe else []),
             *(['-MAKEFLAGS','OPT_FAST=-O3 OPT_SLOW=-O3 OPT_GLOBAL=-O3'] if args.optimized else []),*(['-DFAST_FLASH'] if args.fast_flash else []),*files,base/'sim/runner.cpp',*cpp_extra,*link_extra]
    command=[f'-DB_PREDICT={2 if args.predict_jal else int(args.predict)}' if str(x).startswith('-DB_PREDICT=') else x for x in command]
    command.insert(1,f'-DB_FETCH_PIPELINED={int(args.stream_fetch)}')
    run(tag,['python3',guard,'--report',budget,'--',*command],inputs=inputs,outputs=[exe],timeout=900,resume=True)
    report=ROOT/'reports/B_soc_soc_build.json';rows=json.loads(report.read_text()).get('variants',[]) if report.exists() else []
    rows=[r for r in rows if variant_name(r)!=label]+[{**configuration,'variant':label,'executable':str(exe),'sha256':sha(exe),'inputs':[{'path':str(p),'sha256':sha(p)} for p in inputs],'budget':json.loads(budget.read_text())}]
    dump(report,{'status':'BUILT_NOT_FUNCTIONALLY_ACCEPTED','variants':rows,'scope':'Full generated SoC and real APB UART/SPI/PSRAM/SDRAM controllers; unimplemented endpoint stubs are not declared functional.16 external reset cycles plus framework CPU reset delay. Timing simulation preserves published #1 UART delays with1ns precision.'})
    print('C5_FULL_SOC_BUILD_PASS',hex(reset),flush=True)


if __name__=='__main__':main()
