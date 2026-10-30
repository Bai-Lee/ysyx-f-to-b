# E7 验收报告

30 项必做工程任务已完成本地验收；可选的完整 SoC archbench 长时扫描未选择。

[原理、方法和限制](../E/E7/NOTES.md) · [机器审计](E7_AUDIT.json) · 真实虚拟板截图（原完整交付引用：`../artifacts/E7/gui/completed.png`） · [73 项 SoC 测试](E7_SOC_TESTS.md)

| 结构 | hello 周期 | 提交指令 | IPC | 20 项 train 几何平均分（100 MHz） |
|---|---:|---:|---:|---:|
| ifu | 32922 | 16461 | 0.500000 | 72.209 |
| lsu | 38150 | 16461 | 0.431481 | 61.080 |
| valid | 40288 | 16461 | 0.408583 | 53.721 |

每种结构还运行 21 项 archbench test、3 个内核 benchmark、hello 及两个完整 FCEUX 字符帧。7 组固定/随机延迟各通过 73 项官方测试，读数据翻转和重复写负对照均拒绝。

| SoC 场景 | CPU / 外设 MHz | k | train 最短时间（s） | Marks | 应用 IPC |
|---|---:|---:|---:|---:|---:|
| baseline_k1 | 25 / 25 | 1 | 76.162395 | 1 | 0.008493 |
| baseline_kmax | 125 / 25 | 5 | 75.515393 | 1 | 0.001713 |
| area_kmax | 75 / 25 | 3 | 75.515393 | 1 | 0.002855 |

这里的时间由 mcycle 与指定频率换算，软件校验、逐指令 DiffTest、实际 TX 解码和时钟波形同时检查。Marks 是粗粒度整数，比较小差异时应查看最短时间。

BALANCE 综合报告 130 MHz、9915 µm²；AREA 为 89 MHz、9306 µm²。AREA 在原 100 MHz 约束下未闭合，采用 75 MHz 的合法整数倍用于本阶段比较。60% 利用率和 30000 元/mm² 的教学模型给出约 495.75 元、465.30 元，均不包含 SoC、封装和测试等成本。

原始 RTC 测试在独立 NPC 上的三个输出间隔为 0.961s, 0.983s, 0.980s。真实 SoC 的计数器也逐周期核对，但完整日期打印约需 1.7 秒；两种观察分别保存。

| ID | 状态 | 要求 |
|---|---|---|
| E7-M001 | PASS | 统计 hello 的提交指令数和周期数 |
| E7-M002 | PASS | IFU 接 SimpleBus，一周期后返回取指数据 |
| E7-M003 | PASS | 记录 IFU 改造后的 hello IPC 与 archbench 性能 |
| E7-M004 | PASS | LSU 接 SimpleBus，load 按三周期执行 |
| E7-M005 | PASS | 记录 LSU 改造后的 hello IPC 与 archbench |
| E7-M006 | PASS | IFU/LSU 请求回应增加 valid |
| E7-M007 | PASS | 记录 valid 扩展后的 IPC 与性能 |
| E7-M008 | PASS | 固定 5/10/20 周期及 LFSR 随机延迟测试 |
| E7-M009 | PASS | 取得并锁定 ysyxSoC 与依赖 |
| E7-M010 | PASS | 按 minirv cpu-interface 精确接入 SoC |
| E7-M011 | PASS | 16MB flash 行为数组装载现成 hello |
| E7-M012 | PASS | AM minirv-ysyxsoc 运行自行编译 dummy |
| E7-M013 | PASS | 在 minirv-ysyxsoc 跑 cpu-tests/riscv-tests |
| E7-M014 | PASS | 计算 25MHz/16 倍过采样下 115200 与 57600 波特率的除数与误差 |
| E7-M015 | PASS | 初始化 UART16550 并轮询发送队列 |
| E7-M016 | PASS | UART TX 接 NVBoard 并匹配两种除数定义 |
| E7-M017 | PASS | GPIO LED 寄存器与软件流水灯 |
| E7-M018 | PASS | 程序读取 16 位拨码开关实现密码锁 |
| E7-M019 | PASS | 软件驱动八位十六进制显示 |
| E7-M020 | PASS | csrrs 读取 mvendorid 与 marchid |
| E7-M021 | PASS | 添加 mcycle/mcycleh |
| E7-M022 | PASS | 用 mcycle 实现 AM 计时测试 |
| E7-M023 | PASS | 测 SoC hello IPC，并用波形交叉检查 |
| E7-M024 | PASS | 跑 100.blockchain，记录 min time 和分数 |
| E7-M025 | PASS | cpuClock 为 clock 的整数倍 |
| E7-M026 | PASS | SoC/外设 25MHz、k=1 的性能基线 |
| E7-M027 | PASS | 取 k 最大整数且 k×25MHz 不超过综合频率 |
| E7-M028 | PASS | 按教学模型估算面积和流片费用 |
| E7-M029 | PASS | 换面积优化策略再评估性能/费用 |
| E7-M030 | PASS | 支持独立 NPC 与 SoC 两种仿真模式 |
| E7-O001 | PASS | 修改成多周期处理器后, NPC就并非每个周期都执行一条指令了. 为了让DiffTest机制可以正确工作, 你需要对检查的时机稍作调整: 只有当一条指令执行结束时, 才进行DiffTest的检查. 为此, 你可能需要从RTL中通过DPI-C读取一些状态, 来帮助你判断应该什么时候进行DiffTest的检查. |
| E7-O002 | NOT_SELECTED_OPTIONAL | 如果你有耐心, 你可以在 minirv-ysyxsoc 上运行 archbench 的所有测试程序. 为此, 你可能需要等待将近10小时, 但可以预见, 你将会得到一个不太能让人满意的评测结果. |
| E7-O003 | PASS_DOCUMENTED | 你可能会发现, 在 k = 1 和 k 取最大值这两种情况下, 100.blockchain 程序的运行性能几乎没有变化. 这意味着, 提升NPC的频率, 在程序性能方面几乎没有带来正向的收益. 思考一下, 为什么会这样? 在当前的SoC中, 处理器的频率是否值得我们去优化? 如果值得, 优化处理器频率带来的收益具体是来自于哪里? 如果不值得, 是什么因素抵消了优化处理器频率带来的收益? |
| E7-R001 | PASS | 我们在2026年8月16日19:30:00更新了讲义中 gen.sh 脚本的使用方法, 从而修复了无法在ysyxSoC的程序中传递 mainargs 的问题. 如果你此时还未在AM中创建 minirv-ysyxsoc.mk , 请重新阅读上文 在SoC上运行第一个程序 小节中关于使用 gen.sh 脚本的内容. |
| E7-R002 | PASS | 我们在2026年8月15日17:30:00更新了ysyxSoC的代码, 实现了跨时钟域的功能, 同时提供了 cpuClock 作为仿真顶层的端口. 如果你在这个时间之前获取ysyxSoC的代码, 请备份后必要的改动后, 删除 ysyxSoC 的目录, 然后通过 bash init.sh ysyxSoC 重新获取代码. 然后, 重新阅读上文 接入 ysyxSoC 的步骤, 了解如何驱动 cpuClock`. |
