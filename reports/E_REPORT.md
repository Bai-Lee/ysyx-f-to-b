# E 阶段工程交付报告

**E1–E8 的公开工程要求已在约定范围内完成本地实现与验收。** E5–E8 的 79 项核心任务全部通过；E9 的个人材料、申请和答辩按既定范围排除。E1、E2 的执行分支和 E3 的六项声明例外保留，因此本报告不表示逐字完成所有个人课程要求或取得官方入学资格。

[机器审计](E_AUDIT.json) · [E5–E9 的 96 项结果](E_TASKS.md) · [最终工具与模型指纹](E_toolchain_final.json) · [只读核验入口](../scripts/Verify-E.ps1)

| 阶段 | 已交付的主要结果 | 详细证据 |
|---|---|---|
| E1 | 69 道指定题 + 43 道建议题；14 个错误实现被检出；原理图结构转译 | [E1 报告](E1_REPORT.md) |
| E2 | 独立链表、递归与指针；本机/Python 对照/Compiler Explorer 检测 | [E2 报告](E2_REPORT.md) |
| E3 | 234 个子项：228 项完成、六项声明例外；真实 Linux 实作 | [E3 报告](E3_REPORT.md) |
| E4 | 17 项核心任务、16 个 NJU 子项；sCPU/sEMU、DiffTest、NVBoard/GTKWave | [E4 报告](E4_REPORT.md) |
| E5 | 17 项核心任务；8 指令、16 寄存器 miniRV；12 程序、6 个错误实现对照 | [E5 报告](E5_REPORT.md) |
| E6 | 22 项核心任务；73 个官方测试；AM/设备/FCEUX；80 次 train；真实综合 | [E6 报告](E6_REPORT.md) |
| E7 | 30 项核心任务；511 次总线测试；135 次应用运行；实际 SoC/GPIO/CSR/性能验证 | [E7 报告](E7_REPORT.md) |
| E8 | 10 项核心任务；RTL 与门级四值仿真；完整物理流程及签核导出 | [E8 报告](E8_REPORT.md) |
| E9 | 三项个人事项明确排除；保留原讲义 | [范围说明](../E/E9/SCOPE.md) |

## 最终 CPU 与版图

最终物理候选是 BALANCE 3 综合网表、顶层 `ysyx_00000000`。实际布线输入与已仿真的网表 SHA-256 一致；12 个后端步骤全部完成。使用锁定 ICsprout55 库、SDC 和提取寄生进行检查，**50 MHz 约束闭合，DRC 0、LVS 0**。

| 检查或指标 | 实际结果 |
|---|---:|
| 时序角 / SPEF 文件 | 13 / 9 |
| 最差 setup WNS / hold WNS | 2.707 ns / 0.085 ns |
| setup TNS / hold TNS | 0 / 0 ns |
| die 面积 / core 面积 | 34,596 / 33,124 µm² |
| 签核清单文件 | 210，逐项校验大小与 SHA-256 |
| 完整 microbench | 22,129,163 周期，GOOD_TRAP |

完整 microbench 同时在 RTL、Verilator 网表和 Icarus 14 原始 UDP 标准单元模型中通过。功能仿真未加 SDF；时序结论来自独立的多角 STA。界面显示的 58 MHz 是工具估计，本次正式检查的约束为 50 MHz。

