# D 阶段交付报告

已完成约定的 D1–D8 公开工程范围：**55 项核心任务通过，103 条来源记录逐一归档**。D9 原页仍为“建设中”，没有补造任务；D6 原文 todo 排除。背景索引、未采信说法、实际实验分别列明，不把 103 条都称为实验通过。工程停在 D，不进入 C。

从 [103 条逐项表](D_TASKS.md)、[机器审计](D_AUDIT.json)、[源码与二进制绑定](D_final_bindings.json)进入。累计交付文件为 `YSYX_D_DELIVERY.zip` 和 `.zip.sha256`；旧 `YSYX_E_DELIVERY.zip` 保留原字节。

## 交付内容

| 部分 | 实现与实际验收 | 教学说明 |
| --- | --- | --- |
| D1 编译与 C 语义 | GCC/Clang、LLVM IR、RISC-V 反汇编、优化计时、GDB 启动/退出、UB 对照 | [D1](../D/D1/NOTES.md) |
| D2 PA1 | SDB、表达式、32 个监视点；10000 个实际 GCC oracle 样本、sanitizer 与错误注入；独立 PA1 快照 | [D2](../D/D2/NOTES.md) |
| D3 RV32IM NEMU | 2392 个独立边界检查、Spike 比较、81 个官方程序；编码/地址/加载负例 | [D3](../D/D3/NOTES.md) |
| D4 程序表示 | 指令、调用约定、栈、数组/结构体、C 与 ISA 语义边界；原页无编程题 | [D4](../D/D4/NOTES.md) |
| D5 AM 与 klib | 21199 次主机比较；10000 次分配操作及碎片检查；三平台各 5007 项 | [D5](../D/D5/NOTES.md) |
| D6 RTL、综合和工艺库 | 事件队列、六个 Yosys 阶段、4096 周期映射对照、TT/SS/FF 评估、747 项单元索引、CDL/LIB/LEF 分析 | [D6](../D/D6/NOTES.md) |
| D7 跟踪与差分 | itrace/mtrace/ftrace、ELF 与尾调用、55 个损坏/边界 ELF 样本、真实 ADDI mutant、81 个旧测试回归 | [D7](../D/D7/NOTES.md) |
| D8 RV32E NPC | 16 寄存器 RTL、SDB/trace、动态 NEMU REF、逐提交与 store 对照、复位/故障检查、完整应用回归 | [D8](../D/D8/NOTES.md) |

D8 重新编译并通过 73 个官方测试、1758 个边界检查、48 次 native/RV32E 应用 test 运行和 20 个 archbench train。另核对早期 12 个自编测试、计时器、klib、官方原生键盘以及 FCEUX 图像/按键/音频回调。FCEUX NPC 观察到两帧完整字符画，按第三帧头停止；计时器按 1/2/3 秒输出停止，均不是把超时当成功。

为运行这些应用，补齐了受限内存文件 API，并修复分配器在碎片较多时的性能问题。保留原始输入与预期 checksum，没有删除断言或降低正确性要求。所有修复前失败、真实故障注入与中止原因保存在 attempts 或诊断目录。

## 范围与限制

- NEMU 是本阶段 RV32IM TRM，NPC 是 RV32E 基础整数执行环境；未实现 C 阶段中断/特权、M/C 扩展硬件、缓存或 Linux 启动。软件乘除程序通过不代表硬件有 M 指令。
- 普通提交与 REF 独立比较；MMIO 先独立解码/校验，再同步参考状态，单独计数，不能称作两个独立设备模型的证明。
- D6 时序/功耗来自锁定库下的综合后估计：ZeroWireload、默认活动、未完整约束外部 I/O。D8 新 CPU 没有物理签核；E8 旧 CPU 的 50 MHz/DRC/LVS 结论不能移用于 D8。
- DFF 的图、28 管计数和两锁存器相位解释已完成。额外的理想 MOS 瞬态模型出现 X/TIMEOUT，**未通过**；保留失败，不以相位模型冒充晶体管瞬态、SPICE 或 LVS。
- 4 位 ALU 的 2048 组输入通过组合 SAT 等价；CPU 验收仍是有限测试，不是完整 ISA 全输入证明。原生音频验证的是真实 SDL PCM 回调，未测试物理扬声器。
- 早期零地址 RAM 测试按新内存布局记录适配；8 个 RV32M 汇编程序保留在 D3，D8 不支持这些指令，并用 MUL 编码实测拒绝。Dhrystone/CoreMark 使用课程允许的两次迭代；train 的 100 MHz 是模型频率。
- 个人身份、正式申请/考试/答辩不在独立工程交付范围。没有恢复 computer-use 操作 Logisim，没有改全局 PATH 或系统内存设置。

## 核验与文件位置

PowerShell 只读检查：

```powershell
& C:\YSYX_WORKSPACE\projects\ysyx_f_to_b\scripts\Verify-D.ps1 -External
& C:\YSYX_WORKSPACE\projects\ysyx_f_to_b\scripts\Verify-D.ps1 -Archive C:\YSYX_WORKSPACE\projects\ysyx_f_to_b\YSYX_D_DELIVERY.zip
```

该命令核对来源、逐项状态、负对照、日志、冻结源码、ZIP 与哈希，不重新运行长仿真。实际命令、输入输出快照、退出码、用时与资源观测在 `artifacts/D*`。最终 Linux 源码/产物包见 [离线说明](../D/offline/README.md)，逐成员验证见 [导出清单（补充包：reports/D_runtime_export.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)。完整工具与 PDK 继续复用锁定的本机路径。

最终 [工具指纹](D_toolchain_final.json)、[图像审查记录](D_visual_review.json)和[F/E 历史保留核验（补充包：reports/D_history_preservation.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)与主审计一同交付。D 的所有源码/实验在独立工作台 `/home/USER/d-stage`，F/E 原工作台、源码快照和旧 ZIP 保持独立。
