"""Finish bounded final-source regressions after resource admission permits them."""
from common import *
import argparse

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--start-at',choices=['rtl','reset-mutant','cpu-suite'],default='rtl');args=parser.parse_args()
    if not (ROOT/'reports/B4_controlled_evaluation.json').exists():
        run('B/final-regressions/evaluate',['python3',ROOT/'B/B4/evaluate.py','--start-at','b5-block1-325'],inputs=[ROOT/'B/B4/evaluate.py'],timeout=2400)
    jobs=[('rtl','B/B5/verify_design.py',['--mode','rtl']),
          ('reset-mutant','B/B5/verify_design.py',['--mode','rtl','--fault-reset']),
          ('cpu-suite','B/B4/verify_cpu_suite.py',[])]
    if args.start_at!='rtl':
        accepted=json.loads((ROOT/'reports/B5_rtl.json').read_text());assert {r['name'] for r in accepted['runs']}=={'hello','hazards','fence-prefetch','microbench','rtthread'}
        build=json.loads((ROOT/'artifacts/B5/design/rtl/build/run.json').read_text());bound={r['path']:r['sha256'] for r in build['inputs']}
        for source in [*sorted((ROOT/'B/soc/rtl').glob('*.sv')),*sorted((ROOT/'B/soc/rtl').glob('*.v'))]:assert bound[str(source)]==sha(source)
        for row in accepted['runs']:
            assert row['status']=='PASS' and row['executable_sha256']==accepted['executable_sha256']
            raw=json.loads((ROOT/row['evidence']/'run.json').read_text());assert raw['status']=='PASS' and any(r['path'].endswith('/cpu.vvp') and r['sha256']==accepted['executable_sha256'] for r in raw['inputs'])
        jobs=jobs[[r[0] for r in jobs].index(args.start_at):]
    for name,path,options in jobs:
        run('B/final-regressions/'+name,['python3',ROOT/path,*options],inputs=[ROOT/path],timeout=1800)
    image=next(r['image'] for r in json.loads((ROOT/'reports/B_standalone_release.json').read_text())['runs'] if r['name']=='hello')
    for target in ['sim-iverilog','sim-iverilog-netlist']:
        run('B5/entrypoints/'+target,['make','-C',ROOT/'B/soc',target,'IMG='+image],inputs=[ROOT/'B/soc/Makefile',ROOT/'B/B5/public_sim.py',ROOT/'B/B5/export.py',Path(image)],timeout=300)
    run('B5/entrypoints/perf-test',['make','-C',ROOT/'B/soc','perf-test'],inputs=[ROOT/'B/soc/Makefile',ROOT/'B/B3/perf.py'],timeout=300)
    dump(ROOT/'reports/B_final_regressions.json',{'status':'PASS','scope':'Final-source Icarus RTL suite and missing-reset mutant;35 unchanged original CPU positives and wrong.c negative on the final SoC; public make entrypoints and controlled performance comparisons. Long gate programs and full128 acceptance remain separate requirements.'})
    print('B_FINAL_BOUNDED_REGRESSIONS_PASS')

if __name__=='__main__':main()
