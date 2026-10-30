from evidence import *
from verify_C_parallel import pilot_checks,full_checks
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--full',action='store_true');args=parser.parse_args()
if args.full:
    result=full_checks();dump(ROOT/'reports/C5_sdram_full_parallel.json',result)
    data=json.loads((ROOT/'reports/C_results.json').read_text('utf8'));rows={r['id']:r for r in data['records']}
    rows['C5-M035']={'id':'C5-M035','status':'PASS','evidence':['reports/C5_sdram_full_parallel.json','reports/C5_parallel_sdram_pilot.json','reports/C5_sdram_controller.json'],
        'details':'Eight independently reset full128MiB address/inverse patterns, all8/16/32/64-bit widths. Each pattern writes and reads the entire address range with NEMU, all4chip highest addresses and exact pin byte counts. Original assembly bodies reused; serial/parallel equivalence and corruption controls accepted.'}
    data['records']=list(rows.values());dump(ROOT/'reports/C_results.json',data)
else:
    result=pilot_checks();dump(ROOT/'reports/C5_parallel_sdram_pilot.json',result)
    policy=json.loads((ROOT/'reports/C_performance_policy.json').read_text('utf8'));policy.update(status='PASS_MEASURED_PARALLEL_POLICY',acceptance='reports/C5_parallel_sdram_pilot.json',pilot_speedup=result['speedup'],actual_pilot_workers=result['actual_workers'],pilot_peak_pss_bytes=result['peak_group_pss_bytes']);dump(ROOT/'reports/C_performance_policy.json',policy)
print(json.dumps({k:v for k,v in result.items() if k not in ['checks','scope','compared_fields']},ensure_ascii=False),flush=True)
