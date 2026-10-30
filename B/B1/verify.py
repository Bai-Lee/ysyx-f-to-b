from pathlib import Path
import sys,argparse,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

SRC=ROOT/'B/B1'

def compile_app(name,arch,sources,am,extra=()):
    app=WORK/'b1/apps'/name;app.mkdir(parents=True,exist_ok=True)
    for filename,text in sources.items():(app/filename).write_text(text)
    (app/'Makefile').write_text('NAME = '+name+'\nSRCS = '+' '.join(sources)+'\ninclude $(AM_HOME)/Makefile\n')
    image=app/'build'/(name+'-'+arch+'.bin');elf=image.with_suffix('.elf')
    inputs=[*sorted(app.glob('*.c')),*sorted(app.glob('*.S')),app/'Makefile',am/'am/include/arch/riscv.h',*sorted((am/'am/src/riscv'/('nemu' if arch.endswith('nemu') else 'bnpc' if arch.endswith('bnpc') else 'ysyxsoc')).glob('*'))]
    run('B1/build/'+name,['make','-j4','ARCH='+arch,*extra,'insert-arg'],cwd=app,env={'AM_HOME':str(am),'NPC_HOME':str(WORK/'soc/workbench/npc')},inputs=inputs,outputs=[image,elf],timeout=300,resume=True)
    return image,elf

def context_sources(bits):
    text=(ROOT/'B/soc/programs/context-test.c').read_text().replace('C5_CTE_PASS','B1_CTE_PASS')
    if bits==16:probe=(ROOT/'B/soc/programs/context-probe.S').read_text()
    else:
        text=text.replace('i<16','i<32').replace('saved[19]','saved[35]').replace('i==15','i==17')
        lines=['.text','.balign 4','.global context_probe','.type context_probe,@function','context_probe:','  addi sp,sp,-256']
        lines += [f'  sw x{i},{128+4*i}(sp)' for i in range(32)]
        lines += [f'  li x{i},'+('-1' if i==17 else hex(0x10000000+i)) for i in range(1,32) if i not in (2,3)]
        lines += ['  ecall']+[f'  sw x{i},{4*i}(sp)' for i in range(32)]+['  mv a0,sp','  call probe_check']
        lines += [f'  lw x{i},{128+4*i}(sp)' for i in range(1,32) if i not in (2,10)]
        lines += ['  addi sp,sp,256','  ret','.size context_probe,.-context_probe'];probe='\n'.join(lines)+'\n'
    return {'main.c':text,'probe.S':probe}

def native_run(name,image,elf,expected=0,diff=True):
    nemu=BENCH/'nemu';exe=nemu/'build/riscv32-nemu-interpreter';spike=nemu/'tools/spike-diff/build/riscv32-spike-so'
    out=ROOT/'artifacts/B1/native'/name;out.mkdir(parents=True,exist_ok=True);report=out/'simulation.json';etrace=out/'etrace.jsonl'
    env={'LD_LIBRARY_PATH':str(nemu/'tools/capstone/repo'),'SDL_VIDEODRIVER':'dummy','SDL_AUDIODRIVER':'dummy','B_ETRACE':str(etrace)}
    stdout,stderr,_=run('B1/native/'+name,[exe,'-b','--diff='+str(spike) if diff else '--diff=none','--report='+str(report),image],cwd=nemu,env=env,inputs=[exe,image,elf,*([spike] if diff else [])],outputs=[report,etrace],expected=(expected,),timeout=180)
    data=json.loads(report.read_text());events=[json.loads(line) for line in etrace.read_text().splitlines()]
    assert data['result']==('GOOD_TRAP' if expected==0 else 'BAD_TRAP'),data
    assert data['diff_enabled']==diff
    if diff:assert data['diff_checked']+data['diff_skipped']==data['instructions']
    row={'name':name,'status':'PASS','simulation':data,'exception_events':len(events),'ecalls':sum(x['event']=='ECALL' for x in events),'mrets':sum(x['event']=='MRET' for x in events),'evidence':'artifacts/B1/native/'+name}
    return row,stdout+stderr

def soc_run(name,image,elf,expected=0,extra_env=None):
    builds=json.loads((ROOT/'reports/B_soc_soc_build.json').read_text())['variants']
    build=next(r for r in builds if r['variant']=='30000000-cycle-psram4m-qpi-sdram32x2-opt')
    exe=Path(build['executable']);assert sha(exe)==build['sha256'];ref=WORK/'nemu-ref/build/riscv32-nemu-interpreter-so'
    out=ROOT/'artifacts/B1/npc'/name;out.mkdir(parents=True,exist_ok=True);report=out/'simulation.json';budget=out/'budget.json';etrace=out/'etrace.jsonl'
    command=['python3',ROOT/'B/runtime/budget_exec.py','--report',budget,'--',exe,'--flash',image,'--ref',ref,'--report',report,'--max-cycles','800000000','--progress-cycles','20000000']
    stdout,stderr,_=run('B1/npc/'+name,command,inputs=[exe,ref,image,elf],outputs=[report,budget,etrace],expected=(expected,),env={'B_ETRACE':str(etrace),**(extra_env or {})},timeout=900)
    data=json.loads(report.read_text());assert data['diff_enabled']
    if expected in (0,1):assert data['diff_checked']+data['device_sync_checked']==data['instructions']
    uart=bytes.fromhex(data['uart']['hex']).decode('ascii').replace('\r','')
    return {'name':name,'status':'PASS','simulation':data,'uart':uart,'evidence':'artifacts/B1/npc/'+name},stdout+stderr

