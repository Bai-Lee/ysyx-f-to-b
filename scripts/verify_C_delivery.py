"""Read-only C evidence/package verification; never reruns long simulations."""
from __future__ import annotations
import argparse,hashlib,io,json,posixpath,re,tarfile,zipfile
from pathlib import Path
from collections import Counter
from urllib.parse import unquote
from verify_E_delivery import require,load,sha,digest,check_file,safe_member,checker_controls,verify_tar
from verify_D_delivery import runtime_tar
from verify_C_parallel import full_checks as parallel_full_checks,pilot_checks as parallel_pilot_checks

ROOT=Path(__file__).resolve().parents[1]
COUNTS={'C1':(0,1),'C2':(11,13),'C3':(0,1),'C4':(12,24),'C5':(45,62)}
DIAGNOSTICS={
 'artifacts/C4/rtl_unit/fabric/run/run.json':('TIMEOUT',None,'Original Icarus zero-time scheduling stall. Retained as unresolved for that tool configuration; timed Verilator fabric tests and four rejecting mutants are separately accepted in C4_fabric.'),
 'artifacts/C4/synthesis/single/run.json':('RESOURCE_LIMIT',125,'Historical integrated ECC single-cycle STA reached its then-active PSS budget. Independent mapped OpenSTA and Nangate45 structural/timing assessments are accepted separately; max-transition failures remain unqualified.'),
 'artifacts/C5/rtthread/origin-commit/run.json':('FAIL',128,'Read-only Linux Git ownership check failed. No global trust setting changed; the detached archive HEAD and copied source provenance are recorded in C5_rtthread_setup.')}
DIAGNOSTICS['artifacts/C5/sdram-sweep/sdram32x2-134217728-asm/run/run.json']=('FAIL',143,'Serial full128 attempt intentionally stopped after user-authorized parallel strategy passed functional, throughput and aggregate-resource controls. Partial serial results are not accepted; final full128 evidence comes from eight independently reset, full-address-range patterns.')
C5_REPORTS=['axi_interface','bitrev_unit','boot','context','cpu_tests','csr','cycle_profile','diff','final_cpu','flash_boot',
 'generation','gpu_driver','io_units','loader','lshr','psram_apps','psram_controller','psram_model','psram_small','psram_sweep',
 'ram','reference_build','rtthread','rtthread_sdram32','scons_controls','sdram_apps','sdram_boundaries','sdram_controller',
 'sdram_model','sdram_sweep','sdram_bus_coverage','source_lock','spi','spi_shared','uart','vga_prerequisite','xip','chiplink','gui_input_control']
GUI_CASES=['gpio','keyboard','video','typing','fceux','rtthread','rtbench','rtguard']


def local_path(value):
    text=str(value).replace('\\','/')
    for prefix in ['/workspace/projects/ysyx_f_to_b/','/workspace/projects/ysyx_f_to_b/']:
        if text.startswith(prefix):return ROOT/text[len(prefix):]
    path=Path(text);return path if path.is_absolute() else ROOT/path


def coverage_check(coverage,size):
    require(coverage['unique_read_bytes']==coverage['unique_written_bytes']==size,'Full byte coverage missing')
    require(coverage['read_ops_by_width']==coverage['write_ops_by_width']==[2*size,size,size],'Width/pattern operation counts changed')


def recorded_simulation(evidence):
    folder=ROOT/evidence;record=load(folder/'run/run.json');path=folder/'simulation.json'
    rows=[r for r in record['outputs'] if local_path(r['path'])==path]
    require(len(rows)==1,'Simulation output is not bound to its command: '+evidence)
    check_file(path,rows[0]['sha256'])
    return load(path)


def controls():
    result=checker_controls();size=134217728
    valid={'unique_read_bytes':size,'unique_written_bytes':size,'read_ops_by_width':[2*size,size,size],'write_ops_by_width':[2*size,size,size]}
    coverage_check(valid,size)
    try:coverage_check({**valid,'unique_read_bytes':65536},size)
    except ValueError:result['small_pilot_not_accepted_as_full_memory']=True
    else:raise ValueError('A small pilot was accepted as full memory')
    result.update(zip_controls())
    return result


