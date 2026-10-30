from pathlib import Path
import sys,re,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'B1'))
from common import *
from verify import compile_app

def main():
    p=argparse.ArgumentParser();p.add_argument('--variant',default='b3-cache128-axi-burst');a=p.parse_args()
    am=WORK/'soc/workbench/abstract-machine'
    for name,target in [('start.S',am/'am/src/riscv/ysyxsoc/start.S'),('ysyxsoc.mk',am/'scripts/platform/ysyxsoc.mk')]:shutil.copyfile(ROOT/'B/soc/am'/name,target)
    build=next(r for r in json.loads((ROOT/'reports/B_soc_soc_build.json').read_text())['variants'] if r['variant']==a.variant);exe=Path(build['executable']);assert sha(exe)==build['sha256'];ref=WORK/'nemu-ref/build/riscv32-nemu-interpreter-so';rows=[]
    for fence in [False,True]:
        name='loader-warm-'+('fence' if fence else 'no-fence');arch='riscv32e-ysyxsoc-sdram128-'+name
        (am/'scripts'/(arch+'.mk')).write_text(f'SOC_BOOT_WARM := 1\nSOC_BOOT_FENCE := {int(fence)}\ninclude $(AM_HOME)/scripts/riscv32e-ysyxsoc-sdram128.mk\n')
        image,elf=compile_app(name,arch,{'main.c':'#include <am.h>\n#include <klib.h>\nint main(const char*a){(void)a;printf("B_LOADER_FENCE_PASS\\n");return 0;}\n'},am)
        text,_,_=run('B3/loader/'+name+'/symbols',['riscv64-linux-gnu-nm','-n',elf],inputs=[elf]);entry=int(next(line.split()[0] for line in text.splitlines() if line.endswith(' _trm_init')),16)
        tag='B3/loader/'+a.variant+'-'+name;out=ROOT/'artifacts'/tag;out.mkdir(parents=True,exist_ok=True);result=out/'simulation.json';budget=out/'budget.json';trace=out/'events.log'
        stdout,stderr,_=run(tag,['python3',ROOT/'B/runtime/budget_exec.py','--report',budget,'--',exe,'--flash',image,'--ref',ref,'--report',result,'--trace',trace,'--trace-limit','2000000','--max-cycles','100000000'],inputs=[exe,ref,image,elf],outputs=[result,budget,trace],expected=(0 if fence else 1,),timeout=180)
        data=json.loads(result.read_text());uart=bytes.fromhex(data['uart']['hex']).decode('ascii')
        if fence:assert data['result']=='GOOD_TRAP' and uart=='B_LOADER_FENCE_PASS\n'
        else:
            assert data['result']=='DIFF_FAIL'
            match=re.search(r'DIFF_INSTRUCTION pc=([0-9a-f]+) dut=00000013 ref=([0-9a-f]+)',stderr)
            assert match and int(match[1],16)==entry and int(match[2],16)!=0x13,stderr
        rows.append({'fence':fence,'status':'PASS','entry':entry,'simulation':data,'uart':uart,'evidence':'artifacts/'+tag})
    dump(ROOT/'reports/B3_loader_fence.json',{'status':'PASS','variant':a.variant,'runs':rows,'scope':'Real two-stage Flash->SRAM bootstrap first writes/executes32B NOP/RET at the final SDRAM entry, then copies the actual program over it. The unfenced run retains the stale NOP in ICache; exact instruction bytes differ from newly stored RAM at the ELF entry, not a timeout. FENCE.I after final stores invalidates it and main completes. Missing-fence behavior is a program coherence error, not a claim that RISC-V requires immediate coherence.'})
    print('B3_LOADER_FENCE_PASS')

if __name__=='__main__':main()
