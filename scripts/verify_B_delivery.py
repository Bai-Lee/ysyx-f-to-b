"""Read-only semantic, provenance and archive checks for the B delivery."""
from __future__ import annotations
from evidence import ROOT,sha,dump,datetime,timezone
from pathlib import Path
import argparse,collections,hashlib,json,re,zipfile,shutil,io
from urllib.parse import unquote
from verify_D_delivery import runtime_tar
from verify_E_delivery import safe_member,digest,checker_controls

class Pending(ValueError):pass
DIAGNOSTICS={'artifacts/B4/formal/interlock/run/run.json':('TIMEOUT',None,'Optional three-instruction arithmetic miter reached600s. No proof/counterexample; assertions retained. Not required functional acceptance.')}
def require(condition,message):
    if not condition:raise ValueError(message)
def read(name):return json.loads((ROOT/'reports'/f'{name}.json').read_text('utf8'))
def load(path):return json.loads(path.read_text('utf-8-sig'))
def local(value):
    text=str(value).replace('\\','/')
    for prefix in ['/workspace/projects/ysyx_f_to_b/','/workspace/projects/ysyx_f_to_b/']:
        if text.startswith(prefix):return ROOT/text[len(prefix):]
    return Path(text) if Path(text).is_absolute() else ROOT/text
def check(path,value):require(path.is_file() and sha(path)==value,'Hash mismatch: '+str(path))
def good_simulation(data):
    require(data['result']=='GOOD_TRAP' and data['diff_enabled'],'Simulator did not complete a checked GOOD_TRAP')
    require(data['diff_checked']+data['device_sync_checked']==data['instructions'],'Retirement comparison count')

