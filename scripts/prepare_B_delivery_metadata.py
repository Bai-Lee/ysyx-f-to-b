"""Publish B completion documents only after hardware and frozen replay pass."""
from evidence import *
from collections import Counter
import shutil

def read(name):return json.loads((ROOT/'reports'/f'{name}.json').read_text('utf8'))
def main():
    for name in ['B_results','B5_ACCEPTANCE','B4_full128','B_offline_replay','B_final_bindings','B_host_memory_monitor']:
        value=read(name)['status'];assert value.startswith('PASS') or value=='COMPLETE_ENGINEERING_WITH_DECLARED_LIMITS',name
    workspace=ROOT.parents[1];stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f');backup=ROOT/'config/history'/('B_documents_'+stamp);backup.mkdir(parents=True)
    targets={'project_README.md':ROOT/'README.md','workspace_README.md':workspace/'README.md','project_toolchain.json':ROOT/'config/toolchain.json','workspace_toolchain.json':workspace/'config/toolchain.lock.json','execution_policy.json':ROOT/'config/execution_policy.json','B_REPORT.md':ROOT/'reports/B_REPORT.md'}
    for name,path in targets.items():shutil.copyfile(path,backup/name)
    timing=read('B5_final_timing');memory=read('B4_full128');gate=read('B5_netlist');runtime=read('B_runtime_export');replay=read('B_offline_replay');history=read('B_history_preservation');performance=read('B3_performance')
    def perf(name,size,padding):return next(r for r in performance['runs'] if r['variant']==name and r['size']==size and r.get('padding',0)==padding)
    train=perf('b5-release','train',24);test=perf('b5-release','test',24);mc=perf('b5-multicycle-325','test',24);old=perf('b3-uncached-calibrated','train',0);old_cache=perf('b3-cache128-profile','train',24)
    modeled=lambda r:r['simulation']['cycles']/r['model_frequency_mhz']/1000000
    gate_rows='\n'.join(f"| {r['name']} | {r['counts']['cycles']:,} | {r['counts']['resident_pages']} | {r['wall_seconds']:.1f} |" for r in gate['runs'])
    specs=json.loads((ROOT/'B/runtime/course_specs.json').read_text('utf8'));status_counts=Counter(r['status'] for r in read('B_results')['records'])
    report_text=f'''# B 阶段交付报告

B 阶段公开工程范围已完成：**56 项核心工程、2 项工程编号适配、110 条 B 来源记录**均有逐项结果。F～B 的本地公开工程链条由此贯通；选做、官方身份/申请/考试与物理签核边界继续保留。[逐项清单](B_TASKS.md)与[机器审计](B_AUDIT.json)是完成依据。

范围使用已冻结的 v26.07 B1～B4；B2 原页建设中，无独立编程任务。B5 是 v26.07 索引实际链接的 **v23.06 旧页面**，未冒充新发布的流片规范。B1 的 37 条嵌套 PA 来源按“PA3 阶段1、PA4.1 直到启动 RT-Thread”的边界解释，不扩张到后续 Nanos-lite/用户进程。

## 当前可用成果

最终 DUT 为 RV32E、16 个 GPR、四级顺序流水线，带数据转发、128 B 两路 icache、连续命中取指、早期 JAL 目标计算与正确的 fence.i 冲刷。缓存总计 4 行，每行 8 个 32 位字，2 路/2 组。M 模式同步 ECALL/MRET、所需 CSR 和独立 mcycle 支持 RT-Thread 的上下文切换。

完整 SoC 从 Flash 0x30000000 启动，使用真实课程框架的 32 位 AXI/APB、UART、SPI/PSRAM 与 AXI SDRAM 路径。SDRAM 为两 rank、四颗 x16 的 128 MiB 数字功能模型。独立 NPC 从 0x80000000 启动，使用快速功能 RAM，负责快速回归；它的运行时间不作为完整 SoC 性能。

框架沿用已声明的官方 `ysyx6` 固定提交 `bcdcbc3e8d97a11c07d3007e14f33c6147c02a8e` 及递归依赖，再实际重新生成 AXI SDRAM 配置。任务讲义的 v26.07 与兼容框架分支分别锁定，没有把 `ysyx6` 冒充 `2607` 分支原样构建。[框架来源锁](C5_source_lock.json)、[B 的实际生成](B3_axi_generation.json)。

- [实际发布配置的单文件 RTL](../B/soc/build/ysyx_00000000.sv)；[手写流水线模块](../B/soc/rtl/ysyx_00000000_pipe.sv)；[icache](../B/soc/rtl/ysyx_00000000_icache.sv)。
- [最终映射网表](../B/B5/netlist/ysyx_00000000.v)；[最终配置与哈希](B_final_selection.json)。
- [异常与 OS](../B/B1/NOTES.md)、[缓存方法](../B/B3/NOTES.md)、[缓存/性能数据](../B/B3/RESULTS.md)、[流水线方法](../B/B4/NOTES.md)、[流水线对照](../B/B4/RESULTS.md)、[最终检查方法](../B/B5/NOTES.md)。

模块前缀 `ysyx_00000000` 与软件识别常量 `marchid=0x26070001` 分别用于命名和本地识别；都不代表个人学号或官方资格。

## 各章节完成内容

| 章节 | 核心 / 适配 / 来源记录 | 实际工作 |
|---|---:|---|
| B1 | 4 / 1 / 7 | NEMU 自陷/etrace、32/16 寄存器上下文、mcycle 回绕、NEMU 与完整 SoC 的 RT-Thread；错误 t0 恢复与错误参考时钟被拒绝。 |
| B2 | 0 / 0 / 0 | 原页建设中，未补造实验。 |
| B3 | 29 / 0 / 51 | 性能计数、APB/AXI 延迟校准、cache/cachesim/块大小/布局/面积探索、实际 AXI SDRAM、burst、自修改代码和 bootloader fence.i。 |
| B4 | 17 / 0 / 37 | 阻塞流水线、异常、转发、连续取指、分支模拟和上限估算；独立指令/内存期望、错路控制和 fence.i 反例；如实保留性能退化。 |
| B5 | 6 / 1 / 15 | 32 位接口、无 latch/下降沿、规范化导出、静态检查、Icarus RTL/门级完整程序、公开 make 接口本地演练。 |

## 关键验证

最终完整 SoC 跑通 35 个未修改的原始 CPU 正例，包括 hello-str；原 wrong.c 被正确拒绝。另有 1200 条确定性随机算术/访存操作，期望值由独立 Python 整数模型生成，并检查受影响内存字。每条退休指令都计入 NEMU 比较或有明确记录的 MMIO 同步；MMIO 经过独立检查后同步参考状态，不宣称两个独立设备模型。[最终 CPU 回归](B4_final_cpu.json)、[流水线功能](B4_functional_release.json)、[SoC 上下文/OS](B4_release_soc.json)。

最终网表的 Icarus 四值用例如下；大程序使用快速功能 RAM 去除人为等待，完整程序规模、X 行为和检查器不变。没有把 Verilator 二值执行替代四值验收，也没有回标 SDF。

| 程序 | 实际周期 | 驻留 4 KiB 页 | 实际运行秒数 |
|---|---:|---:|---:|
{gate_rows}

RTL 四值对应程序与缺 PC 复位反例均在最终源版本重跑。52 种实际使用标准单元依据 Liberty 检查了 718 个组合向量及 DFF 四值行为，错误 AND2 模型被拒绝。最终导出规范化的 5248 个等价点全部证明通过；这只是配对状态下的导出等价，不能替代完整 CPU ISA 证明。[B5 验收](B5_ACCEPTANCE.json)。

门级测试曾发现旧缓存填充地址表达式在锁定 Yosys 中丢失高位。已用独立小例复现并修复，含旧表达式的历史网表明确失效；最终网表重新综合、时序分析并运行全部上述程序。两处 NOR4 驱动强度调整由脚本重现，连接和逻辑函数一致。历史失败与诊断资料保留。[地址表达式](B5_address_expression.json)、[最终时序](B5_final_timing.json)。

## 全容量内存

八个图样分别独立复位，**每个图样完整写入并读回 128 MiB**；没有把地址区间拆给不同仿真器。覆盖 8/16/32/64 位的软件访问与地址/反码图样，64 位操作在 RV32E 上拆为两次 32 位访问。小样本及八个故意损坏图样先通过检查，才派发完整容量。

八组累计 **{memory['total_cycles']:,} 周期、{memory['total_instructions']:,} 条退休指令**，四颗模型的最高字节地址均达到 33,554,431。CPU 全图样读/写次数分别为 `[2N,N,N]`；当前 AXI BL8 单字读取会观察到一个被丢弃的额外节拍，物理引脚读负载为 32N、写负载为 8N。这与旧 C 阶段 BL1 物理计数的差异明确记录。这里不宣称一次不间断的八图样控制器状态历史。[全容量审计](B4_full128.json)。

一次批次因 Windows 可用内存低于 1 GiB 被守卫停止。{memory['resumed_patterns']} 组已完成图样通过精确哈希复用，其原始资源记录单独绑定，且完成前的已采样余量符合门槛；其余图样从完整地址范围起点重新运行，没有接纳中途未读完的结果，也没有缩减地址范围或降低门槛。

## 性能与面积

最终配置采用 **325 MHz 模型点**，APB/AXI 的 Q8 比率均为 832；这是对 100 MHz 设备的延迟校准。CPU（含 icache 与内部接口）的单元面积 **{timing['area_um2']:.3f} μm²**，低于 25000 μm²，不含完整 SoC 外设与片外存储。建立时间估计约 {timing['setup_frequency_estimate_mhz']:.3f} MHz，采用的 325 MHz 检查有余量；保持时间与最大转换时间检查通过。

| 完整 SoC 配置 | 规模 | 周期 | 指令 | 模型时间 |
|---|---|---:|---:|---:|
| 最终流水线，325 MHz | test | {test['simulation']['cycles']:,} | {test['simulation']['instructions']:,} | {modeled(test)*1000:.3f} ms |
| 最终流水线，325 MHz | train | {train['simulation']['cycles']:,} | {train['simulation']['instructions']:,} | {modeled(train)*1000:.3f} ms |
| 无缓存校准基线，400 MHz | train | {old['simulation']['cycles']:,} | {old['simulation']['instructions']:,} | {modeled(old)*1000:.3f} ms |
| 多周期缓存历史配置，400 MHz | train | {old_cache['simulation']['cycles']:,} | {old_cache['simulation']['instructions']:,} | {modeled(old_cache)*1000:.3f} ms |

最终 train 的主机实际运行时间为 {train['simulation']['wall_seconds']:.2f} 秒；模型程序时间与仿真器墙钟耗时不是同一概念。相对无缓存基线，按校准后的模型时间比较约快 {modeled(old)/modeled(train):.3f} 倍。同为 325 MHz 的 test 对照，最终版本比多周期版本减少 {(1-test['simulation']['cycles']/mc['simulation']['cycles']):.2%} 周期。

不同频率下不能仅比较周期数：历史 400 MHz 多周期 cache 的 train 模型时间比最终 325 MHz 流水线更短，最终约慢 {(modeled(train)/modeled(old_cache)-1):.2%}。最终选择限于已测的 325 MHz 同频候选，不声称是全局最快配置；更高频率组合尚未完整搜索。完整数据、缺失代价近似误差、dcache 成本/收益、分支上限与未采用方案都在 B3/B4 数据表中。

## 如何查看和运行

从本报告与[逐项清单](B_TASKS.md)进入。只读核验：

```powershell
& C:\\YSYX_WORKSPACE\\projects\\ysyx_f_to_b\\scripts\\Verify-B.ps1
# 加 -Archive 会读取整个交付 ZIP 并核对每个成员
```

短演示使用冻结包中的二进制、参考模型和程序，写入新的演示目录，不覆盖原验收报告：

```powershell
& C:\\YSYX_WORKSPACE\\projects\\ysyx_f_to_b\\scripts\\Start-B-HostMemory.ps1
wsl -d YSYX-Linux -u ysyx -- python3 /workspace/projects/ysyx_f_to_b/B/runtime/replay_offline.py --demo
```

源码重建与性能入口见 [B5 使用说明](../B/B5/NOTES.md)。`make perf-test` 是完整 test 规模，`make perf` 默认 train；需要原工作台或按[离线说明](../B/offline/README.md)恢复环境。不要把快速功能 RAM 的时间当成 SoC 性能。

## 交付与明确限制

累积交付为 `YSYX_B_DELIVERY.zip` 和 `.zip.sha256`。实际 ZIP 成员数、大小、CRC/SHA 与当前文件核验结果见 `B_delivery_archive.json`；正式交付前会真实读取验证全部成员。B 冻结运行包含 {len(runtime['members']):,} 个成员，并已从新目录提取后实际完成 {len(replay['runs'])} 个离线重放用例，包括原 wrong.c 反例。[冻结目录](B_runtime_export.json)、[离线重放](B_offline_replay.json)。

此前 {history['checked_files']:,} 个 F/E/D/C 交付文件及旧 D/C ZIP 的哈希保持一致。旧报告中的未通过时序、可选未测项和过去停点仍保留；旧 E 的物理结果不移用于 B。[历史保护](B_history_preservation.json)。

- Nangate45 是教学库；当前没有布局、布线、提取寄生、多角或电源签核，最大电容检查也没有通过结论。325 MHz/单元面积不是实物芯片指标。
- CPU 功能验证是有限程序与图样。流水线可选形式化 miter 在 600 秒达到 TIMEOUT，没有证明或反例结论，断言未删减。
- 未实现完整特权架构、异步抢占、MMU、dcache、BTB、返回地址栈；选做状态在清单中逐项保留。
- RT-Thread 为同步切换与有限脚本工作负载；原 C 的 GUI/应用集成属于其旧候选，不冒充 B 的 GUI 验收。
- 已有 Linux 系统库、编译器、EDA/Maven/JDK 工具及完整原课程库属于锁定的外部依赖。冻结二进制在现有 Linux 环境实际重放，不是任意机器上的免依赖发行版。
- 按用户授权，最多 8 个独立仿真共用 6 GiB PSS，构建 -j4；实际并发按余量下降。资源门槛拒绝的尝试保留，不算功能失败或成功。当前验证任务与内存采样器均已结束。

执行边界停在 B，未进入 A；没有代办官方身份、申请、白名单或考试。
'''
    (ROOT/'reports/B_REPORT.md').write_text(report_text,encoding='utf8')
    offline=f'''# B 冻结运行包

`b-final-runtime.tar.gz` 保存 B 的独立工作台源码、最终/历史已记录模拟器配置、NEMU/Spike 参考、Icarus 字节码与程序镜像，共 {len(runtime['members']):,} 个成员。每个普通文件的 SHA 和受限相对符号链接已逐项核对；清单见 [运行包清单](../../reports/B_runtime_export.json)。完整累积 ZIP 另外保存原始命令、输入/输出快照和阶段报告。

[离线验收](../../reports/B_offline_replay.json)从这个包提取二进制、参考和镜像到新目录后真实运行：上下文、RT-Thread、microbench test、原 wrong.c、4 KiB 全图样中的一个完整图样、门级 Icarus hello。DUT/REF/程序没有借用原工作台中的活文件；运行所需的 Linux 动态装载器/系统库、锁定 Icarus 与项目资源守卫仍来自已安装环境。完整128MiB的原运行证据按哈希核验，短重放不重复耗时的大容量测试。

当前路径为 `/workspace/projects/ysyx_f_to_b`，WSL 分发为 `YSYX-Linux`，用户为 `ysyx`。Linux 工作台在 `/home/USER/b-stage`。使用 `B/runtime/replay_offline.py --demo` 会再次从包提取到唯一新目录，并将结果写到 `artifacts/B/demo/时间戳`，不覆盖交付验收报告。Windows 上先运行 `scripts/Start-B-HostMemory.ps1`，为资源守卫提供只读原生内存采样；它是有时限的任务进程，不是服务或系统设置。

完整源码重建还需要 [工具指纹](../../reports/B_toolchain_final.json)中的工具、原有编译器/系统依赖和生成器缓存。这里未声称在一台空白机器上离线重建了全部工具链。迁移到其它路径或版本需要重新配置绝对路径并复验。不要把包解压覆盖现有工作台；选择空目录或先保留现有工作。

原官方仓库/递归依赖的固定源归档随累积 F/E/D/C 资料保留，B 的实际覆盖源码在本运行包和 `B/` 中。课程 B1～B5 与所用 PA 原文副本在 `B/*/sources`、`B/runtime/sources/pa`；全量原文、图片、附件和外部阅读链接仍以 `/workspace/YSYX_F_B_Archive` 的独立知识库为准。B2 建设中，B5 明确是索引所链接的 v23.06 页面。

旧交付 ZIP、Git 对象和构建缓存没有嵌套进新 ZIP。旧阶段的最终停点审计应对照其原交付包；当前工作树已进入 B，不能把旧报告的“止于 C/D/E”条件当成当前阶段。
'''
    (ROOT/'B/offline/README.md').write_text(offline,encoding='utf8')
    path=ROOT/'README.md';text=path.read_text('utf8');anchor=text.index('- [F阶段验收报告]');tail=text[anchor:].replace('当前已完成 C','当前已完成 B')
    path.write_text('''# 一生一芯：独立实现工程

F～B 的本地公开工程链条已完成到 B。B 的 56 项核心、2 项工程编号适配和 110 条来源记录已核对；B2 原页建设中，B5 使用索引实际链接的旧版公开要求。个人申请/白名单/考试排除，未进入 A。

从 [B 总报告](reports/B_REPORT.md)、[逐项清单](reports/B_TASKS.md)和[机器审计](reports/B_AUDIT.json)进入。最终 RV32E 四级流水线 SoC 可启动 RT-Thread，完整 train、RTL/门级四值及八组独立全128MiB图样已通过。325MHz、24878.182μm²是声明条件下的教学时序/单元面积模型，没有新的物理签核。

交付为 `YSYX_B_DELIVERY.zip` 与 `.zip.sha256`。只读检查用 [Verify-B.ps1](scripts/Verify-B.ps1)；[离线说明](B/offline/README.md)说明实际重放、短演示和外部工具依赖。旧 F/E/D/C 源码、报告、证据与交付包保留；[C 报告](reports/C_REPORT.md)仍是旧阶段的历史完成记录。

'''+tail,encoding='utf8')
    path=workspace/'README.md';text=path.read_text('utf8');anchor=text.index('科学计算、SPICE、数字仿真');tail=text[anchor:]
    path.write_text('''# A_Circuit

“一生一芯”独立实现已完成到 B 阶段公开工程范围：B 的56项核心、2项编号适配、110条来源记录，以及最终流水线SoC、RT-Thread、四值网表和八组完整128MiB验证。详见 [B交付报告](projects/ysyx_f_to_b/reports/B_REPORT.md)和[项目入口](projects/ysyx_f_to_b/README.md)。325MHz/24878.182μm²为教学库模型结果，没有新的物理签核；个人流程排除，未进入A。

已有F/E/D/C源码与证据保留。当前验证任务已结束；后续运行沿用单重任务、最多8个独立仿真共用6GiBPSS、-j4，以及Windows/WSL实时余量门槛。

'''+tail,encoding='utf8')
    path=ROOT/'config/toolchain.json';toolchain=json.loads(path.read_text('utf8'))
    toolchain['B_stage']={'status':'COMPLETE_ENGINEERING_WITH_DECLARED_LIMITS','audit':'reports/B_AUDIT.json','workspace':'/home/USER/b-stage','final_binary_and_model_lock':'reports/B_toolchain_final.json','final_sources':'reports/B_final_bindings.json','runtime':'reports/B_runtime_export.json','qualification':'Finite RV32E pipeline/SoC/RT-Thread validation, Icarus RTL/gate checks, full-range memory patterns,325MHz ideal-wire Nangate45 model; no new physical signoff or official qualification.'}
    toolchain['linux_environment']['current_fingerprints']='reports/B_toolchain_final.json';toolchain['linux_environment']['memory_snapshot_scope']='E fields remain historical configuration; B measured memory and active limits are recorded in B toolchain/resource evidence.';dump(path,toolchain)
    path=workspace/'config/toolchain.lock.json';lock=json.loads(path.read_text('utf8'));old_limits=json.loads(json.dumps(lock['limits']));lock['workspace_state'].update(phase='ysyx_public_engineering_through_B_complete',research_task='ysyx_f_to_b B public engineering',current_project_status='B_COMPLETE')
    lock['project_toolchains']['ysyx_f_to_b'].update(status='B_COMPLETE',audit=str(ROOT/'reports/B_AUDIT.json'),fingerprints=str(ROOT/'reports/B_toolchain_final.json'),note='Public engineering accepted with declared optional/official exclusions and pre-layout timing limits; F/E/D/C preserved. No new physical signoff.')
    lock['last_updated_utc']=datetime.now(timezone.utc).isoformat();assert lock['limits']==old_limits;dump(path,lock)
    path=ROOT/'config/execution_policy.json';policy=json.loads(path.read_text('utf8'));policy.update(current_scope='B public engineering completed with declared limits. Stop before A.',stage_status='COMPLETE_ENGINEERING_WITH_DECLARED_LIMITS',stop_after='B',next_stage='A_NOT_AUTHORIZED');dump(path,policy)
    dump(ROOT/'reports/B_delivery_metadata.json',{'status':'PASS','backup':str(backup),'status_counts':dict(status_counts),'report_sha256':sha(ROOT/'reports/B_REPORT.md'),'runtime_members':len(runtime['members']),'offline_replay_cases':len(replay['runs']),'scope':'Documents and current status merged after validated engineering/replay. Resource numeric limits and previous stage records retained. ZIP verification is the following delivery step.'})
    print('B_DELIVERY_METADATA_READY',flush=True)

if __name__=='__main__':main()
