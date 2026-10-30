from pathlib import Path
import sys,argparse,struct
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--variant',default='b3-icache-16x4');args=parser.parse_args()
    out=WORK/'b3/tools';out.mkdir(parents=True,exist_ok=True);exe=out/'cachesim';source=ROOT/'B/B3/cachesim.cpp'
    run('B3/cachesim/build',['g++','-std=c++17','-O3','-Wall','-Wextra',source,'-o',exe],inputs=[source],outputs=[exe],timeout=120,resume=True)
    # Hand-derived conflict, hit, invalidation, and uncached references.
    fixture=out/'control.bin'
    addresses=[0xa0000000,0xa0000000,0xa0000040,0xa0000000,0x0f000000,0xa0000000,0xa0000000]
    fixture.write_bytes(b''.join(struct.pack('<5I',a,0x100f if i==5 else 0x13,a+4,0,0) for i,a in enumerate(addresses)))
    text,_,_=run('B3/cachesim/control',[exe,'--trace',fixture,'--lines','16','--words','1'],inputs=[exe,fixture]);control=json.loads(text)['configs'][0];assert control['misses']==4 and control['bypasses']==1 and control['invalidations']==1,control
    short=out/'truncated.bin';short.write_bytes(fixture.read_bytes()[:-1])
    _,err,_=run('B3/cachesim/truncated',[exe,'--trace',short],inputs=[exe,short],expected=(2,));assert 'TRUNCATED_TRACE' in err
    runs=json.loads((ROOT/'reports/B3_performance.json').read_text())['runs'];current=next(r for r in runs if r['variant']==args.variant and r['size']=='test');trace=Path(current['trace'])
    build=next(r for r in json.loads((ROOT/'reports/B_soc_soc_build.json').read_text())['variants'] if r['variant']==args.variant)
    lines=build.get('cache_lines',16) or 16;words=build.get('cache_words',1);ways=build.get('cache_ways',1)
    text,_,_=run('B3/cachesim/'+args.variant,[exe,'--trace',trace,'--lines',str(lines),'--words',str(words),'--ways',str(ways)],inputs=[exe,trace]);actual=json.loads(text)
    if build.get('cache_lines',0):
        events=current['simulation']['performance']['cache_events'];sim=actual['configs'][0]
        assert sim['misses']==events[2] and sim['bypasses']==events[3] and sim['accesses']==events[0],(sim,events)
    explorations=[]
    for padding in [0,4,8,12,16,20,24,28]:
        text,_,_=run('B3/cachesim/'+args.variant+'-sweep-pad'+str(padding),[exe,'--trace',trace,'--sweep','--padding',str(padding)],inputs=[exe,trace]);explorations.append(json.loads(text))
    text,_,_=run('B3/cachesim/'+args.variant+'-dcache',[exe,'--trace',trace,'--sweep','--data'],inputs=[exe,trace]);dcache=json.loads(text)
    p=current['simulation']['performance'];cycles=p['core_cycles'];saved_d=max(0,p['lsu_latency_sum']-p['lsu_responses']);saved_i=max(0,p['ifu_latency_sum']-p['ifu_responses'])
    row={'status':'PASS_TRACE_MODEL_CHECKS','variant':args.variant,'actual_cache':actual,'sweep':explorations,'dcache_estimates':dcache,'amdahl':{'total_cycles':cycles,'ifu_latency_fraction':p['ifu_latency_sum']/cycles,'lsu_latency_fraction':p['lsu_latency_sum']/cycles,'ideal_one_cycle_ifu_speedup':cycles/(cycles-saved_i),'ideal_one_cycle_dcache_speedup_upper_bound_including_MMIO':cycles/(cycles-saved_d),'ifu_amat_cycles':p['ifu_latency_sum']/p['ifu_responses'],'lsu_mean_cycles':p['lsu_latency_sum']/p['lsu_responses']},'trace_sha256':sha(trace),'controls':{'hand_trace':control,'truncated_input_rejected':True},'scope':'Complete test-scale retired instruction/data trace, no sampling. Instruction misses matched RTL when caching enabled. Padding is a trace-level estimate pending real linked-image experiments. Finite dcache is a hypothetical WB/WA LRU model with dirty evictions, not implemented RTL or measured speedup. Ideal dcache upper bound includes uncacheable accesses and is deliberately optimistic.'}
    row['class_CPI']=[time/count if count else None for time,count in zip(p['class_cycles'],p['class_counts'])]
    row['class_fraction']=[count/current['simulation']['instructions'] for count in p['class_counts']]
    if 'fetch_latency_hit_miss_bypass' in p:
        lat=p['fetch_latency_hit_miss_bypass'];events=p['cache_events']
        assert not build.get('pipeline'),'Blocking-cache analysis must not silently include pipeline backpressure'
        assert lat[0]==events[1],'The measured cache lookup baseline is not one cycle'
        penalty=lat[1]-events[2]
        row['cache_timing']={'TMT_cycles':penalty,'miss_service_cycles':lat[1],'miss_count':events[2],
            'lookup_cycles':1,'mean_miss_service_cycles':lat[1]/events[2] if events[2] else None,
            'mean_miss_penalty_cycles':penalty/events[2] if events[2] else None,
            'cacheable_AMAT_cycles':(lat[0]+lat[1])/(events[1]+events[2]),
            'port_AMAT_cycles':sum(lat)/p['ifu_responses'],'hit_cycles':lat[0],'bypass_cycles':lat[2],'block_words':words,
            'definition':'Course TMT is extra miss time: miss service sum minus one measured lookup cycle per miss. Port AMAT includes uncached bypass; cacheable AMAT excludes bypass. Legacy pre-normalization reports used TMT_cycles for the inclusive miss-service sum.'}
        saved=sum(p['data_latency'][:2])-sum(p['data_counts'][:2])
        row['amdahl']['ideal_dcache_speedup_memory_regions_only']=cycles/(cycles-saved)
        row['amdahl']['ideal_dcache_saved_cycles_memory_regions_only']=saved
    dump(ROOT/('reports/B3_cache_analysis_'+args.variant+'.json'),row);print('B3_CACHESIM_PASS',args.variant,actual['configs'][0]['misses'],row['amdahl'],flush=True)

if __name__=='__main__':main()