def c5_checks(allow_pending=False):
    data={name:load(ROOT/f'reports/C5_{name}.json') for name in C5_REPORTS}
    require(all(row['status'].startswith('PASS') for row in data.values()),'C5 required functional report not PASS')
    require(len(data['axi_interface']['runs'])==8,'AXI interface case count')
    require(len(data['cpu_tests']['runs'])==35,'MROM CPU acceptance count')
    final=data['final_cpu'];require(len(final['runs'])==36 and sum(r['status']=='PASS' for r in final['runs'])==35,'Final CPU regression count')
    require(next(r for r in final['runs'] if r['name']=='wrong')['result']=='BAD_TRAP','Original wrong.c not rejected')
    require(any(r['name']=='hello-str' and r['status']=='PASS' for r in final['runs']),'hello-str omitted from final regression')
    context={r['name']:r for r in data['context']['runs']};require(context['positive']['ecalls']==context['positive']['mrets']==52,'Context transfer coverage')
    require(context['bad-restore']['result']=='BAD_TRAP','Context restore fault not rejected')
    psram=next(r for r in data['psram_sweep']['runs'] if r['bytes']==4194304 and not r['corrupt'])
    require(recorded_simulation(psram['evidence'])==psram['simulation'],'PSRAM report/raw output drift')
    coverage_check(psram['simulation']['coverage'],4194304)
    require(psram['simulation']['result']=='GOOD_TRAP','Full PSRAM failed')
    sweeps=data['sdram_sweep']['runs'];pending=[];parallel=None
    for width,ranks,size in [(16,1,33554432),(32,2,134217728)]:
        matches=[r for r in sweeps if (r['width'],r['ranks'],r['bytes'])==(width,ranks,size) and not r['corrupt']]
        if not matches and size==134217728 and (ROOT/'reports/C5_sdram_full_parallel.json').exists():
            parallel=parallel_full_checks();require(load(ROOT/'reports/C5_sdram_full_parallel.json')==parallel,'Parallel full-capacity report drift');continue
        if not matches and allow_pending and size==134217728:pending.append('C5-M035');continue
        require(bool(matches),'Required full SDRAM sweep missing: '+str(size));row=matches[-1];coverage_check(row['coverage'],size)
        raw=recorded_simulation(row['evidence'])
        require(raw['result']=='GOOD_TRAP' and raw['diff_enabled'] and raw['diff_checked']+raw['device_sync_checked']==raw['instructions'],'Full SDRAM differential completion')
        require(raw['coverage']==row['coverage'] and raw['sdram_chips']==row['chips'] and raw['cycles']==row['cycles'] and raw['instructions']==row['instructions'],'SDRAM report/raw output drift')
        chips=row['chips'];require(sum(c['read_bytes'] for c in chips)==16*size and sum(c['write_bytes'] for c in chips)==8*size,'Physical SDRAM byte totals')
        for index in range((width//16)*ranks):
            require(chips[index]['maximum_byte_address']==33554431,'Physical chip capacity boundary not reached')
            require(chips[index]['read_bytes']==536870912 and chips[index]['write_bytes']==268435456,'Per-chip full-pattern payload mismatch')
    require(data['sdram_apps']['comparisons'],'No same-firmware SDRAM width comparison')
    require(data['sdram_bus_coverage']['source_sha256']==sha(ROOT/'reports/C5_sdram_sweep.json'),'SDRAM pin coverage audit is stale')
    if not pending and parallel is None:
        folder=ROOT/'artifacts/C5/full128-job';worker=load(folder/'status.json')
        require(worker['status']=='PASS' and worker['exit_code']==0 and worker['result_report_sha256']==sha(ROOT/'reports/C5_sdram_sweep.json'),'Long-worker completion is missing or stale')
        for stream in ['stdout','stderr']:check_file(folder/f'worker.{stream}.log',worker[stream+'_sha256'])
        with zipfile.ZipFile(folder/'source_snapshot.zip') as archive:
            require(len(archive.namelist())==len(worker['source_files']),'Long-worker source snapshot count')
            for member,row in zip(archive.namelist(),worker['source_files']):
                safe_member(member);check_file(local_path(row['path']),row['sha256'])
                with archive.open(member) as stream:require(digest(stream)==row['sha256'],'Long-worker input snapshot drift')
    require(all(r['status']=='PASS' for r in data['sdram_apps']['runs']),'SDRAM benchmark failed')
    link={row['name']:row for row in data['chiplink']['runs']};require(set(link)=={'positive','bad-read'},'ChipLink positive/negative pair incomplete')
    require(link['positive']['result']=='GOOD_TRAP' and link['bad-read']['result']=='DIFF_FAIL','ChipLink failure control')
    coverage_check(link['positive']['cpu_coverage'],4096);remote=link['positive']['link']
    require(remote['remote_unique_read_bytes']==remote['remote_unique_written_bytes']==4096 and remote['remote_written_bytes']==32768,'Remote RAM coverage')
    require(min(remote['words'])>0 and link['positive']['reset_cycles']>=10,'ChipLink pin/reset evidence')
    shared={r['name']:r for r in data['spi_shared']['runs']}
    require(shared['flash']['result'] in ['FLASH_PROTOCOL_ASSERTION','BAD_TRAP'] and shared['sram']['result']=='GOOD_TRAP','Shared SPI conflict/relocation control')
    require(data['gui_input_control']['pin_scan_codes']==[59,240,59] and data['gui_input_control']['ps2_queue']['dropped']==0,'Native key-event calibration')
    gui={};builds={Path(r['executable']).parent.name:r for r in load(ROOT/'reports/C5_soc_build.json')['variants']}
    for case in GUI_CASES:
        path=ROOT/f'reports/C5_gui_{case}.json';row=load(path);require(row['status']=='PASS' and row.get('visual_review'),'Unreviewed/failed GUI case '+case)
        require(builds[row['variant']]['sha256']==row['executable_sha256'] and row['reference_sha256']==data['reference_build']['sha256'],'GUI accepted binary/build binding differs')
        for capture in row['screenshots']:check_file(ROOT/capture['path'],capture['sha256'])
        require(row['visual_review']['screenshots']==row['screenshots'],'Visual review targets changed')
        summary=row['simulation_summary'];require(summary['diff_checked']+summary['device_sync_checked']==summary['instructions'],'GUI differential coverage')
        expected='BAD_TRAP' if case=='rtguard' else 'GUI_OBSERVATION_STOP' if case in ['gpio','keyboard','video'] else 'GOOD_TRAP'
        require(summary['result']==expected,'GUI completion semantics changed: '+case)
        simulation=load(ROOT/row['evidence']/'session/simulation.json')
        require(simulation['result']==expected and simulation['instructions']==summary['instructions'],'GUI raw/summary mismatch')
        tx=bytes.fromhex(simulation['uart']['hex']);rx=bytes.fromhex(simulation['uart_rx_pin']['hex'])
        folder=ROOT/row['evidence']/'session'
        require((folder/'nvboard-tx.bin').read_bytes()==tx==bytes.fromhex(simulation['uart_pin']['hex']),'UART decoder disagreement')
        require(rx==((folder/'nvboard-rx.bin').read_bytes() if (folder/'nvboard-rx.bin').exists() else b''),'UART input disagreement')
        require(simulation['uart_pin']['framing_errors']==simulation['uart_rx_pin']['framing_errors']==0,'UART framing failure')
        if 'ps2_queue' in simulation:require(simulation['ps2_queue']['dropped']==simulation['ps2_queue']['invalid']==0,'PS2 FIFO loss in accepted GUI run')
        gui[case]={'path':str(path.relative_to(ROOT)),'sha256':sha(path),'result':expected,'simulation_sha256':sha(folder/'simulation.json')}
    require(load(ROOT/'reports/C5_gui_fceux.json')['observations']['not_recovered_after_release']==0,'NES release did not recover')
    rtos=load(ROOT/'reports/C5_gui_rtthread.json');require(rtos['observations']['app_exits']==[['hello','0'],['fceux','0'],['hello','0'],['microbench','0']],'RT application lifecycle coverage')
    log=(ROOT/rtos['evidence']/'session/stdout.log').read_text('utf8',errors='replace').replace('\r','')
    require('c5_no_such_command: command not found.' in log and log.count(' Passed.')==10,'Shell error recovery / MicroBench coverage')
    require('mode=private guards=1 allocator=-1' in log and 'mode=klib guards=1 allocator=1' in log,'Application heap ownership not validated')
    builds=load(ROOT/'reports/C5_rtthread_apps_sdram128.json');require(builds['image_sha256']==rtos['image_sha256'],'GUI ran another RT application image')
    generation=load(ROOT/'reports/C5_chiplink_generation.json');check_file(local_path(generation['generated']['path']),generation['generated']['sha256'])
    require(len(generation['generated']['modules'])==175,'ChipLink elaboration module count changed')
    return {'status':'PENDING_FINAL_MEMORY' if pending else 'PASS','pending':pending,'checks':{name:sha(ROOT/f'reports/C5_{name}.json') for name in C5_REPORTS},'parallel_full_capacity':parallel,'build_index_sha256':sha(ROOT/'reports/C5_soc_build.json'),'gui':gui,'verified_full_psram_bytes':4194304,'verified_sdram_capacities':[33554432]+([] if pending else [134217728]),'checker_controls':controls()}


def command_evidence(deep=True,allow_pending=False):
    counts=Counter();diagnostics=[];snapshots=0;negative=0;changed=[];pending=[];helpers=[]
    for name in ['C','C1','C2','C3','C4','C5']:
        directory=ROOT/'artifacts'/name
        if not directory.exists():continue
        for path in directory.rglob('run.json'):
            record=load(path);historical='attempts' in path.relative_to(directory).parts
            counts[('history:' if historical else 'current:')+record.get('status','UNKNOWN')]+=1
            if historical:continue
            relative=path.relative_to(ROOT).as_posix();accepted=record.get('status','').startswith('PASS')
            if not accepted:
                require(relative in DIAGNOSTICS,'Undeclared nonaccepted current command: '+relative)
                status,code,reason=DIAGNOSTICS[relative];require(record['status']==status and record.get('exit_code')==code,'Diagnostic changed: '+relative)
                diagnostics.append({'path':relative,'status':status,'exit_code':code,'resolution':reason})
            for stream in ['stdout','stderr']:
                if stream+'_sha256' in record:check_file(path.parent/(stream+'.log'),record[stream+'_sha256'])
            if accepted and record.get('exit_code') not in [None,0]:
                expected=record.get('expected_exit');expected=[expected] if isinstance(expected,int) else expected
                require(expected is not None and record['exit_code'] in expected,'Unexpected nonzero result: '+relative);negative+=1
            if record.get('inputs_after') and record.get('inputs')!=record['inputs_after']:changed.append(relative)
            if deep:
                for filename,field in [('input_snapshot.zip','inputs'),('output_snapshot.zip','outputs')]:
                    archive=path.parent/filename
                    if not archive.exists():continue
                    expected=[item for item in record.get(field,[]) if item.get('sha256')]
                    with zipfile.ZipFile(archive) as z:
                        names=z.namelist();require(len(names)==len(set(names))==len(expected),'Snapshot member count: '+str(archive))
                        for member,row in zip(names,expected):
                            safe_member(member)
                            with z.open(member) as stream:require(digest(stream)==row['sha256'],'Snapshot SHA mismatch: '+str(archive)+':'+member)
                    snapshots+=1
        for path in directory.rglob('started.json'):
            if 'attempts' in path.relative_to(directory).parts or path.with_name('run.json').exists():continue
            relative=path.relative_to(ROOT).as_posix()
            if relative.startswith('artifacts/C/host-memory-monitor/'):
                result_path=path.with_name('result.json')
                if allow_pending and not result_path.exists():pending.append(relative);continue
                require(result_path.exists(),'Host sampler has no terminal record: '+relative)
                result=load(result_path);started=load(path);require(all(result.get(k)==v for k,v in started.items()),'Host sampler start/result mismatch')
                frozen=load(ROOT/'reports/C_host_memory_monitor.json')
                expected=next((r for r in frozen['files']+frozen['prior_sessions'] if r['path']==result_path.relative_to(ROOT).as_posix()),None)
                require(expected is not None,'Undeclared host sampler session');check_file(result_path,expected['sha256'])
                expected_status='STOPPED_BY_REQUEST' if path.parent.name==frozen['session'] else expected['status']
                require(result['status']==expected_status,'Host sampler terminal status changed')
                counts['helper:'+result['status']]+=1;helpers.append({'path':relative,'status':result['status'],'error':result.get('error')});continue
            pending.append(relative)
            require(allow_pending and (relative=='artifacts/C5/sdram-sweep/sdram32x2-134217728-asm/run/started.json' or relative.startswith('artifacts/C5/parallel-sdram/full128/')),'Unfinished command: '+relative)
    require(not changed,'Accepted command inputs changed during execution: '+str(changed))
    return {'counts':dict(counts),'expected_nonzero_controls':negative,'snapshot_archives_verified':snapshots,'deep_snapshot_check':deep,'declared_nonaccepted_diagnostics':diagnostics,'native_helper_sessions':helpers,'unfinished_commands':pending,'scope':'Current command stdout/stderr and snapshot byte integrity. Native sampler terminal records are explicitly bound, including the retained failed predecessor. Historical attempt states are counted, not promoted to passes; all retained history bytes are also covered by the final delivery manifest.'}


def source_scope(external=False,allow_pending=False):
    specs=load(ROOT/'C/runtime/course_specs.json');result=load(ROOT/'reports/C_results.json');records={r['id']:r for r in result['records']};ids={r['id'] for r in specs['tasks']}
    require(len(ids)==len(specs['tasks'])==101 and len(records)==len(result['records']),'Source/result duplicates or scope count')
    missing=ids-set(records);require(not(set(records)-ids),'Invented C record')
    require(not missing or (allow_pending and missing=={'C5-M035'}),'Missing source records: '+str(missing))
    core=[r for r in specs['tasks'] if r['classification']=='PUBLIC_CORE_TASK'];adapted=[r for r in specs['tasks'] if r['classification']=='USER_ADAPTED']
    require(len(core)==68 and len(adapted)==2,'Frozen classifications changed')
    for task in core+adapted:
        if task['id'] in missing:continue
        require(records[task['id']]['status'].startswith('PASS'),'Required task not accepted: '+task['id'])
    require(records['C5-O008']['status']=='OPTIONAL_NOT_IMPLEMENTED','SPI-interrupt optional state concealed')
    for key,row in records.items():
        require(bool(row['evidence']),'Missing evidence: '+key)
        for evidence in row['evidence']:require(local_path(evidence).exists(),'Missing evidence target: '+evidence)
    audits={}
    for stage,(count,total) in COUNTS.items():
        if stage=='C5' and allow_pending:continue
        path=ROOT/f'reports/{stage}_AUDIT.json';audit=load(path)
        require(audit['status'].startswith('PASS') and audit['stage_complete'] and audit['core_tasks']==count and audit['scope_records']==total,'Prior C stage incomplete: '+stage)
        require({r['id']:r for r in audit['records']}=={key:row for key,row in records.items() if key.startswith(stage+'-')},'Prior stage record drift: '+stage)
        for name,expected in audit.get('checks',{}).items():check_file(ROOT/f'reports/{name}.json',expected)
        audits[stage]={'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path)}
    require(load(ROOT/'reports/C2_AUDIT.json')['nested_required']==17 and load(ROOT/'reports/C2_pa2_results.json')['required_passed']==17,'PA2 nested scope incomplete')
    timing=load(ROOT/'reports/C4_nangate.json');require(all(row['frequency_estimate_qualified'] is False for row in timing['variants']),'Unqualified C4 timing promoted to qualified')
    for row in specs['sources']+specs.get('pa_sources',[]):
        check_file(local_path(row['copy']),row['sha256'])
        if external:check_file(Path(row['source']),row['sha256'])
    require('建设中' in (ROOT/'C/C6/sources/C6.md').read_text('utf8') and not any(r['id'].startswith('C6-') for r in specs['tasks']),'Invented C6 task')
    return {'core_required':68,'adapted_required':2,'records_present':len(records),'records_required':101,'missing':sorted(missing),'statuses':dict(Counter(r['status'] for r in records.values())),'stage_audits':audits,'source_copies':len(specs['sources'])+len(specs.get('pa_sources',[]))}


def markdown_links(external=False):
    documents=[ROOT/'README.md',ROOT/'reports/C_REPORT.md',ROOT/'reports/C_TASKS.md',
        ROOT/'C/offline/README.md',ROOT/'C/runtime/README.md',ROOT/'C/C6/SCOPE.md']
    documents += [ROOT/f'C/C{i}/NOTES.md' for i in range(1,6)]
    documents += [ROOT/'C/C2/PA2_NOTES.md',ROOT/'C/C4/RTL_CONTRACT.md']
    count=0;outside=[]
    for path in documents:
        require(path.is_file(),'Missing document: '+str(path))
        text=re.sub(r'```.*?```','',path.read_text('utf8'),flags=re.S)
        for match in re.finditer(r'!?\[[^\]]*\]\(([^\n)]+)\)',text):
            link=match[1].strip().strip('<>')
            if not link or link.startswith(('#','http:','https:','mailto:')):continue
            value=unquote(link.split('#',1)[0]).replace('\\','/')
            if value.startswith(('/workspace/projects/ysyx_f_to_b/','/workspace/projects/ysyx_f_to_b/')):
                target=local_path(value)
            elif re.match(r'^[A-Za-z]:/',value) and not Path(value).is_absolute():
                outside.append(value)
                require(not external,'External Windows link cannot be resolved on this platform: '+value)
                continue
            else:
                target=Path(value);target=target if target.is_absolute() else path.parent/target
            target=target.resolve()
            if not target.is_relative_to(ROOT.resolve()):
                outside.append(str(target))
                if not external:continue
            require(target.exists(),f'Broken Markdown link: {path}: {link}');count+=1
    return {'documents':len(documents),'resolved_links':count,'external_reference_paths':sorted(set(outside)),
        'scope':'File-target resolution; not a full Markdown/math rendering test.'}


def media_files():
    found={}
    def walk(value,report):
        if isinstance(value,list):
            for item in value:walk(item,report)
        elif isinstance(value,dict):
            raw=str(value.get('path','')).replace('\\','/')
            # NVBoard's source manifest paths are relative to its own workbench,
            # not the project. Only explicit project artifact paths belong here.
            if 'sha256' in value and Path(raw).suffix.lower() in ['.png','.ppm','.wav'] and (raw.startswith(('C/','artifacts/','/workspace/projects/ysyx_f_to_b/','/workspace/projects/ysyx_f_to_b/'))):
                path=local_path(raw);check_file(path,value['sha256']);found[str(path.relative_to(ROOT))]=value['sha256']
            for item in value.values():walk(item,report)
    for pattern in ['C1_*.json','C2_*.json','C3_*.json','C5_*.json']:
        for path in (ROOT/'reports').glob(pattern):walk(load(path),path.name)
    return {'verified_files':len(found),'scope':'Hashes declared by accepted image/audio records; prior visual observations remain in their original reports. This check does not perform a new visual or listening review.'}


def frozen_files(external=False):
    names=['C_runtime_export','C_offline_sources','C_offline_replay','C_final_bindings','C_toolchain_final','C_history_preservation','C_background_execution','C_performance_policy','C_parallel_resource_controls','C_serial_superseded','C_host_memory_controls','C_host_memory_io_controls','C_host_memory_monitor','C6_AUDIT']
    data={name:load(ROOT/f'reports/{name}.json') for name in names}
    require(all(row['status'].startswith('PASS') for row in data.values()),'Final report not accepted')
    background=data['C_background_execution'];check_file(ROOT/background['probe']['path'],background['probe']['sha256'])
    interrupted=background['interrupted_run']['classification_record'];check_file(ROOT/interrupted['path'],interrupted['sha256'])
    require(load(ROOT/interrupted['path'])['status']=='UNKNOWN','Interrupted full-memory attempt was promoted to success')
    probe=load(ROOT/background['probe']['path']);require(probe['status']=='PASS' and len(probe['timeline'])>=3,'Detached resource monitor was not accepted')
    check_file(ROOT/background['launcher']['path'],background['launcher']['sha256'])
    duplicate=background['duplicate_worker_control'];require(duplicate['status']=='PASS_REJECTED','Duplicate-worker protection missing')
    check_file(ROOT/duplicate['evidence']/'run.json',duplicate['run_sha256'])
    performance=data['C_performance_policy'];require(performance['profile']['max_simulators']==8 and performance['profile']['compile_jobs']==4,'Authorized throughput profile changed')
    duplicate=performance['duplicate_full_job_control'];require(duplicate['status']=='PASS_REJECTED','Parallel full-job duplicate guard missing');check_file(ROOT/duplicate['evidence']/'run.json',duplicate['run_sha256'])
    serial=data['C_serial_superseded'];require(serial['serial_validation_status']=='NOT_COMPLETED','Superseded partial serial run was promoted');check_file(ROOT/serial['run'],serial['run_sha256'])
    host=data['C_host_memory_controls'];require(host['stale_rejected'] and host['missing_rejected'] and host['no_interop_calls'],'Host telemetry fail-closed controls missing')
    check_file(ROOT/'C/runtime/resource_policy.py',host['reader_sha256']);check_file(ROOT/'scripts/host_memory_monitor.py',host['sampler_sha256'])
    monitor=data['C_host_memory_monitor'];require(monitor['status']=='PASS_STOPPED_AFTER_VALIDATION' and monitor['controls_sha256']==sha(ROOT/'reports/C_host_memory_controls.json'),'Host sampler not finalized')
    for row in monitor['files']:check_file(ROOT/row['path'],row['sha256'])
    for row in monitor['prior_sessions']:check_file(ROOT/row['path'],row['sha256'])
    io=data['C_host_memory_io_controls'];require(all(io[key] for key in ['replace_rejected_under_read_handle','append_while_read_handle','live_stream_advanced_while_held','partial_tail_uses_previous_complete_record','malformed_complete_record_rejected']),'Host stream I/O controls incomplete')
    require(monitor['io_controls_sha256']==sha(ROOT/'reports/C_host_memory_io_controls.json'),'Host I/O control binding differs')
    frozen=data['C_runtime_export'];count=runtime_tar(frozen);members={r['path']:r for r in frozen['members']}
    for row in frozen['members']:
        if row['kind']=='symlink':
            resolved=posixpath.normpath(posixpath.join(posixpath.dirname(row['path']),row['target']))
            require(resolved in members or any(name.startswith(resolved+'/') for name in members),'Dangling frozen link: '+row['path'])
    snapshot=load(ROOT/'C/C2/snapshot/manifest.json');check_file(ROOT/snapshot['archive'],snapshot['sha256'])
    c2count=verify_tar(ROOT/snapshot['archive'],snapshot['members'])
    for row in data['C_offline_sources']['files']:check_file(ROOT/row['path'],row['sha256'])
    bindings=data['C_final_bindings'];require(bindings['archive_sha256']==frozen['sha256'],'Final binding archive drift')
    for row in bindings['binaries']:
        require(members[row['member']]['sha256']==row['sha256'],'Frozen binary mismatch')
    for row in bindings['authored_hardware_sources']:check_file(ROOT/row['path'],row['sha256'])
    for row in bindings['software_overlays']:
        check_file(ROOT/row['path'],row['sha256']);require(members[row['member']]['sha256']==row['sha256'],'Overlay/frozen workbench mismatch')
    for row in bindings['historical_software_sources']:
        require(members[row['member']]['sha256']==row['sha256'],'Historical source/freeze mismatch')
        check_file(ROOT/row['accepted_build_record'],row['accepted_build_record_sha256']);record=load(ROOT/row['accepted_build_record'])
        require(any(r['path']==row['runtime_source'] and r['sha256']==row['sha256'] for r in record['inputs']),'Historical source/accepted build mismatch')
    for row in bindings['rtthread_final_build_inputs']:require(members[row['member']]['sha256']==row['sha256'],'RT build/frozen input mismatch')
    rt=load(ROOT/'reports/C5_rtthread_apps_sdram128.json')
    check_file(ROOT/bindings['rtthread_build_record'],bindings['rtthread_build_record_sha256'])
    replay=data['C_offline_replay'];require(replay['archive_sha256']==frozen['sha256'] and len(replay['runs'])==4,'Offline replay scope')
    require({r['case'] for r in replay['runs']}=={'microbench','rtthread','chiplink','chiplink-bad-read'},'Replay cases changed')
    for row in replay['runs']:
        require(row['status']=='PASS','Offline replay failed');folder=ROOT/row['evidence'];check_file(folder/'run/run.json',row['run_sha256'])
        current=load(folder/'simulation.json');prior=load(ROOT/row['original_evidence']/'simulation.json')
        require(all(current[key]==prior[key] for key in row['compared_fields']),'Offline replay raw values differ')
        for item in row['inputs']:require(members[item['member']]['sha256']==item['sha256'],'Replay input not frozen')
    require(next(r for r in replay['runs'] if r['case']=='chiplink-bad-read')['result']=='DIFF_FAIL','Replay negative was not rejected')
    baseline=load(ROOT/'reports/C_baseline.json');history=data['C_history_preservation']
    require(history['D_zip_sha256']==baseline['D_zip_sha256'],'Prior delivery baseline changed')
    check_file(ROOT/'reports/D_delivery_manifest.json',history['prior_manifest_sha256'])
    for row in history['preserved_files']:check_file(ROOT/row['path'],row['sha256'])
    scope_ids={r['id'] for r in load(ROOT/'C/runtime/course_specs.json')['tasks']}
    outside=[r for r in load(ROOT/'config/task_status.json')['tasks'] if r['id'] not in scope_ids]
    outside_digest=hashlib.sha256(json.dumps(outside,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    require(outside_digest==history['outside_C_task_records_sha256'] and len(outside)==history['outside_C_task_record_count'],'Task states outside C changed')
    if external:check_file(ROOT/'YSYX_D_DELIVERY.zip',history['D_zip_sha256'])
    c6=data['C6_AUDIT'];require(c6['core_tasks']==0 and c6['scope_records']==0 and c6['source_status']=='UNDER_CONSTRUCTION','C6 scope changed')
    check_file(ROOT/c6['source'],c6['sha256'])
    return {'checks':{name:sha(ROOT/f'reports/{name}.json') for name in names},'runtime_members':count,'C2_snapshot_members':c2count,
        'preserved_history_files':len(history['preserved_files']),'offline_source_archives':len(data['C_offline_sources']['files']),'offline_replay_cases':4}


def verify_project(external=False,require_final=True,allow_pending=False,deep=True):
    result={'status':'IN_PROGRESS' if allow_pending else 'PASS','verification_kind':'read-only retained evidence, not simulation rerun',
        'scope':source_scope(external,allow_pending),'C5':c5_checks(allow_pending),'commands':command_evidence(deep,allow_pending)}
    if allow_pending:return result
    ledger=load(ROOT/'config/task_status.json');records=load(ROOT/'reports/C_results.json');tasks={r['id']:r for r in ledger['tasks']}
    require(ledger['current_stage']=='C' and ledger['stage_status']=='COMPLETE_ENGINEERING_WITH_DECLARED_LIMITS' and ledger['stop_after']=='C','C final ledger state')
    require(records['status']=='COMPLETE_ENGINEERING_WITH_DECLARED_LIMITS' and load(ROOT/'config/execution_policy.json')['stop_after']=='C','C execution boundary')
    for row in records['records']:
        require(tasks[row['id']]['status']==row['status'] and tasks[row['id']]['evidence']==row['evidence'],'Final task ledger differs: '+row['id'])
    require(all(row['status'] in ['NOT_RUN','EXCLUDED_SCOPE'] for row in tasks.values() if row['id'].startswith('B')),'B work was started or promoted')
    audit=load(ROOT/'reports/C5_AUDIT.json');require(audit['verification']==result['C5'],'C5 evidence changed after acceptance')
    result.update(frozen=frozen_files(external),media=media_files(),markdown=markdown_links(external))
    if require_final:
        final=load(ROOT/'reports/C_AUDIT.json');require(final['status']=='PASS' and final['stage_complete'] and final['stop_after']=='C','Whole C audit incomplete')
        for key in ['scope','C5','frozen']:
            require(final['verification'][key]==result[key],'C evidence changed after final audit: '+key)
    return result


def verify_zip(path,entries,manifest_sha256,current_files=True):
    name='reports/C_delivery_manifest.json'
    with zipfile.ZipFile(path) as archive:
        names=archive.namelist();require(len(names)==len(set(names)),'Duplicate ZIP entry')
        for item in names:safe_member(item)
        require(set(names)=={r['path'] for r in entries}|{name},'ZIP entry set mismatch')
        blob=archive.read(name);require(hashlib.sha256(blob).hexdigest()==manifest_sha256,'Manifest SHA mismatch')
        require(json.loads(blob)['entries']==entries,'ZIP manifest entries differ')
        for index,row in enumerate(entries):
            info=archive.getinfo(row['path']);require(info.file_size==row['bytes'],'ZIP member size: '+row['path'])
            # Reading to EOF validates ZipExtFile's CRC as well as the SHA below.
            with archive.open(info) as stream:require(digest(stream)==row['sha256'],'ZIP member SHA: '+row['path'])
            if current_files:check_file(ROOT/row['path'],row['sha256'])
            if (index+1)%10000==0:print('C_VERIFIED_ZIP_MEMBERS',index+1,flush=True)
    return {'status':'PASS','verified_entries':len(entries)+1,'crc_verified':True,'all_member_sha256_verified':True,'current_files_match':current_files}


def zip_controls():
    payload=b'C delivery member\n';correct=hashlib.sha256(payload).hexdigest();out={}
    for case,name,expected,extra in [('valid','fixture.txt',correct,False),('bad_digest','fixture.txt','0'*64,False),
            ('unexpected_member','fixture.txt',correct,True),('unsafe_path','../escape.txt',correct,False)]:
        row={'path':name,'bytes':len(payload),'sha256':expected};blob=json.dumps({'entries':[row]}).encode();buffer=io.BytesIO()
        with zipfile.ZipFile(buffer,'w') as archive:
            archive.writestr(name,payload);archive.writestr('reports/C_delivery_manifest.json',blob)
            if extra:archive.writestr('unexpected.txt',b'extra')
        try:verify_zip(buffer,[row],hashlib.sha256(blob).hexdigest(),False)
        except ValueError:
            require(case!='valid','Valid C archive rejected');out['C_zip_'+case+'_rejected']=True
        else:
            require(case=='valid','Invalid C archive accepted: '+case);out['C_zip_valid_accepted']=True
    return out


def verify_delivery(path):
    path=Path(path);expected=path.with_suffix('.zip.sha256').read_text('ascii').split()[0];check_file(path,expected)
    with zipfile.ZipFile(path) as archive:blob=archive.read('reports/C_delivery_manifest.json')
    manifest=load(ROOT/'reports/C_delivery_manifest.json');require(json.loads(blob)==manifest,'Local/archive manifest mismatch')
    receipt=ROOT/'reports/C_delivery_archive.json'
    if receipt.exists():
        row=load(receipt);require(row['sha256']==expected and row['manifest_sha256']==hashlib.sha256(blob).hexdigest(),'Delivery receipt drift')
    result=verify_zip(path,manifest['entries'],hashlib.sha256(blob).hexdigest(),True);result['sha256']=expected
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--external',action='store_true');parser.add_argument('--allow-pending',action='store_true');parser.add_argument('--shallow',action='store_true');parser.add_argument('--pre-final',action='store_true');parser.add_argument('--archive',type=Path);parser.add_argument('--output',type=Path);args=parser.parse_args()
    require(not args.archive or (not args.allow_pending and not args.pre_final),'Archive check requires final scope')
    result=verify_project(args.external,not args.pre_final,args.allow_pending,not args.shallow)
    if args.archive:result['delivery']=verify_delivery(args.archive)
    if args.output:args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({'status':result['status'],'scope':result['scope'],'C5':result['C5']['status'],'commands':result['commands'],
        **{key:result[key] for key in ['frozen','media','markdown','delivery'] if key in result}},ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':main()
