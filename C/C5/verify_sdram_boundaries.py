from pathlib import Path
import sys,argparse,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from support import select_build
p=argparse.ArgumentParser();p.add_argument('--width',type=int,choices=[16,32],default=32);p.add_argument('--ranks',type=int,choices=[1,2],default=2);p.add_argument('--corrupt',action='store_true');args=p.parse_args()
capacity=33554432*(args.width//16)*args.ranks;variant=f'30000000-cycle-psram4m-qpi-sdram{args.width}x{args.ranks}-opt';exe=Path(select_build(variant)['executable']);ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so'
base=WORK/'c5/workbench';am=base/'abstract-machine';name=f'boundaries-{args.width}x{args.ranks}'+('-bad' if args.corrupt else '');app=base/name;app.mkdir(exist_ok=True)
source=ROOT/'C/C5/programs/memory-boundaries.c';shutil.copyfile(source,app/'main.c');(app/'Makefile').write_text('NAME = '+name+'\nSRCS = main.c\nCFLAGS += -DMEMORY_CAPACITY='+str(capacity)+'u\ninclude $(AM_HOME)/Makefile\n')
arch='riscv32e-ysyxsoc-sram-code';image=app/'build'/(name+'-'+arch+'.bin');elf=image.with_suffix('.elf');tag='C5/sdram-boundaries/'+name
run(tag+'/build',['make','-j1','ARCH='+arch,'mainargs='+('x' if args.corrupt else ''),'insert-arg'],cwd=app,env={'AM_HOME':str(am)},inputs=[source,app/'Makefile',am/'scripts/ysyxsoc-code-sram.ld'],outputs=[image,elf],timeout=180)
folder=ROOT/'artifacts'/tag;result=folder/'simulation.json';budget=folder/'resources.json'
run(tag+'/run',['python3',ROOT/'C/runtime/budget_exec.py','--report',budget,'--',exe,'--flash',image,'--ref',ref,'--report',result,'--coverage-base','0xa0000000','--coverage-size',str(capacity),'--max-cycles','100000000'],inputs=[exe,ref,image,elf],outputs=[result,budget],expected=(1 if args.corrupt else 0,),timeout=120)
data=json.loads(result.read_text());uart=bytes.fromhex(data['uart']['hex']).decode('ascii');assert data['diff_enabled'] and data['diff_checked']+data['device_sync_checked']==data['instructions']
if args.corrupt:assert data['result']=='BAD_TRAP' and data['a0']==86
else:
    points={0,capacity-4,capacity//2-4,capacity//2,capacity//2+4}
    for bit in range(2,capacity.bit_length()-1):points.update([(1<<bit)-4,1<<bit,(1<<bit)+4])
    points={offset for offset in points if 0<=offset<capacity and not(offset&3)};number=len(points)
    assert f'C5_MEMORY_BOUNDARIES_PASS points={number} bytes={capacity}' in uart
    assert data['coverage']['unique_read_bytes']==data['coverage']['unique_written_bytes']==4*number
    assert data['coverage']['read_ops_by_width']==[0,0,2*number] and data['coverage']['write_ops_by_width']==[number,number,number]
    for chip in range(args.ranks*(args.width//16)):assert data['sdram_chips'][chip]['maximum_byte_address']==33554431 and data['sdram_chips'][chip]['read_bytes']>0 and data['sdram_chips'][chip]['write_bytes']>0
row={'status':'PASS','width':args.width,'ranks':args.ranks,'corrupt':args.corrupt,'capacity':capacity,'uart':uart,'coverage':data['coverage'],'chips':data['sdram_chips'],'cycles':data['cycles'],'instructions':data['instructions'],'image_sha256':sha(image),'evidence':'artifacts/'+tag}
report=ROOT/'reports/C5_sdram_boundaries.json';rows=json.loads(report.read_text()).get('runs',[]) if report.exists() else []
rows=[r for r in rows if (r['width'],r['ranks'],r['corrupt'])!=(args.width,args.ranks,args.corrupt)]+[row]
dump(report,{'status':'PASS_COMPLETED_BOUNDARY_PROFILES','runs':rows,'scope':'ActualfullSoCCPU probes alladdressbitboundaries andphysicalhighestaddresses, upperrank andbothlanes, afterwritingdistinctvalues before reverse-orderreadback; byte/halfwordmasks. Lastphysicalwordcorruption rejected. These probes do not replace requiredfull32/128MiB sweeps.'})
print('C5_SDRAM_BOUNDARIES_PASS',args.width,args.ranks,args.corrupt,flush=True)
