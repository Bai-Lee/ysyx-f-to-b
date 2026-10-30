# C 阶段交付报告

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
| PSRAM / QPI | 4 MiB | 2,147,777,647 | 260,048,988 |
| SDRAM 16 位 × 1 组 | 32 MiB | 4,537,769,241 | 734,006,529 |
| SDRAM 32 位 × 2 组，8 组独立复位并行（合计） | 128 MiB | 16,997,356,624 | 2,936,031,274 |

对容量 N，全部图样合计的 CPU 读、写次数分别为 `[2N, N, N]`；SDRAM 引脚实际传送读 `16N` 字节、掩码后写 `8N` 字节。四颗 128 MiB 配置中，每颗合计读出 512 MiB、写入 256 MiB，每个独立图样均到达各颗的最高字节地址 32 MiB−1。原 C、展开 C、展开汇编的预跑按相同计数核对；优化只减少循环开销。故意破坏内存的短程对照保留，未用短程成功替代完整容量。[PSRAM（补充包：reports/C5_psram_sweep.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[串行 SDRAM 记录](C5_sdram_sweep.json)、[串行引脚覆盖](C5_sdram_bus_coverage.json)、[并行全容量与逐组引脚覆盖](C5_sdram_full_parallel.json)。

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

C5 MicroBench test 从 Flash 改为 PSRAM 执行后，全程序周期由 140,276,107 降到 53,813,493。相同 SDRAM32 固件从 16 位接口换成 32 位接口，周期由 11,069,716 降到 9,262,308；软件堆上限保持相同。这些是固定仿真配置的周期比较。CoreMark 的单次迭代只作功能/CRC 验收，不是认证分数。[PSRAM 应用（补充包：reports/C5_psram_apps.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[同镜像宽度比较](C5_sdram_apps.json)。

用户要求更积极使用内存后，项目把闲置内存用于独立图样并行，允许最多 8 路并按实时余量减少并发，整个批次共用 6 GiB PSS 预算。64 KiB 小样本的同一批固件串行耗时 13.45 秒，4 路并行耗时 4.04 秒，实测 3.33 倍，峰值 PSS 约 1.19 GiB。最后一次 128 MiB 批次最多 4 路实际执行，续用了 4 组已完成结果，本次墙钟约 4108.7 秒，峰值 PSS 约 1.33 GiB；该耗时不包含此前已完成组和中断尝试，小样本倍率也不被直接当作全容量实测速比。固件构建使用 `-j4`，每组已完成结果可按哈希续用。[策略与备份](C_performance_policy.json)、[合计内存超限反例](C_parallel_resource_controls.json)。

E 阶段旧 CPU 的 50 MHz、DRC 0、LVS 0 仅属于旧候选。C 的新 CPU/SoC 未进行布局布线、寄生提取、DRC/LVS 或实板签核。

## 状态、失败和可复验交付

| 来源记录状态 | 数量 |
|---|---:|
| `OPTIONAL_NOT_IMPLEMENTED` | 1 |
| `PASS` | 79 |
| `PASS_BACKGROUND_REVIEW` | 2 |
| `PASS_EVALUATION_WITH_DECLARED_LIMITS` | 2 |
| `REFERENCE_ONLY` | 17 |

`PASS_EVALUATION_WITH_DECLARED_LIMITS` 表示完成了要求的测量与评估，并保留未达标结果；背景阅读不冒充运行通过。SPI 中断完成通知仍为 `OPTIONAL_NOT_IMPLEMENTED`。C2 的音频可选接口未补做；其较早 GUI 失败部分截图未全部留存，保留了外层失败日志与输入，后续已修正归档保护。这些限制都保留在章节审计中。

当前未通过的诊断记录包括 C4 Icarus TIMEOUT、旧内存预算下的综合 RESOURCE_LIMIT，以及 C5 对归档 Git 的 ownership 检查失败；均没有改记为通过。对应独立替代验证和源码来源已列明。所有保留的失败尝试随包交付。

曾有一次 128 MiB 长测的进程消失，未写入完成记录；其部分图样标记仅作为中断前观察，整体按 UNKNOWN 保存。后台启动方式修复后，用户进一步要求更积极使用内存；并行方案通过小样本功能、速度及资源正反例后，第二次串行尝试被主动终止并保留 FAIL/143 及原因，没有将其部分结果计为通过。最终完成依据是八个独立的全容量图样。[早期中断](C_background_execution.json)、[串行替换记录](C_serial_superseded.json)。

并行初轮完成三组后，WSL 调用 Windows 内存查询时遇到连接错误，监测器按 MONITOR_ERROR 停止整组。三组具有完整结果和输入输出哈希，后续续用；未完成组重新执行。Windows 内存采样随后改用有时限的本机进程与原生物理内存 API；首次实现又遇到文件访问拒绝，完成的第四组仍完整保留。最终改为只追加的项目遥测日志，读取最后一个完整记录；实际 Windows 文件共享冲突、半条记录、格式错误记录、过期和缺失数据均有正反例，后四类无效输入不会被当作新有效样本。采样器在所有受保护任务结束后正常退出，历次原始采样记录随包保存。[通道正反例](C_host_memory_controls.json)、[Windows 共享与记录边界](C_host_memory_io_controls.json)、[采样记录](C_host_memory_monitor.json)。

[最终源码/二进制绑定](C_final_bindings.json)、[工具指纹](C_toolchain_final.json)、[运行包清单（补充包：reports/C_runtime_export.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)和[从包中解出程序后重放](C_offline_replay.json)提供追溯入口。初始 `C_PREFLIGHT.json`、setup/build 报告保留它们当时的阶段状态；当前完成结论以总审计和功能报告为准。

`YSYX_C_DELIVERY.zip` 为累积 F/E/D/C 工程包，包含源码、选定原始仓库归档、运行包、报告、截图和逐命令输入/输出快照；旧交付 ZIP 不嵌套进去。完整原始课程库、已安装工具、JDK/Maven 缓存和系统库是另行锁定的依赖。[离线说明](../C/offline/README.md)列出复验入口与边界。

使用 [Verify-C.ps1](../scripts/Verify-C.ps1)或跨平台 Python 核对保留证据。加 `-Archive` 会检查 ZIP 的全部成员 SHA-256 和 CRC；这个核验不重跑数小时的遍历。实际验收命令、cwd、退出码、用时、输入输出哈希、随机种子/模型选项和资源观测保留在 `artifacts/C*`。

[历史保护（补充包：reports/C_history_preservation.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)确认此前 F/E/D 的 31,216 个文件及原 D ZIP 字节不变；C 范围外的 1,141 条任务记录也与 D 交付时一致。当前并行批次的合计软预算为 6 GiB，Windows 启动余量 2 GiB、运行余量 1 GiB，WSL 运行余量 512 MiB；按每个仿真估算 400 MiB 并预留 Windows 1280 MiB 计算并发数。运行器采样保护不等于操作系统硬限制。
