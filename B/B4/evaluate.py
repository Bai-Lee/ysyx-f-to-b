"""Controlled same-frequency cache and pipeline comparisons, serialized builds."""
from pathlib import Path
import sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--start-at');args=parser.parse_args()
    base=['--reset','0x30000000','--cycle-sim','--psram-qpi','--psram-bytes','4194304',
          '--sdram-width','32','--sdram-ranks','2','--optimized','--apb-ratio-q','832',
          '--axi-sdram','--axi-ratio-q','832']
    cases=[('b5-multicycle-325',4,8,2,[]),('b5-stall-325',4,8,2,['--pipeline']),
           ('b5-forward-325',4,8,2,['--pipeline','--forward']),
           ('b5-stream-325',4,8,2,['--pipeline','--forward','--stream-fetch']),
           ('b5-block1-325',32,1,2,[]),('b5-block4-325',8,4,2,[])]
    selected=cases[cases.index(next(row for row in cases if row[0]==args.start_at)):] if args.start_at else cases
    for label,lines,words,ways,options in selected:
        cache=['--cache-lines',str(lines),'--cache-words',str(words),'--cache-ways',str(ways),'--cache-burst']
        command=['python3',ROOT/'B/soc/build_soc.py',*base,'--label',label,*cache,*options]
        run('B4/evaluate/'+label+'/build-driver',command,inputs=[ROOT/'B/soc/build_soc.py'],timeout=1200)
        run('B4/evaluate/'+label+'/performance-driver',['python3',ROOT/'B/B3/perf.py','--variant',label,'--size','test','--frequency-mhz','325','--padding','24','--trace'],inputs=[ROOT/'B/B3/perf.py'],timeout=600)
        if not options:
            run('B4/evaluate/'+label+'/analysis-driver',['python3',ROOT/'B/B3/analyze.py','--variant',label],inputs=[ROOT/'B/B3/analyze.py',ROOT/'B/B3/cachesim.cpp'],timeout=180)
        if label not in ['b5-block1-325']:
            run('B4/evaluate/'+label+'/synthesis-driver',['python3',ROOT/'B/B3/synthesis.py','--name',label,*cache,*options],inputs=[ROOT/'B/B3/synthesis.py'],timeout=1800)
    # A rejected larger design supplies a real cost, not a scaled area guess.
    run('B4/evaluate/b5-cache256/synthesis-driver',['python3',ROOT/'B/B3/synthesis.py','--name','b5-cache256','--cache-lines','16','--cache-words','4','--cache-ways','2','--cache-burst'],inputs=[ROOT/'B/B3/synthesis.py'],timeout=1800)
    accepted=json.loads((ROOT/'reports/B3_performance.json').read_text())['runs']
    for label,*_ in cases:assert any(r['variant']==label and r['size']=='test' and r['padding']==24 and r['status']=='PASS' for r in accepted)
    dump(ROOT/'reports/B4_controlled_evaluation.json',{'status':'PASS','frequency_mhz':325,'padding':24,'variants':[x[0] for x in cases],
        'scope':'Actual full-SoC test-scale executions with per-retirement NEMU and the same325MHz Q8 delay ratios. Fixed128B capacity for1/4/8-word block comparisons. Independent synthesis records are area/timing-model measurements, not physical signoff. Train results are reported separately.'})
    print('B4_CONTROLLED_EVALUATION_PASS')

if __name__=='__main__':main()
