"""Write C delivery documents only after all required engineering evidence exists."""
from evidence import *
import shutil, zipfile, re
from collections import Counter
from verify_C_delivery import c5_checks, local_path


def read(name):
    return json.loads((ROOT/'reports'/f'{name}.json').read_text('utf8'))


def main():
    c5_checks(False)
    assert read('C5_AUDIT')['stage_complete'] and read('C_offline_replay')['status']=='PASS'
    timestamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
    workspace=ROOT.parents[1];backup=ROOT/'config/history'/('C_final_'+timestamp);backup.mkdir(parents=True)
    targets={'project_README.md':ROOT/'README.md','workspace_README.md':workspace/'README.md',
        'project_toolchain.json':ROOT/'config/toolchain.json','workspace_toolchain.json':workspace/'config/toolchain.lock.json',
        'task_status.json':ROOT/'config/task_status.json','C_results.json':ROOT/'reports/C_results.json',
        'runtime_README.md':ROOT/'C/runtime/README.md','C5_NOTES.md':ROOT/'C/C5/NOTES.md'}
    for name,path in targets.items():shutil.copyfile(path,backup/name)
    specs=json.loads((ROOT/'C/runtime/course_specs.json').read_text('utf8'));ids={r['id'] for r in specs['tasks']}
    results=read('C_results');rows={r['id']:r for r in results['records']};assert set(rows)==ids and len(rows)==101
    ledger=json.loads((ROOT/'config/task_status.json').read_text('utf8'))
    with zipfile.ZipFile(ROOT/'YSYX_D_DELIVERY.zip') as old:prior=json.loads(old.read('config/task_status.json'))
    outside=[r for r in ledger['tasks'] if r['id'] not in ids]
    assert outside==[r for r in prior['tasks'] if r['id'] not in ids]
    preservation=read('C_history_preservation')
    preservation.update(outside_C_task_record_count=len(outside),
        outside_C_task_records_sha256=hashlib.sha256(json.dumps(outside,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        outside_C_baseline_source='config/task_status.json read from the unchanged prior D delivery ZIP')
    dump(ROOT/'reports/C_history_preservation.json',preservation)
    for task in ledger['tasks']:
        if task['id'] in rows:
            row=rows[task['id']];task.update(status=row['status'],evidence=row['evidence'],result_details=row['details'])
    ledger.update(current_stage='C',stage_status='COMPLETE_ENGINEERING_WITH_DECLARED_LIMITS',stop_after='C',
        next_stage='B_NOT_AUTHORIZED',completion_scope='C1-C5 public engineering:68 core,2 project-ID adaptations,101 source records; C6 under construction; no B execution.')
    results['status']='COMPLETE_ENGINEERING_WITH_DECLARED_LIMITS'
    dump(ROOT/'config/task_status.json',ledger);dump(ROOT/'reports/C_results.json',results)
    c6=ROOT/'C/C6/sources/C6.md';assert '建设中' in c6.read_text('utf8')
    dump(ROOT/'reports/C6_AUDIT.json',{'status':'PASS_SOURCE_SCOPE_RECONCILED','stage_complete':True,'core_tasks':0,'scope_records':0,
        'source_status':'UNDER_CONSTRUCTION','source':c6.relative_to(ROOT).as_posix(),'sha256':sha(c6),
        'scope':'Frozen v26.07 C6 contains only the title and under-construction notice. No invented tapeout task; old E physical results do not qualify the current C CPU/SoC.'})

    psram=next(r for r in read('C5_psram_sweep')['runs'] if r['bytes']==4194304 and not r['corrupt'])['simulation']
    parallel=read('C5_sdram_full_parallel');pilot=read('C5_parallel_sdram_pilot')
    sdram=[next(r for r in read('C5_sdram_sweep')['runs'] if r['bytes']==33554432 and not r['corrupt']),
        {'width':32,'ranks':2,'bytes':134217728,'cycles':parallel['total_cycles'],'instructions':parallel['total_instructions'],'independent_patterns':8}]
    memory_rows=[f"| PSRAM / QPI | 4 MiB | {psram['cycles']:,} | {psram['instructions']:,} |"]
    memory_rows += [f"| SDRAM {r['width']} 位 × {r['ranks']} 组"+('，8 组独立复位并行（合计）' if r.get('independent_patterns') else '')+f" | {r['bytes']//1048576} MiB | {r['cycles']:,} | {r['instructions']:,} |" for r in sdram]
    statuses=Counter(r['status'] for r in rows.values())
    status_table='\n'.join(f'| `{name}` | {count} |' for name,count in sorted(statuses.items()))
    report=f'''# C 阶段交付报告

C 阶段公开工程范围已完成：68 项核心工程、2 项项目编号适配完成，101 条来源记录逐项核对。C2 所链接 PA2 范围中的 17 项必做也已完成。C4 的性能评估保留实际时序违例；完成评估不代表所有被测配置都达到频率目标。工程停在 C，未进入 B。

固定范围来自 v26.07 的 C1～C6 原文与已锁定的 PA 子章节。[逐项清单](C_TASKS.md)列出每项来源、状态和证据；[机器审计](C_AUDIT.json)检查报告、原始日志、快照、最终运行包及历史文件。个人申请、学号、提交和答辩排除；项目编号适配没有冒充个人身份。

## 各章节实际完成内容

| 章节 | 核心 / 适配 / 总记录 | 实际工作与边界 |
|---|---:|---|
| C1 链接 | 0 / 0 / 1 | 固定背景资料核对；自编 ELF、重定位、静态库抽取与错误链接实验。原页暂无独立编程任务，没有声称逐一观看全部视频。 |
| C2 输入输出 | 11 / 0 / 13 | native/NEMU/NPC 的设备和 AM 驱动、显示与键盘、屏保/小游戏、PA2 I/O 与性能构建；嵌套 PA2 必做 17 项。 |
| C3 调试 | 0 / 0 / 1 | 自编确定性缺陷，通过 GDB 观察点定位首次偏差并核对断言；属于有明确范围的背景实验。 |
| C4 多周期与总线 | 12 / 0 / 24 | 六种 CPU/总线配置、AXI4-Lite、仲裁/Xbar/UART/CLINT、综合及时序评估、MicroBench train。 |
| C5 完整 SoC | 45 / 2 / 62 | 完整框架生成、AXI 接口、Flash/PSRAM/SDRAM、启动与上下文、RT-Thread、NVBoard 和 ChipLink。 |
| C6 | 0 / 0 / 0 | 固定原页仍为建设中；[范围审计](C6_AUDIT.json)没有补造流片工作。 |

教学说明保留方法入口、关键实现理由和限制：[C1](../C/C1/NOTES.md)、[C2](../C/C2/NOTES.md)、[C3](../C/C3/NOTES.md)、[C4](../C/C4/NOTES.md)、[C5](../C/C5/NOTES.md)。C1/C3 引用的 v23.06 课件明确标注为背景资料，未冒充 v26.07 新讲义。

## 关键功能与反例

C4 的六种模式累计通过 444 组 ISA 程序运行。独立总线测试覆盖读写地址同拍、持续竞争、背压、复位中断事务和响应归属；错误数据、错误路由、固定优先级及组合 READY 相关错误对照均保留。原 Icarus 调度停滞记为 TIMEOUT，后续使用已验收的 Verilator 获得独立成功记录。[C4 审计](C4_AUDIT.json)、[总线证据](C4_fabric.json)。

C5 通过真实框架构建生成 SoC，未以手写空壳代替完整总线和外设。初始 MROM/SRAM 的 34 个原始 CPU 正例及 `wrong.c` 反例通过；最终 Flash/扩展内存配置又运行 35 个正例（包括 `hello-str`）及原始错误程序。逐指令比较用于非 MMIO 指令；MMIO 经独立地址/宽度/设备检查后同步参考状态。它不等于两个完全独立的设备模型。[最终 CPU 回归](C5_final_cpu.json)、[参考模型](C5_reference_build.json)。

课程任务版本与工程版本分别锁定：任务按已归档的 v26.07 原文执行；完整 SoC 采用官方 `ysyx6` 分支的固定提交 `bcdcbc3e8d97a11c07d3007e14f33c6147c02a8e`，并锁定七个递归依赖。这个工程与讲义所需的完整 SoC 拓扑相符；原采集的 `2607` 工程快照继续原样保存。本次属于已声明的兼容工程选择，不声称按 `2607` 分支原样构建。[来源锁](C5_source_lock.json)、[实际生成](C5_generation.json)。

| 功能 | 实际验收及拒绝的错误 |
|---|---|
| AXI、SRAM、启动 | 通道先后/背压/ID/LAST；SRAM 全可用区；染色内存后检查 `.data` 复制与 `.bss` 清零。遗漏初始化和错误响应均被拒绝。 |
| UART | FIFO 满导致的丢字已复现；轮询后 512 字节、全部 256 种字节值经独立 TX 引脚解码一致；错误波特率对照失败。 |
| SPI、Flash | 256 种位反转、真实命令/地址/数据、XIP 与只读错误；在 Flash 内调用共享 SPI 读取的冲突被复现，搬到 SRAM 的对照通过。 |
| PSRAM、SDRAM | SPI/QPI、掩码/突发/行列/存储体/片选；完整容量遍历；错误数据、掩码及片选变体被拒绝。 |
| 上下文、RT-Thread | 真实 CSR、ECALL/MRET；52 次独立上下文切换；破坏 t0 恢复会失败；原始内置命令及线程正常退出通过。 |
| GPIO、PS/2、VGA | 四值 RTL 测试及错误对照；外部同步信号定位并核对完整 307,200 像素帧；原生 NVBoard 操作与截图另行验收。 |
| ChipLink | 实际两端链路和远端 RAM，要求的 4 KiB 按全部宽度/图样写读；远端读数据损坏触发 DIFF_FAIL。 |

## 全容量内存测试

以下均为真实 RTL CPU 执行软件遍历，非主机直接填充后检查。软件按 8/16/32/64 位访问地址图样及其反码；RV32E 上 64 位操作拆成两次 32 位访问。每个字节都被实际写入并读回，NEMU 检查全部非 MMIO 退休指令。

128 MiB 的八组图样按用户授权的提速策略独立复位、并行执行；**每一组都先写满、再读回完整 128 MiB**，没有把地址区间分给不同模型。汇编遍历函数与原串行测试字节一致，小样本串行/并行的确定性结果以及原串行程序的总读写负载均已核对。这里不宣称一次不中断的八图样控制器状态序列；表中的该行周期和指令为八组之和。[并行方法验收](C5_parallel_sdram_pilot.json)、[全容量结果](C5_sdram_full_parallel.json)。

| 配置 | 完整测试容量 | 周期数 | 退休指令数 |
|---|---:|---:|---:|
{chr(10).join(memory_rows)}

对容量 N，全部图样合计的 CPU 读、写次数分别为 `[2N, N, N]`；SDRAM 引脚实际传送读 `16N` 字节、掩码后写 `8N` 字节。四颗 128 MiB 配置中，每颗合计读出 512 MiB、写入 256 MiB，每个独立图样均到达各颗的最高字节地址 32 MiB−1。原 C、展开 C、展开汇编的预跑按相同计数核对；优化只减少循环开销。故意破坏内存的短程对照保留，未用短程成功替代完整容量。[PSRAM](C5_psram_sweep.json)、[串行 SDRAM 记录](C5_sdram_sweep.json)、[串行引脚覆盖](C5_sdram_bus_coverage.json)、[并行全容量与逐组引脚覆盖](C5_sdram_full_parallel.json)。

这些是功能模型上的有限测试，不覆盖真实 DRAM 的电气保持、相邻单元耦合或所有数据组合，也不是无界形式化证明。

## 操作系统、界面与应用

PSRAM 和 SDRAM 均实际启动固定版本 RT-Thread。FSBL 从 Flash 将 SSBL 搬到 SRAM，SSBL 再加载主体；独立载荷测试中周期由 4,607,267 降到 1,626,085，遗漏 SSBL 复制会在实际入口失败。当前实现为 RV32E 机器态、单核、同步自陷/协作切换，不声明异步中断、抢占式时钟调度或完整特权架构。[加载器](C5_loader.json)、[上下文](C5_context.json)、[SDRAM RT-Thread](C5_rtthread_sdram32.json)。

八组 NVBoard 验收包括 GPIO、键盘、VGA 动画、打字游戏、FCEUX、RT-Thread 综合交互、独立 MicroBench 和堆保护反例。实际窗口使用隔离 Xvfb；输入来自原生键盘/UART 操作，输出由外设引脚和 NVBoard 解码记录。按键自动重复在私有显示内关闭并校准，最终记录没有 PS/2 FIFO 丢字；之前的准备时机和输入溢出失败仍保留。

RT-Thread 综合流程完成 `help`、未知命令后恢复、上下文测试、Hello、CC0 测试 ROM 的 FCEUX 交互/退出、再次 Hello、MicroBench 全部 10 项和正常结束。应用每次启动重建数据/BSS，参数具有独立生命周期；klib 与 MicroBench 私有 arena 分别检查，故意损坏堆边界会触发 BAD_TRAP。[综合交互](C5_gui_rtthread.json)、[FCEUX](C5_gui_fceux.json)、[堆反例](C5_gui_rtguard.json)。

VGA 的 FPS 输出、动画和像素测试属于当前模拟平台；没有真实显示器时序或模拟亚稳态结论。ChipLink 保留上游 1 GiB 远端模型容量，实际验收范围为 4 KiB，没有声称遍历整个 1 GiB。[ChipLink](C5_chiplink.json)。

## 性能评估的结论边界

C4 的单周期与 AXI 配置都完成 MicroBench train 的 10 项原始校验；train 关闭 DiffTest/trace，另有开启参考比较的 test 与 ISA 回归。模拟器中的 128 MiB 运行内存与综合用的两块 1 KiB 存储器不是同一容量，不能把它们合成一个“完整芯片性能”结论。[性能运行](C4_performance.json)。

IC55 锁定单元库下的独立映射/STA 对照得到 100 MHz 约束下的建立和保持结果，具体源文件、库、SDC 见[映射时序](C4_mapped_timing.json)。Nangate45 教学基线完成映射和分析，但单周期配置不满足 100 MHz；两配置分别存在 91,050 与 4,176 个最大转换时间违例。由建立裕量计算出的频率没有资格作为可靠 Fmax，报告没有据此宣称芯片提速或物理签核。[失败与限制](C4_nangate.json)。

Nangate45 库取自固定的官方 OpenROAD-flow-scripts 提交，已核对 Git blob 与本地摘要，许可证随包保留。原课程库压缩包下载未完成，其失败记录保留；当前库来源与独立 OpenSTA 流程的替代关系写在[库来源说明](C4_nangate_library.json)，没有宣称精确复现原课程的 yosys-sta/iSTA/DELAY4 环境。

C5 MicroBench test 从 Flash 改为 PSRAM 执行后，全程序周期由 140,276,107 降到 53,813,493。相同 SDRAM32 固件从 16 位接口换成 32 位接口，周期由 11,069,716 降到 9,262,308；软件堆上限保持相同。这些是固定仿真配置的周期比较。CoreMark 的单次迭代只作功能/CRC 验收，不是认证分数。[PSRAM 应用](C5_psram_apps.json)、[同镜像宽度比较](C5_sdram_apps.json)。

用户要求更积极使用内存后，项目把闲置内存用于独立图样并行，允许最多 8 路并按实时余量减少并发，整个批次共用 6 GiB PSS 预算。64 KiB 小样本的同一批固件串行耗时 {pilot['serial_seconds']:.2f} 秒，{pilot['actual_workers']} 路并行耗时 {pilot['parallel_seconds']:.2f} 秒，实测 {pilot['speedup']:.2f} 倍，峰值 PSS 约 {pilot['peak_group_pss_bytes']/1024**3:.2f} GiB。最后一次 128 MiB 批次最多 {parallel['actual_workers']} 路实际执行，续用了 {len(parallel['resumed_phases'])} 组已完成结果，本次墙钟约 {parallel['elapsed_seconds']:.1f} 秒，峰值 PSS 约 {parallel['peak_group_pss_bytes']/1024**3:.2f} GiB；该耗时不包含此前已完成组和中断尝试，小样本倍率也不被直接当作全容量实测速比。固件构建使用 `-j4`，每组已完成结果可按哈希续用。[策略与备份](C_performance_policy.json)、[合计内存超限反例](C_parallel_resource_controls.json)。

E 阶段旧 CPU 的 50 MHz、DRC 0、LVS 0 仅属于旧候选。C 的新 CPU/SoC 未进行布局布线、寄生提取、DRC/LVS 或实板签核。

## 状态、失败和可复验交付

| 来源记录状态 | 数量 |
|---|---:|
{status_table}

`PASS_EVALUATION_WITH_DECLARED_LIMITS` 表示完成了要求的测量与评估，并保留未达标结果；背景阅读不冒充运行通过。SPI 中断完成通知仍为 `OPTIONAL_NOT_IMPLEMENTED`。C2 的音频可选接口未补做；其较早 GUI 失败部分截图未全部留存，保留了外层失败日志与输入，后续已修正归档保护。这些限制都保留在章节审计中。

当前未通过的诊断记录包括 C4 Icarus TIMEOUT、旧内存预算下的综合 RESOURCE_LIMIT，以及 C5 对归档 Git 的 ownership 检查失败；均没有改记为通过。对应独立替代验证和源码来源已列明。所有保留的失败尝试随包交付。

曾有一次 128 MiB 长测的进程消失，未写入完成记录；其部分图样标记仅作为中断前观察，整体按 UNKNOWN 保存。后台启动方式修复后，用户进一步要求更积极使用内存；并行方案通过小样本功能、速度及资源正反例后，第二次串行尝试被主动终止并保留 FAIL/143 及原因，没有将其部分结果计为通过。最终完成依据是八个独立的全容量图样。[早期中断](C_background_execution.json)、[串行替换记录](C_serial_superseded.json)。

并行初轮完成三组后，WSL 调用 Windows 内存查询时遇到连接错误，监测器按 MONITOR_ERROR 停止整组。三组具有完整结果和输入输出哈希，后续续用；未完成组重新执行。Windows 内存采样随后改用有时限的本机进程与原生物理内存 API；首次实现又遇到文件访问拒绝，完成的第四组仍完整保留。最终改为只追加的项目遥测日志，读取最后一个完整记录；实际 Windows 文件共享冲突、半条记录、格式错误记录、过期和缺失数据均有正反例，后四类无效输入不会被当作新有效样本。采样器在所有受保护任务结束后正常退出，历次原始采样记录随包保存。[通道正反例](C_host_memory_controls.json)、[Windows 共享与记录边界](C_host_memory_io_controls.json)、[采样记录](C_host_memory_monitor.json)。

[最终源码/二进制绑定](C_final_bindings.json)、[工具指纹](C_toolchain_final.json)、[运行包清单](C_runtime_export.json)和[从包中解出程序后重放](C_offline_replay.json)提供追溯入口。初始 `C_PREFLIGHT.json`、setup/build 报告保留它们当时的阶段状态；当前完成结论以总审计和功能报告为准。

`YSYX_C_DELIVERY.zip` 为累积 F/E/D/C 工程包，包含源码、选定原始仓库归档、运行包、报告、截图和逐命令输入/输出快照；旧交付 ZIP 不嵌套进去。完整原始课程库、已安装工具、JDK/Maven 缓存和系统库是另行锁定的依赖。[离线说明](../C/offline/README.md)列出复验入口与边界。

使用 [Verify-C.ps1](../scripts/Verify-C.ps1)或跨平台 Python 核对保留证据。加 `-Archive` 会检查 ZIP 的全部成员 SHA-256 和 CRC；这个核验不重跑数小时的遍历。实际验收命令、cwd、退出码、用时、输入输出哈希、随机种子/模型选项和资源观测保留在 `artifacts/C*`。

[历史保护](C_history_preservation.json)确认此前 F/E/D 的 31,216 个文件及原 D ZIP 字节不变；C 范围外的 1,141 条任务记录也与 D 交付时一致。当前并行批次的合计软预算为 6 GiB，Windows 启动余量 2 GiB、运行余量 1 GiB，WSL 运行余量 512 MiB；按每个仿真估算 400 MiB 并预留 Windows 1280 MiB 计算并发数。运行器采样保护不等于操作系统硬限制。
'''
    (ROOT/'reports/C_REPORT.md').write_text(report,encoding='utf8')
    task_lines=['# C 阶段逐项清单','','固定范围 101 条；原题全文保留在各章 sources。核心工程 68 项、项目编号适配 2 项，其余 31 条为选做/背景/提醒。此表的题意列只作导航，省略处不改变原题要求。嵌套 PA2 的 17 项必做与全部 48 条子记录另见 [PA2 账本](C2_pa2_results.json)。','']
    def cell(text):return re.sub(r'\s+',' ',str(text)).replace('|','\\|').replace('<','&lt;').replace('>','&gt;').replace('[','&#91;').replace(']','&#93;')
    for chapter in ['C1','C2','C3','C4','C5']:
        task_lines += ['## '+chapter,'','| 编号 | 分类 | 原文题意入口 | 状态与结果 | 证据 |','|---|---|---|---|---|']
        for task in specs['tasks']:
            if not task['id'].startswith(chapter+'-'):continue
            row=rows[task['id']];requirement=cell(task['requirement']);requirement=requirement if len(requirement)<=180 else requirement[:180]+'…'
            evidence=[]
            for entry in row['evidence']:
                rel=local_path(entry).relative_to(ROOT).as_posix();evidence.append(f'[{Path(rel).name}](../{rel})')
            task_lines.append(f"| `{task['id']}` | {cell(task['classification'])} | [{requirement}](../C/{chapter}/sources/{chapter}.md) | **{row['status']}**：{cell(row['details'])} | {'；'.join(evidence)} |")
        task_lines.append('')
    task_lines += ['C6 原页建设中，任务数为 0，见 [来源范围](../C/C6/SCOPE.md)。B 阶段未执行。','']
    (ROOT/'reports/C_TASKS.md').write_text('\n'.join(task_lines),encoding='utf8')

    offline='''# C 阶段离线材料

`c-final-runtime.tar.gz` 保存 C 的最终运行工作台、AM/NEMU/RT-Thread/NVBoard、两种 SoC 生成器副本、记录的 C4/C5 模拟器二进制和主要固件。逐成员类型、源路径和 SHA-256 的对应关系见 [冻结清单](../../reports/C_runtime_export.json)，Linux 权限保存在 tar 内。链接保留为相对路径；原生成器指向外部 firtool 的绝对链接已作为锁定工具文件实体保存。

`sources/` 保存 C 新增的固定 SoC 主仓库、递归依赖和补充资料原包，见[来源清单](../../reports/C_offline_sources.json)。完整旧课程库和大部分已安装工具不重复打包；F/E/D 的原始源包与冻结运行包仍在累积交付树中。C2 的独立 NEMU I/O 快照在 [C2 snapshot](../C2/snapshot/manifest.json)，其中含 feature/performance 二进制、Capstone 和 Spike 参考库。

包中 `bin/C5/<配置>/sim` 的旧配置分别对应各自验收时的源输入；不能拿最新共享 runner 的时间戳推断所有旧二进制都已重建。每个构建的输入快照、命令和选项保留在 `artifacts/C5/build`。最终源码与软件覆盖文件的关系见[绑定检查](../../reports/C_final_bindings.json)。

## 已执行的离线重放

[重放报告](../../reports/C_offline_replay.json)记录从 tar 中实际解出的模拟器、固件和参考库，重新运行 MicroBench、脚本化 RT-Thread、ChipLink 正例及远端读数据损坏反例。正常结果、周期、退休指令、寄存器、UART 和适用的覆盖计数与原验收一致。重放使用已安装 Linux 的动态加载器/系统库，没有重新编译，也不代表在一台全新离线机器上重新构建所有工具。

在原工作区使用现有发行版/普通用户复跑，命令为：

```powershell
wsl -d YSYX-Linux -u ysyx -- python3 /workspace/projects/ysyx_f_to_b/C/runtime/replay_offline.py
```

它会创建新的隔离解包目录，沿用单重任务预算并保存独立运行记录。再次运行不会覆盖原验收输入，但会更新重放报告和当前证据槽，因此正式交付后重跑会使当前文件与旧 ZIP 的一致性检查如实失败；原 ZIP 是不变的交付快照。

## 只读完整性核验

```powershell
& C:\\YSYX_WORKSPACE\\projects\\ysyx_f_to_b\\scripts\\Verify-C.ps1
& C:\\YSYX_WORKSPACE\\projects\\ysyx_f_to_b\\scripts\\Verify-C.ps1 -External -Archive C:\\YSYX_WORKSPACE\\projects\\ysyx_f_to_b\\YSYX_C_DELIVERY.zip
```

第一条检查范围、结果、快照、冻结运行包、报告链接及历史文件。第二条额外核对原始课程副本和原 D ZIP，并检查交付 ZIP 的全部成员及旁置 `.sha256`。默认不运行长仿真；Python 核验器只使用标准库，可在解压后的工程根目录执行 `python scripts/verify_C_delivery.py`。PowerShell 包装器仍指向本项目已有解释器。

完整功能重建入口位于各章脚本和[执行说明](../runtime/README.md)。多小时的全容量遍历需要单独运行；不要以几十 KiB 的预跑替代完整容量。GUI 复验依赖 SDL、Xvfb、xdotool、scrot 及锁定 NVBoard；综合/生成依赖锁定 Verilator/Yosys/OpenSTA/单元库/JDK/Mill/firtool 和已有 Maven 缓存。安装资产/版本证据见[最终工具锁](../../reports/C_toolchain_final.json)，本包不承诺完全自包含的系统工具环境。

旧 F/E/D 原包保留在工作区，未嵌套到 `YSYX_C_DELIVERY.zip`。它们的旧终点断言仍以当时阶段为准，不能在 C 账本下直接运行旧阶段的完整“停点”核验来判断 C。C 核验器使用历史成员哈希检查保护。
'''
    (ROOT/'C/offline/README.md').write_text(offline,encoding='utf8')
    runtime='''# C 阶段执行入口

C 公开工程完成，执行边界止于 C。固定原文 101 条：68 项公开核心、2 项项目编号适配、22 条选做/背景、9 条方法提醒。C1/C3 没有独立编程作业，C6 原页建设中。总入口是 [C 报告](../../reports/C_REPORT.md)、[任务清单](../../reports/C_TASKS.md)和[机器审计](../../reports/C_AUDIT.json)。

独立工作台 `/home/USER/c-stage` 从 D 的冻结副本创建，F/E/D 不受修改。主框架、子模块、模型、规范、工具路径及版本分别在章节报告中锁定。初始预检保留当时的 pending 状态，后续实际功能结果和[最终指纹](../../reports/C_toolchain_final.json)是完成依据。

大型综合/生成默认一个重任务。用户于 2026-10-29 授权的并行验收允许一个批次最多 8 个独立仿真，共用 PSS 软上限 6144 MiB，按实时余量自动减少并发；固件构建使用 `-j4`。历史脚本保留其原命令和串行默认值。Windows 可用内存不足 2 GiB 不启动批次，运行中 Windows 低于 1 GiB 或 WSL 低于 512 MiB 则停止并记录 RESOURCE_LIMIT。生成器 JVM 堆上限 4 GiB；WSL 实际容量每次运行前复测。策略及实测见 [并行策略](../../reports/C_performance_policy.json)。

只读核验使用 [Verify-C.ps1](../../scripts/Verify-C.ps1)。[导出脚本](export_final.py)生成一次性冻结包，拒绝覆盖；[最终绑定](final_bindings.py)检查源码、二进制及工具指纹；[离线重放](replay_offline.py)从冻结包中取出程序并实际运行。不要在正式交付后随意运行 setup 脚本覆盖已冻结的工作台。

功能复验按需要选择章节入口：C1 和 C3 的 `run_experiment.py`；C2 的 `nemu_io/`、PA2 与设备脚本；C4 的六模式回归、`rtl_tests/run_fabric.py`、性能和时序脚本；C5 的 `verify_*`、`gui_verify.py` 及 `audit_sdram_coverage.py`。具体命令以已保存的 `artifacts/C*/.../run.json` 为准，包含完整选项、cwd、输入哈希与退出码。原始失败和反例保留在 `attempts`，不能通过更改规格来获得通过。

128 MiB 四颗 SDRAM 的当前入口是 [Start-C5-Full-Sdram.ps1](../../scripts/Start-C5-Full-Sdram.ps1)，内部启动 `run_parallel_sdram_job.py --launch`。它调用 `parallel_sdram.py --bytes 134217728 --jobs 8 --label full128`，每个图样独立复位并完整遍历全范围，全部宽度、图样和参考比较保留。实际并发数受内存余量约束，已完成图样经严格哈希核对后可续用。批次结束后用 `scripts/accept_C_parallel.py --full` 作独立汇总。不要同时启动另一个大批次或大型综合。

本工程没有进入 B，没有把旧 E 物理签核移用于 C CPU/SoC。原题、原图与原课程库不作原地修改。
'''
    (ROOT/'C/runtime/README.md').write_text(runtime,encoding='utf8')
    notes=ROOT/'C/C5/NOTES.md';text=notes.read_text('utf8');marker='\n## C 阶段最终验收补充\n'
    text=text.replace('C5 尚在进行，不能把已经跑通的 MROM/UART/Flash 路径当成所有外围设备均已完成。','C5 的公开核心工程与项目编号适配已完成；当前结论及限制见 [C5 审计](../../reports/C5_AUDIT.json)，各开发步骤的原始成败记录仍保留。')
    if marker in text:text=text.split(marker)[0]
    full=sdram[-1]
    text+=marker+f'''
四颗 SDRAM 的完整 128 MiB 验收最终通过：八组独立复位图样合计 {full['cycles']:,} 周期、{full['instructions']:,} 条退休指令。每一组都完整写入并读回 128 MiB，每颗的最高物理字节地址均到达 33,554,431，八组的引脚总量与 CPU 计数相符。按地址范围拆分模型可能隐藏跨范围地址别名，因此本方案只按图样并行，不拆分每组的地址范围；原串行汇编函数字节不变，串行/并行小样本及八个损坏反例已验收。它不声称八图样之间存在一次连续的控制器状态历史。[并行全容量](../../reports/C5_sdram_full_parallel.json)。

最终 Flash/扩展内存候选额外完成了包括 `hello-str` 在内的 35 个 CPU 正例，原始 `wrong.c` 仍被正确拒绝。它补齐了早期 MROM 阶段明确暂缓的项目，详见[最终回归](../../reports/C5_final_cpu.json)。

全部八组真实 NVBoard 会话已完成运行与保存截图的视觉核对。FCEUX 按住 J 改变画面，释放后恢复；原生 PS/2 FIFO 未丢字。RT-Thread 先等原内置命令和完整 Shell 提示符结束，再输入新命令；未知命令后可以继续。应用集成覆盖 Hello、FCEUX 进入/退出/再次启动与 MicroBench 十项校验，堆保护字故意破坏后会失败。[综合会话](../../reports/C5_gui_rtthread.json)。

ChipLink 从相同固定框架打开配置后重新生成，实际生成 175 个模块，仿真同时连接两端的链路引脚及真实远端 RAM。CPU 对 4 KiB 做全部宽度及图样的写读，远端监视器核对字节使能、实际写入和读回；仅在远端读通路翻转一位就触发参考比较失败。上游模型容量仍为 1 GiB，但验收没有遍历这个完整容量。[ChipLink 正反例](../../reports/C5_chiplink.json)。

所有 C5 核心与项目编号适配记录、限制和快照已经汇总到 [C5 审计](../../reports/C5_AUDIT.json)。SPI 中断完成选做项仍未实现；同步切换 RT-Thread 不等于完整抢占式系统，模型功能通过不等于新芯片物理签核。
'''
    notes.write_text(text,encoding='utf8')
    path=ROOT/'README.md';text=path.read_text('utf8');tail=text[text.index('- [F阶段验收报告]'):]
    prefix='''# 一生一芯：独立实现工程

C 阶段公开工程范围已完成：68 项核心工程、2 项项目编号适配及 101 条来源记录已核对，含 C2 的 17 项 PA2 嵌套必做。C4 性能评估中的时序违例明确保留；C6 原页建设中。工程止于 C，未进入 B，个人申请/提交/答辩继续排除。

从 [C 总报告](reports/C_REPORT.md)、[逐项清单](reports/C_TASKS.md)、[机器审计](reports/C_AUDIT.json)进入。累积交付为 `YSYX_C_DELIVERY.zip` 与 `.zip.sha256`；[Verify-C.ps1](scripts/Verify-C.ps1)只读核验保存证据和 ZIP 全部成员。[离线说明](C/offline/README.md)列出最终源码、二进制、已执行重放及外部工具依赖。

F/E/D 原源码、报告、快照和旧交付包保留。D 完成时为 55 项核心、103 条记录，见 [D 历史报告](reports/D_REPORT.md)。E 旧 CPU 的 50 MHz、DRC 0、LVS 0 只属于其原候选，不移用于 D/C 新 CPU。当前单重任务软预算为 6 GiB，按 [执行规则](config/execution_policy.json)检查实时余量；禁止恢复 computer-use 操作 Logisim。

'''
    tail=tail.replace('当前已完成 D，不直接重跑它的最终停点审计','当前已完成 C，不直接重跑它的最终停点审计')
    tail=tail.replace('当前 D 账本下不直接执行其终点断言','当前 C 账本下不直接执行其终点断言')
    tail+='\nD 的 Verify-D.ps1 同样保留 D 终点条件。当前 C 核验器按历史清单核对 F/E/D 的文件与状态，旧交付包继续表示各自完成时的快照。\n'
    path.write_text(prefix+tail,encoding='utf8')
    path=workspace/'README.md';parts=path.read_text('utf8').split('\n\n',2)
    paragraph='这是已完成工具准备的本地电路研究工作区。“一生一芯”独立实现已完成 C 阶段公开工程范围：68 项核心工程、2 项适配、101 条来源记录，详见 [C 交付报告](projects/ysyx_f_to_b/reports/C_REPORT.md)。C4 时序评估中的违例保留，C6 原页建设中；工程止于 C，未进入 B。F/E/D 及旧交付包保持原状，旧 E 的物理签核不移用于新 CPU/SoC。单重任务软内存上限为 6 GiB，运行前复测余量；个人申请/答辩排除。'
    path.write_text(parts[0]+'\n\n'+paragraph+'\n\n'+parts[2],encoding='utf8')
    path=ROOT/'config/toolchain.json';tool=json.loads(path.read_text('utf8'))
    tool['C_stage']={'status':'COMPLETE_ENGINEERING_WITH_DECLARED_LIMITS','audit':'reports/C_AUDIT.json','workspace':'/home/USER/c-stage',
        'final_binary_and_model_lock':'reports/C_toolchain_final.json','final_sources':'reports/C_final_bindings.json','runtime':'reports/C_runtime_export.json',
        'qualification':'Finite RTL/software/device tests and bounded coverage, retained failed timing assessments; no new physical signoff, full privileged-ISA proof or B execution.'};dump(path,tool)
    path=workspace/'config/toolchain.lock.json';lock=json.loads(path.read_text('utf8'));entry=lock['project_toolchains']['ysyx_f_to_b']
    entry.update(status='C_COMPLETE_ENGINEERING_WITH_DECLARED_LIMITS',audit=str(ROOT/'reports/C_AUDIT.json'),fingerprints=str(ROOT/'reports/C_toolchain_final.json'),
        note='C public core68 + adapted2 complete,101 records; C4 timing violations retained. C6 source under construction; no B work or new physical signoff.')
    lock['workspace_state'].update(current_project_status=entry['status'],phase='research_project_checkpoint_complete',research_task='ysyx_f_to_b C public engineering')
    lock['last_updated_utc']=datetime.now(timezone.utc).isoformat();dump(path,lock)
    print('C_METADATA_READY',len(rows),'records',len(outside),'outside-scope records unchanged',flush=True)


if __name__=='__main__':main()
