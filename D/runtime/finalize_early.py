from common import *

def main():
    for name in ['D1_experiments','D1_background','D2_expression','D2_sdb']:
        d=json.loads((ROOT/'reports'/f'{name}.json').read_text());assert d['status'].startswith('PASS'),name
    mark(['D1-O001'],'PASS',['D/D1/colorize.py','artifacts/D1/extras/colorizer'],'Small lexical highlighter distinguishes comments/strings/keywords/identifiers; stripping ANSI reproduces exact source bytes.')
    mark(['D2-M001'],'PASS',['D/D2/NOTES.md','D/runtime/sources/pa/5f9e9322a3fdd920.md'],'FAQ scope, debugging, manual use and official personal submission boundary documented.')
    mark(['D2-M002'],'PASS',['reports/D2_expression.json','reports/D2_sdb.json','D/D2/NOTES.md','D/D2/snapshot/manifest.json'],'PA1 SDB, uint32 expression grammar, actual GCC oracle 10000 cases, watchpoint pool and commit boundary tests, sanitizer runs, and all five required report topics.')
    mark(['D2-O001'],'PASS_BACKGROUND_REVIEW',['D/D2/NOTES.md','D/D2/sources/D2.md'],'MOOC supplement indexed; no claim of completing video courses.')
    records=json.loads((ROOT/'reports/D_results.json').read_text())['records'];specs=json.loads((ROOT/'D/runtime/course_specs.json').read_text())['tasks']
    for stage in ['D1','D2']:
        wanted=[x for x in specs if x['id'].startswith(stage+'-')];rs=[x for x in records if x['id'].startswith(stage+'-')];assert len(rs)==len(wanted) and all(x['status'].startswith('PASS') for x in rs)
        core=[x for x in wanted if x['classification']=='PUBLIC_CORE_TASK']
        audit={'status':'PASS','stage_complete':True,'core_tasks':len(core),'scope_records':len(rs),'records':rs,'report':'D/'+stage+'/NOTES.md','qualification':'Local engineering scope, not official course submission or learner mastery.'}
        dump(ROOT/'reports'/f'{stage}_AUDIT.json',audit)
    ledger=json.loads((ROOT/'config/task_status.json').read_text());mapping={x['id']:x for x in records}
    for row in ledger['tasks']:
        if row['id'] in mapping:row.update(status=mapping[row['id']]['status'],evidence=mapping[row['id']]['evidence'],result_details=mapping[row['id']]['details'])
    ledger.update(current_stage='D3',stage_status='IN_PROGRESS',stop_after='D');dump(ROOT/'config/task_status.json',ledger)
    print('D1_D2_COMPLETE',flush=True)

if __name__=='__main__':main()