def b5_checks():
    timing=read('B5_final_timing');netlist=ROOT/'B/B5/netlist/ysyx_00000000.v';check(netlist,timing['netlist_sha256'])
    require(timing['area_um2']<=25000 and timing['hold_slack_ns']>=0 and timing['max_transition_violations']==0,'Final area/declared timing model failed')
    require(timing['evaluation_frequency_mhz']==325 and timing['setup_frequency_estimate_mhz']>=325,'Final evaluation frequency')
    exported=read('B5_export');check(local(exported['path']),exported['sha256'])
    for source in exported['sources']:check(ROOT/source['path'],source['sha256'])
    eq=read('B5_export_equivalence');require(eq['status']=='PASS' and eq['exported_rtl_sha256']==exported['sha256'],'Export equivalence missing or stale')
    check(ROOT/'B/B5/export/unsanitized.sv',eq['raw_rtl_sha256'])
    structure=read('B5_structure');require(structure['status']=='PASS' and structure['netlist_sha256']==timing['netlist_sha256'] and structure['exported_rtl_sha256']==exported['sha256'],'Structure report drift')
    require(structure['latches']==0 and structure['axi_data_bits']==32 and len(structure['negative_controls'])==3,'Structural controls incomplete')
    cells=read('B5_cell_models');require(cells['status']=='PASS' and cells['netlist_structure_sha256']==timing['mapped_json_sha256'],'Cell-model coverage is stale')
    check(ROOT/'B/models/nangate45/sim/cells.v',cells['models_sha256'])
    require(set(structure['cell_types'])<=set(cells['used_cells']),'A final cell type was not validated')
    required={'hello','hazards','fence-prefetch','microbench','rtthread'};programs={}
    for mode in ['rtl','netlist']:
        report=read('B5_'+mode);rows={r['name']:r for r in report['runs']}
        if set(rows)!=required:raise Pending('B5 '+mode+' programs pending: '+str(required-set(rows)))
        build=load(ROOT/'artifacts/B5/design'/mode/'build/run.json')
        if mode=='rtl':
            inputs={str(local(r['path'])):r['sha256'] for r in build['inputs']}
            if any(inputs.get(str(ROOT/r['path']))!=r['sha256'] for r in exported['sources']):raise Pending('B5 RTL suite predates the final source')
        else:require(report['netlist_sha256']==timing['netlist_sha256'],'Gate simulation used another netlist')
        for name,row in rows.items():
            require(row['status']=='PASS','B5 program failed: '+mode+'/'+name)
            require(row.get('executable_sha256')==report['executable_sha256'],'B5 mixed executable revisions: '+mode+'/'+name)
            if mode=='netlist':require(row['netlist_sha256']==timing['netlist_sha256'],'B5 per-case netlist drift')
            folder=ROOT/row['evidence'];record=load(folder/'run.json');require(record['status']=='PASS' and record['exit_code']==0,'B5 raw process failure')
            check(folder/'stdout.log',record['stdout_sha256']);text=(folder/'stdout.log').read_text('utf8',errors='replace')
            require('B5_PROGRAM_PASS' in text,'No B5 completion marker')
            if name=='microbench':require(text.count('Passed.')==10 and 'MicroBench PASS' in text and 'insufficient memory' not in text,'Incomplete MicroBench')
            if name=='rtthread':require('C5_RTTHREAD_PASS' in text and 'C5_CONTEXT_PASS a=12 b=12' in text,'Incomplete RT-Thread/context check')
        programs[mode]={'report_sha256':sha(ROOT/'reports'/f'B5_{mode}.json'),'programs':sorted(rows)}
    negative=read('B5_rtl-bad-reset');require(negative['fault_reset'] and negative['runs'][0]['status']=='PASS_MISSING_RESET_REJECTED','Four-state reset negative missing')
    entry=ROOT/'reports/B5_public_entrypoints.json'
    if not entry.exists():raise Pending('B5 public make entrypoints have not completed')
    public=load(entry);modes={r['mode'] for r in public['runs'] if r['status']=='PASS'};require(modes=={'rtl','netlist'},'Make simulator entrypoint coverage')
    require(any(r['mode']=='rtl' and r['source_sha256']==[exported['sha256']] for r in public['runs']),'Exported RTL was not actually run through public entrypoint')
    require(any(r['mode']=='netlist' and r['source_sha256']==[timing['netlist_sha256'],cells['models_sha256']] for r in public['runs']),'Final gate public entrypoint mismatch')
    return {'status':'PASS','netlist_sha256':timing['netlist_sha256'],'exported_rtl_sha256':exported['sha256'],'area_um2':timing['area_um2'],'model_frequency_mhz':325,'programs':programs,
        'checks':{name:sha(ROOT/'reports'/f'{name}.json') for name in ['B5_final_timing','B5_structure','B5_cell_models','B5_export','B5_export_equivalence','B5_public_entrypoints','B5_rtl-bad-reset']},
        'scope':'Final configured DUT, four-state test programs, exact functionally mapped netlist and declared pre-layout timing model. No official CI, hidden tests, full CPU proof or physical signoff.'}