完整签核包（原完整交付引用：`../E/E8/signoff/cpu-baseline-signoff.tar.gz`）包含网表、GDS/DEF/LEF/LIB、SDC、SPEF 和 STA 结果；原生日志包（原完整交付引用：`../E/E8/signoff/native-run-evidence.tar.gz`）补充 120 个运行日志、配置与分析文件。[版图 PNG（补充包：E/E8/signoff/layout.png）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、ECOS 面板（原完整交付引用：`../artifacts/E8/gui/dashboard_ready.png`）和原生二维查看器（原完整交付引用：`../artifacts/E8/gui/native_micrometers.png`）均已实际查看，视觉结论与图片哈希绑定。

![最终 CPU 版图](../E/E8/signoff/layout.png)

## 功能与性能结论的范围

E7 在真实 SoC Flash 启动后执行 73 个原始测试体，各对象已分配节的字节保持不变；这是一次批处理启动，另有独立 wrong 负对照，不是 73 次独立冷启动。UART 同时核对寄存器访问和 TX 实际字节；GPIO 实际窗口完成口令、流水灯和数码管检查。演示编号 26070001 不是本人学号。

原始 RTC 测试在独立 NPC 环境经主机时间校准，三个间隔为 0.961、0.983、0.980 秒。SoC 上完整日期格式化较慢，未把它说成严格一秒输出。

实际 SoC 的 blockchain train 在 25、125、75 MHz 三个条件下完成。25→125 MHz 的最小报告时间仅改善约 0.85%，说明此程序受系统交互限制；时钟变化由实际镜像和波形确认。AREA 综合策略降低单元面积，但未满足 100 MHz 目标，性能比较使用其可行的 75 MHz。课程成本模型为假设估算，不是制造报价。

原始失败、RESOURCE_LIMIT、超时和兼容性问题均保留。最终物理流程采用官方 `--only` 入口逐步运行，每步使用新进程释放内存；没有修改质量门槛、删断言或改基准答案。无宏单元设计仅保留工具允许的 `config.macro_locations` 提示。

## 已声明的适配与个人范围

E1 采用原始 `.circ` 连线解析到结构 Verilog 的命令行方案；未操作 Logisim GUI。E2 采用原文允许的独立链表能力分支，未声称完成全部 CEX 练习。E1、E2 的扩展书籍、视频及注册 OJ 未冒称全部完成。

E3 六项例外是：每日卡片练习时长、一个月编辑器习惯、两项不存在的真实启动历史、本地点文件未发布、已准备的修正补丁未公开发 PR。合成历史样例始终标为样例。E7 的全量 SoC archbench 长测、E8 的最大利用率搜索属于未选选做；Chisel 专项不适用于当前 Verilog 路线。

E9 不代写个人经历、提交申请、填写本人身份或安排答辩。这里的“完成”指约定工程范围，不是芯片实物、课程官方认证或任意输入的形式化证明。

## 文件、环境与复验

项目 ZIP 名为 `YSYX_E_DELIVERY.zip`，包含 F 历史成果、E1–E9 代码与说明、逐命令证据、冻结快照及上述签核包。配套 `.zip.sha256` 和 `reports/E_delivery_manifest.json` 用于核对。归档内保留此前阶段报告的历史时间与当时状态；当前总状态以本报告和 `E_AUDIT.json` 为准。

[离线材料](../E/offline/README.md)包含 8 个固定提交顶层源码归档、官方 klib 和 726 文件的补丁运行副本。完整课程仓库、全部工具及 PDK 安装资产仍位于已锁定的 D 盘/WSL 路径；该 ZIP 不是系统安装包。来源归档未修改。

用户授权后，WSL 内存上限从 2 GiB 调整为 4 GiB；原配置已经备份。配置中的 swap 仍为 2 GiB，但本次实测 Linux 可用 swap 为 0。重任务仍串行执行；物理流程限制两个逻辑核并监测内存。没有安装 CUDA 或修改全局 PATH。

在 PowerShell 执行只读核验：

```powershell
& C:\YSYX_WORKSPACE\projects\ysyx_f_to_b\scripts\Verify-E.ps1 -External
& C:\YSYX_WORKSPACE\projects\ysyx_f_to_b\scripts\Verify-E.ps1 -Archive C:\YSYX_WORKSPACE\projects\ysyx_f_to_b\YSYX_E_DELIVERY.zip
```

核验器检查保留结果、冻结文件、签核成员、文档链接及 ZIP 完整性，并包含损坏摘要和非法归档路径负对照；它不重新执行长时仿真。功能重放分别见 [E7 入口](../E/E7/README.md)、[E8 入口](../E/E8/README.md)及各阶段报告。整项工作在 E 阶段停止，未自动进入 D 阶段。
