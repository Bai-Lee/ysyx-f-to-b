"""Final F-stage audit. Verify real report semantics and current input hashes."""
from evidence import *
import re,collections,zipfile
from markdown_it import MarkdownIt
from urllib.parse import urlsplit,unquote

def main():
    task=json.loads((ROOT/'config/task_status.json').read_text('utf8'));policy=json.loads((ROOT/'config/execution_policy.json').read_text('utf8'));checks=[];errors=[]
    def check(name,ok,detail):
        checks.append({'check':name,'status':'PASS' if ok else 'FAIL','detail':detail})
        if not ok:errors.append(name)
    source=Path(task['source']);check('source_inventory_unchanged',source.exists() and sha(source)==task['source_sha256'],str(source))
    fs=[x for x in task['tasks'] if re.fullmatch(r'F[1-6]-M\d{3}',x['id'])];required=[x for x in fs if x['status']!='EXCLUDED_SCOPE']
    check('64_required_technical_tasks',len(fs)==67 and len(required)==64 and all(x['status'].startswith('PASS') for x in required),dict(collections.Counter(x['status'] for x in fs)))
    check('state_fields_consistent',all(x['implementation_status']==x['status'] for x in task['tasks']),len(task['tasks']))
    future=[x for x in task['tasks'] if not x['id'].startswith('F') and x['status'].startswith('PASS')]
    check('no_E_to_B_started',not future and all(not any(p.is_file() for p in (ROOT/s).rglob('*')) for s in ('E','D','C','B')),future)
    check('stop_after_F_and_no_GUI',policy.get('stop_after')=='F' and policy.get('advance_to_E') is False and policy.get('allow_logisim_gui') is False,policy)
    evidence=[]
    for x in task['tasks']:
        if x['id'].startswith('F') and x['status'].startswith('PASS'):
            for p in x['evidence']:
                if not (ROOT/p).is_file():evidence.append({'id':x['id'],'missing':p})
    check('each_pass_has_evidence',not evidence,evidence)
    summary=json.loads((ROOT/'reports/F_stage_summary.json').read_text('utf8'));reports={p:json.loads((ROOT/'reports'/p).read_text('utf8')) for p in summary['evidence_reports']}
    check('all_evidence_reports_pass',all(r['status'] in ('PASS','PASS_ADAPTED') for r in reports.values()),{p:r['status'] for p,r in reports.items()})
    native=reports['F_circuit_results.json'];check('native_33_circuits_25753_vectors',len(native['jobs'])==33 and sum(x['rows'] for x in native['jobs'])==25753 and all(x['result']['status']=='PASS' for x in native['jobs']),len(native['jobs']))
    cpu=reports['F_cpu_results.json'];entries=cpu['results'];fw=[x for x in entries.values() if 'cycles' in x and not x.get('fault')];units=[x for x in entries.values() if 'cases' in x]
    check('CPU_case_counts',len(fw)==23 and sum(x['cases'] for x in units)==32768,{'normal_firmware':len(fw),'firmware_cycles':sum(x['cycles'] for x in fw),'isa_samples':sum(x['cases'] for x in units),'checks':len(entries)})
    failed_controls=[]
    for name,row in entries.items():
        if not name.startswith('reject_'):continue
        runrow=row['simulation'];p=ROOT/'artifacts'/runrow['name']/'stdout.log'
        if not(runrow['exit_code']==1 and row['status']=='PASS' and 'MISMATCH' in p.read_text('utf8')):failed_controls.append(name)
    check('four_actual_DUT_fault_rejections',sum(k.startswith('reject_') for k in entries)==4 and not failed_controls,failed_controls)
    check('hold_release_behavior_independent_check',entries['step_release'].get('independent_behavior_check','').startswith('PASS'),entries['step_release'].get('independent_behavior_check'))
    # Compare every current positive input and run log, not historic failed attempts.
    current=[]
    current += [x['result'] for x in native['jobs']]
    for entry in entries.values():
        if 'compile' in entry:current.append(entry['compile'])
        if 'simulation' in entry:current.append(entry['simulation'])
        if 'command' in entry:current.append(entry)
    seen=set();mismatches=[];hashcache={};logs=[]
    for r in current:
        key=(r['name'],r['timestamp'])
        if key in seen:continue
        seen.add(key)
        for x in r.get('inputs',[]):
            p=Path(x['path'])
            if p not in hashcache and p.is_file():hashcache[p]=sha(p)
            if not p.exists() or hashcache.get(p)!=x['sha256']:mismatches.append({'run':r['name'],'path':str(p)})
        for filename,field in [('stdout.log','stdout_sha256'),('stderr.log','stderr_sha256')]:
            p=ROOT/'artifacts'/r['name']/filename
            if not p.exists() or sha(p)!=r[field]:logs.append(str(p))
        if r.get('inputs_unchanged') is not True:mismatches.append({'run':r['name'],'reason':'input pre/post check not true'})
    check('final_hardware_inputs_and_logs_match',not mismatches and not logs,{'commands':len(seen),'unique_inputs':len(hashcache),'input_mismatches':mismatches,'log_mismatches':logs})
    online=json.loads((ROOT/'reports/F4_results.json').read_text('utf8'))
    check('real_online_C_execution',all(online['online'][n]['didExecute'] and online['online'][n]['status']=='PASS' for n in ('z3','z42','sum10_c')),online['online'])
    ce=[]
    for name,entry in online['online'].items():
        for suffix,key in [('request','request_sha256'),('response','response_sha256')]:
            p=ROOT/'artifacts/F4/compiler_explorer'/(name+'_'+suffix+'.json')
            if sha(p)!=entry[key]:ce.append(str(p))
    check('Compiler_Explorer_evidence_hashes',not ce,ce)
    mdparser=MarkdownIt('commonmark',{'html':True}).enable('table');broken=[];references=0
    for p in list((ROOT/'F/notes').glob('*.md'))+[ROOT/'README.md',ROOT/'reports/F_STAGE_REPORT.md']:
        def visit(ts):
            nonlocal references
            for t in ts:
                if t.type in ('link_open','image'):
                    url=t.attrGet('href') or t.attrGet('src')
                    if url and not urlsplit(url).scheme and not url.startswith('#'):
                        references+=1;target=(p.parent/unquote(urlsplit(url).path)).resolve()
                        if not target.exists():broken.append({'page':str(p),'link':url})
                if t.children:visit(t.children)
        visit(mdparser.parse(p.read_text('utf8')))
    check('delivery_links',not broken,{'references':references,'broken':broken})
    status='PASS' if not errors else 'FAIL';result={'timestamp':datetime.now(timezone.utc).isoformat(),'status':status,'checks':checks,'failures':errors,'scope':'F only; required technical tasks plus explicitly selected optional work; no official qualification or physical signoff claim'}
    dump(ROOT/'reports/F_final_audit.json',result)
    if status=='PASS':
        task['stage_status']='F_COMPLETE';dump(ROOT/'config/task_status.json',task);summary['status']='F_COMPLETE';summary['final_audit']='reports/F_final_audit.json';summary['completed_utc']=result['timestamp'];dump(ROOT/'reports/F_stage_summary.json',summary)
        p=ROOT/'reports/F_STAGE_REPORT.md';text=p.read_text('utf8').replace('实现闭环已完成，等待最终文件审计。','F阶段必做技术任务已完成，最终文件审计PASS。');text+='\n\n最终审计：`F_final_audit.json`，所有检查PASS；已停止在F，等待用户更换模型。\n';p.write_text(text,encoding='utf8')
        p=ROOT/'README.md';p.write_text(p.read_text('utf8').replace('F阶段已实现，等待最终审计','F阶段已完成并通过最终审计'),encoding='utf8')
    print('F_FINAL_AUDIT',status,'failures',errors,flush=True)
    if status!='PASS':
        for c in checks:
            if c['status']=='FAIL':print(c['check'],str(c['detail'])[:3500],flush=True)
    return 0 if status=='PASS' else 1
if __name__=='__main__':sys.exit(main())
