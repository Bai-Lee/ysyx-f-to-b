"""Synchronize the C progress records without changing F/E/D/B task states."""
from evidence import *


def main():
    result=json.loads((ROOT/'reports/C_results.json').read_text('utf8'));rows={row['id']:row for row in result['records']}
    specs=json.loads((ROOT/'C/runtime/course_specs.json').read_text('utf8'));expected={row['id'] for row in specs['tasks']}
    assert set(rows)<=expected and len(rows)==len(result['records'])
    path=ROOT/'config/task_status.json';ledger=json.loads(path.read_text('utf8'));before={row['id']:row for row in ledger['tasks'] if not row['id'].startswith('C')}
    for task in ledger['tasks']:
        if task['id'] in rows:
            row=rows[task['id']];task.update(status=row['status'],evidence=row['evidence'],result_details=row['details'])
    ledger.update(current_stage='C5',stage_status='IN_PROGRESS',stop_after='C')
    assert before=={row['id']:row for row in ledger['tasks'] if not row['id'].startswith('C')}
    dump(path,ledger);print('C_LEDGER_PROGRESS',len(rows),'pending',sorted(expected-set(rows)),flush=True)


if __name__=='__main__':main()