def rt_build(arch,am):
    app=WORK/'rt-thread-am/bsp/abstract-machine';(app/'build'/arch).mkdir(parents=True,exist_ok=True)
    (app/'build'/arch/'am-apps.mk').write_text('# B1 boot/context profile; app integration was tested separately in C.\n')
    image=app/'build'/('rtthread-'+arch+'.bin');elf=image.with_suffix('.elf')
    inputs=[*sorted((app/'src').glob('*.c')),app/'Makefile',app/'rtconfig.h',app/'files.mk',app/'extra.ld',app/'extra-nemu.ld',app/'include/extra.h',am/'am/include/arch/riscv.h']
    inputs += [(app/line.split('+=',1)[1].strip()).resolve() for line in (app/'files.mk').read_text().splitlines() if line.startswith('SRCS +=')]
    inputs += sorted((am/'am/src/riscv'/('nemu' if arch.endswith('nemu') else 'bnpc' if arch.endswith('bnpc') else 'ysyxsoc')).glob('*'))
    run('B1/rtthread-build/'+arch,['make','-j4','ARCH='+arch,'insert-arg'],cwd=app,env={'AM_HOME':str(am),'NPC_HOME':str(WORK/'soc/workbench/npc'),'PATH':'/home/USER/tools/scons-4.0.1/bin:'+os.environ['PATH']},inputs=list(dict.fromkeys(inputs)),outputs=[image,elf],timeout=600,resume=True)
    return image,elf

def main():
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['native','npc']);args=parser.parse_args();rows=[]
    if args.mode=='native':
        am=BENCH/'abstract-machine';arch='riscv32-nemu'
        image,elf=compile_app('yield32',arch,{'main.c':(SRC/'yield-test.c').read_text()},am)
        row,text=native_run('yield32',image,elf);assert row['ecalls']==row['mrets']==16 and 'B1_YIELD_PASS count=16' in text;rows.append(row)
        for bad in [False,True]:
            sources=context_sources(32)
            if bad:sources['bad-trap.S']=(SRC/'trap.S').read_text().replace('  RESTORE(5)','  li t0,0')
            name='context32'+('-bad-restore' if bad else '')
            image,elf=compile_app(name,arch,sources,am)
            row,text=native_run(name,image,elf,1 if bad else 0)
            if bad:assert row['simulation']['halt_ret']==95
            else:assert row['ecalls']==row['mrets']==52 and 'B1_CTE_PASS a=12 b=12' in text
            rows.append(row)
        image,elf=rt_build(arch,am);row,text=native_run('rtthread32',image,elf)
        assert 'Thread Operating System' in text and 'C5_RTTHREAD_PASS' in text and 'C5_CONTEXT_PASS a=12 b=12' in text
        for command in ['help','date','version','free','ps','pwd','ls','memtrace','memcheck','utest_list','c5_context_test','c5_done']:assert re.search(r'msh\s*/>\s*'+command+r'\s',text),command
        rows.append(row)
    else:
        am=WORK/'soc/workbench/abstract-machine';arch='riscv32e-ysyxsoc-sdram128'
        image,elf=compile_app('cycle16',arch,{'main.c':(SRC/'cycle-test.c').read_text()},am,extra=['SOC_PRINT_ID=1'])
        row,text=soc_run('cycle16',image,elf);assert row['simulation']['result']=='GOOD_TRAP' and 'B1_MCYCLE_PASS' in row['uart'];rows.append(row)
        row,text=soc_run('cycle16-bad-reference',image,elf,expected=1,extra_env={'B_FAULT_REFERENCE_CLOCK':'1'});assert row['simulation']['result']=='DIFF_FAIL';rows.append(row)
        for bad in [False,True]:
            sources=context_sources(16)
            if bad:sources['bad-trap.S']=(SRC/'trap.S').read_text().replace('  RESTORE(5)','  li t0,0')
            name='context16'+('-bad-restore' if bad else '')
            image,elf=compile_app(name,arch,sources,am)
            row,text=soc_run(name,image,elf,1 if bad else 0)
            if bad:assert row['simulation']['result']=='BAD_TRAP' and row['simulation']['a0']==95
            else:assert row['simulation']['result']=='GOOD_TRAP' and row['simulation']['traps']=={'ecall':52,'mret':52}
            rows.append(row)
        image,elf=rt_build(arch,am);row,text=soc_run('rtthread16',image,elf)
        assert row['simulation']['result']=='GOOD_TRAP' and 'C5_RTTHREAD_PASS' in row['uart'] and 'C5_CONTEXT_PASS a=12 b=12' in row['uart']
        rows.append(row)
    dump(ROOT/('reports/B1_'+args.mode+'.json'),{'status':'PASS','runs':rows,'scope':'Actual execution. Negative fixtures pass only when the intended error is detected. Synchronous machine-mode traps and bounded scripted RT-Thread commands; no claim of full privileged ISA or interrupt preemption.'})
    print('B1_'+args.mode.upper()+'_PASS')

if __name__=='__main__':main()
