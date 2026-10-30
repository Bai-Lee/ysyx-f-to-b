"""Bind each frozen B requirement to its actual result, with optional limits."""
from evidence import *
from collections import Counter
import shutil

def report(name):return 'reports/'+name+'.json'
def main():
    for name in ['B_final_regressions','B5_ACCEPTANCE','B4_full128','B_performance_analysis']:
        assert json.loads((ROOT/report(name)).read_text('utf8'))['status'].startswith('PASS'),name
    specs=json.loads((ROOT/'B/runtime/course_specs.json').read_text('utf8'));source_by_stage={r['stage']:r for r in specs['sources']};bindings={}
    def add(ids,evidence,detail,status='PASS'):
        for identifier in ids.split():
            assert identifier not in bindings;bindings[identifier]={'status':status,'evidence':evidence,'details':detail}
    b1=[report('B1_native'),report('B1_npc'),'B/B1/NOTES.md']
    add('B1-M001',b1,'ECALL/MRET、CSR、etrace、完整上下文形成与恢复；32寄存器NEMU、16寄存器NPC，t0破坏反例。')
    add('B1-M002',b1,'独立NEMU真实启动RT-Thread，原始Shell命令及线程参数/返回完成；止于启动范围。')
    add('B1-M003',b1+[report('B4_release_soc')],'mcycle/mcycleh递增、回绕和CSR操作；参考时钟独立推进，冻结参考时钟会失败。')
    add('B1-M004',b1,'mvendorid=0x79737978、marchid=0x26070001及进入main前输出；稳定项目编号适配，非个人学号。','PASS_PROJECT_ID_ADAPTATION')
    add('B1-M005',b1+[report('B4_release_soc')],'M模式同步ECALL、上下文切换、完整SoC上的RT-Thread；不扩充为完整特权级或异步抢占。')
    analysis=[report('B_performance_analysis'),'B/B3/NOTES.md','B/B3/RESULTS.md']
    perf=[report('B3_performance'),*analysis]
    cache=[report('B3_icache_unit'),report('B3_cache_analysis_b5-multicycle-325'),*analysis]
    add('B3-M001 B3-M002 B3-M003',perf+['B/soc/sim/performance.hpp'],'指令、周期、分类、IFU/LSU和缺指原因计数及恒等式检查；退休间隔分类与可重叠事件的含义分别说明。')
    add('B3-M004 B3-M007',perf,'Amdahl和校准前后数据定位瓶颈；保留未校准对照，不将其视为真实芯片性能。')
    add('B3-M005',[report('B3_apb_unit'),'B/B3/NOTES.md'],'APB Q8比例1、1.25、2、5.5实际时序测试；向上取整误差小于一CPU周期，错误延迟对照拒绝。')
    add('B3-M006',[report('B3_synthesis'),'B/B3/components.sv','B/B3/NOTES.md'],'输入/输出触发器隔离的寄存器堆、32位加法器独立综合/STA；局部频率不冒充整机Fmax。')
    add('B3-M008',perf,'真实完整microbench train无cache校准基线通过，保留周期/指令/计时与原始日志。')
    add('B3-M009',[report('B_standalone_release'),report('B4_release_soc'),report('B3_performance')],'独立0x80000000快速功能回归与0x30000000完整SoC校准性能分开；两者逐退休比较参考模型。')
    add('B3-M010',cache+[report('B3_performance')],'最初4B×16行cache已真实运行；数据/元数据使用FF，后续参数化版本保留独立回归。')
    add('B3-M011',cache,'缓存仅限Flash/PSRAM/SDRAM范围；SRAM/MMIO绕过，单元测试核对绕过数量及未缓存数据行为。')
    add('B3-M012 B3-M025',analysis+[report('B3_trace_controls')],'理想/有限dcache为明确假设的估算；保留不可缓存访问、脏写回和存储位面积下界，没有dcache RTL或实际报价。')
    add('B3-M013 B3-M022',cache,'由请求到返回时间和计算AMAT/TMT；1/4字块校准的快速模型预测8字块，并量化与实测的误差。')
    add('B3-M014 B3-M015 B3-M016',cache+[report('B3_trace_controls')],'完整同一trace的参数扫描；多周期与最终受控取指配置逐项匹配RTL hit/miss/bypass；4倍块大小按独立事务估算。')
    add('B3-M017',cache,'RTL配置1/4/8字块及1/2路，覆盖块内、跨块、冲突、反压和错误tag反例；保持全程序DiffTest。')
    add('B3-M018',[report('B3_axi_generation'),report('B3_sdram_axi_unit'),report('B4_final_cpu'),report('B4_release_soc'),report('B4_full128')],'实际重新生成32位AXI SDRAM框架；控制器边界、原35个CPU正例/错误原例、OS和全容量图样检查。')
    add('B3-M019',[report('B3_icache_unit'),report('B3_sdram_axi_unit'),report('B3_performance')],'INCR burst的地址/beat/RLAST/反压检查；真实串行与突发SoC对照保留。')
    add('B3-M020',[report('B3_axi_delay_unit'),'B/B3/NOTES.md'],'AXI四种比例、读写并行、AW/W顺序、1/4/8拍响应和背压校准；错误延迟必须拒绝。')
    add('B3-M021',perf,'多周期cache及最终流水线的完整train均通过；频率、延迟比例与各自模型评估点显式记录。')
    add('B3-M023',perf,'真实ELF/BIN前填充24B并重运行，与未填充结果比较；trace平移估算另列。')
    add('B3-M024',analysis+[report('B5_final_timing')],'同库面积探索后采用128B、总4行×8字、2路；最终24878.182μm²。旧地址表达式网表失效，修复候选重新综合。')
    add('B3-M026 B3-M027',[report('B3_smc'),'B/B3/smc.S','B/B3/NOTES.md'],'同一自修改函数明确复现陈旧指令；加fence.i后执行新指令并通过参考比较。')
    add('B3-M028 B3-M029',[report('B3_loader_fence'),'B/soc/am/start.S','B/B3/NOTES.md'],'临时NOP/ret预热后覆盖入口：缺fence时DiffTest失败，有fence时成功；正常启动不依赖额外NOP。')
    b4=[report('B_performance_analysis'),'B/B4/NOTES.md','B/B4/RESULTS.md']
    add('B4-M001 B4-M002',b4+[report('B3_trace_controls'),report('B3_cache_analysis_b5-multicycle-325')],'按优化后cache的完整data trace重估理想和有限WB/WA dcache；手算脏替换和MMIO绕过例通过。')
    add('B4-M003',b4,'保留实测icache缺失/绕过与load/store退休区间，估算非访存每周期一条；明确均值分摊近似。')
    add('B4-M004',[report('B4_functional_pipeline-stall'),report('B_standalone_pipeline-stall'),report('B4_functional_release'),'B/B4/NOTES.md'],'四级valid/ready流水线；初始阻塞版本和最终版均真实测试，包含独立1200操作/内存期望及RAW故障反例。')
    add('B4-M005',[report('B4_functional_release'),report('B4_release_soc'),'B/B4/NOTES.md'],'较老指令提交、年轻指令清除、串行CSR/ECALL/MRET；上下文与RT-Thread回归。')
    add('B4-M006 B4-M007',b4+[report('B4_controlled_evaluation')],'相同325MHz/延迟比例下多周期、阻塞、转发、连续取指、JAL优化实测；保留朴素流水线退化。')
    add('B4-M008',b4+[report('B3_icache_unit')],'先用命中事件估计供给改善上界；独立256次连续命中512→257周期，整机实际收益另列。')
    add('B4-M009',b4,'RAW总等待减去load-use作为可消除部分的乐观代理，再与实际转发收益比较；不提前使用load数据。')
    add('B4-M010',[report('B4_functional_release'),report('B4_functional_pipeline-bad-raw'),*b4],'MEM/WB向EX转发，x0排除、较近生产者优先、load未返回继续阻塞；独立序列与错误互锁反例。')
    add('B4-M011 B4-M014',b4+[report('B4_branchsim_b5-stream-325')],'控制等待代理上界与jal/jalr/ret频率分别加权；ret是jalr子集，重叠/平均等待假设不隐藏。')
    add('B4-M012 B4-M013',b4+[report('B4_branchsim_b5-stream-325'),report('B4_branchsim_b5-release')],'完整trace与RTL分支计数一致；三种静态策略，六种准确率×三类题设流水线公式及截断输入反例。')
    add('B4-M015',b4+[report('B5_final_timing')],'在128B/8字块/2路缓存的已测325MHz流水线候选中采用转发、连续取指、早期JAL；满足面积。4字块组合成本是筛选估计，更高频率组合未全局搜索。')
    add('B4-M016 B4-M017',[report('B4_functional_pipeline-bad-fence'),report('B4_functional_release'),'B/B4/programs/fence-prefetch.S','B/B4/NOTES.md'],'构造流水寄存器保留旧指令的实际反例；修复清空年轻指令并丢弃旧未完成取指，保持AXI响应可完成。')
    b5=[report('B5_ACCEPTANCE'),'B/B5/NOTES.md']
    add('B5-M001 B5-M002 B5-M003',b5+[report('B5_structure')],'最终32位AXI、2371个同一上升沿DFF、无Nangate latch；位宽/时钟/latch检查器反例通过。')
    add('B5-M004',b5+[report('B5_export')],'工程编号00000000、顶层与全部模块前缀一致；make verilog可复现单文件导出并实际仿真。','PASS_PROJECT_ID_ADAPTATION')
    add('B5-M005',b5+[report('B5_rtl'),report('B5_rtl-bad-reset')],'最终源代码Icarus四值执行完整microbench test与RT-Thread及短用例；未写RAM保留X，缺复位被拒绝。')
    add('B5-M006',b5+[report('B5_netlist'),report('B5_cell_models')],'精确最终网表及验证过的标准单元模型，完整microbench test/RT-Thread四值运行；无SDF签核声明。')
    add('B5-M007',b5+[report('B_final_regressions'),report('B4_full128')],'修复后最终源码、网表、模型、程序和报告按哈希绑定；原CPU套件/负例、OS、性能及全容量测试均完成。')
    add('B1-O001',b1+[report('B4_release_soc')],'串口按字节输出，完整msh提示符和后续命令可见；不依赖末尾换行。')
    add('B1-O002 B5-R001 B5-M008',['B/runtime/course_specs.json','B/B5/NOTES.md'],'个人身份、申请、白名单、官方提交或联系流程排除。','EXCLUDED_SCOPE')
    add('B5-M009',b5+[report('B5_public_entrypoints')],'公开make接口做本地演练；没有申请、代替用户参加或宣称通过官方调试考核。','EXCLUDED_OFFICIAL_LOCAL_REHEARSAL_RECORDED')
    add('B3-O002 B3-O003 B3-O006 B3-O009',['B/B3/NOTES.md'],'原选做保留：逐周期性能曲线、可编程调频、独立NEMU mtrace可视化、cache请求序列形式化未完成；现有DUT trace/计数不冒充这些选做。','NOT_RUN_OPTIONAL')
    add('B3-O007',[report('B3_trace_controls'),'B/B3/NOTES.md'],'相同64次读取与cache参数下，连续数组16缺失、分散节点64缺失；为明确标注的自编地址序列。','PASS_AUTHORED_TRACE_EXAMPLE')
    add('B3-O010',[report('B3_trace_storage')],'完整二进制trace的gzip压缩/恢复逐字节SHA一致，空间比和实际写入/恢复耗时有记录；未实现所有可选编码。','PASS_SCOPED_OPTIONAL')
    add('B4-O006',b4+[report('B4_functional_release')],'最终完整trace含连续动态控制指令对，均随退休与NEMU比较；另有错路store/非法指令清除用例，不声称穷尽。','PASS_FINITE_CONTROL_SEQUENCES')
    add('B4-O010',[report('B4_formal'),'B/B4/NOTES.md'],'三条任意算术指令有界miter达到600秒上限；保留断言与输入，没有证明或反例结论。','TIMEOUT_OPTIONAL')
    add('B4-O012',b4+[report('B3_icache_unit')],'cache返回被接收的同周期可接收下一命中；独立供给率与完整SoC收益均实测。','PASS_SCOPED_OPTIONAL')
    add('B4-O014 B4-O016',['B/B4/NOTES.md','B/B4/RESULTS.md'],'BTB和返回地址栈没有实现；性能上限与面积余量用于解释选择，不冒充RTL结果。','NOT_RUN_OPTIONAL')
    add('B4-O015',b4+[report('B4_functional_release')],'JAL目标由当前指令提前计算，保留链接寄存器和错路恢复；与无预测同频配置比较。','PASS_SCOPED_OPTIONAL')
    for task in specs['tasks']:
        identifier=task['id'];stage=identifier.split('-')[0]
        if identifier in bindings:continue
        if task['classification']=='技术约束/方法提醒':
            note=[f'B/{stage}/NOTES.md']
            if stage in ['B3','B4']:note+=[f'B/{stage}/RESULTS.md',report('B_performance_analysis')]
            if identifier=='B3-R004':detail='使用锁定Yosys/ABC/OpenSTA和课程同一Nangate库的可复现流程；历史升级提醒不执行盲目git pull。'
            elif identifier=='B3-R005':detail='每次实际输入快照/配置/数据/测量时HEAD均保留；脏工作树不伪称仅靠HEAD可重现。make perf入口实际核验。'
            elif identifier=='B5-R002':detail='所有导出/驱动替换在脚本中重现；本地研究记录保留网表证据，未生成或提交官方小于1MB的申请补丁。'
            else:detail='按本框方法要求审视实际设计与数据；单元面积、校准模型、有限覆盖和全局最优边界在说明中明确。'
            add(identifier,note,detail,'REVIEWED_TECHNICAL_CONSTRAINT')
        else:
            assert task['classification']=='原选做/扩展或背景阅读',identifier
            add(identifier,[f'B/{stage}/NOTES.md'],'背景/思考按实际范围说明；Chisel、其它ISA、外部研究或历史产品示例不冒充本工程实现。','REVIEWED_BACKGROUND')
    require_ids={r['id'] for r in specs['tasks']};assert set(bindings)==require_ids and len(bindings)==110
    rows=[]
    for task in specs['tasks']:
        identifier=task['id'];row={'id':identifier,**bindings[identifier]};source=source_by_stage[identifier.split('-')[0]]
        for path in row['evidence']:assert (ROOT/path).is_file(),path
        row['evidence_sha256']={path:sha(ROOT/path) for path in row['evidence']}
        row['source']={'path':source['copy'].replace('\\','/'),'sha256':source['sha256'],'raw_sha256':source['raw_sha256'],'version':source['version']}
        if task['classification'] in ['PUBLIC_CORE_TASK','USER_ADAPTED']:assert row['status'].startswith('PASS'),identifier
        rows.append(row)
    result={'status':'COMPLETE_ENGINEERING_WITH_DECLARED_LIMITS','records':rows,'core_tasks':56,'adapted_tasks':2,'scope_records':110,'optional_statuses':dict(Counter(r['status'] for r in rows if '-O' in r['id']))}
    dump(ROOT/'reports/B_results.json',result)
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f');backup=ROOT/'config/history'/('B_final_'+stamp);backup.mkdir(parents=True)
    ledger_path=ROOT/'config/task_status.json';shutil.copyfile(ledger_path,backup/'task_status.json');ledger=json.loads(ledger_path.read_text('utf8'))
    baseline=json.loads((ROOT/'reports/B_baseline.json').read_text('utf8'));prior=json.loads((Path(baseline['backup'])/'task_status.json').read_text('utf8'))
    nested={r['id']:r for r in json.loads((ROOT/'reports/B1_AUDIT.json').read_text('utf8'))['nested_records']}
    allowed=require_ids|set(nested)
    assert [r for r in ledger['tasks'] if r['id'] not in allowed]==[r for r in prior['tasks'] if r['id'] not in allowed]
    by_id={r['id']:r for r in rows}
    for task in ledger['tasks']:
        identifier=task['id']
        if identifier in by_id:
            row=by_id[identifier];task.update(status=row['status'],implementation_status=row['status'],evidence=row['evidence'],result_details=row['details'])
        elif identifier in nested:
            row=nested[identifier];task.update(status=row['status'],implementation_status=row['status'],evidence=row['evidence'],result_details=row['scope'])
    ledger.update(current_stage='B',stage_status='COMPLETE_ENGINEERING_WITH_DECLARED_LIMITS',stop_after='B',next_stage='A_NOT_AUTHORIZED',completion_scope='56 public core tasks,2 project-ID adaptations,110B records; declared optional and official-process exclusions.')
    dump(ledger_path,ledger)
    unchanged=[r for r in ledger['tasks'] if r['id'] not in allowed]
    dump(ROOT/'reports/B_scope_preservation.json',{'status':'PASS','allowed_current_ids':sorted(allowed),'outside_scope_records':len(unchanged),
        'outside_scope_sha256':hashlib.sha256(json.dumps(unchanged,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        'baseline':'config/history/before_B checkpoint preserved before B implementation','scope':'All task records outside frozen B and its37PA source records remain byte-equivalent as JSON objects; source_inventory_initial_status is preserved.'})
    for stage in ['B1','B3','B4','B5']:
        tasks=[r for r in specs['tasks'] if r['id'].startswith(stage+'-')];ids={r['id'] for r in tasks}
        # B1 has a detailed nested audit; preserve it and write common coverage separately.
        filename=stage+'_coverage' if stage=='B1' else stage+'_AUDIT'
        dump(ROOT/'reports'/f'{filename}.json',{'status':'PASS_PUBLIC_ENGINEERING_WITH_DECLARED_LIMITS','stage_complete':True,'stage':stage,
            'core_tasks':sum(r['classification']=='PUBLIC_CORE_TASK' for r in tasks),'adapted_tasks':sum(r['classification']=='USER_ADAPTED' for r in tasks),'scope_records':len(tasks),
            'records':[r for r in rows if r['id'] in ids],'scope':'Mandatory public engineering accepted; optional NOT_RUN/TIMEOUT, background and official-process exclusions remain explicit.'})
    headers=['# B 阶段逐项证据','', '110 条冻结 B 来源记录：56 核心、2 工程编号适配。选做未运行和超时单列；官方流程不计入完成。','', '| ID | 原要求 | 状态 | 结果边界与证据 |','|---|---|---|---|']
    for task in sorted(specs['tasks'],key=lambda r:r['id']):
        row=by_id[task['id']];links='、'.join(f'[{Path(path).name}](../{path})' for path in row['evidence'])
        requirement=task['requirement'].replace('|','/').replace('\n',' ')[:180]
        headers.append(f"| {row['id']} | {requirement} | {row['status']} | {row['details']} {links} |")
    headers+=['','嵌套 PA 的 37 条来源记录及“启动 RT-Thread 即止”的边界见 [B1 审计](B1_AUDIT.json) 和 [B1 说明](../B/B1/NOTES.md)。B2 原页建设中，没有补造作业。','']
    (ROOT/'reports/B_TASKS.md').write_text('\n'.join(headers),encoding='utf8')
    print('B_LEDGER_BOUND',len(rows),dict(Counter(r['status'] for r in rows)),flush=True)

if __name__=='__main__':main()
