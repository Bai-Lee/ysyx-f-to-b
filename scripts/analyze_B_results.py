"""Source-bound tables and explicit performance estimates, with pending guards."""
from evidence import *
import argparse,math,re,struct

def read(name):return json.loads((ROOT/'reports'/f'{name}.json').read_text('utf8'))
def local(value):
    text=str(value).replace('\\','/')
    for prefix in ['/workspace/projects/ysyx_f_to_b/','/workspace/projects/ysyx_f_to_b/']:
        if text.startswith(prefix):return ROOT/text[len(prefix):]
    return Path(text)

def classified_cache(trace,lines=4,words=8,ways=2):
    sets=lines//ways;entries=[[None]*ways for _ in range(sets)]
    counters=[[0,0,0] for _ in range(8)];counts=[0]*8;step=0;previous_kind=None;control_pairs={}
    kinds={3:1,0x23:2,0x63:3,0x6f:4,0x67:5,0x73:6,0x0f:7}
    with trace.open('rb') as stream:
        while data:=stream.read(20):
            assert len(data)==20
            pc,inst,next_pc,address,flags=struct.unpack('<5I',data);kind=kinds.get(inst&127,0);counts[kind]+=1;step+=1
            if previous_kind in [3,4,5] and kind in [3,4,5]:
                key=str(previous_kind)+'->'+str(kind);control_pairs[key]=control_pairs.get(key,0)+1
            previous_kind=kind
            cached=0x30000000<=pc<0x31000000 or 0x80000000<=pc<0x80400000 or 0xa0000000<=pc<0xa8000000
            if not cached:counters[kind][2]+=1
            else:
                block=pc//(4*words);index=block%sets;tag=block//sets
                hit=next((i for i,item in enumerate(entries[index]) if item is not None and item[0]==tag),None)
                if hit is None:
                    counters[kind][1]+=1
                    free=next((i for i,item in enumerate(entries[index]) if item is None),None)
                    hit=free if free is not None else min(range(ways),key=lambda i:entries[index][i][1])
                else:counters[kind][0]+=1
                entries[index][hit]=(tag,step)
            if inst&0x707f==0x100f:entries=[[None]*ways for _ in range(sets)]
    return {'class_counts':counts,'hit_miss_bypass_by_class':counters,'adjacent_control_pairs':control_pairs,'trace_sha256':sha(trace)}

