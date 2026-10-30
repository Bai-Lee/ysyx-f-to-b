"""Bind all original CPU fixtures, including trap.h assertions, to frozen C."""
from pathlib import Path
import sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--worker',action='store_true');args=parser.parse_args()
    copy_report=ROOT/'reports/B_cpu_source_copy.json';frozen_report=ROOT/'reports/C_runtime_export.json';suite_report=ROOT/'reports/B4_final_cpu.json'
    copied=json.loads(copy_report.read_text());frozen={r['source']:r for r in json.loads(frozen_report.read_text())['members'] if r['kind']=='file'}
    suite=json.loads(suite_report.read_text());assert suite['status']=='PASS_35_ORIGINAL_POSITIVES_AND_WRONG_REJECTED'
    inputs=[Path(__file__),copy_report,frozen_report,suite_report]+[Path(r[key]) for r in copied['files'] for key in ['source','target']]
    output=ROOT/'reports/B_cpu_corpus.json'
    if args.worker:
        rows=[]
        for row in copied['files']:
            assert row['source'] in frozen and frozen[row['source']]['sha256']==row['sha256']
            assert sha(Path(row['source']))==sha(Path(row['target']))==row['sha256']
            rows.append({'target':row['target'],'sha256':row['sha256'],'prior_frozen_member':frozen[row['source']]['path']})
        assert len(rows)==39 and sum(r['target'].endswith('.c') for r in rows)==36 and any(r['target'].endswith('/trap.h') for r in rows)
        dump(output,{'status':'PASS','files':rows,'prior_runtime_sha256':json.loads(frozen_report.read_text())['sha256'],'suite_sha256':sha(suite_report),
            'scope':'All36 original C fixtures plus Makefile, trap.h and gitignore were hashed when copied before the test loop, and rechecked after execution against the frozen C runtime. Assertions/header and original wrong.c remain unchanged; this is provenance validation, not a duplicate simulation run.'});return
    run('B4/cpu-corpus/check',['python3',Path(__file__),'--worker'],inputs=inputs,outputs=[output],timeout=60)
    print('B_CPU_CORPUS_PASS',len(copied['files']))

if __name__=='__main__':main()
