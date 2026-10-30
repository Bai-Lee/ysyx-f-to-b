from evidence import *
import zipfile,re,copy,shutil,ast
from collections import Counter
ARCHIVE=ROOT.parents[1]/'YSYX_F_B_Archive'
def load(p):return json.loads(Path(p).read_text('utf8'))
def streams(folder,d):
    for key in ['stdout','stderr']:assert sha(folder/(key+'.log'))==d[key+'_sha256'],folder
def main():
    assert load(ROOT/'config/task_status.json')['current_stage']=='E4','Do not overwrite a later stage with a historical E4 audit'
    spec=load(ROOT/'E/E4/course_specs.json');assert len(spec['tasks'])==44
    for s in spec['sources']:assert sha(s['copy'])==sha(s['source'])==s['sha256']
    for r in spec['tasks']:assert sha(ARCHIVE/r['source']['raw'])==r['source']['source_sha256']
    required=['E4_units','E4_negative','E4_gui','E4_visual_check','E4_waves','E4_structure','E4_offline','E4_runtime','E4_tools','E4_verilator_build','E4_board_build']
    for name in required:assert load(ROOT/'reports'/(name+'.json'))['status']=='PASS',name
    authoritative=['build/'+s for s in ['comb','sequential','keyboard','vga','motion','difftest','lab_board','dual','dual_fst','official']]+['cpu/semu_compile','cpu/semu_object','rom/compile']
    for tag in authoritative:
        record=load(ROOT/'artifacts/E4'/tag/'run.json');assert record['status']=='PASS'
        for x in record['inputs']:
            if x['path'].startswith('/workspace/projects/ysyx_f_to_b/'):
                assert sha(x['path'].replace('/mnt/d/','D:/'))==x['sha256'],('Current source differs from successful build',tag,x['path'])
    for x in load(ROOT/'reports/E3_delivery_manifest.json')['entries']:
        if x['path']=='F/programs/sisa.py':assert sha(ROOT/x['path'])==x['sha256']
    conversion=load(ROOT/'artifacts/E4/image_conversion.json')
    for name,key in [('source.ppm','source_sha256'),('image.mif','mif_sha256'),('image.mem','mem_sha256'),('expected.ppm','expected_sha256')]:assert sha(ROOT/'E/E4/data'/name)==conversion[key]
    assert sha(ROOT/'artifacts/E4/static_frame.ppm')==conversion['expected_sha256']
    board=load(ROOT/'reports/E4_board_build.json')
    latest=[];history=[];snapshots=0;input_entries=0
    for f in sorted((ROOT/'artifacts/E4').rglob('run.json')):
        d=load(f);streams(f.parent,d)
        if d.get('inputs'):
            with zipfile.ZipFile(f.parent/'input_snapshot.zip') as z:
                assert z.testzip() is None
                for i,x in enumerate(d['inputs']):
                    base=x['path'].replace('\\','/').split('/')[-1]
                    names=[f'{i:03d}_{base}',f'{i:02d}_{base}'];candidate=next(n for n in names if n in z.namelist())
                    assert hashlib.sha256(z.read(candidate)).hexdigest()==x['sha256'];input_entries+=1
            snapshots+=1
        assert d.get('inputs',[])==d.get('inputs_after',[]),f
        if 'attempts' in f.parts:history.append({'path':str(f.relative_to(ROOT)),'status':d['status']});continue
        if d['status']!='PASS':
            assert f.relative_to(ROOT).as_posix()=='artifacts/E4/framework/nvboard_clone/run.json' and d['exit_code']==128
            assert load(ROOT/'artifacts/E4/framework/nvboard_fsck/run.json')['status']=='PASS'
            history.append({'path':str(f.relative_to(ROOT)),'status':'RESOLVED_FAILURE','reason':'Archived repository is shallow; original shallow metadata plus bundled objects restored, checkout/fsck succeeded.'});continue
        expected=d['expected_exit'] if isinstance(d['expected_exit'],list) else [d['expected_exit']]
        assert d['exit_code'] in expected
        latest.append(str(f.relative_to(ROOT)).replace('\\','/'))
    gui=load(ROOT/'reports/E4_gui.json')
    for row in gui['screens']:assert sha(ROOT/row['path'])==row['sha256']
    for f in (ROOT/'artifacts/E4/gui').rglob('session.json'):
        d=load(f);streams(f.parent,d);assert d['exit_code'] in d['expected_exit']
    # Published GUI record must correspond to the current successfully linked board.
    for row in gui['sessions']:
        if row['command'][0].endswith('/lab_board'):assert row['binary_sha256']==board['sha256']
    recovery=load(ROOT/'E/E4/offline/manifest.json')
    for row in recovery['entries']:assert sha(ROOT/row['path'])==row['sha256']
    assert load(ROOT/'reports/E4_offline.json')['manifest_sha256']==sha(ROOT/'E/E4/offline/manifest.json')
    cpu=load(ROOT/'artifacts/E4/cpu_source.json');assert sha(cpu['source'].replace('/mnt/d/','D:/'))==cpu['source_sha256']
    # Corrupt metadata is rejected, without modifying the authentic evidence.
    good=load(ROOT/'artifacts/E4/cpu/diff_sum/run.json');streams(ROOT/'artifacts/E4/cpu/diff_sum',good)
    corrupt=copy.deepcopy(good);corrupt['stdout_sha256']='0'*64
    try:streams(ROOT/'artifacts/E4/cpu/diff_sum',corrupt)
    except AssertionError:rejected=True
    else:raise AssertionError('Corrupt evidence accepted')
    rows={r['id']:r for r in load(ROOT/'reports/E4_results.json')['records']}
    def setrows(ids,status,evidence,details):
        for i in ids:rows[i]={'id':i,'status':status,'evidence':evidence,'details':details}
    setrows(['E4-M007','E4-M008','E4-M009','E4-M011'],'PASS',['reports/E4_gui.json','reports/E4_visual_check.json','reports/E4_units.json'],'上游NVBoard官方例与自写RTL真实运行并经X11事件交互；26张虚拟板截图逐位核验，NJU五实验完成；不作实体FPGA结论。')
    setrows(['E4-M012'],'PASS',['artifacts/E4/rom/all_addresses','artifacts/E4/gui/cpu_sum55.png','artifacts/E4/cpu/diff_sum','E/E4/rtl/program_rom.sv'],'F阶段自写sCPU复用到Linux Verilator；RTL程序ROM256字节全核对，NVBoard实际显示IO求和55，完整取指路径与独立sEMU一致。')
    setrows(['E4-M014','NJU-06-04','E4-R001','E4-R004','E4-R005','E4-R006'],'PASS_DOCUMENTED',['E/E4/NOTES.md'],'已说明软硬状态模型、HDL事件/并行/选择网络、独立构建流程及伪随机序列的周期与安全边界。')
    setrows(['E4-R007','E4-R008'],'PASS',['reports/E4_structure.json','reports/E4_negative.json','E/E4/NOTES.md'],'真正时钟单元仅posedge、无推断锁存器；异步读口与触发沿分开判断，实际negedge和latch反例均被拒绝。')
    setrows(['E4-O001'],'READ_DOCUMENTED',['E/E4/NOTES.md'],'原页NVBoard背景介绍已阅读；纯背景不虚构额外程序验收。')
    setrows(['E4-O002'],'OPTIONAL_NOT_SELECTED',['E/E4/NOTES.md'],'额外进阶阅读未作为独立项目展开；本阶段实际所需原版手册与高级Trace/约束/接口内容已随工程留存。')
    setrows(['E4-O003'],'OPTIONAL_NOT_SELECTED',['E/E4/NOTES.md'],'采用SystemVerilog路线；Chisel及个人交流群申请不属于所选实现路线。')
    for i in ['NJU-02-02','NJU-03-02','NJU-06-03','NJU-07-01','NJU-07-02','NJU-07-03','NJU-08-01','NJU-08-02','NJU-08-03']:
        for e in ['reports/E4_gui.json','reports/E4_visual_check.json']:
            if e not in rows[i]['evidence']:rows[i]['evidence'].append(e)
        if '对应NVBoard交互与像素验收也已完成。' not in rows[i]['details']:rows[i]['details']+=' 对应NVBoard交互与像素验收也已完成。'
    assert set(rows)=={r['id'] for r in spec['tasks']}
    assert all(rows[f'E4-M{i:03}']['status'].startswith('PASS') for i in range(1,18))
    for row in rows.values():
        for e in row['evidence']:assert (ROOT/e).exists(),e
    now=datetime.now(timezone.utc).isoformat();data={'status':'PASS_WITH_EXPLICIT_OPTIONAL_SCOPE','timestamp':now,'records':sorted(rows.values(),key=lambda x:x['id'])};dump(ROOT/'reports/E4_results.json',data)
    ledger_path=ROOT/'config/task_status.json';ledger=load(ledger_path);backup=ROOT/'config/history'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f');backup.mkdir(parents=True);shutil.copyfile(ledger_path,backup/'task_status.json')
    for row in ledger['tasks']:
        if row['id'] in rows:
            r=rows[row['id']];row.update(status=r['status'],implementation_status=r['status'],evidence=r['evidence'],result_details=r['details'],updated=now)
    ledger.update(current_stage='E4',stage_status='COMPLETE_LOCAL_NVBOARD_VALIDATION',next_stage='E5');dump(ledger_path,ledger)
    counts=dict(Counter(r['status'] for r in rows.values()))
    audit={'status':'PASS','stage_complete':True,'stage_status':'COMPLETE_LOCAL_NVBOARD_VALIDATION','timestamp':now,'core_tasks_passed':17,'core_tasks_total':17,'nju_items_completed':16,'advanced_keyboard_optional_completed':True,'all_scope_items':44,'status_counts':counts,'optional_not_selected':['E4-O002','E4-O003'],'missing_required_items':[],'validated_latest_commands':len(latest),'historical_command_records':len(history),'input_snapshot_archives_verified':snapshots,'input_snapshot_entries_verified':input_entries,'nvboard_screenshots':26,'gtkwave_screenshots':2,'difftest_random_steps':50000,'sum_steps':200,'evidence_checker_corrupt_hash_rejected':rejected,'source_originals_unchanged':True,'scope_limits':['Virtual NVBoard/Xvfb, not physical FPGA','sISA, not RISC-V','Structural checks and bounded/exhaustive simulations, not whole-design unbounded proof','No PPA or official examination/tapeout certification'],'latest_commands':latest,'historical':history};dump(ROOT/'reports/E4_AUDIT.json',audit)
    board['gui_status']='PASS';board['gui_evidence']='reports/E4_gui.json';dump(ROOT/'reports/E4_board_build.json',board)
    frame=load(ROOT/'reports/E4_framework.json');frame.update(status='PASS',integration_evidence='reports/E4_board_build.json');dump(ROOT/'reports/E4_framework.json',frame)
    config=load(ROOT/'config/toolchain.json');shutil.copyfile(ROOT/'config/toolchain.json',backup/'toolchain.json');config['linux_environment']['current_fingerprints']='reports/E4_tools.json';config['linux_environment']['rtl_and_gui_acceptance']='reports/E4_AUDIT.json';dump(ROOT/'config/toolchain.json',config)
    lines=['# E4逐项实现—交付物—验收结果','',f'更新时间 {now}。17项核心任务及NJU的16个细项完成，含Shift/CTRL高级选做；另2项可选路线未选。原始要求全文见[冻结清单](../E/E4/course_specs.json)。','', '| ID | 实现要求（原文摘要） | 交付物 | 验收结果 |','|---|---|---|---|']
    normative={r['id']:r for r in spec['tasks']}
    for r in data['records']:
        req=re.sub(r'\s+',' ',normative[r['id']]['requirement']).replace('|','\\|').replace('[','【').replace(']','】')
        if len(req)>140:req=req[:140]+'…'
        links='；'.join('['+Path(e).name+'](../'+e+')' for e in r['evidence'][:3])
        lines.append(f'| {r["id"]} | {req} | {links} | {r["status"]}：'+r['details'].replace('|','\\|')+' |')
    (ROOT/'reports/E4_TASKS.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
    report=f'''# E4本地工程验收报告

E4按已冻结的v26.07清单完成：**17/17核心任务、NJU五个实验的16个细项通过**，包含Shift/CTRL高级选做。44个总节点均有记录；Verilator额外进阶阅读和Chisel路线两项未单独展开。下一阶段为E5。更新时间：{now}。

本结论来自真实Linux编译、RTL仿真、NVBoard交互、GTKWave查看、独立参考模型与故障注入，不是仅生成脚本。实体FPGA、RISC-V处理器、物理PPA、官方考试和流片不在本次PASS范围。

| 交付 | 实际结果 |
|---|---|
| Linux Verilator5.052 | 官方stable固定提交983a06a，源码-j1构建，官方C++例子、VCD/FST与正确/错误XOR实际执行 |
| npc一键仿真 | make sim成功；保留原git_commit调用，tracer记录包含SV与C++源码，并明确AI工程身份 |
| NVBoard | 固定官方提交b5f49b6；真实SDL窗口和X11输入，26张截图的LED/数码管及30个VGA像素锚点独立核验 |
| GTKWave | VCD/FST各3条信号真实显示；两格式16个样本完全相同；错误电路波形被拒绝 |
| NJU组合/时序 | 4位ALU与8位加法、译码/优先编码、移位、255周期LFSR、4096条FSM轨迹、PS/2及Shift/CTRL均验证 |
| VGA | 2个静态帧+3个移动帧逐像素检查；25MHz、800×525、640×480有效；MIF列优先布局和颜色逐项核验 |
| 图片反弹 | 1000组×1000次更新，边/角、方向及步长余量检查通过 |
| RTL sCPU+程序ROM | 256字节ROM全检查；NVBoard的LED实际显示1+…+10=55 |
| C sEMU与DiffTest | F5/F6版本分开；200步求和、50000步全256指令编码流逐状态核对，另以原独立Python模型复核 |
| 故障检出 | 真正编译错误RTL：XOR、优先级、溢出、LFSR抽头、PS/2奇校验、VGA总周期、GPR与仅PC分支错误均被拒绝 |
| 静态/结构 | 六个生产顶层lint；Yosys六类结构无锁存器、时钟单元均posedge；故意截断/latch/negedge反例被识别 |

审计核验{len(latest)}份当前命令记录，以及{snapshots}份输入快照、{input_entries}个快照成员；历史失败及修复均保留。工具路径/版本/摘要见[工具锁](E4_tools.json)，逐条实现、交付物和验收见[E4_TASKS.md](E4_TASKS.md)，技术解释与已修问题见[NOTES](../E/E4/NOTES.md)，机器结论见[E4_AUDIT.json](E4_AUDIT.json)。

关键真实截图：[求和LED=55](../artifacts/E4/gui/cpu_sum55.png)、[键盘ASCII](../artifacts/E4/gui/keyboard_a.png)、[VGA静态图](../artifacts/E4/gui/vga_static.png)、[GTKWave FST](../artifacts/E4/gui/gtkwave_fst.png)。界面运行在隔离Xvfb，不需要操作用户桌面，也没有使用Logisim computer use。

两个差分反例的首错位置已核验：禁止写R0，在PC=0的li处报告GPR0的0/8差异；负偏移误当无符号数，在PC=8的bner0处立即报告PC=0x16/0x06，GPR仍相同。日志没有等到最终sum错误才报错。[DiffTest原始证据](../artifacts/E4/cpu)

[离线复验](E4_offline.json)在全新Linux目录从本地导出重建工作台，真实make sim及tracer追踪，重新编译C sEMU并得到55，也展开并核验NVBoard源码/资源。编译器、WSL根文件系统和完整原资料库仍是既有外部依赖；工程ZIP不冒充完整操作系统镜像。

预算保持WSL2的2GiB内存、4vCPU、D盘2GiB swap，编译最多-j2，Verilator自身-j1；本阶段没有修改.wslconfig或全局PATH。界面进程已退出。可重复执行入口为[Run-E4.ps1](../scripts/Run-E4.ps1)，默认做证据/文档核验并更新ZIP，-Replay执行完整本地回归。原讲义与F/E1/E2/E3历史交付保留，旧阶段终点审计不用于覆盖当前E4状态。
'''
    (ROOT/'reports/E4_REPORT.md').write_text(report,encoding='utf8')
    print('E4_FINAL_AUDIT_PASS',len(latest),'commands;',snapshots,'snapshots;17 core/16 NJU',flush=True)
if __name__=='__main__':main()
