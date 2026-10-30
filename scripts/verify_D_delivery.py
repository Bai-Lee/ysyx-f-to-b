"""Read-only verification of retained D evidence, frozen sources and optional ZIP."""
from __future__ import annotations
import argparse,hashlib,json,posixpath,re,tarfile,zipfile
from pathlib import Path
from collections import Counter
from urllib.parse import unquote
from verify_E_delivery import (require,load,sha,digest,check_file,safe_member,
    verify_tar,check_zip_members,checker_controls)

ROOT=Path(__file__).resolve().parents[1]
CORE_COUNTS={'D1':16,'D2':2,'D3':1,'D4':0,'D5':1,'D6':28,'D7':1,'D8':6}
CHECKS=['D1_experiments','D1_background','D2_expression','D2_sdb','D3_isa','D3_official_tests',
 'D5_headers','D5_host_klib','D5_allocator','D5_portable','D6_logic','D6_pdk','D6_pvt',
 'D7_trace','D7_regression','D8_reference','D8_reset','D8_front','D8_isa','D8_official_tests',
 'D8_apps_test','D8_apps_train','D8_extra','D8_fileio','D8_alu','D8_prior_tests','D8_timer',
 'D8_fceux_native','D8_fceux_ascii','D8_native_keyboard','D_runtime_export','D_offline_sources',
 'D_final_bindings','D_toolchain_final','D_visual_review','D_history_preservation']

def local_path(text):
    s=str(text).replace('\\','/')
    for prefix in ('/workspace/projects/ysyx_f_to_b/','/workspace/projects/ysyx_f_to_b/'):
        if s.startswith(prefix):return ROOT/s[len(prefix):]
    p=Path(s)
    return p if p.is_absolute() else ROOT/p

def runtime_tar(data):
    path=ROOT/data['archive'];check_file(path,data['sha256'])
    rows={r['path']:r for r in data['members']};require(len(rows)==len(data['members']),'Duplicate frozen members')
    seen=set()
    with tarfile.open(path,'r|gz') as tar:
        for m in tar:
            safe_member(m.name);require(m.name in rows and m.name not in seen,'Unexpected/duplicate frozen member: '+m.name)
            seen.add(m.name);r=rows[m.name]
            if r['kind']=='symlink':
                resolved=posixpath.normpath(posixpath.join(posixpath.dirname(m.name),m.linkname))
                require(m.issym() and m.linkname==r['target'] and not m.linkname.startswith('/') and not resolved.startswith('../'),'Invalid frozen symlink: '+m.name)
            else:
                require(m.isfile() and m.size==r['bytes'],'Frozen member type/size: '+m.name)
                with tar.extractfile(m) as f:require(digest(f)==r['sha256'],'Frozen member hash: '+m.name)
    require(seen==set(rows),'Missing frozen source')
    return len(rows)

def markdown_links(external):
    docs=[ROOT/'README.md',ROOT/'reports/D_REPORT.md',ROOT/'reports/D_TASKS.md',ROOT/'D/offline/README.md',ROOT/'D/D9/SCOPE.md',ROOT/'D/runtime/README.md']
    docs += [ROOT/f'D/D{n}/NOTES.md' for n in range(1,9)]
    count=0;outside=[]
    for p in docs:
        require(p.is_file(),'Missing document: '+str(p))
        text=re.sub(r'```.*?```','',p.read_text('utf8'),flags=re.S)
        for m in re.finditer(r'!?\[[^\]]*\]\(([^\n)]+)\)',text):
            link=m[1].strip().strip('<>')
            if not link or link.startswith(('#','https:','http:','mailto:')):continue
            target=Path(unquote(link.split('#',1)[0]));target=target if target.is_absolute() else p.parent/target
            target=target.resolve()
            if not target.is_relative_to(ROOT.resolve()):
                outside.append(str(target))
                if not external:continue
            require(target.exists(),f'Broken Markdown target: {p}: {link}');count+=1
    return {'documents':len(docs),'resolved_links':count,'external_reference_paths':sorted(set(outside)),'scope':'File targets, not full math/Markdown rendering.'}

