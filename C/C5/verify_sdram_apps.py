from pathlib import Path
import sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from support import select_build
from build_app import compile_app


def main():
    p=argparse.ArgumentParser();p.add_argument('--variant',default='30000000-cycle-psram4m-qpi-sdram16x1-opt');args=p.parse_args()
    build=select_build(args.variant);assert build['sdram_width'] in [16,32]
    job=compile_app('microbench','sdram32','test');image=Path(job['image']);elf=Path(job['elf']);exe=Path(build['executable']);ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so'
    tag='C5/sdram-apps/microbench-'+str(build['sdram_width'])+'x'+str(build['sdram_ranks']);folder=ROOT/'artifacts'/tag;result=folder/'simulation.json';budget=folder/'resources.json'
    run(tag+'/run',['python3',ROOT/'C/runtime/budget_exec.py','--report',budget,'--',exe,'--flash',image,'--ref',ref,'--report',result,'--max-cycles','1000000000'],inputs=[exe,ref,image,elf],outputs=[result,budget],timeout=1200)
    data=json.loads(result.read_text());uart=bytes.fromhex(data['uart']['hex']).decode('ascii')
    assert data['result']=='GOOD_TRAP' and data['diff_enabled'] and data['diff_checked']+data['device_sync_checked']==data['instructions']
    assert data['retired_by_region'][4]>1000 and data['retired_by_region'][1]>0 and data['retired_by_region'][2]>0
    assert uart.count(' Passed.')==10 and 'Ignored' not in uart and 'Failed.' not in uart and 'MicroBench PASS' in uart
    row={'variant':args.variant,'width':build['sdram_width'],'ranks':build['sdram_ranks'],'status':'PASS','image_sha256':sha(image),'elf_sha256':sha(elf),'memory_profile':'sdram32','cycles':data['cycles'],'instructions':data['instructions'],'wall_seconds':data['wall_seconds'],'retired_by_region':data['retired_by_region'],'sdram_chips':data['sdram_chips'],'uart':uart,'evidence':'artifacts/'+tag}
    report=ROOT/'reports/C5_sdram_apps.json';rows=json.loads(report.read_text()).get('runs',[]) if report.exists() else []
    rows=[r for r in rows if r['variant']!=args.variant]+[row]
    comparisons=[]
    for extended in [r for r in rows if r['width']==32]:
        baseline=next((r for r in rows if r['width']==16 and r['image_sha256']==extended['image_sha256']),None)
        if baseline:comparisons.append({'baseline':baseline['variant'],'extended':extended['variant'],'same_firmware_sha256':extended['image_sha256'],'baseline_cycles':baseline['cycles'],'extended_cycles':extended['cycles'],'cycle_ratio':extended['cycles']/baseline['cycles'],'scope':'Identical microbench test firmware and32MiB softwareheap limit. Actual model-cycle totals include bootstrap andUART output; walltime is simulator speed, not hardware clock.'})
    dump(report,{'status':'PASS_COMPLETED_PROFILES','runs':rows,'comparisons':comparisons,'scope':'Real FSBL/SSBL loading and execution fromSDRAM, all10 original microbench test programs, full non-MMIO NEMU checking. The same sdram32 ELF is used for width comparison so increased heap does not confound it.'})
    if any(r['width']==32 and r['ranks']==1 for r in rows) and any('sdram32x1' in r['extended'] for r in comparisons):
        mark(['C5-M034'],'PASS',['reports/C5_sdram_apps.json','reports/C5_sdram_controller.json','reports/C5_sdram_sweep.json','C/C5/sdram_wiring.py'],'Actualtwo-chip32-bit controller, byte masks andbothlanes validated; width edits are generated reproducibly. Same-firmware MicroBench cycle comparison recorded.')
    rt_report=ROOT/'reports/C5_rtthread_sdram32.json'
    if rt_report.exists() and any(r['width']==16 for r in rows):
        rt=json.loads(rt_report.read_text());assert rt['status']=='PASS_BOOT_ORIGINAL_COMMANDS_AND_CONTEXTS' and 0xa0000000<=rt['symbols']['main']<0xa2000000
        mark(['C5-M033'],'PASS',['reports/C5_sdram_apps.json','reports/C5_rtthread_sdram32.json'],'MicroBench all10originaltestcases andrealRT-Thread runfromSDRAM afteractualFSBL/SSBL, withfullnon-MMIONEMUchecking; RTshellcommands andthreadcreation/yield/return checks pass.')
    print('C5_SDRAM_MICROBENCH_PASS',args.variant,data['cycles'],flush=True)


if __name__=='__main__':main()