def memory_case(data,size,phase,negative=False):
    require(data['diff_enabled'] and data['diff_checked']+data['device_sync_checked']==data['instructions'],'Memory retirement comparison count')
    if negative:
        require(data['result']=='BAD_TRAP' and data['a0']==71,'Corrupted memory fixture was not rejected');return
    good_simulation(data);coverage=data['coverage']
    require(coverage['size']==size and coverage['base']==0xa0000000 and coverage['unique_read_bytes']==coverage['unique_written_bytes']==size,'Full byte coverage missing')
    count=size if phase<2 else size//2 if phase<4 else size//4
    ops=[0,0,0];ops[min(phase//2,2)]=count
    require(coverage['read_ops_by_width']==coverage['write_ops_by_width']==ops,'Width-specific operation count')
    multiplier=8 if phase<2 else 4 if phase<4 else 2
    require(sum(c['read_bytes'] for c in data['sdram_chips'])==multiplier*size and sum(c['write_bytes'] for c in data['sdram_chips'])==size,'Physical read/write payload')
    tag=ord('BHWQ'[phase//2])+(32 if phase%2 else 0)
    require(bytes.fromhex(data['uart']['hex'])==bytes([tag,10]),'Memory phase completion tag')
    if size==134217728:
        for chip in data['sdram_chips']:
            require(chip['maximum_byte_address']==33554431 and chip['write_bytes']==size//4 and chip['read_bytes']==multiplier*size//4,'Chip boundary/payload mismatch')

def memory_batch(label,size,negative=False):
    folder=ROOT/'artifacts/B4/parallel-sdram'/label
    if not (folder/'summary.json').exists():raise Pending('Memory batch still pending: '+label)
    report=load(folder/'summary.json');require(report['status']=='PASS' and report['bytes_per_pattern']==size and report['corrupt']==negative,'Memory summary status')
    require({r['phase'] for r in report['runs']}==set(range(8)) and len(report['runs'])==8,'Memory patterns incomplete')
    resource_bindings=[];registry_path=folder/'accepted_case_budgets.json';registry=load(registry_path)['cases'] if registry_path.exists() else {}
    for row in report['runs']:
        memory_case(row['simulation'],size,row['phase'],negative)
        case=ROOT/row['evidence'];record=load(case/'run.json');check(case/'run.json',row['run_sha256']);require(record['status']=='PASS','Memory raw command failure')
        raw=load(case/'simulation.json');require(raw==row['simulation'],'Memory summary/raw drift')
        require(any(local(r['path'])==case/'simulation.json' and r.get('sha256')==sha(case/'simulation.json') for r in record['outputs']),'Unbound memory result')
        if row.get('resumed'):
            require(row['run_sha256'] in registry,'Resumed phase lacks its original resource evidence')
            binding=registry[row['run_sha256']]
            require(binding['phase']==row['phase'],'Wrong original phase budget binding')
            for field in ['resource','driver','started']:check(ROOT/binding[field]['path'],binding[field]['sha256'])
            prior=load(ROOT/binding['resource']['path']);original_driver=load(ROOT/binding['driver']['path']);original_start=load(ROOT/binding['started']['path'])
            require(prior['status']=='RESOURCE_LIMIT' and prior['reason']=='WINDOWS_RUNNING_HEADROOM' and original_driver['status']=='RESOURCE_LIMIT','Unexpected original batch failure type')
            original_inputs={r['path']:r['sha256'] for r in original_driver['inputs']}
            require(all(original_inputs.get(r['path'])==r['sha256'] for r in record['inputs']),'Reused phase inputs do not belong to the bound original batch')
            end=(datetime.fromisoformat(record['timestamp'])-datetime.fromisoformat(original_start['timestamp'])).total_seconds()
            require(0<end<prior['elapsed_seconds'] and record['timestamp']<original_driver['timestamp'],'Reused phase did not precede the batch ending')
            samples=[r for r in prior['timeline'] if r['elapsed_seconds']<=end+1]
            require(samples and min(r['windows_available_bytes'] for r in samples)>=1024*1024**2,'Reused phase headroom before completion')
            require(prior['peak_aggregate_B_group_pss_bytes']<=6144*1024**2 and prior['minimum_system_available_bytes']>=512*1024**2,'Reused phase aggregate/Linux budget')
            resource_bindings.append({'phase':row['phase'],'resumed':True,'run_sha256':row['run_sha256'],'resource':binding['resource'],
                'original_driver':binding['driver'],'original_started':binding['started'],
                'original_batch_status':prior['status'],'phase_completion_elapsed_seconds':end,'original_batch_end_seconds':prior['elapsed_seconds'],
                'minimum_sampled_windows_bytes_through_completion':min(r['windows_available_bytes'] for r in samples),
                'scope':'Phase completed with valid sampled headroom before the later batch resource stop. Its original immutable budget copy is used; the current retry budget does not retroactively cover it.'})
    budget=load(folder/'resources.json');require(budget['status']=='PASS' and budget['peak_aggregate_B_group_pss_bytes']<=6144*1024**2,'Memory batch resource guard')
    require(budget['minimum_windows_available_bytes']>=1024*1024**2 and budget['minimum_system_available_bytes']>=512*1024**2,'Final batch headroom')
    for row in report['runs']:
        if not row.get('resumed'):resource_bindings.append({'phase':row['phase'],'resumed':False,'run_sha256':row['run_sha256'],'resource':{'path':(folder/'resources.json').relative_to(ROOT).as_posix(),'sha256':sha(folder/'resources.json')},'original_batch_status':'PASS'})
    driver=load(folder/'driver/run.json');require(driver['status']=='PASS' and driver['exit_code']==0,'Memory batch driver did not complete')
    report['accepted_resource_bindings']=sorted(resource_bindings,key=lambda r:r['phase'])
    return report

def full_memory_checks():
    for label,size,negative in [('release-pilot4k',4096,False),('release-pilot4k-bad',4096,True),('release-pilot64k',65536,False)]:memory_batch(label,size,negative)
    data=memory_batch('release-full128',134217728);build=next(r for r in read('B_soc_soc_build')['variants'] if r['variant']=='b5-release')
    require(data['executable_sha256']==build['sha256'],'Full memory used another CPU configuration')
    check(ROOT/'B/soc/programs/mem-sweep-asm.S',data['assembly_sha256'])
    require(sha(ROOT/'C/C5/programs/mem-sweep-asm.S')==data['assembly_sha256'],'Accepted assembly patterns changed')
    require(sha(ROOT/'B/soc/programs/mem-sweep-phase.c')==data['pattern_driver_sha256'],'Pattern driver changed')
    cycles=sum(r['simulation']['cycles'] for r in data['runs']);instructions=sum(r['simulation']['instructions'] for r in data['runs'])
    return {'status':'PASS_FULL_CAPACITY_PARALLEL_PATTERNS','variant':'b5-release','patterns':8,'bytes_per_pattern':134217728,'total_cycles':cycles,'total_instructions':instructions,
        'executable_sha256':data['executable_sha256'],'reference_sha256':data['reference_sha256'],'summary_sha256':sha(ROOT/'artifacts/B4/parallel-sdram/release-full128/summary.json'),
        'resumed_patterns':sum(r.get('resumed',False) for r in data['runs']),'resource_bindings':data['accepted_resource_bindings'],
        'resume_registry_sha256':sha(ROOT/'artifacts/B4/parallel-sdram/release-full128/accepted_case_budgets.json') if any(r.get('resumed') for r in data['runs']) else None,
        'scope':'Each independently reset pattern traverses all128MiB. No address partitioning. Full logical width/address/inverse counts and four physical chips checked. AXI BL8 model has an extra discarded beat on single-word reads; total pin read payload is32N across8patterns, writes8N.'}

def command_checks(deep=False,allow_pending=False):
    counts=collections.Counter();diagnostics=[];pending=[];snapshots=0;negative=0;records=0;reused=0
    cache_path=ROOT/'temp/B_snapshot_verification_cache.json';cache=load(cache_path) if deep and cache_path.exists() else {}
    checker_sha=sha(Path(__file__))
    monitor_path=ROOT/'reports/B_host_memory_monitor.json'
    accepted_samplers={r['path'] for r in load(monitor_path)['sessions']} if monitor_path.exists() else None
    for name in ['B','B1','B2','B3','B4','B5']:
        folder=ROOT/'artifacts'/name
        if not folder.exists():continue
        for path in folder.rglob('run.json'):
            if path.is_relative_to(ROOT/'artifacts/B/demo'):continue
            history='attempts' in path.relative_to(folder).parts
            data=load(path);counts[('history:' if history else 'current:')+data.get('status','UNKNOWN')]+=1
            if history:continue
            records+=1;started=path.with_name('started.json')
            if started.exists() and load(started).get('timestamp','')>data.get('timestamp',''):
                pending.append(str(path.relative_to(ROOT)));continue
            relative=path.relative_to(ROOT).as_posix()
            if data['status']!='PASS':diagnostics.append({'path':relative,'status':data['status'],'exit_code':data.get('exit_code')})
            if data.get('inputs_after') is not None:require(data['inputs_after']==data['inputs'],'Command inputs changed during execution: '+relative)
            for stream in ['stdout','stderr']:
                if stream+'_sha256' in data:check(path.with_name(stream+'.log'),data[stream+'_sha256'])
            if data['status']=='PASS' and data.get('exit_code') not in [None,0]:
                expected=data.get('expected_exit');expected=[expected] if isinstance(expected,int) else expected
                require(expected and data['exit_code'] in expected,'Unexplained accepted nonzero exit: '+relative);negative+=1
            if deep:
                for filename,field in [('input_snapshot.zip','inputs'),('output_snapshot.zip','outputs')]:
                    archive=path.with_name(filename)
                    if not archive.exists():continue
                    expected=[r for r in data.get(field,[]) if r.get('sha256')]
                    cache_key=archive.relative_to(ROOT).as_posix()
                    fingerprint={'archive_sha256':sha(archive),'expected_sha256':hashlib.sha256(json.dumps(expected,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'checker_sha256':checker_sha}
                    if cache.get(cache_key)==fingerprint:
                        snapshots+=1;reused+=1;continue
                    with zipfile.ZipFile(archive) as z:
                        names=z.namelist();require(len(names)==len(set(names))==len(expected),'Snapshot member count: '+str(archive))
                        for member,row in zip(names,expected):
                            safe_member(member)
                            with z.open(member) as stream:require(digest(stream)==row['sha256'],'Snapshot SHA mismatch: '+str(archive)+'/'+member)
                    cache[cache_key]=fingerprint
                    snapshots+=1
        for path in folder.rglob('started.json'):
            if path.is_relative_to(ROOT/'artifacts/B/demo'):continue
            if 'attempts' in path.relative_to(folder).parts or path.with_name('run.json').exists():continue
            if 'host-memory-monitor' in path.parts:
                if path.with_name('result.json').exists():continue
                if accepted_samplers is not None and path.parent.relative_to(ROOT).as_posix() not in accepted_samplers:continue
            pending.append(path.relative_to(ROOT).as_posix())
    if not allow_pending:
        require(not pending,'Pending commands: '+str(pending))
        for row in diagnostics:
            require(row['path'] in DIAGNOSTICS,'Undeclared failed current command: '+row['path'])
            status,code,reason=DIAGNOSTICS[row['path']];require(row['status']==status and row['exit_code']==code,'Diagnostic drift: '+row['path']);row['resolution']=reason
    if deep:dump(cache_path,cache)
    return {'counts':dict(counts),'current_records':records,'negative_exit_controls':negative,'snapshot_archives_verified':snapshots,'snapshot_archives_reused_after_byte_hash_check':reused,'diagnostics':diagnostics,'pending':pending}

def base_checks():
    required=['B1_native','B1_npc','B1_AUDIT','B2_AUDIT','B3_apb_unit','B3_axi_delay_unit','B3_axi_generation','B3_icache_unit','B3_sdram_axi_unit','B3_smc','B3_loader_fence','B3_trace_controls',
        'B4_functional_release','B_standalone_release','B4_release_soc','B4_branchsim_b5-stream-325','B4_branchsim_b5-release','B_resource_aggregate','B_history_preservation']
    for name in required:require(read(name)['status'].startswith('PASS'),name+' is not accepted')
    for name in ['B_final_regressions','B4_final_cpu','B4_controlled_evaluation','B_performance_analysis','B_cpu_corpus']:
        if not (ROOT/'reports'/f'{name}.json').exists() or not read(name)['status'].startswith('PASS'):raise Pending(name+' is pending')
    cpu=read('B4_final_cpu');require(len(cpu['runs'])==36 and sum(r['status']=='PASS' for r in cpu['runs'])==35,'Original CPU regression count')
    require(read('B_cpu_corpus')['suite_sha256']==sha(ROOT/'reports/B4_final_cpu.json'),'Original CPU corpus receipt drift')
    require(next(r for r in cpu['runs'] if r['name']=='wrong')['result']=='BAD_TRAP','Original wrong.c was not rejected')
    for name in ['B4_release_soc','B_standalone_release','B4_functional_release']:
        for r in read(name)['runs']:good_simulation(r['simulation'])
    train=next((r for r in read('B3_performance')['runs'] if r['variant']=='b5-release' and r['size']=='train'),None)
    require(train is not None and train['status']=='PASS' and train['model_frequency_mhz']==325,'Final full train missing');good_simulation(train['simulation'])
    require(train['uart'].count('Passed.')==10 and 'MicroBench PASS' in train['uart'],'Final train has incomplete benchmark coverage')
    required+=['B_final_regressions','B4_final_cpu','B4_controlled_evaluation','B_performance_analysis','B_cpu_corpus']
    return {'status':'PASS','checks':{name:sha(ROOT/'reports'/f'{name}.json') for name in required},'final_train_cycles':train['simulation']['cycles'],'final_train_instructions':train['simulation']['instructions']}

def verify_project(deep=False,allow_pending=False):
    pending=[];checks={}
    for name,function in [('functional',base_checks),('B5',b5_checks),('full_memory',full_memory_checks)]:
        try:checks[name]=function()
        except Pending as error:
            if not allow_pending:raise
            pending.append(str(error))
    commands=command_checks(deep,allow_pending);pending+=commands['pending']
    return {'status':'IN_PROGRESS' if pending else 'PASS','pending':pending,'checks':checks,'commands':commands,'checker_controls':checker_controls()}

def final_project_checks(deep=True):
    result=verify_project(deep,False)
    require(read('B5_ACCEPTANCE')==result['checks']['B5'],'Final B5 receipt drift')
    require(read('B4_full128')==result['checks']['full_memory'],'Final memory receipt drift')
    specs=load(ROOT/'B/runtime/course_specs.json');results=read('B_results');rows={r['id']:r for r in results['records']}
    require(len(rows)==len(results['records'])==110 and set(rows)=={r['id'] for r in specs['tasks']},'B task coverage mismatch')
    ledger=load(ROOT/'config/task_status.json');ledger_by={r['id']:r for r in ledger['tasks']}
    require(ledger['current_stage']=='B' and ledger['stop_after']=='B' and ledger['next_stage']=='A_NOT_AUTHORIZED','Wrong current task scope')
    core=adapted=0
    for task in specs['tasks']:
        row=rows[task['id']];check(ROOT/row['source']['path'],row['source']['sha256'])
        if task['classification'] in ['PUBLIC_CORE_TASK','USER_ADAPTED']:
            require(row['status'].startswith('PASS'),'Mandatory B task incomplete: '+task['id'])
            core+=task['classification']=='PUBLIC_CORE_TASK';adapted+=task['classification']=='USER_ADAPTED'
        for path,value in row['evidence_sha256'].items():check(ROOT/path,value)
        require(ledger_by[task['id']]['status']==row['status'] and ledger_by[task['id']]['implementation_status']==row['status'],'Ledger/result drift')
    require((core,adapted)==(56,2),'Mandatory B counts')
    preservation=read('B_scope_preservation');outside=[r for r in ledger['tasks'] if r['id'] not in set(preservation['allowed_current_ids'])]
    value=hashlib.sha256(json.dumps(outside,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    require(value==preservation['outside_scope_sha256'] and len(outside)==preservation['outside_scope_records'],'Prior task records changed')
    nested=read('B1_AUDIT')['nested_records'];require(len(nested)==37,'PA source coverage')
    for row in nested:require(ledger_by[row['id']]['status']==row['status'],'PA ledger/result drift')
    b2=read('B2_AUDIT');check(local(b2['source']),b2['sha256']);require(b2['core_tasks']==0,'Invented B2 tasks')
    final=read('B_final_selection');require(final['status']=='PASS_FINAL_CONFIGURATION_BOUND' and final['soc_variant']=='b5-release' and final['model_frequency_mhz']==325,'Final selection incomplete')
    for row in final['rtl']:check(ROOT/row['path'],row['sha256'])
    check(ROOT/final['netlist'],final['netlist_sha256'])
    frozen=read('B_runtime_export');require(frozen['status']=='PASS','Runtime not frozen');members=runtime_tar(frozen) if deep else len(frozen['members'])
    if not deep:check(ROOT/frozen['archive'],frozen['sha256'])
    bindings=read('B_final_bindings');require(bindings['status']=='PASS' and bindings['archive_sha256']==frozen['sha256'],'Frozen binding drift')
    frozen_files={r['path']:r for r in frozen['members'] if r['kind']=='file'}
    for row in bindings['authored_rtl']:check(ROOT/row['path'],row['sha256'])
    for row in bindings['binaries']:require(frozen_files[row['member']]['sha256']==row['sha256'],'Frozen binary changed')
    replay=read('B_offline_replay');require(replay['status']=='PASS' and replay['archive_sha256']==frozen['sha256'] and len(replay['runs'])==6,'Offline replay incomplete')
    for row in replay['runs']:
        for item in row['inputs']:require(frozen_files[item['member']]['sha256']==item['sha256'],'Replay input not in frozen archive')
    monitor=read('B_host_memory_monitor');require(monitor['status']=='PASS_FINAL_SESSION_STOPPED','Final host sampler did not stop')
    for session in monitor['sessions']:
        for file in session['files']:check(ROOT/file['path'],file['sha256'])
    analysis=read('B_performance_analysis');require(analysis['status']=='PASS' and not analysis['pending'],'Final analysis is incomplete')
    require(analysis['block_prediction'] is not None and len(analysis['blocks'])==3,'Block-size comparison missing')
    require(sum(analysis['final_classified_cache']['adjacent_control_pairs'].values())>0,'Final dynamic control-sequence coverage missing')
    for name,value in analysis['bindings'].items():check(ROOT/'reports'/f'{name}.json',value)
    documents=[ROOT/'reports/B_REPORT.md',ROOT/'reports/B_TASKS.md',ROOT/'B/offline/README.md']
    documents += [ROOT/f'B/{name}/NOTES.md' for name in ['B1','B3','B4','B5']]+[ROOT/'B/B3/RESULTS.md',ROOT/'B/B4/RESULTS.md']
    count=0
    for path in documents:
        require(path.is_file(),'Missing authored document: '+str(path));text=re.sub(r'```.*?```','',path.read_text('utf8'),flags=re.S)
        for match in re.finditer(r'!?\[[^\]]*\]\(([^\n)]+)\)',text):
            link=unquote(match[1].strip().strip('<>').split('#',1)[0])
            if not link or link.startswith(('http:','https:','mailto:')):continue
            target=Path(link);target=target if target.is_absolute() else path.parent/target
            if target.name=='B_AUDIT.json':continue
            require(target.exists(),'Broken authored link: '+str(path)+' -> '+link);count+=1
    final_reports=['B_results','B1_AUDIT','B1_coverage','B2_AUDIT','B3_AUDIT','B4_AUDIT','B5_AUDIT','B5_ACCEPTANCE','B4_full128','B_final_selection','B_final_bindings','B_toolchain_final','B_runtime_export','B_offline_replay','B_host_memory_monitor','B_scope_preservation','B_history_preservation','B_delivery_metadata','B_performance_analysis']
    result.update(scope={'core_tasks':56,'adapted_tasks':2,'B_source_records':110,'nested_PA_source_records':37,'stop_after':'B'},
        frozen={'runtime_members':members,'runtime_sha256':frozen['sha256'],'offline_replay_cases':6},authored_document_links_checked=count,
        final_report_bindings={name:sha(ROOT/'reports'/f'{name}.json') for name in final_reports})
    return result

def verify_zip(path,entries,manifest_sha256,current_files=True):
    manifest_name='reports/B_delivery_manifest.json'
    with zipfile.ZipFile(path) as archive:
        names=archive.namelist();require(len(names)==len(set(names)),'Duplicate ZIP member')
        for name in names:safe_member(name)
        require(set(names)=={r['path'] for r in entries}|{manifest_name},'ZIP entry set mismatch')
        blob=archive.read(manifest_name);require(hashlib.sha256(blob).hexdigest()==manifest_sha256,'Manifest hash')
        require(json.loads(blob)['entries']==entries,'Manifest content mismatch')
        for index,row in enumerate(entries):
            item=archive.getinfo(row['path']);require(item.file_size==row['bytes'],'ZIP size: '+row['path'])
            with archive.open(item) as stream:require(digest(stream)==row['sha256'],'ZIP SHA: '+row['path'])
            if current_files:check(ROOT/row['path'],row['sha256'])
            if (index+1)%10000==0:print('B_ZIP_MEMBERS_VERIFIED',index+1,flush=True)
    return {'status':'PASS','verified_entries':len(entries)+1,'crc_verified':True,'all_member_sha256_verified':True,'current_files_match':current_files}

def zip_controls():
    payload=b'B archive integrity control\n';correct=hashlib.sha256(payload).hexdigest();out={}
    for case,name,value,extra in [('valid','fixture.txt',correct,False),('bad_digest','fixture.txt','0'*64,False),('extra','fixture.txt',correct,True),('unsafe','../escape.txt',correct,False)]:
        row={'path':name,'bytes':len(payload),'sha256':value};blob=json.dumps({'entries':[row]}).encode();buffer=io.BytesIO()
        with zipfile.ZipFile(buffer,'w') as z:
            z.writestr(name,payload);z.writestr('reports/B_delivery_manifest.json',blob)
            if extra:z.writestr('extra.txt',b'unexpected')
        try:verify_zip(buffer,[row],hashlib.sha256(blob).hexdigest(),False)
        except ValueError:require(case!='valid','Valid B ZIP rejected');out[case+'_rejected']=True
        else:require(case=='valid','Invalid B ZIP accepted');out['valid_accepted']=True
    return out

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--preview',action='store_true');parser.add_argument('--deep',action='store_true');parser.add_argument('--accept-components',action='store_true');parser.add_argument('--final',action='store_true');parser.add_argument('--archive',type=Path);parser.add_argument('--output',type=Path);args=parser.parse_args()
    require(not args.final or not args.preview,'Final mode cannot allow pending work')
    result=final_project_checks(args.deep) if args.final else verify_project(args.deep,args.preview)
    if args.accept_components:
        require(set(result['checks'])=={'functional','B5','full_memory'},'Cannot accept incomplete components')
        require(all('host-memory-monitor' in x for x in result['pending']),'Other work remains pending')
        dump(ROOT/'reports/B5_ACCEPTANCE.json',result['checks']['B5']);dump(ROOT/'reports/B4_full128.json',result['checks']['full_memory'])
        prior=ROOT/'reports/B_final_selection.json';history=ROOT/'artifacts/B5/selection-history';history.mkdir(exist_ok=True)
        if prior.exists():shutil.copyfile(prior,history/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')+'.json'))
        timing=read('B5_final_timing');exported=read('B5_export')
        dump(prior,{'status':'PASS_FINAL_CONFIGURATION_BOUND','soc_variant':'b5-release','standalone_variant':'release','model_frequency_mhz':325,'apb_ratio_q':832,'axi_ratio_q':832,'padding':24,
            'rtl':exported['sources'],'exported_rtl_sha256':exported['sha256'],'netlist':'B/B5/netlist/ysyx_00000000.v','netlist_sha256':timing['netlist_sha256'],'area_um2':timing['area_um2'],
            'acceptance':{'B5':sha(ROOT/'reports/B5_ACCEPTANCE.json'),'full128':sha(ROOT/'reports/B4_full128.json'),'bounded_regressions':sha(ROOT/'reports/B_final_regressions.json')},
            'reason':'Best end-to-end time among measured325MHz pipeline candidates with the selected128B/8word/2way cache. Required forwarding and stated area/timing model pass. Not a global optimum: faster4word multicycle and higher-Fmax alternatives remain visible; the4word pipeline cost is only an explicitly labeled screening estimate.'})
    if args.archive:
        require(args.final,'Archive verification requires final scope');manifest=read('B_delivery_manifest')
        value=args.archive.with_suffix('.zip.sha256').read_text('ascii').split()[0];check(args.archive,value)
        result['archive']=verify_zip(args.archive,manifest['entries'],sha(ROOT/'reports/B_delivery_manifest.json'),True)
    target=args.output or ROOT/('temp/B_verification_preview.json' if args.preview else 'temp/B_verification_readonly.json');dump(target,result)
    print(json.dumps({'status':result['status'],'pending':result['pending'],'diagnostics':result['commands']['diagnostics'],'commands':result['commands']['counts'],'snapshots':result['commands']['snapshot_archives_verified']},ensure_ascii=False),flush=True)

if __name__=='__main__':main()
