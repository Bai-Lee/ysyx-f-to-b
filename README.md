# 一生一芯 F～B：处理器设计、验证与工程记录

从基础数字电路逐步实现到 **RV32E 四级顺序流水线 CPU** 的独立工程归档。公开内容包括各阶段源码、设计笔记、正反例、测试与报告，以及对应的任务要求原文。

最终 B 版本具有 16 个整数寄存器、数据转发、128 B 两路指令缓存、AXI 接口，以及运行 RT-Thread 所需的同步异常与 CSR 支持。它是可编程的教学/嵌入式处理器设计，当前以 RTL、网表和仿真工程存在。

> 本项目使用 AI 编程代理辅助实现、调试、测试和整理。它是个人工程实验及可复现记录，不代表课程官方参考答案、官方结业资格或已制造的芯片。有限测试通过也不等于完整 ISA 的形式化证明。

## 从这里开始

| 你想做什么 | 入口 |
|---|---|
| 立即运行最终 B CPU | [快速仿真](docs/SIMULATION.md)；运行 `python3 tools/run_demo.py` |
| 查看最终硬件设计 | [单文件发布 RTL](B/soc/build/ysyx_00000000.sv)、[流水线](B/soc/rtl/ysyx_00000000_pipe.sv)、[icache](B/soc/rtl/ysyx_00000000_icache.sv)、[最终门级网表](B/B5/netlist/ysyx_00000000.v) |
| 理解结构和支持范围 | [处理器与软件说明](docs/ARCHITECTURE.md) |
| 对照任务要求 | [任务原文与逐项索引](requirements/README.md) |
| 查看阶段成果 | 下方阶段表与 [B 阶段原始交付报告](reports/B_REPORT.md) |
| 核对数据与结论边界 | [验证与性能](docs/VALIDATION.md) |
| 查明公开了哪些文件 | [公开清单与脱敏说明](publication/README.md) |
| 获取体积较大的历史输出 | [Releases](https://github.com/Bai-Lee/ysyx-f-to-b/releases) 中的补充成果归档 |

## 快速仿真

准备 Python 3.10+、Icarus Verilog 与 `vvp`。脚本仅使用 Python 标准库；不需要 RISC-V 编译器、GPU 或原作者的目录。

```bash
git clone https://github.com/Bai-Lee/ysyx-f-to-b.git
cd ysyx-f-to-b
python3 tools/run_demo.py
python3 tools/run_demo.py --negative
```

正例输出 `Hello from the final B-stage RV32E CPU!`、`B5_PROGRAM_PASS` 和 `PUBLIC_DEMO_PASS`。反例故意写入非零退出码，检查器应识别 `B5_BAD_TRAP`，脚本再输出 `PUBLIC_DEMO_PASS_EXPECTED_REJECTION`。两次调用都以退出码 0 表示检查器得到预期结果。

```bash
python3 tools/run_demo.py --wave build/hello.vcd
python3 tools/run_demo.py --netlist
```

这是最终 B CPU 加功能 AXI RAM/UART 的轻量四值仿真，不包含完整课程 SoC、NEMU 或 RT-Thread。完整 SoC 与 OS 的历史实测结果单独列在报告中。工具路径覆盖、Windows 运行及自定义程序接口见 [仿真说明](docs/SIMULATION.md)。

## F～B 的工作成果

| 阶段 | 实际工作 | 报告与任务原文 |
|---|---|---|
| F | 逻辑基础、Logisim 电路、测试向量、独立 8 位 sISA CPU 与汇编/状态对照 | [报告](reports/F_STAGE_REPORT.md) · [F 原文](requirements/original/F/) |
| E | HDL/C/Linux 工具练习、NJU 实验、miniRV、C/RTL 对照、AM、设备和总线、早期物理流程 | [E 报告](reports/E_REPORT.md) · [E 原文](requirements/original/E/) |
| D | C 语言和工具链、NEMU/调试/Trace、库函数、RV32E RTL、应用与验证 | [报告](reports/D_REPORT.md) · [D 原文](requirements/original/D/) |
| C | AXI 总线、UART/CLINT、完整 SoC、Flash/PSRAM/SDRAM、外设、RT-Thread、C 候选的图形交互 | [报告](reports/C_REPORT.md) · [C 原文](requirements/original/C/) |
| B | 异常/上下文、性能计数、缓存、流水线与转发、四值门级验证、128 MiB 全容量图样 | [报告](reports/B_REPORT.md) · [逐项结果](reports/B_TASKS.md) · [B 原文](requirements/original/B/) |

章节、计数与适配以各阶段清单为准。B2 原页建设中；B5 使用索引实际指向的 v23.06 页面，其他 B 主章依据冻结的 v26.07 内容。未进入 A；个人申请、白名单和考试不包含在工程完成声明中。

## 最终 B 版本的结果

| 项目 | 已记录结果 |
|---|---|
| 结构 | 单核、单发射、顺序四级流水线；IF / ID / EX / MEM-WB |
| 缓存 | 128 B icache，2 路、2 组，每行 8 个 32 位字；支持 `fence.i` |
| 程序 | 35 个原始 CPU 正例、确定性随机操作、MicroBench、RT-Thread 等有限工作负载 |
| 内存 | 八个图样分别完整写入、读回 128 MiB，累计 28,850,962,770 周期 |
| 四值验证 | Icarus RTL 与门级运行；门级 hello、hazards、fence-prefetch、MicroBench 和 RT-Thread |
| 教学模型 | 325 MHz 选定时序模型点；CPU 单元面积 24,878.182 μm² |
| train 基准 | 1,575,356,367 周期；模型时间 4,847.250 ms；当次主机仿真耗时 2,174.52 s |

325 MHz 和面积来自声明条件下的 Nangate45 教学库模型。B 版本没有布局布线、寄生提取、多角/电源签核或实物测量；最大电容检查也没有通过结论。E8 旧候选的物理结果不适用于 B。历史 400 MHz 多周期缓存候选在部分基准上更快，最终流水线并非已证明的全局最优设计。

## 目录与复现范围

`F/`、`E/`、`D/`、`C/`、`B/` 保留阶段目录，`reports/` 保留历史报告，`requirements/` 提供任务文本与来源，`tools/run_demo.py` 是本次新增的便携入口。

脱敏后的历史脚本保留研究过程，部分依赖外部课程仓库、Linux 工具链和原工作台布局。`/workspace`、`C:\YSYX_WORKSPACE`、`/home/USER` 是占位路径；历史脚本并不因此自动成为跨机器的一键安装器。请从新仿真入口开始，按 [依赖说明](docs/REPRODUCIBILITY.md) 恢复更多功能。

公开快照采用独立提交历史。大交付 ZIP、完整第三方仓库、可再生成的二进制缓存和未核验的外部素材没有混入 Git 历史；逐项去向见公开清单。历史失败、TIMEOUT、未运行项及模型限制仍然保留。

## 来源与许可

课程来自 [一生一芯官方文档](https://ysyx.oscc.cc/docs/)，框架与工具归各上游项目。任务原文、第三方代码及模型保留其来源和权利声明，不适用本项目对原创内容的授权。见 [LICENSE](LICENSE)、[THIRD_PARTY.md](THIRD_PARTY.md) 与 [原始依赖清单](THIRD_PARTY_SOURCES.md)。

如需报告问题，请提供阶段、源码版本、工具版本、最小输入和首次偏离预期的输出；不要在 Issue 中发布个人凭据或课程个人资格信息。

