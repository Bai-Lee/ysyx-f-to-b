from pathlib import Path
import sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from support import select_build


def main():
    p=argparse.ArgumentParser();p.add_argument('--corrupt',action='store_true');p.add_argument('--build-only',action='store_true');args=p.parse_args()
    base=WORK/'c5/workbench';am=base/'abstract-machine';app=base/'chiplink-test';app.mkdir(exist_ok=True)
    source=[ROOT/'C/C5/programs/mem-sweep-asm.c',ROOT/'C/C5/programs/mem-sweep-asm.S']
    shutil.copyfile(source[0],app/'main.c');shutil.copyfile(source[1],app/'sweep.S')
    (app/'Makefile').write_text('NAME = chiplink-test\nSRCS = main.c sweep.S\nCFLAGS += -DMEMTEST_BASE=0xc0000000u -DMEMTEST_BYTES=4096u\ninclude $(AM_HOME)/Makefile\n')
    arch='riscv32e-ysyxsoc-sram-code';image=app/'build'/('chiplink-test-'+arch+'.bin');elf=image.with_suffix('.elf')
    run('C5/chiplink/firmware',['make','-j1','ARCH='+arch,'insert-arg'],cwd=app,env={'AM_HOME':str(am)},inputs=[*source,app/'Makefile',am/'scripts/ysyxsoc-code-sram.ld'],outputs=[image,elf],timeout=180)
    if args.build_only:print('C5_CHIPLINK_FIRMWARE_BUILT',flush=True);return
    variant='30000000-cycle-psram4m-qpi-sdram16x1-opt-chiplink'+('-bad-read' if args.corrupt else '')
    exe=Path(select_build(variant)['executable']);ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so';name='bad-read' if args.corrupt else 'positive';tag='C5/chiplink/'+name
    folder=ROOT/'artifacts'/tag;result=folder/'simulation.json';budget=folder/'resources.json'
    stdout,stderr,run_record=run(tag+'/run',['python3',ROOT/'C/runtime/budget_exec.py','--report',budget,'--',exe,'--flash',image,'--ref',ref,'--report',result,'--coverage-base','0xc0000000','--coverage-size','4096','--max-cycles','200000000','--progress-cycles','10000000'],inputs=[exe,ref,image,elf],outputs=[result,budget],expected=(1 if args.corrupt else 0,),timeout=900)
    data=json.loads(result.read_text());link=data['chiplink'];assert data['reset_cycles']>=10 and data['diff_enabled']
    assert min(link['words'])>0 and link['remote_write_requests']>0 and link['remote_read_requests']>0
    if args.corrupt:
        assert data['result']=='DIFF_FAIL' and 'DIFF_MEMORY' in stderr
    else:
        assert data['result']=='GOOD_TRAP' and data['diff_checked']+data['device_sync_checked']==data['instructions']
        assert data['coverage']['unique_read_bytes']==data['coverage']['unique_written_bytes']==4096
        assert data['coverage']['read_ops_by_width']==data['coverage']['write_ops_by_width']==[8192,4096,4096]
        assert bytes.fromhex(data['uart']['hex'])==b'B\nb\nH\nh\nW\nw\nQ\nq\n'
        assert link['remote_unique_read_bytes']==link['remote_unique_written_bytes']==4096 and link['maximum_remote_byte_address']==0xc0000fff
        assert link['remote_written_bytes']==32768
        assert data['retired_by_region'][1]>0 and data['retired_by_region'][5]==0
    row={'status':'PASS','name':name,'variant':variant,'result':data['result'],'cycles':data['cycles'],'instructions':data['instructions'],'wall_seconds':data['wall_seconds'],'cpu_coverage':data['coverage'],'link':link,'reset_cycles':data['reset_cycles'],'image_sha256':sha(image),'executable_sha256':sha(exe),'evidence':'artifacts/'+tag,'resources':json.loads(budget.read_text())}
    report=ROOT/'reports/C5_chiplink.json';rows=json.loads(report.read_text()).get('runs',[]) if report.exists() else []
    rows=[r for r in rows if r['name']!=name]+[row]
    complete={r['name'] for r in rows}=={'positive','bad-read'}
    dump(report,{'status':'PASS_PIN_LINK_REMOTE_RAM_AND_NEGATIVE' if complete else 'PASS_COMPLETED_PROFILES','runs':rows,'scope':'Actual175-moduleupstreamChipLinkelaboration, ASICandFPGA transmitpins observedbothdirections, original1GiBremoteRTLMemory retained. CPUtests4KiB withallrequestedwidths/patterns; remoteRAMunique-byte/maskedwritecoverage agrees. Readbitfault occurs inthefarRAMandisdetectedafterthereturnlink byNEMU.16externalresetcycles; sameidealclocks, nooffchip electrical/CDCsignoff. 1GiB is modeledcapacity, not a1GiBexhaustivetest.'})
    if complete:mark(['C5-M047'],'PASS',['reports/C5_chiplink.json','reports/C5_chiplink_generation.json'],'RealupstreamChipLink enabledandgenerated, bidirectionalpinwords andfar-endRAMactivity observed; all4KiBwidth/patternchecks plusfarRAMread-bitmutation detected. Reset16cycles.')
    print('C5_CHIPLINK_PASS',name,flush=True)


if __name__=='__main__':main()