def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','|'+'|'.join(['---']*len(headers))+'|',*['| '+' | '.join(str(v) for v in row)+' |' for row in rows]])

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--allow-pending',action='store_true');args=parser.parse_args()
    perf=read('B3_performance');synth=read('B3_synthesis');timing=read('B5_final_timing')
    def get(name,size='test',padding=24):return next((r for r in perf['runs'] if r['variant']==name and r['size']==size and r.get('padding',0)==padding),None)
    variants=['b5-multicycle-325','b5-stall-325','b5-forward-325','b5-stream-325','b5-release','b5-block1-325','b5-block4-325']
    missing=[name for name in variants if get(name) is None]
    if missing and not args.allow_pending:raise ValueError('Pending controlled runs: '+','.join(missing))
    base=get('b5-multicycle-325');assert base
    p=base['simulation']['performance'];cycles=p['core_cycles'];n=base['simulation']['instructions']
    classified=classified_cache(local(base['trace']))
    assert classified['class_counts']==p['class_counts']
    totals=[sum(r[i] for r in classified['hit_miss_bypass_by_class']) for i in range(3)]
    assert totals==[p['cache_events'][1],p['cache_events'][2],p['cache_events'][3]]
    mean=[lat/count if count else 0 for lat,count in zip(p['fetch_latency_hit_miss_bypass'],totals)]
    nonmem=[i for i in range(8) if i not in [1,2]];count_non=sum(p['class_counts'][i] for i in nonmem)
    miss_non=sum(classified['hit_miss_bypass_by_class'][i][1] for i in nonmem)
    bypass_non=sum(classified['hit_miss_bypass_by_class'][i][2] for i in nonmem)
    estimated_non=count_non+miss_non*max(0,mean[1]-1)+bypass_non*max(0,mean[2]-1)
    ideal_pipeline_cycles=sum(p['class_cycles'][1:3])+estimated_non
    cache_analysis=read('B3_cache_analysis_b5-multicycle-325')
    dcache=cache_analysis['dcache_estimates']['configs'];cache_count=sum(p['data_counts'][:2]);uncached_latency=sum(p['data_latency'][2:])
    read_latency=p['data_latency'][0]/p['data_counts'][0];write_latency=p['data_latency'][1]/p['data_counts'][1]
    dc_rows=[]
    for r in dcache:
        if r['capacity_bytes'] not in [64,128,256] or r['ways']!=2 or r['words']!=4:continue
        assert r['accesses']==p['lsu_responses'] and r['bypasses']==sum(p['data_counts'][2:])
        modeled=uncached_latency+cache_count+r['misses']*(read_latency+3.25*(r['words']-1))+r['writebacks']*r['words']*write_latency
        new_cycles=cycles-p['lsu_latency_sum']+modeled
        dc_rows.append({**r,'modeled_data_cycles':modeled,'modeled_program_cycles':new_cycles,'estimated_speedup':cycles/new_cycles})
    library=(ROOT/'B/models/nangate45/lib/Nangate45_typ.lib').read_text('utf8')
    dff_area=float(re.search(r'cell\s*\(\s*DFF_X1\s*\).*?area\s*:\s*([0-9.]+)',library,re.S)[1])
    stall=get('b5-stall-325');forward=get('b5-forward-325');stream=get('b5-stream-325');release=get('b5-release')
    final_classified=classified_cache(local(release['trace']))
    final_events=release['simulation']['performance']['cache_events']
    require_final=[sum(r[i] for r in final_classified['hit_miss_bypass_by_class']) for i in range(3)]
    assert require_final==[final_events[1],final_events[2],final_events[3]]
    sp=stall['simulation']['performance'];fp=forward['simulation']['performance'];stp=stream['simulation']['performance']
    removable_raw=max(0,sp['pipeline_events'][0]-sp['pipeline_events'][1])
    branch=read('B4_branchsim_b5-stream-325')['results'];control_count=branch['conditional_branches']+branch['jal']+branch['jalr']
    mean_control=stp['pipeline_events'][3]/control_count
    branch_bounds={name:{'instructions':branch[name],'fraction_all_instructions':branch[name]/branch['instructions'],
        'uniform_control_stall_estimated_saved_cycles':branch[name]*mean_control,
        'estimated_speedup':stp['core_cycles']/(stp['core_cycles']-branch[name]*mean_control)} for name in ['jal','jalr','returns']}
    block_rows=[]
    for name,words in [('b5-block1-325',1),('b5-block4-325',4),('b5-multicycle-325',8)]:
        row=get(name)
        if row is None:continue
        stat=row['simulation']['performance'];events=stat['cache_events'];lat=stat['fetch_latency_hit_miss_bypass']
        assert sum(lat)==stat['ifu_latency_sum']
        assert lat[0]==events[1]
        block_rows.append({'variant':name,'words':words,'misses':events[2],'TMT':lat[1]-events[2],
            'miss_service_cycles':lat[1],'mean_miss_cycles':(lat[1]-events[2])/events[2],
            'AMAT':(lat[0]+lat[1])/(events[1]+events[2]),'port_AMAT':sum(lat)/stat['ifu_responses'],'core_cycles':stat['core_cycles']})
    prediction=None;same_trace=[]
    if len(block_rows)==3:
        one,four,eight=block_rows;slope=(four['mean_miss_cycles']-one['mean_miss_cycles'])/3
        predicted=eight['misses']*(one['mean_miss_cycles']+7*slope)
        prediction={'calibration_words':[1,4],'validation_words':8,'intercept':one['mean_miss_cycles'],'increment_per_word':slope,'predicted_TMT_8':predicted,'actual_TMT_8':eight['TMT'],'relative_error':(predicted-eight['TMT'])/eight['TMT']}
        same=cache_analysis['sweep'][0]['configs']
        for item in same:
            if item['capacity_bytes']==128 and item['ways']==2 and item['words'] in [1,4,8]:
                same_trace.append({**item,'serial_word_TMT_estimate':item['misses']*item['words']*one['mean_miss_cycles']})
    summary={'status':'IN_PROGRESS' if missing else 'PASS','pending':missing,'test_frequency_mhz':325,'test_padding':24,
        'classified_cache':classified,'final_classified_cache':final_classified,'ideal_pipeline':{'nonmemory_instructions':count_non,'nonmemory_misses':miss_non,'nonmemory_bypasses':bypass_non,
            'estimated_cycles':ideal_pipeline_cycles,'speedup':cycles/ideal_pipeline_cycles,
            'assumptions':'Load/store retirement intervals retained; each nonmemory hit costs1 cycle; actual miss/bypass counts retained with measured aggregate mean service penalties. No all-wait-removal assumption; aggregate-to-class latency allocation is approximate.'},
        'finite_dcache':dc_rows,'dcache_assumptions':{'read_first_cycle_cost':read_latency,'extra_read_beat_cost':3.25,'write_word_cost':write_latency,'policy':'WB/WA LRU;1-cycle access plus miss fill and dirty line writeback; uncached latency unchanged; frozen instruction sequence, no RTL dcache or measured gain'},
        'storage_area_lower_bound':{'DFF_X1_area_um2':dff_area,'64B_data_only_um2':512*dff_area,'release_remaining_um2':25000-timing['area_um2']},
        'forwarding':{'nonload_raw_cycles_upper_proxy':removable_raw,'upper_proxy_speedup':sp['core_cycles']/(sp['core_cycles']-removable_raw),'actual_same_frequency_speedup':sp['core_cycles']/fp['core_cycles']},
        'stream_fetch':{'single_hit_cycle_saved_upper_proxy':fp['cache_events'][1],'upper_proxy_speedup':fp['core_cycles']/(fp['core_cycles']-fp['cache_events'][1]),'actual_same_frequency_speedup':fp['core_cycles']/stp['core_cycles']},
        'control':{'all_control_stall_cycles':stp['pipeline_events'][3],'all_control_proxy_speedup':stp['core_cycles']/(stp['core_cycles']-stp['pipeline_events'][3]),'uniform_average_wait_per_control_instruction':mean_control,'jump_estimates':branch_bounds,'assumption':'Removing counted wait events is an optimistic proxy, not a disjoint causal partition. Per-jump weighting assumes uniform mean control wait; older memory dependencies can remain.'},
        'blocks':block_rows,'block_prediction':prediction,'same_trace_serial_estimates':same_trace,
        'bindings':{name:sha(ROOT/'reports'/f'{name}.json') for name in ['B3_performance','B3_synthesis','B3_cache_analysis_b5-multicycle-325','B4_branchsim_b5-stream-325','B5_final_timing']}}
    areas={r['name']:r['area_um2'] for r in synth['variants']}
    if 'b5-block4-325-cpu' in areas:
        summary['cache_area_tradeoff']={'multicycle_8word_area_um2':areas['b5-multicycle-325-cpu'],'multicycle_4word_area_um2':areas['b5-block4-325-cpu'],
            'measured_forward_pipeline_increment_um2':areas['b5-forward-325-cpu']-areas['b5-multicycle-325-cpu'],
            'estimated_4word_forward_pipeline_area_um2':areas['b5-block4-325-cpu']+areas['b5-forward-325-cpu']-areas['b5-multicycle-325-cpu'],
            'scope':'Additive screening estimate from measured standalone changes; the4-word pipeline combination was not synthesized. No claim that this estimate proves an impossibility or global optimality.'}
    dump(ROOT/'reports/B_performance_analysis.json',summary)
    rows=[]
    for r in perf['runs']:
        rows.append([r['variant'],r['size'],r.get('padding',0),r['model_frequency_mhz'],f"{r['simulation']['cycles']:,}",f"{r['simulation']['instructions']:,}",f"{r['ipc']:.6f}",f"{r['simulation']['cycles']/r['model_frequency_mhz']/1000:.3f}",(r.get('git_commit') or 'UNKNOWN')[:10]])
    source_notes='''原始性能记录保留测量时的 Git HEAD，同时每次构建保存实际工作树输入哈希和源码快照。存在尚未提交的修改时，HEAD 本身不足以定位被测设计；必须一起使用 input_snapshot.zip 和配置。没有把事后整理的提交伪称为测量当时的提交。最终复验入口是 B/soc/Makefile；具体 PROFILE/SIZE/FREQUENCY_MHZ/PADDING 与原始 run.json 对应。历史无效综合网表的 RTL 功能/周期记录仍可查看，但不作为最终门级验收或频率资格。'''
    text='# B3 性能与缓存测量\n\n'+('当前仍有待运行对照：'+', '.join(missing)+'。\n\n' if missing else '以下必做对照均有已完成的运行证据。\n\n')
    text+='## 全部性能记录\n\n'+table(['配置','规模','填充 B','模型 MHz','整次周期','退休指令','核心 IPC','模型时间 ms','测量时 HEAD'],rows)+'\n\n'+source_notes+'\n\n'
    text+='模型时间按整次周期/f 计算；程序打印时间只覆盖程序内部计时区间，不能与启动、打印和退出全程混为一谈。测试规模和 train 规模分列；不同频率时优先比较时间。\n\n'
    text+='## 固定容量下的块大小\n\n'+table(['字/块','缺失数','额外缺失 TMT','平均 miss_penalty','可缓存 AMAT','含绕过端口 AMAT','核心周期'],[[r['words'],r['misses'],r['TMT'],f"{r['mean_miss_cycles']:.4f}",f"{r['AMAT']:.4f}",f"{r['port_AMAT']:.4f}",r['core_cycles']] for r in block_rows])+'\n\nTMT 扣除每次缺失的一周期查找基线；原始 miss service 总和仍保留在机器报告。可缓存 AMAT 只除以 hit+miss，端口 AMAT 另含绕过请求。早期报告的 TMT_cycles 字段包含查找时间，不能直接与本表混用。\n\n'
    if prediction:
        text+=f"用 1/4 字块实测均值拟合每块代价，再预测 8 字块：TMT 估计 {predicted:,.1f}，实际 {eight['TMT']:,}，相对误差 {prediction['relative_error']:.2%}。块大小改变 Flash/SDRAM 缺失的混合比例、冲突和共享总线行为，线性近似的误差不可省略。\n\n"
        text+=table(['同一 trace、128 B、2 路','缺失数','按独立单字事务估算 TMT'],[[str(r['words'])+' 字/块',r['misses'],f"{r['serial_word_TMT_estimate']:,.1f}"] for r in same_trace])+'\n\n该表复用同一条完整 trace；代价模型是每个字独立支付单字缺失均值，未把 AXI burst 的收益预先塞进估计。真实 burst 对照见原始 b3-cache128-axi-serial/burst 两条运行。\n\n'
    text+='## dcache 的假设收益与成本\n\n'+table(['容量 B','缺失','脏写回','估算整程周期','估算加速比'],[[r['capacity_bytes'],r['misses'],r['writebacks'],f"{r['modeled_program_cycles']:,.1f}",f"{r['estimated_speedup']:.4f}"] for r in dc_rows])+'\n\n'
    text+=f"假定 2 路、16 B 块、WB/WA，读缺失首字 {read_latency:.3f} 周期，后续字 3.25 周期，脏写回每字 {write_latency:.3f} 周期；保留全部绕过延迟。这些是固定 trace 的估算，不是 dcache RTL 实测。最终面积余量 {25000-timing['area_um2']:.3f} μm²，而仅 64 B 数据的 512 个 DFF 就需 {512*dff_area:.3f} μm²，尚未计入 tag/dirty/比较器/控制器。\n\n"
    text+='## 采用同一库重新综合的候选\n\n'
    text+=table(['配置','单元面积 μm²','建立时间频率估计 MHz','最大转换违例','latch'],[[r['name'],r['area_um2'],f"{r['setup_frequency_estimate_mhz']:.3f}",r['max_transition_violations'],r['latches']] for r in synth['variants'] if r['name'].startswith('b5-')])+'\n\n'
    text+=f"最终调整网表面积 {timing['area_um2']:.3f} μm²，评估点 {timing['evaluation_frequency_mhz']} MHz；两处 NOR4 驱动替换后最大转换违例为零。上表原 b5-release-cpu 的 21 条违例是替换前记录，不能当成最终已通过。所有数值均为 Nangate45、理想线网及明确 IO 约束的模型结果，没有布线后签核。\n"
    if 'cache_area_tradeoff' in summary:
        trade=summary['cache_area_tradeoff']
        text+=f"\n4 字块的多周期 test 确实比 8 字块快，但面积为 {trade['multicycle_4word_area_um2']:.3f} μm²，剩余 {25000-trade['multicycle_4word_area_um2']:.3f} μm²。8 字块下实测仅加入转发流水线就增加 {trade['measured_forward_pipeline_increment_um2']:.3f} μm²；简单相加估计 4 字块转发组合约 {trade['estimated_4word_forward_pipeline_area_um2']:.3f} μm²。这个组合未实际综合，相加只是保守筛选依据，不能证明它必定超限。选择 8 字块是给本轮已测流水线保留面积，不宣称它在所有组合中最快。\n"
    (ROOT/'B/B3/RESULTS.md').write_text(text,encoding='utf8')
    rows=[]
    for name in variants[:5]:
        r=get(name);c=r['simulation']['performance']['core_cycles'];rows.append([name,f'{c:,}',f"{r['ipc']:.6f}",f'{cycles/c:.4f}',f'{c/325000:.4f}'])
    text='# B4 流水线对照与上限估算\n\n'+table(['配置','核心周期','IPC','相对多周期加速比','325 MHz 核心时间 ms'],rows)+'\n\n'
    text+=f"相同频率和外存延迟模型下，朴素阻塞流水线发生退化；转发、连续命中取指和 JAL 目标提前计算逐步降低周期。最终相对多周期的加速比为 {cycles/release['simulation']['performance']['core_cycles']:.4f}，不是按流水线级数推算的倍数。\n\n"
    text+=f"非访存指令每周期一条的估算保留 {miss_non:,} 次非访存取指缺失、{bypass_non:,} 次绕过以及原 load/store 退休区间；估算周期 {ideal_pipeline_cycles:,.1f}，加速比 {cycles/ideal_pipeline_cycles:.4f}。缺失/绕过时间按各自实测总体均值分摊到指令类别，这一近似没有假装是逐指令的周期精确模型。\n\n"
    text+='## 转发和取指供给\n\n'
    text+=f"阻塞版本 RAW 等待 {sp['pipeline_events'][0]:,} 周期，其中 load-use {sp['pipeline_events'][1]:,}；只乐观消除差值 {removable_raw:,} 的代理上限为 {summary['forwarding']['upper_proxy_speedup']:.4f}，同频实测转发加速比为 {summary['forwarding']['actual_same_frequency_speedup']:.4f}。不能删除仍在等待 load 数据的周期。\n\n"
    text+=f"独立 cache 单元连续 256 次命中由 512 周期变为 257 周期。假定整机每次命中均省一周期，代理上限为 {summary['stream_fetch']['upper_proxy_speedup']:.4f}；同频实测连续取指加速比 {summary['stream_fetch']['actual_same_frequency_speedup']:.4f}。前后端重叠、外存缺失与反压限制了收益。\n\n"
    text+='## 控制相关与静态预测\n\n'+table(['策略','预测正确 next-PC','准确率'],[[name,value,f"{value/branch['conditional_branches']:.4%}"] for name,value in branch['correct_next_pc'].items()])+'\n\n'
    text+=f"当前输入为 b5-stream-325 的完整 test trace，条件分支比例 {branch['branch_fraction']:.6%}。控制等待事件 {stp['pipeline_events'][3]:,} 周期，若假定它们都能消除，事件代理上限为 {summary['control']['all_control_proxy_speedup']:.4f}。这些事件可与数据等待重叠，不能当成精确的因果分解。\n\n"
    text+=table(['类别','动态数量','占全部指令','均匀控制等待假设下加速比'],[[k,v['instructions'],f"{v['fraction_all_instructions']:.4%}",f"{v['estimated_speedup']:.5f}"] for k,v in branch_bounds.items()])+'\n\nret 已包含在 jalr 中，不能把两项收益相加。均匀分配平均控制等待是上限估算的假设；真实预测器的容量冲突、恢复和依赖会进一步改变结果。\n\n'
    text+=table(['预测准确率','五级单发射 IPC','十五级单发射 IPC','十五级四发射 IPC'],[[f"{r['accuracy']:.1%}",f"{r['five_stage_single_ipc']:.6f}",f"{r['fifteen_stage_single_ipc']:.6f}",f"{r['fifteen_stage_four_issue_ipc']:.6f}"] for r in branch['ideal_scenarios']])+'\n\n'
    text+='题设公式与前提见 NOTES.md；该表忽略访存、RAW 和结构冲突，不是本 CPU 的 IPC 预测。\n\n'
    text+='## 最终选择的边界\n\n最终选择限于已选 128B、8字块、2路缓存下实测的 325 MHz 流水线候选，不声称全局最优。4字块多周期方案更快但留给流水线的面积更少，组合成本的筛选估计见 B3/RESULTS.md；未假装已经综合该组合。部分不启用连续取指的候选有更高的建立时间频率估计；尚未据此完成各频率下的端到端优化搜索。历史 400 MHz 多周期 cache train 的模型时间也短于最终 325 MHz 流水线，所有记录均保留；不能只比较不同频率的周期数来宣称加速。更高频率的性能、功耗和布局签核均不能由这里推定。\n'
    (ROOT/'B/B4/RESULTS.md').write_text(text,encoding='utf8')
    print('B_ANALYSIS_WRITTEN',summary['status'],missing,flush=True)

if __name__=='__main__':main()
