from pathlib import Path
import sys,re,tarfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    lock=json.loads((ROOT/'reports/D5_report_support.json').read_text());env=lock['environment'];am=BENCH/'abstract-machine';n=BENCH/'nemu';exe=n/'build/riscv32-nemu-interpreter';ref=n/'tools/spike-diff/build/riscv32-spike-so';rows=[]
    plans=[('riscv',BENCH/'riscv-tests','NJU-ProjectN__riscv-tests-am__master',[]),('cpu',BENCH/'am-kernels/tests/cpu-tests','NJU-ProjectN__am-kernels__ics2026',[])]
    for suite,cwd,archive_name,_ in plans:
        if suite=='riscv':files=sorted([*list((cwd/'isa/rv32ui').glob('*.S')),*list((cwd/'isa/rv32um').glob('*.S'))]);files=[f for f in files if f.stem not in ('fence_i','ma_data')]
        else:files=sorted((cwd/'tests').glob('*.c'));files=[f for f in files if f.stem!='wrong']
        tar=Path('/workspace/downloads/ysyx_e_stage/sources/canonical')/(archive_name+'.tar.gz')
        with tarfile.open(tar) as original:
            for f in files:
                rel=str(f.relative_to(cwd)) if suite=='riscv' else str(f.relative_to(BENCH/'am-kernels'))
                assert original.extractfile(rel).read()==f.read_bytes(),f
        for source in files:
            name=source.stem;base=cwd/'build'/(name+'-riscv32-nemu');report=Path(str(base)+'.nemu.json');image=Path(str(base)+'.bin');elf=Path(str(base)+'.elf');trace=Path(str(base)+'.nemu.log')
            args=['make','-j1','ARCH=riscv32-nemu','ALL='+name,'run','YSYX_HOME='+str(BENCH),'STUID=LOCAL_D_STAGE','STUNAME=Independent_Local_Implementation']
            if suite=='riscv':args.append('TEST_ISA=i m')
            inputs=[source,cwd/'Makefile',am/'Makefile',am/'scripts/isa/riscv.mk',am/'scripts/platform/nemu.mk',exe,ref,am/'klib/build/klib-riscv32-nemu.a']
            o,e,r=run('D3/official/'+suite+'/'+name,args,cwd=cwd,env=env,inputs=inputs,outputs=[report,image,elf,trace],timeout=300,resume=True)
            d=json.loads(report.read_text());assert d['result']=='GOOD_TRAP' and d['halt_ret']==0 and d['gpr'][0]==0 and d['diff_enabled'] and d['diff_checked']>0 and d['diff_checked']+d['diff_skipped']==d['instructions'],(suite,name,d)
            assert '***FAIL***' not in o and re.search(r'\[\s*'+re.escape(name)+r'\]\s*\x1b\[1;32mPASS',o)
            rows.append({'suite':suite,'name':name,'status':'PASS','source_sha256':sha(source),'image_sha256':sha(image),'elf_sha256':sha(elf),'report_sha256':sha(report),'trace_sha256':sha(trace),'simulation':d,'evidence':'artifacts/D3/official/'+suite+'/'+name,'elapsed_seconds':r['elapsed_seconds']})
            dump(ROOT/'reports/D3_official_tests.json',{'status':'IN_PROGRESS','programs':rows,'nemu_sha256':sha(exe),'spike_sha256':sha(ref)})
    cwd=BENCH/'am-kernels/tests/cpu-tests';source=cwd/'tests/wrong.c';report=cwd/'build/wrong-riscv32-nemu.nemu.json'
    o,e,r=run('D3/official/cpu_wrong',['make','-j1','ARCH=riscv32-nemu','ALL=wrong','run','YSYX_HOME='+str(BENCH),'STUID=LOCAL_D_STAGE','STUNAME=Independent_Local_Implementation'],cwd=cwd,env=env,inputs=[source,cwd/'Makefile',exe,ref],outputs=[report],expected=(2,),timeout=120,resume=True)
    negative=json.loads(report.read_text());assert negative['result']=='BAD_TRAP' and negative['halt_ret']!=0 and '***FAIL***' in o
    result={'status':'PASS','programs':rows,'positive_count':len(rows),'riscv_count':sum(x['suite']=='riscv' for x in rows),'cpu_count':sum(x['suite']=='cpu' for x in rows),'negative_wrong':negative,'make_failure_propagated':r['exit_code']==2,'official_exclusions':['fence_i','ma_data'],'exclusion_source':'Original RISC-V test Makefile defaults; separate authored FENCE/FENCE.I and unaligned evidence are explicitly scoped.','nemu_sha256':sha(exe),'spike_sha256':sha(ref),'source_preservation':'Every test source compared byte-for-byte against its locked canonical Git archive; parent CPU-test failure aggregation was fixed, not its tests.'}
    dump(ROOT/'reports/D3_official_tests.json',result);print('D3_OFFICIAL_PASS',len(rows),flush=True)

if __name__=='__main__':main()
