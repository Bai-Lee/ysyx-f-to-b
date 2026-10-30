"""Freeze B scope and preserve the completed C checkpoint before new work."""
from evidence import *
from collections import Counter
import re,shutil


def main():
    workspace=ROOT.parents[1];archive_root=workspace/'YSYX_F_B_Archive';runtime=ROOT/'B/runtime'
    assert not (runtime/'course_specs.json').exists(),'B scope already prepared; resume it instead.'
    ledger=json.loads((ROOT/'config/task_status.json').read_text('utf8'))
    rows=[r for r in ledger['tasks'] if re.fullmatch(r'B[1-5]-[MOR]\d+',r['id'])]
    assert len(rows)==110 and all(r['status'] in ['NOT_RUN','EXCLUDED_SCOPE'] for r in rows)
    counts=dict(Counter(r['classification'] for r in rows));assert counts['PUBLIC_CORE_TASK']==56 and counts['USER_ADAPTED']==2
    receipt=json.loads((ROOT/'reports/C_delivery_archive.json').read_text('utf8'));oldzip=ROOT/'YSYX_C_DELIVERY.zip'
    assert oldzip.stat().st_size==receipt['bytes'];print('CHECKING_FROZEN_C_ZIP',flush=True)
    digest=sha(oldzip);assert digest==receipt['sha256'];print('C_ZIP_SHA256_MATCH',flush=True)
    exported=json.loads((ROOT/'reports/C_runtime_export.json').read_text('utf8'));assert sha(ROOT/exported['archive'])==exported['sha256']
    manifest=json.loads((ROOT/'reports/C_delivery_manifest.json').read_text('utf8'));entries={r['path']:r for r in manifest['entries']}
    assert sha(ROOT/'reports/C_AUDIT.json')==entries['reports/C_AUDIT.json']['sha256']
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f');backup=ROOT/'config/history'/('before_B_'+stamp);backup.mkdir(parents=True)
    protected={'task_status.json':ROOT/'config/task_status.json','execution_policy.json':ROOT/'config/execution_policy.json','toolchain.json':ROOT/'config/toolchain.json',
        'project_README.md':ROOT/'README.md','workspace_README.md':workspace/'README.md','workspace_AGENTS.md':workspace/'AGENTS.md','workspace_toolchain.json':workspace/'config/toolchain.lock.json'}
    for name,path in protected.items():shutil.copyfile(path,backup/name)
    sources=[]
    for n in range(1,6):
        stage=f'B{n}';source=archive_root/'docs/markdown/B'/f'{stage}.md';target=ROOT/'B'/stage/'sources'/source.name
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target);assert sha(target)==sha(source)
        sources.append({'stage':stage,'source':str(source),'copy':str(target.relative_to(ROOT)),'sha256':sha(source),
            'raw_sha256':sha(archive_root/'docs/raw_html/B'/f'{stage}.html'),'version':'v23.06 linked by v26.07 index' if n==5 else 'v26.07'})
    pa_sources=[]
    for name,scope in [('e1ded88f69aa05c5.md','PA3.1 conceptual introduction'),('9501e9e16aaf5adf.md','PA3.2 through PA3 stage1 completion marker'),('43b650b773c2bef7.md','PA4.1 through RT-Thread startup; no subsequent Nanos-lite/execve/BusyBox scope')]:
        source=archive_root/'references/markdown'/name;target=runtime/'sources/pa'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
        pa_sources.append({'source':str(source),'copy':str(target.relative_to(ROOT)),'sha256':sha(source),'scope':scope})
    nested=[r for r in ledger['tasks'] if r['id'].startswith(('PA-3.1-','PA-3.2-','PA-4.1-'))]
    dump(runtime/'course_specs.json',{'status':'FROZEN_REQUIREMENTS_NOT_VERDICT','tasks':rows,'classification_counts':counts,'sources':sources,'pa_sources':pa_sources,
        'nested_source_records':nested,'scope_notes':['B2 is under construction with no programming task.','B5 is the old v23.06 page actually linked by the v26.07 index, not a newly published v26.07 tapeout specification.','Official identity/whitelist/submission/exam remain excluded; public local technical checks are implemented.','B3/B4 must satisfy workload-driven cache/pipeline evaluation and the stated Nangate45 area bound; C timing limitations are not promoted into B frequency qualification.']})
    dump(ROOT/'reports/B_baseline.json',{'status':'PASS','timestamp':stamp,'C_zip_sha256':digest,'C_zip_bytes':receipt['bytes'],
        'C_audit_sha256':sha(ROOT/'reports/C_AUDIT.json'),'C_runtime_sha256':exported['sha256'],'C_manifest_sha256':sha(ROOT/'reports/C_delivery_manifest.json'),
        'git_head':subprocess.check_output(['D:/Git/Git/cmd/git.exe','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),
        'scope_records':110,'core_tasks':56,'adapted_tasks':2,'classification_counts':counts,'backup':str(backup),
        'preservation':'F/E/D/C sources, reports, accepted binaries and delivery ZIPs remain unchanged. B uses independent source/runtime copies.'})
    ledger.update(current_stage='B',stage_status='IN_PROGRESS',next_stage=None,stop_after='B',completion_scope=None)
    dump(ROOT/'config/task_status.json',ledger)
    path=ROOT/'config/execution_policy.json';policy=json.loads(path.read_text('utf8'))
    policy.update(current_scope='Complete B1/B3/B4/B5 public engineering, source-scope B2, preserving F/E/D/C and personal/official exclusions.',stop_after='B',
        source_instruction='2026-10-29 user explicitly authorized completing B with the current parallel/memory strategy.',user_resume='继续完成B阶段，沿用现在的并行和内存策略。')
    policy['resource_policy'].update(scope='Active B runs; inherit max8 independent validated simulations in one6GiBPSS group, adaptive memory admission, -j4 builds; synthesis/generation one at a time.',execution_guard='B/runtime/budget_exec.py',B_compile_jobs=4)
    dump(path,policy)
    path=workspace/'config/toolchain.lock.json';lock=json.loads(path.read_text('utf8'));lock['limits']['B_parallel_validation']=dict(lock['limits']['C_parallel_validation']);lock['limits']['B_jvm_heap_MiB']=lock['limits']['C_jvm_heap_MiB']
    lock['workspace_state'].update(phase='research_project_in_progress',research_task='ysyx_f_to_b B public engineering',current_project_status='B_IN_PROGRESS')
    lock['project_toolchains']['ysyx_f_to_b'].update(status='B_IN_PROGRESS',current_preflight=str(ROOT/'reports/B_PREFLIGHT.json'),note='B authorized with C parallel/resource strategy; completed C audit and fingerprint references remain historical until B acceptance.')
    lock['last_updated_utc']=datetime.now(timezone.utc).isoformat();dump(path,lock)
    path=workspace/'AGENTS.md';text=path.read_text('utf8').replace('C 阶段新构建使用 -j4','C/B 阶段新构建使用 -j4').replace('C 阶段按进程组 PSS 采样','C/B 阶段按进程组 PSS 采样');path.write_text(text,encoding='utf8')
    for path in [ROOT/'README.md',workspace/'README.md']:
        text=path.read_text('utf8');first,tail=text.split('\n\n',1)
        note='用户已授权继续 B 阶段，当前正在独立 B 工作台推进，沿用最多 8 路独立仿真、合计 6 GiB PSS 与 `-j4` 构建策略。已完成的 C 交付与旧阶段证据保留。'
        text=first+'\n\n'+note+'\n\n'+tail.replace('工程止于 C，未进入 B','这是 C 完成时的历史停点；当前已获准进入 B').replace('当前授权止于 C','当前授权止于 B')
        path.write_text(text,encoding='utf8')
    excluded=[{'id':r['id'],'status':'EXCLUDED_SCOPE','evidence':['B/runtime/course_specs.json'],'details':'Personal/official identity, application, whitelist or examination is excluded. Public local engineering requirements are tracked separately.'} for r in rows if r['status']=='EXCLUDED_SCOPE']
    dump(ROOT/'reports/B_results.json',{'status':'IN_PROGRESS','records':excluded})
    source=ROOT/'B/B2/sources/B2.md'
    dump(ROOT/'reports/B2_AUDIT.json',{'status':'PASS_SOURCE_SCOPE_RECONCILED','stage_complete':True,'core_tasks':0,'scope_records':0,'source':str(source.relative_to(ROOT)),
        'sha256':sha(source),'scope':'Frozen v26.07 source says under construction, no programming content. No invented B2 task.'})
    dump(ROOT/'temp/B-workstate.json',{'stage':'B_PREFLIGHT','status':'IN_PROGRESS','scope':'56 public core +2 ID adaptations,110 source records; B2 construction; B5 linked oldv23.06; personal/official processes excluded.',
        'work':'/home/USER/b-stage','running_jobs':[],'completed':['B source freeze','C ZIP/runtime/audit baseline checked'],'remaining':['B tool/runtime preflight','B1 NEMU trap/CTE/RTThread and NPCmcycle','B3 counters/calibration/icache/burst/DSE/fence.i','B4 pipeline/forwarding/branch analysis/fence.i','B5 static/four-state/netlist/local compatibility checks','full B audit/package'],
        'important':'Do not modify completed C or earlier sources. Inherit aggregate6GiBPSS/max8 independent tests and robust append-only nativeWindows memory telemetry in B-owned paths.'})
    print('B_SCOPE_FROZEN',len(rows),counts,flush=True)


if __name__=='__main__':main()