def command_evidence():
    total=negatives=snapshots=0;changed=[];history=Counter();unaccepted=[]
    dirs=[p for p in (ROOT/'artifacts').iterdir() if re.fullmatch(r'D[1-9]?',p.name) and p.is_dir()]
    for directory in dirs:
        for p in directory.rglob('run.json'):
            r=load(p)
            if 'attempts' in p.relative_to(directory).parts:
                history[r.get('status','UNKNOWN')]+=1;continue
            accepted=r.get('status','').startswith('PASS')
            if not accepted:
                require(p.relative_to(ROOT).as_posix()=='artifacts/D/downloads/capstone/resolve/run.json' and r.get('status')=='FAIL' and r.get('exit_code')==128,'Undeclared unaccepted command: '+str(p))
                unaccepted.append({'path':p.relative_to(ROOT).as_posix(),'status':'FAIL','exit_code':128,'resolution':'Git transport failed. Official HTTPS archive at the resolved commit was acquired and hashed separately in D_additional_sources/D_offline_sources. This command is not counted as PASS.'})
            else:total+=1
            for kind in ('stdout','stderr'):
                if kind+'_sha256' in r:check_file(p.parent/(kind+'.log'),r[kind+'_sha256'])
            if accepted and r.get('exit_code') not in (None,0):
                expected=r.get('expected_exit')
                if isinstance(expected,int):expected=[expected]
                require(expected is not None and r['exit_code'] in expected,'Unexpected command failure: '+str(p))
                negatives+=1
            if r.get('inputs_after') and r.get('inputs')!=r['inputs_after']:
                changed.append({'path':p.relative_to(ROOT).as_posix(),'reason':'Build input may be generated or deliberately mutated; before/after and snapshot retained.'})
            for name,field in [('input_snapshot.zip','inputs'),('output_snapshot.zip','outputs')]:
                archive=p.parent/name
                if not archive.exists():continue
                expected=[x for x in r.get(field,[]) if x.get('sha256')]
                with zipfile.ZipFile(archive) as z:
                    # ZipExtFile checks CRC on a complete read below; avoid a
                    # second decompression of every large input snapshot.
                    names=z.namelist();require(len(names)==len(set(names))==len(expected),'Snapshot count/duplicates: '+str(archive))
                    for member,row in zip(names,expected):
                        safe_member(member)
                        with z.open(member) as f:require(digest(f)==row['sha256'],'Snapshot SHA mismatch: '+str(archive)+':'+member)
                snapshots+=1
    return {'current_accepted_commands':total,'expected_nonzero_controls':negatives,'snapshot_archives_verified':snapshots,'changed_inputs_recorded':changed,'historical_attempt_status_counts':dict(history),'unaccepted_diagnostic_commands':unaccepted,'scope':'Current command acceptance and retained byte integrity. Historical failures stay visible; diagnostic extra DFF failure is separately declared.'}

