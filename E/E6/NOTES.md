# E6 实现与验收说明

原题以 [冻结的 v26.07 讲义](sources/E6.md) 为准。执行入口是本目录的 Python 文件，通过已安装的 WSL 发行版 `YSYX-Linux` 运行；它们复用 `E/runtime/common.py` 保存命令、输入快照、结果、退出码和时限。

AM 的 miniRV 编译器将较完整的 RISC-V 操作展开成 E5 的八条指令；没有为了通过测试而扩充 E5 指令集。运行时选择 16 个寄存器、字节编址、小端内存和 0x80000000 入口。课程提供的预编译 klib 已校验并使用，其源码实现不是本阶段自称完成的交付。

`halt` 先设置 a0 再执行 ebreak。a0=0 才是 GOOD_TRAP；wrong 程序返回非零，仿真和顶层 make 都必须失败。测试目录原有的 grep 管道会吞掉失败，已在工作副本修正，wrong 单独保留为负对照。DiffTest 比较提交后的 PC、全部 GPR、内存写入字节和 MMIO 读取序列；实际 RTL 符号扩展错误会被检出，并传递到 make 的失败退出码。

UART 状态每次真正提交的读取更新一次固定种子的随机状态，返回就绪的概率为 1/8。组合求值时的多次 peek 不推进设备状态；参考模拟器消费 DUT 记录的同一次 MMIO 样本。未就绪时写 UART 会明确报错。计时器读取低 32 位时锁存完整的 64 位采样值，随后读高 32 位，避免回绕期间拼出错误时间。

时间有三种不同含义：主机单调时钟衡量仿真墙钟耗时；周期数除以假设频率得到模型中的 CPU 时间；综合时序估计只在指定工艺库和 SDC 下成立。100 MHz 与 1000 MHz 的分数预计相差约十倍，整数微秒和整数分数会造成舍入差异。布局前频率不包含实际布线、完整 SoC 和实物测量；后续 E8 需另外验收。

`test` 规模只适合快速检查功能，循环次数和数据量通常不足以代表稳定负载。性能表必须使用 `train`，并保留每个程序的检查结果、计时、分数及算术/几何平均。并行脚本被显式限制为 nproc=1，以符合本机资源预算。Dhrystone、CoreMark 按原题许可使用两轮；修复了原生平台两轮运行可能不足 1 ms 时，分数格式化的除零问题，算法、验证条件和工作量均保留。两轮所得分数不能作为正式 benchmark 成绩。

FCEUX 使用项目自制的 [交互 ROM 生成器](make_homebrew.py) 和 ROM（原完整交付引用：`homebrew/interaction.nes`），包含原创棋盘图案、按 J 改色和改变脉冲音调，不含商业游戏数据。验证使用真正的 AM/SDL 窗口、X11 按键事件及 SDL 回调产生的 PCM；未声称测试了物理扬声器或完成商业游戏。在 NPC 上使用字符模式，完成规定帧数后按语义条件停止，超时不算通过。

真实排错记录：Windows Git 的 core.autocrlf 导出设置改变了 archbench 文本输入字节，导致 bzip3 在 native 上也无法通过原校验。已用进程级 `-c core.autocrlf=false` 从同一固定提交导出并恢复输入，再完整复验，没有修改预期校验值。新版 Yosys 输出的部分映射单元端口与 LEF 不匹配，导致 ECC 中止；兼容版本的 Yosys 完成了映射和时序分析，并通过独立端口检查。失败日志与修复前后的哈希保留在 artifacts 和 reports 中。

主要证据：[官方测试](../../reports/E6_official_tests.json)、[错误传播](../../reports/E6_difftest_negative.json)、[应用测试](../../reports/E6_benchmarks.json)、[设备](../../reports/E6_devices.json)、[计时器](../../reports/E6_timer.json)、[综合](../../reports/E6_synthesis.json)。最终性能结果及阶段审计待实际完成后加入。
