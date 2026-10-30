# B5：最终导出、四值检查与网表验收

来源是 v26.07 索引实际链接的旧 v23.06 B5 页面。这里执行其公开本地技术检查，不把旧页面改称新发布的流片规范；不申请白名单、学号、排期或考试，不声称官方 CI、流片或物理签核通过。

## 可复现的输入

手写 RTL 在 `B/soc/rtl`。`make -C B/soc verilog` 生成 `B/soc/build/ysyx_00000000.sv`，包含所有所需的带前缀模块；`00000000` 是稳定工程编号，不是个人学号。生成时固定复位 PC=0x30000000、128 B 两路 icache、流水线、转发、连续取指与早期 JAL 目标计算，并去除仿真 DPI/事件计数。

导出脚本只做三类语法规范化：三个 beat 比较显式零扩展为 32 位，两个整数预测参数显式比较是否非零，给生成块分支命名。Yosys 的 `equiv_make`、`equiv_simple`、`equiv_induct` 对 5248 个等价点给出全部通过；它说明配对状态下规范化前后保持一致，不是处理器 ISA 正确性证明。初次只用组合检查未证明所有状态点、自动结构匹配产生错误中间配对的尝试均保留，最终没有删去未证明的原始点来凑通过。

最终网表为 `B/B5/netlist/ysyx_00000000.v`。它来自 `B/B3/synthesis/b5-release-cpu`，再由 `final_netlist.py` 的 Yosys 脚本把两只 NOR4_X1 换成 NOR4_X2；端口、网络、每个实例的连接以及除这两处类型之外的全部单元字段逐项一致。没有手工编辑一个不会被构建流程重现的中间文件。

## 为什么要做网表仿真

RTL 上正确不代表综合后的逻辑一定符合预期。本次锁定 Yosys 下，旧的缓存填充地址表达式 `address & ~32'(WORDS*4-1)` 在组合上下文中丢失了高位，第一次应访问 0x30000000，却访问了 0。独立小例同时保存 Icarus 与 Yosys 结果，现有实现改用明确的 32 位掩码和有界字偏移。

所有带旧表达式的综合网表都保留为无效历史候选。新网表的首次 Flash 访问、后续 0x80000000 程序及缓存功能重新检查。不能用旧的面积、频率和 PASS 字样作为修复后网表的验收。`select_release.py` 是历史选择脚本，不应对最终发布源再次执行。

## 结构和静态检查

最终映射的 2371 个 DFF_X1 的 CK 都直接连接顶层 clock；DFF 模型的上升沿/下降沿/未知输入行为另有实际 Icarus 验收。没有 DLL_X1/X2、DLH_X1/X2 或其它锁存器。两个 AXI 方向的数据和地址均为 32 位，写 strobe 为 4 位。检查器会拒绝注入 latch、错误时钟连接和缩窄接口的变体。

导出文件不含下降沿时序逻辑或 DPI。原始源中的 negedge 块只是 `ifndef SYNTHESIS` 内的仿真观测，不会进入交付 DUT。Verilator 原始 `-Wall` 日志保留全部 warning；导出后仅剩已核对的文件名、UNUSED 调试/性能信号和接口参数。显式忽略这些类别后检查必须成功；没有通过 `-Wno-fatal` 掩盖位宽、锁存器或多驱动问题。

## 标准单元与四值模型

使用课程 Nangate45 包中的模型和典型库，许可证随文件保留。最终网表用到 52 种单元：组合逻辑依据解析的 Liberty 函数穷举共 718 个二进制向量；DFF 检查保持、正确时钟沿和 X 传播。错误 AND2 模型必须失败。它们是零延迟功能模型，没有回标 SDF。

四值 testbench 接在公开 AXI 边界，未写过的 RAM 和未复位缓存 payload 保持 X；控制/地址和有效写字节中的未知值会失败。虚拟地址范围覆盖 128 MiB，按 4 KiB 页分配，驻留页上限为 8 MiB；每个程序实际页数在报告中给出。这不是用稠密大 RAM 初始化为零来掩盖缺复位问题。

RTL 和门级分别运行完整 test 规模 microbench、脚本式 RT-Thread，以及 hello、冒险和 fence.i 程序。门级大程序启用快速功能 RAM，只消除人为的等待周期；程序输入、X 行为、AXI 规则和全部断言不变。该模式不提供 SoC 性能数据。缺少取指 PC 复位的反例会明确失败。最终成功与否以 `B5_ACCEPTANCE.json` 为准，只有启动记录或进度输出不能算通过。

## 面积与时序的有限结论

最终 CPU（含 icache 与内部接口）的单元面积为 24878.182 μm²，低于 25000 μm²；不含完整 SoC 外设和片外存储。时序模型采用 Nangate45 typical、理想 clock/线网、20 ps 输入转换、50～100 ps 输入延迟和 5 fF 输出负载。建立时间估计对应约 348.732 MHz，选择 325 MHz 评估；保持时间余量约 0.057726 ns，调整驱动后最大转换时间违例为零。

锁定 OpenSTA 的最大电容报告选项不可用，因此这项没有通过结论。没有布局、布线、提取寄生、真实时钟树、PVT 多角或芯片电源分析；上述频率与面积只能用于声明的教学模型，不能当成实物芯片指标。

## 本地入口

先在 Windows 启动当前项目的内存采样器，再进入已安装的 WSL 环境。以下目录相对于项目根目录，实际工具使用锁定的绝对路径：

```sh
make -C B/soc verilog
make -C B/soc sim-iverilog IMG=/absolute/path/to/standalone.bin
make -C B/soc sim-iverilog-netlist IMG=/absolute/path/to/standalone.bin \
  NETLIST=/absolute/path/to/ysyx_00000000.v CELLS=/absolute/path/to/cells.v
make -C B/soc perf-test
make -C B/soc perf
```

`IMG` 是本项目独立 AM ABI 的二进制，从 0x80000000 放置；固定 Flash reset 通过两条指令跳转到它。结束由 AM 的可检查 MMIO 退出协议给出。`make sim` 运行完整 SoC 的计数器、上下文和 RT-Thread 有限回归。以上是公开命令形状的本地演练，不是对任意未适配 ABI、官方隐藏测试、NVBoard CI 环境的兼容承诺。

`perf` 默认完整 train，可能耗时很久；`perf-test` 为完整 test 规模。CPU、参考模型、镜像和原始报告哈希一致时，性能入口可以复用已经完成的记录，复用会保留原始执行证据。首次恢复请先按 `B/offline/README.md` 准备工作台和外部锁定工具。
