from pathlib import Path
import sys,re,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--from-case');args=parser.parse_args()
    subprocess.run(['python3',str(ROOT/'C/C5/prepare_am.py')],check=True)
    base=WORK/'c5/workbench';am=base/'abstract-machine';cpu=base/'cpu-tests';ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so'
    build=next(r for r in json.loads((ROOT/'reports/C5_soc_build.json').read_text())['variants'] if r['reset_pc']==0x20000000 and not r.get('mutant',False) and not r.get('psram_qpi',False) and r.get('psram_bytes',4096)==4096 and not r.get('fast_flash',False) and not r.get('cycle_sim',False))
    exe=Path(build['executable']);assert sha(exe)==build['sha256']
    env={'AM_HOME':str(am),'NPC_HOME':str(base/'npc')};rows=[]
    sources=[p for p in sorted((am/'am/src/riscv/ysyxsoc').glob('*'))]+[am/'scripts/ysyxsoc-mrom.ld',am/'scripts/ysyxsoc-initial.ld',am/'scripts/platform/ysyxsoc.mk']
    nm=Path(shutil.which('riscv64-linux-gnu-nm'));readelf=Path(shutil.which('riscv64-linux-gnu-readelf'))
    cases=[('dummy','initial','',0),('dummy','','',0),('fib-initial','initial','',1),
           ('mem-test','initial','',0),('mem-test-corrupt','initial','x',1),
           ('boot-data','poison','',0),('boot-data-skip-data','broken-data','',1),('boot-data-skip-bss','broken-bss','',1)]
    if args.from_case:
        index=next(i for i,c in enumerate(cases) if c[0]==args.from_case)
        prior=json.loads((ROOT/'reports/C5_ram.json').read_text())['runs']
        keys={(c[0],c[1]) for c in cases[:index]}
        rows=[r for r in prior if (r['name'],r['profile']) in keys]
        assert len(rows)==index
        cases=cases[index:]
    for name,profile,mainargs,expected in cases:
        program='fib' if name=='fib-initial' else 'mem-test' if name.startswith('mem-test') else 'boot-data' if name.startswith('boot-data') else 'dummy'
        if program in ['dummy','fib']:
            folder=cpu;src=cpu/'tests'/(program+'.c');manifest=cpu/('C5-Makefile.'+program)
            manifest.write_text('NAME = '+program+'\nSRCS = tests/'+program+'.c\ninclude $(AM_HOME)/Makefile\n')
        else:
            folder=base/program;folder.mkdir(exist_ok=True);src=ROOT/'C/C5/programs'/(program+'.c')
            shutil.copyfile(src,folder/'main.c');manifest=folder/'Makefile';manifest.write_text('NAME = '+program+'\nSRCS = main.c\ninclude $(AM_HOME)/Makefile\n')
        arch='riscv32e-ysyxsoc'+('-'+profile if profile else '')
        tag='C5/ram/'+name+('-'+profile if program=='dummy' and profile else '')
        image=folder/'build'/(program+'-'+arch+'.bin');elf=image.with_suffix('.elf')
        run(tag+'/build',['make','-j1','-f',manifest,'ARCH='+arch,'mainargs='+mainargs,'insert-arg'],cwd=folder,env=env,inputs=[manifest,src,*sources,am/'scripts'/(arch+'.mk')],outputs=[image,elf],timeout=180)
        assert image.stat().st_size<=4096,(name,image.stat().st_size)
        symbols,_,_=run(tag+'/symbols',[nm,'-n',elf],inputs=[nm,elf]);symbols={parts[2]:int(parts[0],16) for line in symbols.splitlines() if len(parts:=line.split())==3 and re.fullmatch('[0-9a-fA-F]+',parts[0])}
        assert symbols['_start']==0x20000000 and symbols['_stack_pointer']==0x0f002000
        run(tag+'/elf',[readelf,'-h','-l','-S',elf],inputs=[readelf,elf])
        directory=ROOT/'artifacts'/tag;result=directory/'simulation.json';trace=directory/'events.log'
        options=[]
        if program=='mem-test':options=['--coverage-base',str(symbols['_heap_start']),'--coverage-size',str(symbols['_heap_end']-symbols['_heap_start'])]
        stdout,stderr,_=run(tag+'/run',[exe,'--mrom',image,'--ref',ref,'--report',result,'--trace',trace,'--trace-limit','1000','--max-cycles','20000000',*options],inputs=[exe,image,elf,ref],outputs=[trace] if name=='fib-initial' else [result,trace],timeout=180,expected=(expected,))
        if name=='fib-initial':
            assert 'do not support write operations' in stdout+stderr and 'asic.lmrom' in stdout+stderr
            rows.append({'name':name,'profile':profile,'status':'PASS_REJECTED_BY_REAL_SOC_ROM_ASSERTION','symbols':symbols,
                         'image_sha256':sha(image),'elf_sha256':sha(elf),'evidence':'artifacts/'+tag,
                         'scope':'Simulation terminates at the real MROM controller assertion before final statistics; no final DiffTest count or natural completion inferred.'})
            dump(ROOT/'reports/C5_ram.json',{'status':'IN_PROGRESS','runs':rows})
            continue
        data=json.loads(result.read_text());assert data['diff_enabled'] and data['diff_checked']+data['device_sync_checked']==data['instructions']
        if expected==0:assert data['result']=='GOOD_TRAP'
        else:
            assert data['result']=='BAD_TRAP'
            if name.endswith('skip-data'):assert data['a0']==11
            if name.endswith('skip-bss'):assert data['a0']==12
        if name=='mem-test':
            n=symbols['_heap_end']-symbols['_heap_start'];coverage=data['coverage']
            assert n==6144 and coverage['unique_read_bytes']==n and coverage['unique_written_bytes']==n
            # Two patterns. A uint64 access is emitted as two RV32 word transfers.
            assert coverage['read_ops_by_width']==[2*n,n,n] and coverage['write_ops_by_width']==[2*n,n,n],coverage
        rows.append({'name':name,'profile':profile,'status':'PASS','simulation':data,'symbols':symbols,'image_sha256':sha(image),'elf_sha256':sha(elf),'evidence':'artifacts/'+tag})
        dump(ROOT/'reports/C5_ram.json',{'status':'IN_PROGRESS','runs':rows})
    dump(ROOT/'reports/C5_ram.json',{'status':'PASS_SRAM_TRM_MEMORY_AND_BOOT_CONTROLS','runs':rows,
         'scope':'Actual full SoC SRAM path and NEMU comparisons. Initial fib cannot write MROM; final link separates LMA/VMA.6KiB heap fully exercised with8/16/32/64-bit address/inverse patterns; reserved2KiB stack excluded. Poisoned SRAM makes omission of data copying or BSS clearing fail deterministically. Full official CPU suite is a separate check.'})
    mark(['C5-M007','C5-M008','C5-M009'],'PASS',['reports/C5_ram.json','reports/C5_diff.json'],'New AM, real MROM/SRAM DiffTest without range skipping, complete bounded heap memory test and data/bootstrap controls.')
    print('C5_SRAM_TRM_AND_BOOT_CONTROLS_PASS',flush=True)


if __name__=='__main__':main()
