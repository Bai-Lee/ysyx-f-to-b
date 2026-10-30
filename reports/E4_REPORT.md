# E4本地工程验收报告

E4按已冻结的v26.07清单完成：**17/17核心任务、NJU五个实验的16个细项通过**，包含Shift/CTRL高级选做。44个总节点均有记录；Verilator额外进阶阅读和Chisel路线两项未单独展开。下一阶段为E5。更新时间：2026-10-24T21:33:57.605698+00:00。

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

审计核验129份当前命令记录，以及119份输入快照、298个快照成员；历史失败及修复均保留。工具路径/版本/摘要见[工具锁](E4_tools.json)，逐条实现、交付物和验收见[E4_TASKS.md](E4_TASKS.md)，技术解释与已修问题见[NOTES](../E/E4/NOTES.md)，机器结论见[E4_AUDIT.json](E4_AUDIT.json)。

关键真实截图：求和LED=55（原完整交付引用：`../artifacts/E4/gui/cpu_sum55.png`）、键盘ASCII（原完整交付引用：`../artifacts/E4/gui/keyboard_a.png`）、VGA静态图（原完整交付引用：`../artifacts/E4/gui/vga_static.png`）、GTKWave FST（原完整交付引用：`../artifacts/E4/gui/gtkwave_fst.png`）。界面运行在隔离Xvfb，不需要操作用户桌面，也没有使用Logisim computer use。

两个差分反例的首错位置已核验：禁止写R0，在PC=0的li处报告GPR0的0/8差异；负偏移误当无符号数，在PC=8的bner0处立即报告PC=0x16/0x06，GPR仍相同。日志没有等到最终sum错误才报错。DiffTest原始证据（原完整交付引用：`../artifacts/E4/cpu`）

[离线复验](E4_offline.json)在全新Linux目录从本地导出重建工作台，真实make sim及tracer追踪，重新编译C sEMU并得到55，也展开并核验NVBoard源码/资源。编译器、WSL根文件系统和完整原资料库仍是既有外部依赖；工程ZIP不冒充完整操作系统镜像。

预算保持WSL2的2GiB内存、4vCPU、D盘2GiB swap，编译最多-j2，Verilator自身-j1；本阶段没有修改.wslconfig或全局PATH。界面进程已退出。可重复执行入口为[Run-E4.ps1](../scripts/Run-E4.ps1)，默认做证据/文档核验并更新ZIP，-Replay执行完整本地回归。原讲义与F/E1/E2/E3历史交付保留，旧阶段终点审计不用于覆盖当前E4状态。
