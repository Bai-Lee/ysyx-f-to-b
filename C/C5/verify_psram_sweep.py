from pathlib import Path
import sys,argparse,re,math
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from support import select_build


def main():
    p=argparse.ArgumentParser();p.add_argument('--bytes',type=int,choices=[65536,4194304],default=65536);p.add_argument('--corrupt',action='store_true');a=p.parse_args()
    subprocess.run(['python3',str(ROOT/'C/C5/prepare_am.py')],check=True)
    base=WORK/'c5/workbench';am=base/'abstract-machine';name='psram-sweep-'+str(a.bytes)+('-bad' if a.corrupt else '')
    app=base/name;app.mkdir(exist_ok=True);source=ROOT/'C/C5/programs/mem-sweep.c';shutil.copyfile(source,app/'main.c')
    (app/'Makefile').write_text('NAME = '+name+'\nSRCS = main.c\nCFLAGS += -DMEMTEST_BASE=0x80000000u -DMEMTEST_BYTES='+str(a.bytes)+'u\ninclude $(AM_HOME)/Makefile\n')
    arch='riscv32e-ysyxsoc-sram-code';image=app/'build'/(name+'-'+arch+'.bin');elf=image.with_suffix('.elf');tag='C5/psram-sweep/'+name
    run(tag+'/build',['make','-j1','ARCH='+arch,'mainargs='+('x' if a.corrupt else ''),'insert-arg'],cwd=app,env={'AM_HOME':str(am),'NPC_HOME':str(base/'npc')},inputs=[source,app/'Makefile',*sorted((am/'am/src/riscv/ysyxsoc').glob('*')),am/'scripts/ysyxsoc-code-sram.ld'],outputs=[image,elf],timeout=180)
    nm=Path(shutil.which('riscv64-linux-gnu-nm'));text,_,_=run(tag+'/symbols',[nm,'-n',elf],inputs=[nm,elf]);symbols={v[2]:int(v[0],16) for line in text.splitlines() if len(v:=line.split())==3 and re.fullmatch('[0-9a-fA-F]+',v[0])}
    assert symbols['_start']==0x30000000 and 0x0f000000<=symbols['main']<0x0f001800
    build=select_build('30000000-cycle-psram4m-qpi');exe=Path(build['executable']);ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so'
    report=ROOT/'reports/C5_psram_sweep.json';prior=json.loads(report.read_text()).get('runs',[]) if report.exists() else []
    timeout=600;max_cycles=200000000
    if a.bytes==4194304:
        pilot=next(r for r in prior if r['bytes']==65536 and not r['corrupt']);scale=a.bytes/pilot['bytes']
        timeout=math.ceil(pilot['simulation']['wall_seconds']*scale*1.5+120)
        max_cycles=math.ceil(pilot['simulation']['cycles']*scale*1.15+1000000)
    directory=ROOT/'artifacts'/tag;directory.mkdir(parents=True,exist_ok=True);result=directory/'simulation.json'
    budget=ROOT/'C/runtime/budget_exec.py';resource_report=directory/'resources.json'
    run(tag+'/run',['python3',budget,'--report',resource_report,'--',exe,'--flash',image,'--ref',ref,'--report',result,'--coverage-base','0x80000000','--coverage-size',str(a.bytes),'--max-cycles',str(max_cycles),'--progress-cycles','20000000'],inputs=[exe,image,elf,ref,budget],outputs=[result,resource_report],expected=(1 if a.corrupt else 0,),timeout=timeout+20)
    data=json.loads(result.read_text());assert data['diff_enabled'] and data['diff_checked']+data['device_sync_checked']==data['instructions']
    assert data['retired_by_region'][1]>0 and data['retired_by_region'][3]==0
    if a.corrupt:assert data['result']=='BAD_TRAP' and data['a0']==71
    else:
        assert data['result']=='GOOD_TRAP';coverage=data['coverage']
        assert coverage['unique_read_bytes']==coverage['unique_written_bytes']==a.bytes
        assert coverage['read_ops_by_width']==coverage['write_ops_by_width']==[2*a.bytes,a.bytes,a.bytes]
        assert bytes.fromhex(data['uart']['hex'])==b'B\nb\nH\nh\nW\nw\nQ\nq\n'
        assert data['psram']['maximum_byte_address']==a.bytes-1
    row={'bytes':a.bytes,'corrupt':a.corrupt,'status':'PASS','simulation':data,'symbols':symbols,'image_sha256':sha(image),'elf_sha256':sha(elf),'evidence':'artifacts/'+tag,'timeout_seconds':timeout,'cycle_budget':max_cycles}
    rows=[r for r in prior if (r['bytes'],r['corrupt'])!=(a.bytes,a.corrupt)]+[row]
    dump(report,{'status':'PASS_COMPLETED_SWEEPS','runs':rows,'scope':'Actual CPU executing code/rodata in SRAM after Flash loader; every non-MMIO instruction checked by NEMU. All8/16/32/64-bit address/inverse patterns retained, unique bytes and exact width counts verified.65,536-byte pilot is separate from full4MiB acceptance.'})
    if a.bytes==4194304 and not a.corrupt:mark(['C5-M027'],'PASS',['reports/C5_psram_sweep.json'],'Real SRAM code/rodata, actual entire4MiB PSRAM read/write at every requested width/pattern, exact unique-byte and operation counts with NEMU.')
    print('C5_PSRAM_SWEEP_PASS',a.bytes,a.corrupt,flush=True)


if __name__=='__main__':main()
