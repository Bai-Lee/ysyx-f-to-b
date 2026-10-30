# E4 工程入口

当前结论见[验收报告](../../reports/E4_REPORT.md)和[44项清单](../../reports/E4_TASKS.md)。[NOTES](NOTES.md)说明电路、软硬模型、边界与修复过程，[course_specs.json](course_specs.json)冻结原要求。

- `rtl`：组合逻辑、时序逻辑、键盘、VGA、sCPU、RTL程序ROM与NVBoard顶层。
- `csrc`：独立C11 sEMU、C++激励/参考检查、逐指令DiffTest、交互驱动与四态测试。
- `constr`：NVBoard引脚文件。12个开关有效；按钮向量从高到低为L/U/R/D/C，即C产生步进使能、D用于LFSR种子装载。
- `data`：F5/F6程序分开，RGB测试图、MIF及等价MEM，独立预期图像。
- `npc`：可复制到工作台的最小make sim项目，保留官方git_commit调用；父Makefile来自固定官方工作台。
- `offline`：公开NVBoard源码/资源/LICENSE、固定Verilator版本手册、原样工作台基础文件。
- `../../artifacts/E4`：完整运行输出、输入快照、波形、界面截图、逐指令轨迹和历史失败。

本阶段全部已实际运行，用户无需手动补跑。[Run-E4.ps1](../../scripts/Run-E4.ps1)默认重新核验证据与文档后更新ZIP；`-Replay`在既有工具下顺序执行完整回归，含真实NVBoard/GTKWave交互与全新目录离线构建，需宿主可用内存至少3GiB。不会重新安装系统、改变.wslconfig或全局PATH。首次准备脚本不属于日常重放入口。

Linux发行版为YSYX-Linux、普通用户ysyx；工具锁见[E4_tools.json](../../reports/E4_tools.json)。Verilator优化二进制运行于`/home/USER/tools/verilator-stable-src`。按需在当前Linux shell source [env.sh](env.sh)，只设置进程环境。安装工具与WSL磁盘在D盘现有工作区中；ZIP不是OS镜像。原资料库保留于/workspace/YSYX_F_B_Archive，[原文浏览入口](sources/README.md)指向其完整离线HTML。

GUI由隔离Xvfb承载，使用真实上游NVBoard与GTKWave。不是Logisim computer use，也不是实体FPGA验证。独立像素检查验证LED、七段位序和VGA颜色；真实窗口见[GUI清单](../../reports/E4_gui.json)。

构建过程保持一个重任务，Verilator自身-j1，模型最多-j2；大规模循环不生成波形。只在16样本的双控开关上保留VCD/FST。原始源码、错误变体、正确结果和失败记录各自保留，不把非零退出一律当失败，也不把超时当通过。

本轮选用SystemVerilog；Chisel路线及额外进阶阅读未单独展开。17个核心任务、NJU的全部16个细项（含高级键盘选做）已完成；下一个阶段为E5。F/E1/E2/E3的旧阶段终点脚本含当时环境条件，不应拿来覆盖E4状态。
