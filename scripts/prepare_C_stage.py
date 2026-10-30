"""Freeze C requirements and advance only the shared ledger; preserve F/E/D."""
from evidence import *
import shutil,re
from collections import Counter

def main():
    arc=ROOT.parents[1]/'YSYX_F_B_Archive';stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
    ledger=json.loads((ROOT/'config/task_status.json').read_text('utf8'));rows=[x for x in ledger['tasks'] if re.match(r'^C[1-9]-',x['id'])]
    assert len(rows)==101 and all(x['status'] in ('NOT_RUN','EXCLUDED_SCOPE') for x in rows)
    assert not (ROOT/'C/runtime/course_specs.json').exists()
    backup=ROOT/'config/history'/('before_C_'+stamp);backup.mkdir(parents=True)
    for name in ('task_status.json','execution_policy.json','toolchain.json'):shutil.copyfile(ROOT/'config'/name,backup/name)
    sources=[]
    for n in range(1,7):
        stage=f'C{n}';source=arc/'docs/markdown/C'/f'{stage}.md';dest=ROOT/'C'/stage/'sources'/source.name;dest.parent.mkdir(parents=True)
        shutil.copyfile(source,dest);assert sha(dest)==sha(source)
        sources.append({'stage':stage,'source':str(source),'copy':str(dest),'sha256':sha(source),'raw_sha256':sha(arc/'docs/raw_html/C'/f'{stage}.html')})
    refs=[]
    for name,scope in [('c513b8fe1d21123b.md','PA2.5 complete, including mandatory PA2 report questions'),('43b650b773c2bef7.md','Only the C5-linked section on running AM applications in RT-Thread, not all PA4')]:
        source=arc/'references/markdown'/name;dest=ROOT/'C/runtime/sources/pa'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
        refs.append({'source':str(source),'copy':str(dest),'sha256':sha(source),'scope':scope})
    counts=dict(Counter(x['classification'] for x in rows))
    dump(ROOT/'C/runtime/course_specs.json',{'status':'FROZEN_REQUIREMENTS_NOT_VERDICT','tasks':rows,'sources':sources,'pa_sources':refs,'classification_counts':counts,'C6':'Original page is under construction, no invented task.'})
    previous=json.loads((ROOT/'reports/D_delivery_archive.json').read_text('utf8'));archive=ROOT/'YSYX_D_DELIVERY.zip';assert archive.stat().st_size==previous['bytes'];digest=sha(archive);assert digest==previous['sha256']
    dump(ROOT/'reports/C_baseline.json',{'status':'PASS','timestamp':stamp,'D_zip_sha256':digest,'D_audit_sha256':sha(ROOT/'reports/D_AUDIT.json'),'D_runtime_sha256':sha(ROOT/'D/offline/d-final-runtime.tar.gz'),'git_head':subprocess.check_output(['D:/Git/Git/cmd/git.exe','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),'scope_records':101,'classification_counts':counts,'preservation':'F/E/D frozen sources, runtime trees and ZIPs remain unchanged; C uses independent files.'})
    ledger.update(current_stage='C',stage_status='IN_PROGRESS',next_stage=None,stop_after='C',completion_scope=None);ledger.pop('completed_at',None);dump(ROOT/'config/task_status.json',ledger)
    path=ROOT/'config/execution_policy.json';policy=json.loads(path.read_text('utf8'));policy.update(current_scope='Complete C1-C5 public engineering and project-ID adaptations; source-scope audit C6. Preserve F/E/D and personal exclusions.',stop_after='C',user_resume='继续C阶段',source_instruction='2026-10-26 user authorized continuing C; supersedes stop after D.');dump(path,policy)
    common=(ROOT/'D/runtime/common.py').read_text('utf8').replace("WORK=Path('/home/USER/d-stage')","WORK=Path(os.environ.get('YSYX_C_WORK','/home/USER/c-stage'))").replace("ROOT/'reports/D_results.json'","ROOT/'reports/C_results.json'").replace('D_PREFLIGHT.json','C_PREFLIGHT.json')
    (ROOT/'C/runtime/common.py').write_text(common,encoding='utf8',newline='\n')
    for name in ('debug_core.c','debug_core.h','trace_core.c','trace_core.h'):shutil.copyfile(ROOT/'D/runtime'/name,ROOT/'C/runtime'/name)
    print('C_SCOPE_FROZEN',len(rows),counts,flush=True)

if __name__=='__main__':main()
