"""Independent retained-output checks for full-range parallel SDRAM phases."""
from pathlib import Path
import json,hashlib,zipfile
from verify_E_delivery import require,load,check_file,sha,digest,safe_member
ROOT=Path(__file__).resolve().parents[1]


def validate_batch(path,size,negative=False):
    data=load(path);require(data['status']=='PASS' and data['bytes_per_pattern']==size and data['corrupt']==negative,'Batch scope mismatch')
    build=next(r for r in load(ROOT/'reports/C5_soc_build.json')['variants'] if r['executable']==data['executable'])
    require(build['sha256']==data['executable_sha256'] and load(ROOT/'reports/C5_reference_build.json')['sha256']==data['reference_sha256'],'Pattern simulator/reference build binding')
    require(sha(ROOT/'C/C5/programs/mem-sweep-asm.S')==data['assembly_sha256'] and sha(ROOT/'C/C5/programs/mem-sweep-phase.c')==data['pattern_driver_sha256'],'Pattern source changed after acceptance')
    firmwares={r['phase']:r for r in load(ROOT/'reports/C5_parallel_sdram_builds.json')['builds'] if r['bytes']==size and r['corrupt']==negative}
    rows=data['runs'];require(len(rows)==8 and {r['phase'] for r in rows}==set(range(8)),'Missing/duplicate memory pattern')
    for row in rows:
        folder=ROOT/row['evidence'];check_file(folder/'run.json',row['run_sha256']);record=load(folder/'run.json')
        require(record['status']=='PASS' and record['exit_code']==int(negative),'Memory pattern execution failed')
        inputs=record['inputs'];firmware=firmwares[row['phase']]
        require(inputs==record['inputs_after'] and inputs[0]['sha256']==data['executable_sha256'] and inputs[1]['sha256']==data['reference_sha256'],'Pattern execution input drift')
        require(inputs[2]['sha256']==firmware['image_sha256'] and inputs[3]['sha256']==firmware['elf_sha256'],'Pattern firmware input drift')
        check_file(folder/'simulation.json',record['outputs'][0]['sha256']);sim=load(folder/'simulation.json')
        require(sim==row['simulation'],'Pattern summary/raw mismatch')
        require(sim['diff_enabled'] and sim['diff_checked']+sim['device_sync_checked']==sim['instructions'],'Pattern instruction comparison missing')
        if negative:
            require(sim['result']=='BAD_TRAP' and sim['a0']==71,'Corruption not rejected by the intended check');continue
        require(sim['result']=='GOOD_TRAP','Pattern did not finish')
        cov=sim['coverage'];require(cov['base']==0xa0000000 and cov['size']==size and cov['unique_read_bytes']==cov['unique_written_bytes']==size,'Each pattern must cover the entire range')
        phase=row['phase'];width=[8,16,32,64][phase//2];expected=[0,0,0];expected[min(phase//2,2)]=size//min(width//8,4)
        require(cov['read_ops_by_width']==cov['write_ops_by_width']==expected,'Per-pattern width coverage')
        require(bytes.fromhex(sim['uart']['hex'])==bytes([ord('BHWQ'[phase//2])+(32 if phase%2 else 0),10]),'Pattern completion marker')
        multiplier=4//min(width//8,4)
        for rank in range(2):
            capacity=max(0,min(size-rank*67108864,67108864))//2
            for lane in range(2):
                chip=sim['sdram_chips'][rank*2+lane]
                require(chip['write_bytes']==capacity and chip['read_bytes']==capacity*multiplier,'Per-chip physical payload')
                if size==134217728:require(chip['maximum_byte_address']==33554431,'A full chip was not reached')
    return data


def pilot_checks():
    base=ROOT/'artifacts/C5/parallel-sdram';good=validate_batch(base/'controls-good/summary.json',4096)
    bad=validate_batch(base/'controls-bad/summary.json',4096,True)
    serial=validate_batch(base/'pilot-serial/summary.json',65536);parallel=validate_batch(base/'pilot-parallel/summary.json',65536)
    fields=['result','exit_code','cycles','instructions','coverage','gpr','sdram_chips','uart','diff_checked','device_sync_checked']
    for a,b in zip(serial['runs'],parallel['runs']):
        require(a['phase']==b['phase'] and all(a['simulation'].get(k)==b['simulation'].get(k) for k in fields),'Parallel scheduling changed deterministic outputs')
    original=next(r for r in load(ROOT/'reports/C5_sdram_sweep.json')['runs'] if r['bytes']==65536 and r['width']==32 and r['ranks']==2 and r.get('assembly_loop') and not r['corrupt'])
    for field in ['read_ops_by_width','write_ops_by_width']:
        summed=[sum(r['simulation']['coverage'][field][i] for r in parallel['runs']) for i in range(3)]
        require(summed==original['coverage'][field],'Parallel plan weakened original aggregate coverage')
    for chip in range(4):
        for field in ['read_bytes','write_bytes']:
            require(sum(r['simulation']['sdram_chips'][chip][field] for r in parallel['runs'])==original['chips'][chip][field],'Original pin payload changed')
    build=load(ROOT/original['evidence']/'build/run.json');assembly=ROOT/'C/C5/programs/mem-sweep-asm.S'
    require(any(r['path'].endswith('/mem-sweep-asm.S') and r['sha256']==sha(assembly) for r in build['inputs']),'Original assembly body not reused')
    guard=load(ROOT/'reports/C_parallel_resource_controls.json');require(guard['status']=='PASS' and len(guard['controls'])==2,'Aggregate resource controls missing')
    resources=load(base/'pilot-parallel/resources.json');require(resources['status']=='PASS','Pilot resource guard failed')
    return {'status':'PASS_FUNCTION_AND_THROUGHPUT','serial_seconds':serial['elapsed_seconds'],'parallel_seconds':parallel['elapsed_seconds'],
        'speedup':serial['elapsed_seconds']/parallel['elapsed_seconds'],'actual_workers':parallel['actual_jobs'],'peak_group_pss_bytes':resources['peak_group_pss_bytes'],
        'compared_fields':fields,'assembly_sha256':sha(assembly),'checks':{name:sha(base/name/'summary.json') for name in ['controls-good','controls-bad','pilot-serial','pilot-parallel']},
        'resource_controls_sha256':sha(ROOT/'reports/C_parallel_resource_controls.json'),
        'scope':'Same eight full-range pattern firmwares run serially and concurrently. Equal deterministic results and original serial assembly payload counts. Each pattern resets independently; this is not an uninterrupted eight-pattern state sequence. Small pilot speedup is measured, not a promise of identical full-run speedup.'}


def full_checks():
    pilot=load(ROOT/'reports/C5_parallel_sdram_pilot.json');require(pilot==pilot_checks(),'Pilot evidence drift')
    base=ROOT/'artifacts/C5/parallel-sdram/full128';data=validate_batch(base/'summary.json',134217728)
    resources=load(base/'resources.json');require(resources['status']=='PASS','Full parallel group exceeded resources')
    driver=load(base/'driver/run.json');require(driver['status']=='PASS' and driver['exit_code']==0,'Full parallel coordinator did not complete')
    for output in driver['outputs']:
        path=base/Path(output['path']).name;check_file(path,output['sha256'])
    job=ROOT/'artifacts/C5/parallel-full128-job';worker=load(job/'status.json')
    require(worker['status']=='PASS' and worker['exit_code']==0 and worker['inputs']==worker['inputs_after'],'Detached full batch did not complete with unchanged inputs')
    for stream in ['stdout','stderr']:check_file(job/(stream+'.log'),worker[stream+'_sha256'])
    with zipfile.ZipFile(job/'input_snapshot.zip') as archive:
        require(len(archive.namelist())==len(worker['inputs']),'Full batch source snapshot count')
        for name,row in zip(archive.namelist(),worker['inputs']):
            safe_member(name)
            with archive.open(name) as source:require(digest(source)==row['sha256'],'Full batch input snapshot drift')
    resumed=[r['phase'] for r in data['runs'] if r['resumed']]
    return {'status':'PASS_FULL_CAPACITY_PARALLEL_PATTERNS','bytes_per_pattern':134217728,'independent_resets':8,'worker_slots':data['actual_jobs'],
        'actual_workers':min(data['actual_jobs'],8-len(resumed)),
        'elapsed_seconds':data['elapsed_seconds'],'peak_group_pss_bytes':resources['peak_group_pss_bytes'],'resumed_phases':resumed,
        'total_cycles':sum(r['simulation']['cycles'] for r in data['runs']),
        'total_instructions':sum(r['simulation']['instructions'] for r in data['runs']),'executable_sha256':data['executable_sha256'],
        'reference_sha256':data['reference_sha256'],'assembly_sha256':data['assembly_sha256'],'pattern_driver_sha256':data['pattern_driver_sha256'],
        'summary':'artifacts/C5/parallel-sdram/full128/summary.json','summary_sha256':sha(base/'summary.json'),
        'resources_sha256':sha(base/'resources.json'),'driver_sha256':sha(base/'driver/run.json'),'worker_status_sha256':sha(job/'status.json'),'pilot_sha256':sha(ROOT/'reports/C5_parallel_sdram_pilot.json'),
        'scope':data['scope']}
