"""Run full-address-range memory patterns concurrently under one PSS guard.

Each pattern resets independently, writes the entire range, then reads it back.
Address ranges are never divided between separate hardware instances. Completed
cases are independently recorded and can be resumed after an interrupted batch.
"""
from pathlib import Path
import argparse,concurrent.futures,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from resource_policy import POLICY_PATH,windows_available_bytes,linux_memory
from support import select_build

VARIANT='30000000-cycle-psram4m-qpi-sdram32x2-opt'
FULL=134217728


def profile():
    return json.loads(POLICY_PATH.read_text())['limits']['C_parallel_validation']


def build_images(size,corrupt=False):
    base=WORK/'c5/workbench';am=base/'abstract-machine';source=ROOT/'C/C5/programs/mem-sweep-phase.c';assembly=ROOT/'C/C5/programs/mem-sweep-asm.S'
    report=ROOT/'reports/C5_parallel_sdram_builds.json';saved=json.loads(report.read_text()).get('builds',[]) if report.exists() else []
    result=[]
    for phase in range(8):
        name=f'sdram-phase-{size}-{phase}'+('-bad' if corrupt else '');app=base/name;app.mkdir(exist_ok=True)
        shutil.copyfile(source,app/'main.c');shutil.copyfile(assembly,app/'sweep.S')
        (app/'Makefile').write_text(f'NAME = {name}\nSRCS = main.c sweep.S\nCFLAGS += -DMEMTEST_BYTES={size}u -DMEMTEST_PHASE={phase}\ninclude $(AM_HOME)/Makefile\n')
        arch='riscv32e-ysyxsoc-sram-code';image=app/'build'/f'{name}-{arch}.bin';elf=image.with_suffix('.elf')
        inputs=[source,assembly,app/'Makefile',*sorted((am/'am/src/riscv/ysyxsoc').glob('*')),am/'scripts/ysyxsoc-code-sram.ld']
        jobs=profile()['compile_jobs']
        run('C5/parallel-sdram/build/'+name,['make',f'-j{jobs}','ARCH='+arch,'mainargs='+('x' if corrupt else ''),'insert-arg'],
            cwd=app,env={'AM_HOME':str(am),'NPC_HOME':str(base/'npc'),'MAKEFLAGS':f'-j{jobs}'},inputs=inputs,outputs=[image,elf],timeout=180,resume=True)
        row={'phase':phase,'bytes':size,'corrupt':corrupt,'image':str(image),'elf':str(elf),'image_sha256':sha(image),'elf_sha256':sha(elf)}
        saved=[r for r in saved if (r['phase'],r['bytes'],r['corrupt'])!=(phase,size,corrupt)]+[row]
        dump(report,{'status':'BUILT_NOT_ACCEPTED','assembly_sha256':sha(assembly),'driver_sha256':sha(source),'builds':saved});result.append(row)
    return result


