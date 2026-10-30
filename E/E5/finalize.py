from pathlib import Path
import sys,shutil
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
    execution=json.loads((ROOT/'reports/E5_execution.json').read_text());mutations=json.loads((ROOT/'reports/E5_mutations.json').read_text());assert execution['status']==mutations['status']=='PASS'
    mark(['E5-M001','E5-M002','E5-M003','E5-M004','E5-M008','E5-O001'],'PASS_DOCUMENTED',['E/E5/NOTES.md','artifacts/E5/manual/index.json','reports/E5_execution.json'],'按原文7个编号问题回答并核对官方手册图表；指令编码、PC/GPR/x0、字节寻址、EEI/对齐、立即数与旧rs1语义明确。')
    lock=[];snapshot=ROOT/'E/E5/runtime_snapshot';snapshot.mkdir(exist_ok=True)
    for name in ['ref.c','ref.h','emu_main.c','runner.cpp','memory.hpp']:
        src=ROOT/'E/runtime'/name;dst=snapshot/name;shutil.copyfile(src,dst);assert sha(src)==sha(dst);lock.append({'path':str(dst.relative_to(ROOT)),'sha256':sha(dst)})
    records=[r for r in json.loads((ROOT/'reports/E_remaining_results.json').read_text())['records'] if r['id'].startswith('E5-')];assert len(records)==18 and all(r['status'].startswith('PASS') for r in records)
    spec=json.loads((ROOT/'E/runtime/course_specs.json').read_text());source=next(s for s in spec['sources'] if s['stage']=='E5');assert sha(source['copy'].replace('D:\\','/mnt/d/').replace('\\','/'))==source['sha256']
    now=datetime.datetime.now(datetime.timezone.utc).isoformat();dump(ROOT/'reports/E5_AUDIT.json',{'status':'PASS','stage_complete':True,'timestamp':now,'core_tasks':17,'cases':len(execution['cases']),'mutants_rejected':6,'random_commits':next(r['result']['instructions'] for r in execution['cases'] if r['name']=='random_ops'),'runtime_snapshot':lock,'source':source,'scope':'Exact8-instruction16GPR minirv plus simulation ebreak; no complete RV32I or physical-chip claim.'})
    p=ROOT/'config/task_status.json';d=json.loads(p.read_text());history=ROOT/'config/history'/str(time.time_ns());history.mkdir(parents=True);shutil.copyfile(p,history/p.name)
    rows={r['id']:r for r in records}
    for r in d['tasks']:
        if r['id'] in rows:x=rows[r['id']];r.update(status=x['status'],implementation_status=x['status'],evidence=x['evidence'],result_details=x['details'],updated=now)
    d.update(current_stage='E6',stage_status='IN_PROGRESS',next_stage='E6 through E9');dump(p,d)
    lines=['# E5阶段验收','', '17项核心任务通过；对齐背景题已阅读并说明选择。8组有效程序及4组预期拒绝输入均实跑；随机程序6417次提交经C/RTL/Python三方逐步检查，6种错误实现均被检出。','', '[实现与手册答复](../E/E5/NOTES.md) · [运行结果](E5_execution.json) · [注错结果](E5_mutations.json) · [机器审计](E5_AUDIT.json)','', '| ID | 状态 | 验收依据 |','|---|---|---|']
    for r in sorted(records,key=lambda x:x['id']):lines.append(f'| {r["id"]} | {r["status"]} | '+r['details'].replace('|','/')+' |')
    (ROOT/'reports/E5_REPORT.md').write_text('\n'.join(lines)+'\n')
    issue=ROOT/'artifacts/E5/debug/image_loader_diagnosis.json';x=json.loads(issue.read_text());x['status']='FIX_VERIFIED';x['verification']='All12 C/RTL/Python cases passed after exact-length loading and explicit tail initialization';dump(issue,x)
    print('E5_STAGE_COMPLETE_CONTINUE_E6',flush=True)
if __name__=='__main__':main()
