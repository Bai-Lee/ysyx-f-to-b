from pathlib import Path
import sys,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'B1'))
from common import *
from verify import compile_app,rt_build,context_sources

def main():
    base=WORK/'soc/workbench';am=base/'abstract-machine';arch='riscv32e-ysyxsoc-sdram128-p325'
    (am/'scripts'/(arch+'.mk')).write_text('SOC_CLOCK_MHZ := 325\ninclude $(AM_HOME)/scripts/riscv32e-ysyxsoc-sdram128.mk\n')
    build=next(r for r in json.loads((ROOT/'reports/B_soc_soc_build.json').read_text())['variants'] if r['variant']=='b5-release');exe=Path(build['executable']);assert sha(exe)==build['sha256'];ref=WORK/'nemu-ref/build/riscv32-nemu-interpreter-so';rows=[]
    for name in ['cycle','context','rtthread']:
        if name=='rtthread':image,elf=rt_build(arch,am)
        else:image,elf=compile_app('release-'+name,arch,{'main.c':(ROOT/'B/B1/cycle-test.c').read_text()} if name=='cycle' else context_sources(16),am)
        tag='B4/release-soc/'+name;out=ROOT/'artifacts'/tag;out.mkdir(parents=True,exist_ok=True);report=out/'simulation.json';budget=out/'budget.json'
        run(tag,['python3',ROOT/'B/runtime/budget_exec.py','--kind','simulation','--report',budget,'--',exe,'--flash',image,'--ref',ref,'--report',report,'--max-cycles','1000000000','--progress-cycles','50000000'],inputs=[exe,ref,image,elf],outputs=[report,budget],timeout=900)
        data=json.loads(report.read_text());assert data['result']=='GOOD_TRAP' and data['diff_checked']+data['device_sync_checked']==data['instructions']
        uart=bytes.fromhex(data['uart']['hex']).decode('ascii').replace('\r','')
        if name=='cycle':assert 'B1_MCYCLE_PASS' in uart
        if name=='context':assert data['traps']=={'ecall':52,'mret':52} and 'B1_CTE_PASS' in uart
        if name=='rtthread':
            assert 'C5_RTTHREAD_PASS' in uart and 'C5_CONTEXT_PASS a=12 b=12' in uart
            for command in ['help','date','version','free','ps','pwd','ls','memtrace','memcheck','utest_list','c5_context_test','c5_done']:assert re.search(r'msh\s*/>\s*'+command+r'\s',uart)
        rows.append({'name':name,'status':'PASS','simulation':data,'uart':uart,'image':str(image),'elf':str(elf),'image_sha256':sha(image),'elf_sha256':sha(elf),'evidence':'artifacts/'+tag})
        dump(ROOT/'reports/B4_release_soc.json',{'status':'PASS_COMPLETED_RUNS','variant':'b5-release','executable_sha256':sha(exe),'runs':rows})
    print('B_RELEASE_SOC_PASS')
if __name__=='__main__':main()
