# 运行最终 B 阶段 CPU

## 最小入口

需要 Python 3.10+、Icarus Verilog 和 `vvp`。Linux 用户可使用发行版的软件包，或从 [Icarus 官方项目](https://github.com/steveicarus/iverilog)获取工具。Windows 可使用已安装的 [OSS CAD Suite](https://github.com/YosysHQ/oss-cad-suite-build)。本脚本不安装软件、不改变全局 PATH。

```bash
python3 tools/run_demo.py
python3 tools/run_demo.py --negative
python3 tools/run_demo.py --wave build/hello.vcd
python3 tools/run_demo.py --netlist
```

Windows PowerShell 使用 `python` 替代 `python3` 即可。若工具不在进程 PATH 中，可以在当前终端设置：

```powershell
$env:IVERILOG = 'C:\your-tools\oss-cad-suite\bin\iverilog.exe'
$env:VVP = 'C:\your-tools\oss-cad-suite\bin\vvp.exe'
python tools/run_demo.py
```

若便携工具需要其 DLL 目录，先按该工具的官方说明激活当前终端环境。不要照抄上述示例路径。原项目验收采用 Icarus 14.0 devel；本次公开入口的实际验证见 [公开验证记录](../publication/verification.json)。

每次调用在 `build/<case>/<timestamp>/` 生成镜像、HEX、编译与运行日志、输入 SHA-256 和结果 JSON。默认每阶段超时 180 秒、最多 100,000 个 CPU 周期。超时或结果不匹配会以非零退出码结束，保留证据。

## 运行的是什么

`B/soc/build/ysyx_00000000.sv` 是最终已验收 B 配置的单文件 RTL，CPU 结构与发布前一致。测试平台 `B/B5/cpu_four_state_tb.sv` 接上功能 AXI 内存、UART 和退出邮箱，模拟不定等待与背压。未写入的内存保持 X。

CPU 复位 PC 为 `0x30000000`。测试平台在该地址提供两条跳转指令，进入 `0x80000000` 的演示程序。程序由 Python 生成真实的 RV32E 机器指令，CPU 执行指令后通过模拟 UART 输出字符。Python 没有代替 CPU 执行该程序。

`--negative` 将程序的退出状态设为 1，用来确认检查器真的拒绝错误结果。只出现一行打印并不能算通过；脚本同时检查仿真进程退出码、成功标记和错误标记。

`--netlist` 改用最终映射网表和随附的单元功能模型。这个入口没有 SDF 回标，也没有提供实物时序结论。

## 自定义程序

```bash
python3 tools/run_demo.py --image your-program.bin --max-cycles 2000000
```

程序需采用小端 RV32E、16 寄存器约束，入口链接到 `0x80000000`。如使用 C，采用合适的交叉编译器及 `-march=rv32e_zicsr_zifencei -mabi=ilp32e`，并自行提供启动代码、栈和所需运行库。

本测试平台接口：

| 地址 | 含义 |
|---|---|
| `0x80000000`～`0x87ffffff` | 功能 RAM；4 KiB 稀疏分配，驻留页预算 8 MiB |
| `0x10000000` | UART 发送字节 |
| `0x10001000` | 写入 32 位退出状态，0 表示成功 |
| `0x10001004` | 写入 `0xb00d600d`，提交退出状态 |

镜像不超过 4 MiB。退出邮箱是验证平台协议，不能当作 RISC-V 指令或完整 SoC 的设备标准。功能 RAM 的访问延迟不能用于推导完整 SoC 的基准性能。

## RT-Thread 和图形界面

原工程已经在完整 B SoC 上运行 RT-Thread 并验证同步上下文切换，结果见 [B 报告](../reports/B_REPORT.md)。最小入口不附带 OS，也不复现课程的全部 SoC 外设。

C 阶段的 NVBoard、打字游戏等交互记录属于 C 候选；它们没有被重新标成最终 B 版本的图形验收。恢复完整 SoC、参考模型和软件工作台需要 [相应上游依赖](REPRODUCIBILITY.md)。

