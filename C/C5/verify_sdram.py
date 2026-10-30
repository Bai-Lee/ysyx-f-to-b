from pathlib import Path
import sys,argparse,re,math
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from support import select_build


def main():
    p=argparse.ArgumentParser();p.add_argument('--width',type=int,choices=[16,32],default=16);p.add_argument('--ranks',type=int,choices=[1,2],default=1)
    p.add_argument('--bytes',type=int,choices=[4096,65536,33554432,67108864,134217728],default=4096);p.add_argument('--corrupt',action='store_true');p.add_argument('--build-only',action='store_true');p.add_argument('--original-loop',action='store_true');p.add_argument('--assembly-loop',action='store_true');args=p.parse_args()
    assert not(args.original_loop and args.assembly_loop)
    capacity=33554432*(args.width//16)*args.ranks;assert args.bytes<=capacity and (args.width==32 or args.ranks==1)
    subprocess.run(['python3',str(ROOT/'C/C5/prepare_am.py')],check=True)
    variant=f'30000000-cycle-psram4m-qpi-sdram{args.width}x{args.ranks}-opt'
    base=WORK/'c5/workbench';am=base/'abstract-machine';name=f'sdram{args.width}x{args.ranks}-{args.bytes}'+('-bad' if args.corrupt else '')+('-original' if args.original_loop else '')+('-asm' if args.assembly_loop else '')
    app=base/name;app.mkdir(exist_ok=True);source=ROOT/'C/C5/programs'/('mem-sweep-asm.c' if args.assembly_loop else 'mem-sweep.c' if args.original_loop else 'mem-sweep-fast.c');shutil.copyfile(source,app/'main.c')
    additional=[]
    if args.assembly_loop:
        assembly=ROOT/'C/C5/programs/mem-sweep-asm.S';shutil.copyfile(assembly,app/'sweep.S');additional=[assembly]
    (app/'Makefile').write_text('NAME = '+name+'\nSRCS = main.c'+(' sweep.S' if args.assembly_loop else '')+'\nCFLAGS += -DMEMTEST_BASE=0xa0000000u -DMEMTEST_BYTES='+str(args.bytes)+'u\ninclude $(AM_HOME)/Makefile\n')
    arch='riscv32e-ysyxsoc-sram-code';image=app/'build'/(name+'-'+arch+'.bin');elf=image.with_suffix('.elf');tag='C5/sdram-sweep/'+name
    run(tag+'/build',['make','-j1','ARCH='+arch,'mainargs='+('x' if args.corrupt else ''),'insert-arg'],cwd=app,env={'AM_HOME':str(am),'NPC_HOME':str(base/'npc')},inputs=[source,*additional,app/'Makefile',*sorted((am/'am/src/riscv/ysyxsoc').glob('*')),am/'scripts/ysyxsoc-code-sram.ld'],outputs=[image,elf],timeout=180)
    nm=Path(shutil.which('riscv64-linux-gnu-nm'));text,_,_=run(tag+'/symbols',[nm,'-n',elf],inputs=[nm,elf]);symbols={v[2]:int(v[0],16) for line in text.splitlines() if len(v:=line.split())==3 and re.fullmatch('[0-9a-fA-F]+',v[0])}
    assert symbols['_start']==0x30000000 and 0x0f000000<=symbols['main']<0x0f001800
    if args.build_only:print('C5_SDRAM_IMAGE_BUILT',name,flush=True);return
    exe=Path(select_build(variant)['executable']);ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so'
    report=ROOT/'reports/C5_sdram_sweep.json';prior=json.loads(report.read_text()).get('runs',[]) if report.exists() else []
    timeout=300;max_cycles=200000000
    if args.bytes>65536:
        pilot=next(r for r in prior if r['width']==args.width and r['ranks']==args.ranks and r['bytes']==65536 and not r['corrupt'] and r['original_loop']==args.original_loop and r.get('assembly_loop',False)==args.assembly_loop)
        scale=args.bytes/pilot['bytes'];timeout=math.ceil(pilot['wall_seconds']*scale*1.6+180);max_cycles=math.ceil(pilot['cycles']*scale*1.1+1000000)
    directory=ROOT/'artifacts'/tag;result=directory/'simulation.json';resources=directory/'resources.json'
    run(tag+'/run',['python3',ROOT/'C/runtime/budget_exec.py','--report',resources,'--',exe,'--flash',image,'--ref',ref,'--report',result,'--coverage-base','0xa0000000','--coverage-size',str(args.bytes),'--max-cycles',str(max_cycles),'--progress-cycles','50000000'],inputs=[exe,image,elf,ref],outputs=[result,resources],expected=(1 if args.corrupt else 0,),timeout=timeout)
    data=json.loads(result.read_text());assert data['diff_enabled'] and data['diff_checked']+data['device_sync_checked']==data['instructions']
    assert data['retired_by_region'][1]>0 and data['retired_by_region'][4]==0
    if args.corrupt:assert data['result']=='BAD_TRAP' and data['a0']==71
    else:
        assert data['result']=='GOOD_TRAP';coverage=data['coverage'];assert coverage['unique_read_bytes']==coverage['unique_written_bytes']==args.bytes
        assert coverage['read_ops_by_width']==coverage['write_ops_by_width']==[2*args.bytes,args.bytes,args.bytes]
        assert bytes.fromhex(data['uart']['hex'])==b'B\nb\nH\nh\nW\nw\nQ\nq\n'
        if args.bytes==capacity:
            active=(range(1) if args.width==16 else range(args.ranks*2))
            for chip in active:assert data['sdram_chips'][chip]['maximum_byte_address']==33554431 and data['sdram_chips'][chip]['read_bytes']>0 and data['sdram_chips'][chip]['write_bytes']>0
    row={'width':args.width,'ranks':args.ranks,'bytes':args.bytes,'corrupt':args.corrupt,'original_loop':args.original_loop,'status':'PASS','cycles':data['cycles'],'instructions':data['instructions'],'wall_seconds':data['wall_seconds'],'diff_checked':data['diff_checked'],'device_sync_checked':data['device_sync_checked'],'coverage':data['coverage'],'chips':data['sdram_chips'],'symbols':symbols,'image_sha256':sha(image),'elf_sha256':sha(elf),'evidence':'artifacts/'+tag,'timeout_seconds':timeout,'cycle_budget':max_cycles,'variant':variant}
    row['assembly_loop']=args.assembly_loop
    identity=lambda r:(r['width'],r['ranks'],r['bytes'],r['corrupt'],r['original_loop'],r.get('assembly_loop',False));rows=[r for r in prior if identity(r)!=identity(row)]+[row]
    dump(report,{'status':'PASS_COMPLETED_SWEEPS','runs':rows,'scope':'Actual CPU executing SRAM code/rodata after Flash loader. Full NEMU instruction checking and actual pin-level SDRAM; exact8/16/32/64-bit address/inverse counts. OriginalC, four-accessC andeight-accessassembly loops are explicitly labeled; unrolling changes only firmware bookkeeping. Small pilots are distinct from required full32MiB/128MiB sweeps.'})
    if not args.corrupt:
        if args.width==16 and args.bytes==4096:mark(['C5-M031'],'PASS',['reports/C5_sdram_model.json','reports/C5_sdram_controller.json','reports/C5_sdram_sweep.json'],'Original16-bit controller and model pass4KiB actualCPU allwidth/address/inverse tests with NEMU; independent four-state CL/burst/mask controls.')
        if args.width==16 and args.bytes==33554432:mark(['C5-M032'],'PASS',['reports/C5_sdram_sweep.json'],'Entire32MiB actualSDRAM chip read/write, allrequested widths/patterns, unique-byte and operation counts checked, actualhighestchipaddress observed.')
        if args.width==32 and args.ranks==2 and args.bytes==134217728:mark(['C5-M035'],'PASS',['reports/C5_sdram_sweep.json','reports/C5_sdram_controller.json'],'Entire128MiB across4distinctx16 chips, bothranks andbothlanes. Allwidths/patterns, exactCPUcoverage andall4highestchipaddresses, plusmask/rankmutants.')
    print('C5_SDRAM_SWEEP_PASS',name,flush=True)


if __name__=='__main__':main()