def validate(data,size,phase,corrupt):
    assert data['diff_enabled'] and data['diff_checked']+data['device_sync_checked']==data['instructions']
    assert data['retired_by_region'][1]>0 and data['retired_by_region'][4]==0
    if corrupt:
        assert data['result']=='BAD_TRAP' and data['a0']==71
        return
    assert data['result']=='GOOD_TRAP'
    coverage=data['coverage'];assert coverage['size']==size and coverage['base']==0xa0000000
    assert coverage['unique_read_bytes']==coverage['unique_written_bytes']==size
    width=[8,16,32,64][phase//2];operations=[0,0,0];operations[min(phase//2,2)]=size//(width//8) * (2 if width==64 else 1)
    assert coverage['read_ops_by_width']==coverage['write_ops_by_width']==operations
    expected_tag=ord('BHWQ'[phase//2])+(32 if phase%2 else 0)
    assert bytes.fromhex(data['uart']['hex'])==bytes([expected_tag,10])
    read_bytes=size*(4 if width==8 else 2 if width==16 else 1)
    assert sum(r['read_bytes'] for r in data['sdram_chips'])==read_bytes
    assert sum(r['write_bytes'] for r in data['sdram_chips'])==size
    for rank in range(2):
        covered=max(0,min(size-rank*67108864,67108864))
        for lane in range(2):
            chip=data['sdram_chips'][rank*2+lane]
            assert chip['write_bytes']==covered//2
            assert chip['read_bytes']==covered//2*(4 if width==8 else 2 if width==16 else 1)
            if size==FULL:assert chip['maximum_byte_address']==33554431


def run_case(job,folder,exe,ref,timeout):
    phase=job['phase'];case=folder/f'phase-{phase}';case.mkdir(parents=True,exist_ok=True);result=case/'simulation.json'
    inputs=[exe,ref,Path(job['image']),Path(job['elf'])];before=[{'path':str(p),'sha256':sha(p)} for p in inputs]
    assert before[2]['sha256']==job['image_sha256'] and before[3]['sha256']==job['elf_sha256']
    command=[str(exe),'--flash',job['image'],'--ref',str(ref),'--report',str(result),'--coverage-base','0xa0000000','--coverage-size',str(job['bytes']),
             '--max-cycles',str(8000000000 if job['bytes']==FULL else 100000000),'--progress-cycles','50000000']
    record_path=case/'run.json'
    if record_path.exists():
        record=json.loads(record_path.read_text())
        if record['status']=='PASS' and record['command']==command and record['inputs']==before and record['inputs_after']==before and result.exists():
            assert sha(result)==record['outputs'][0]['sha256']
            assert sha(case/'stdout.log')==record['stdout_sha256'] and sha(case/'stderr.log')==record['stderr_sha256']
            data=json.loads(result.read_text());validate(data,job['bytes'],phase,job['corrupt'])
            return {'phase':phase,'status':'PASS','resumed':True,'simulation':data,'evidence':case.relative_to(ROOT).as_posix(),'run_sha256':sha(record_path)}
    if record_path.exists() or (case/'started.json').exists():
        history=case/'attempts'/str(time.time_ns());history.mkdir(parents=True)
        for name in ['run.json','started.json','stdout.log','stderr.log','simulation.json','output_snapshot.zip']:
            if (case/name).exists():shutil.copyfile(case/name,history/name)
        if not record_path.exists():dump(history/'incomplete.json',{'status':'UNKNOWN','reason':'Interrupted phase has no completion record; rerun required.'})
    start=time.monotonic();started={'status':'STARTED_NOT_A_COMPLETION','command':command,'cwd':str(WORK),'inputs':before,
        'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'process_group':os.getpgrp(),'guard':'The outer batch PSS guard includes this inherited process group.'}
    dump(case/'started.json',started)
    with (case/'stdout.log').open('wb') as out,(case/'stderr.log').open('wb') as err:
        process=subprocess.Popen(command,cwd=WORK,stdin=subprocess.DEVNULL,stdout=out,stderr=err) # inherit guarded PGID
        started['pid']=process.pid;dump(case/'started.json',started)
        try:rc=process.wait(timeout=timeout);status='PASS' if rc==(1 if job['corrupt'] else 0) else 'FAIL'
        except subprocess.TimeoutExpired:
            process.terminate()
            try:process.wait(timeout=5)
            except subprocess.TimeoutExpired:process.kill();process.wait()
            rc=None;status='TIMEOUT'
    error=None;data=json.loads(result.read_text()) if result.exists() else None
    if status=='PASS':
        try:validate(data,job['bytes'],phase,job['corrupt'])
        except Exception as exc:status='FAIL';error=repr(exc)
    outputs=[{'path':str(result),'sha256':sha(result)}] if result.exists() else []
    record={'status':status,'command':command,'cwd':str(WORK),'exit_code':rc,'expected_exit':[1 if job['corrupt'] else 0],
        'elapsed_seconds':time.monotonic()-start,'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'inputs':before,'inputs_after':[{'path':str(p),'sha256':sha(p)} for p in inputs],'outputs':outputs,
        'stdout_sha256':sha(case/'stdout.log'),'stderr_sha256':sha(case/'stderr.log'),'semantic_error':error,'resource_guard':'../resources.json; all batch workers inherit one monitored process group'}
    assert record['inputs_after']==before
    if result.exists():
        with zipfile.ZipFile(case/'output_snapshot.zip','w',zipfile.ZIP_DEFLATED) as archive:archive.write(result,'000_simulation.json')
    dump(record_path,record);print('SDRAM_PHASE',phase,status,rc,flush=True);assert status=='PASS',(phase,error)
    return {'phase':phase,'status':'PASS','resumed':False,'simulation':data,'evidence':case.relative_to(ROOT).as_posix(),'run_sha256':sha(record_path)}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--bytes',type=int,choices=[4096,65536,FULL],default=65536)
    parser.add_argument('--jobs',type=int,default=1);parser.add_argument('--corrupt',action='store_true');parser.add_argument('--label',required=True)
    parser.add_argument('--build-only',action='store_true');parser.add_argument('--worker',action='store_true');args=parser.parse_args()
    assert __import__('re').fullmatch('[a-z0-9-]+',args.label) and 1<=args.jobs<=profile()['max_simulators']
    folder=ROOT/'artifacts/C5/parallel-sdram'/args.label;folder.mkdir(parents=True,exist_ok=True)
    if not args.worker:
        jobs=build_images(args.bytes,args.corrupt)
        if args.build_only:return
        exe=Path(select_build(VARIANT)['executable']);ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so'
        inputs=[Path(__file__),ROOT/'C/C5/programs/mem-sweep-phase.c',ROOT/'C/C5/programs/mem-sweep-asm.S',exe,ref,POLICY_PATH]
        inputs += [Path(row[key]) for row in jobs for key in ['image','elf']]
        command=['python3',Path(__file__),'--worker','--bytes',str(args.bytes),'--jobs',str(args.jobs),'--label',args.label]+(['--corrupt'] if args.corrupt else [])
        timeout=30000 if args.bytes==FULL else 240
        run('C5/parallel-sdram/'+args.label+'/driver',['python3',ROOT/'C/runtime/budget_exec.py','--report',folder/'resources.json','--',*command],
            inputs=inputs,outputs=[folder/'summary.json',folder/'resources.json'],timeout=timeout)
        print('C5_PARALLEL_SDRAM_BATCH_PASS',args.label,flush=True);return
    job_rows=json.loads((ROOT/'reports/C5_parallel_sdram_builds.json').read_text())['builds']
    jobs=[r for r in job_rows if r['bytes']==args.bytes and r['corrupt']==args.corrupt];assert {r['phase'] for r in jobs}==set(range(8)) and len(jobs)==8
    limits=profile();host=windows_available_bytes();linux=linux_memory();estimate=limits['estimated_worker_MiB']*1024**2
    affordable=min(int((host-limits['windows_reserve_MiB']*1024**2)//estimate),int((linux['MemAvailable']-512*1024**2)//estimate))
    count=min(args.jobs,affordable);assert count>=1,'No safe simulation slot fits current memory'
    exe=Path(select_build(VARIANT)['executable']);ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so';start=time.monotonic()
    # Long byte patterns start first. Other patterns fill the remaining slots.
    jobs.sort(key=lambda row:row['phase']);rows=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=count) as pool:
        pending=[pool.submit(run_case,job,folder,exe,ref,14000 if args.bytes==FULL else 180) for job in jobs]
        for future in concurrent.futures.as_completed(pending):rows.append(future.result())
    rows.sort(key=lambda row:row['phase'])
    report={'status':'PASS','bytes_per_pattern':args.bytes,'corrupt':args.corrupt,'requested_jobs':args.jobs,'actual_jobs':count,'elapsed_seconds':time.monotonic()-start,
        'process_group':os.getpgrp(),'executable':str(exe),'executable_sha256':sha(exe),'reference_sha256':sha(ref),
        'assembly_sha256':sha(ROOT/'C/C5/programs/mem-sweep-asm.S'),'pattern_driver_sha256':sha(ROOT/'C/C5/programs/mem-sweep-phase.c'),'runs':rows,
        'scope':'Eight independent reset runs, each covering the entire specified address range. Exact accepted assembly bodies, full non-MMIO NEMU checking, original widths/address/inverse patterns. No partitioning of addresses between models. Not a claim of one uninterrupted eight-pattern controller-state sequence.'}
    dump(folder/'summary.json',report)
    print('BATCH_COMPLETE',args.label,round(report['elapsed_seconds'],3),'seconds',count,'workers',flush=True)


if __name__=='__main__':main()