def verify_project(external=False,require_final=True):
    specs=load(ROOT/'D/runtime/course_specs.json');result=load(ROOT/'reports/D_results.json');records={x['id']:x for x in result['records']}
    require(len(records)==len(result['records'])==103,'D record count/duplicates')
    require(set(records)=={x['id'] for x in specs['tasks']},'D frozen scope mismatch')
    core=[x for x in specs['tasks'] if x['classification']=='PUBLIC_CORE_TASK']
    require(len(core)==55 and all(records[x['id']]['status'].startswith('PASS') for x in core),'Core work incomplete')
    require(records['D6-M027']['status']=='EXCLUDED_SCOPE','Official todo scope changed')
    require(records['D6-O016']['status']=='SOURCE_CLAIM_NOT_ADOPTED','Unsupported source claim was adopted')
    ledger=load(ROOT/'config/task_status.json');tasks={x['id']:x for x in ledger['tasks']}
    require(ledger['current_stage']=='D' and ledger['stage_status']=='COMPLETE_ENGINEERING_WITH_DECLARED_LIMITS','D terminal state mismatch')
    require(load(ROOT/'config/execution_policy.json')['stop_after']=='D','Stop boundary changed')
    for key,row in records.items():
        require(tasks[key]['status']==row['status'] and row['evidence'],'Ledger/evidence mismatch: '+key)
        for item in row['evidence']:require(local_path(item).exists(),'Missing evidence: '+item)
    audits={}
    for stage,count in CORE_COUNTS.items():
        p=ROOT/f'reports/{stage}_AUDIT.json';a=load(p)
        require(a['status']=='PASS' and a['stage_complete'] and a['core_tasks']==count,'Stage incomplete: '+stage)
        require({r['id']:r for r in a['records']}=={k:r for k,r in records.items() if k.startswith(stage+'-')},'Stage records mismatch: '+stage)
        audits[stage]={'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
    require(load(ROOT/'reports/D9_AUDIT.json')['core_tasks']==0,'Invented D9 task')
    data={name:load(ROOT/f'reports/{name}.json') for name in CHECKS}
    require(all(r['status'].startswith('PASS') for r in data.values()),'Required evidence report not PASS')
    for name,field,value in [('D2_expression','random_expressions',10000),('D3_isa','checks',2392),('D3_official_tests','positive_count',81),('D5_host_klib','comparisons',21199),('D5_allocator','random_operations',10000),('D7_regression','program_count',81),('D8_isa','case_count',1758),('D8_official_tests','positive_count',73),('D8_apps_test','runs',48),('D8_apps_train','runs',20),('D8_prior_tests','case_count',12)]:
        require(data[name][field]==value,f'{name} coverage changed')
    require(data['D7_trace']['addi_mutant']['result']=='ABORT' and data['D7_trace']['addi_mutant']['instructions']==2,'NEMU mutation not detected')
    front=data['D8_front'];require(front['rtl_addi_mutant']['result']=='DIFF_FAIL' and front['rtl_addi_mutant']['instructions']==2,'RTL mutation not detected')
    require(len(front['negative_encodings'])==7 and any(r['name']=='wrong' and r['make_exit']==2 for r in front['am']),'Missing RV32E negative controls')
    require(data['D6_pdk']['dff_raw_switch_probe']['status']=='FAIL_UNQUALIFIED_MODEL','Extra DFF failure concealed')
    check_file(ROOT/'D/D8/rv32e_core.sv',data['D8_reset']['rtl_sha256'])
    check_file(ROOT/'D/klib_overlay/alloc.c',data['D5_allocator']['implementation_sha256'])
    check_file(ROOT/'D/klib_overlay/fileio.c',data['D8_fileio']['source_sha256'])
    frozen=data['D_runtime_export'];source_by_path={r['source']:r for r in frozen['members'] if r['kind']=='file'}
    for row in data['D_final_bindings']['authored_current_sources']:
        check_file(ROOT/row['path'],row['sha256'])
        require(source_by_path[row['runtime_source']]['sha256']==row['runtime_sha256'],'Frozen source binding mismatch')
    for name in ('D8_apps_test','D8_apps_train'):
        for row in data[name]['rows']:
            require(row['status']=='PASS','Application failed')
            for item in row['inputs']:
                if item['path'] in source_by_path:require(source_by_path[item['path']]['sha256']==item['sha256'],'Application ran different final source: '+item['path'])
            for item in row['saved']:check_file(local_path(item['path']),item['sha256'])
            if 'simulation' in row:
                r=row['simulation'];require(r['result']=='GOOD_TRAP' and r['diff_enabled'] and r['diff_checked']+r['device_sync_checked']==r['instructions'],'Application differential coverage mismatch')
    for row in data['D8_official_tests']['programs']:
        r=row['simulation'];require(r['result']=='GOOD_TRAP' and r['diff_enabled'] and r['diff_checked']+r['device_sync_checked']==r['instructions'],'Official differential coverage mismatch')
    for row in specs['sources']:
        check_file(local_path(row['copy']),row['sha256'])
        if external:check_file(Path(row['source']),row['sha256'])
    # PA source list is stored separately from the nine chapter source copies.
    pa=specs.get('pa_sources',[])
    for row in pa:
        check_file(local_path(row['copy']),row['sha256'])
        if external:check_file(Path(row['source']),row['sha256'])
    for row in data['D_offline_sources']['repositories']:check_file(ROOT/row['delivery_path'],row['sha256'])
    pa1=load(ROOT/'D/D2/snapshot/manifest.json');check_file(ROOT/'D/D2/snapshot/nemu-pa1.tar.gz',pa1['archive_sha256'])
    pa1_count=verify_tar(ROOT/'D/D2/snapshot/nemu-pa1.tar.gz',pa1['members'])
    runtime_count=runtime_tar(frozen)
    for row in data['D_visual_review']['images']:check_file(ROOT/row['path'],row['sha256'])
    for row in data['D_history_preservation']['preserved_files']:check_file(ROOT/row['path'],row['sha256'])
    if external:check_file(ROOT/'YSYX_E_DELIVERY.zip',load(ROOT/'reports/D_baseline.json')['E_zip_sha256'])
    verification={'status':'PASS','verification_kind':'read-only retained evidence, not rerun simulation','checker_controls':checker_controls(),'stage_audits':audits,'scope':{'core_passed':55,'records':103,'statuses':dict(Counter(r['status'] for r in records.values()))},'checks':{name:sha(ROOT/f'reports/{name}.json') for name in CHECKS},'frozen_members':{'PA1':pa1_count,'final_runtime':runtime_count},'source_copies_checked':len(specs['sources'])+len(pa),'commands':command_evidence(),'markdown':markdown_links(external)}
    if require_final:
        final=load(ROOT/'reports/D_AUDIT.json');require(final['status']=='PASS' and final['stage_complete'],'D audit incomplete')
        require(final['verification']['stage_audits']==audits and final['verification']['checks']==verification['checks'],'Evidence changed after acceptance')
    return verification

def verify_delivery(path):
    path=Path(path);receipt=load(ROOT/'reports/D_delivery_archive.json');check_file(path,receipt['sha256'])
    require(path.with_suffix('.zip.sha256').read_text().split()[0]==receipt['sha256'],'Sidecar digest mismatch')
    name='reports/D_delivery_manifest.json'
    with zipfile.ZipFile(path) as z:
        blob=z.read(name);require(hashlib.sha256(blob).hexdigest()==receipt['manifest_sha256'],'Manifest mismatch')
        manifest=json.loads(blob);check_zip_members(z,manifest['entries'],extras=(name,))
        for row in manifest['entries']:check_file(ROOT/row['path'],row['sha256'])
    return {'status':'PASS','sha256':receipt['sha256'],'verified_entries':len(manifest['entries'])+1,'crc_and_all_sha256':True,'current_files_match':True}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--external',action='store_true');p.add_argument('--archive',type=Path);p.add_argument('--pre-final',action='store_true');args=p.parse_args()
    result=verify_project(args.external,not args.pre_final)
    if args.archive:result['delivery']=verify_delivery(args.archive)
    print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)

if __name__=='__main__':main()
