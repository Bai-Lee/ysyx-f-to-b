from pathlib import Path
import sys,argparse,re,os
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from support import select_build


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--build-only',action='store_true');parser.add_argument('--variant',default='30000000-cycle-psram4m-qpi');parser.add_argument('--memory',choices=['psram','sdram32','sdram64','sdram128'],default='psram');args=parser.parse_args()
    base=WORK/'c5/workbench';am=base/'abstract-machine';bsp=WORK/'c5/rt-thread-am/bsp/abstract-machine'
    arch='riscv32e-ysyxsoc-'+args.memory;tag='C5/rtthread/'+args.memory;image=bsp/'build'/('rtthread-'+arch+'.bin');elf=image.with_suffix('.elf')
    apps_make=bsp/'build'/arch/'am-apps.mk';apps_make.parent.mkdir(parents=True,exist_ok=True)
    if not apps_make.exists():apps_make.write_text('# Boot-only acceptance; AM application integration is a separate profile.\n')
    source=[*sorted((bsp/'src').glob('*.c')),bsp/'Makefile',bsp/'rtconfig.h',bsp/'files.mk',bsp/'extra.ld',bsp/'include/extra.h']
    source += [(bsp/line.split('+=',1)[1].strip()).resolve() for line in (bsp/'files.mk').read_text().splitlines() if line.startswith('SRCS +=')]
    source += [*sorted((am/'am/src/riscv/ysyxsoc').glob('*')),am/'scripts'/('ysyxsoc-code-'+args.memory+'.ld'),am/'scripts/platform/ysyxsoc.mk']
    source=list(dict.fromkeys(source))
    run(tag+'/build',['make','-j1','ARCH='+arch,'insert-arg'],cwd=bsp,env={'AM_HOME':str(am),'NPC_HOME':str(base/'npc'),'PATH':'/home/USER/tools/scons-4.0.1/bin:'+os.environ['PATH']},inputs=source,outputs=[image,elf],timeout=600)
    nm=Path(shutil.which('riscv64-linux-gnu-nm'));text,_,_=run(tag+'/symbols',[nm,'-n',elf],inputs=[nm,elf])
    symbols={v[2]:int(v[0],16) for line in text.splitlines() if len(v:=line.split())==3 and re.fullmatch('[0-9a-fA-F]+',v[0])}
    memory_start=0x80000000 if args.memory=='psram' else 0xa0000000
    memory_size=4194304 if args.memory=='psram' else int(args.memory[5:])*1024**2
    for name in ['main','__am_asm_trap','rt_schedule','rt_hw_context_switch','__fsymtab_start','__rt_init_start']:assert memory_start<=symbols[name]<memory_start+memory_size
    assert symbols['__data_start']<=symbols['__fsymtab_start']<symbols['__fsymtab_end']<=symbols['__data_end']
    assert symbols['_stack_pointer']==0x0f002000
    if args.build_only:print('C5_RTTHREAD_BUILD_ONLY_PASS',flush=True);return
    exe=Path(select_build(args.variant)['executable']);ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so'
    directory=ROOT/'artifacts'/tag;result=directory/'simulation.json';budget=directory/'resources.json'
    run(tag+'/run',['python3',ROOT/'C/runtime/budget_exec.py','--report',budget,'--',exe,'--flash',image,'--ref',ref,'--report',result,'--max-cycles','800000000','--progress-cycles','20000000'],inputs=[exe,ref,image,elf],outputs=[result,budget],timeout=1200)
    data=json.loads(result.read_text());assert data['result']=='GOOD_TRAP' and data['diff_enabled'] and data['diff_checked']+data['device_sync_checked']==data['instructions']
    assert data['retired_by_region'][3 if args.memory=='psram' else 4]>1000 and data['mrom_dpi_calls']==0
    uart=bytes.fromhex(data['uart']['hex']).decode('ascii').replace('\r','')
    assert 'Thread Operating System' in uart and 'Hello RISC-V!' in uart and 'C5_CONTEXT_PASS a=12 b=12' in uart and 'C5_RTTHREAD_PASS' in uart
    for command in ['help','date','version','free','ps','pwd','ls','memtrace','memcheck','utest_list','c5_context_test','c5_done']:assert re.search(r'msh\s*/>\s*'+command+r'(?:\n|\r)',uart),command
    report=ROOT/('reports/C5_rtthread.json' if args.memory=='psram' else 'reports/C5_rtthread_'+args.memory+'.json')
    dump(report,{'status':'PASS_BOOT_ORIGINAL_COMMANDS_AND_CONTEXTS','memory':args.memory,'source_commit':'72ba231bb79db53f1c07920f2642ef20679faeff','image_bytes':image.stat().st_size,'image_sha256':sha(image),'elf_sha256':sha(elf),'symbols':symbols,'uart':uart,'cycles':data['cycles'],'instructions':data['instructions'],'wall_seconds':data['wall_seconds'],'diff_checked':data['diff_checked'],'device_sync_checked':data['device_sync_checked'],'evidence':'artifacts/'+tag,'scope':'Flash bootstrap copies original RT-Thread kernel into the recorded memory; real CPU executes it. Original10 scripted shell commands, two threaded stack/cookie/yield/return checks, and explicit halt-after-validation command. No asynchronous interrupt or interactive UART input claim in this profile.'})
    if args.memory=='psram':mark(['C5-M029'],'PASS',['reports/C5_rtthread.json','reports/C5_context.json'],'Real PSRAM RT-Thread with CTE context switches, original10 scripted shell commands, distinct per-thread stacks/args and return-to-exit checks. Independent NEMU checks every non-MMIO instruction.')
    print('C5_RTTHREAD_PASS',args.memory,flush=True)


if __name__=='__main__':main()
