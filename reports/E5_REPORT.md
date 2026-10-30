# E5阶段验收

17项核心任务通过；对齐背景题已阅读并说明选择。8组有效程序及4组预期拒绝输入均实跑；随机程序6417次提交经C/RTL/Python三方逐步检查，6种错误实现均被检出。

[实现与手册答复](../E/E5/NOTES.md) · [运行结果](E5_execution.json) · [注错结果](E5_mutations.json) · [机器审计](E5_AUDIT.json)

| ID | 状态 | 验收依据 |
|---|---|---|
| E5-M001 | PASS_DOCUMENTED | 按原文7个编号问题回答并核对官方手册图表；指令编码、PC/GPR/x0、字节寻址、EEI/对齐、立即数与旧rs1语义明确。 |
| E5-M002 | PASS_DOCUMENTED | 按原文7个编号问题回答并核对官方手册图表；指令编码、PC/GPR/x0、字节寻址、EEI/对齐、立即数与旧rs1语义明确。 |
| E5-M003 | PASS_DOCUMENTED | 按原文7个编号问题回答并核对官方手册图表；指令编码、PC/GPR/x0、字节寻址、EEI/对齐、立即数与旧rs1语义明确。 |
| E5-M004 | PASS_DOCUMENTED | 按原文7个编号问题回答并核对官方手册图表；指令编码、PC/GPR/x0、字节寻址、EEI/对齐、立即数与旧rs1语义明确。 |
| E5-M005 | PASS | Actual C11 and Linux Verilator execution with independent Python traces. Exact8 core instructions,16GPR/x0, signed immediates, jalr alias/odd target, little-endian/partial writes, reserved/unaligned rejection and once-only ebreak callback including post-halt probes. |
| E5-M006 | PASS | Actual C11 and Linux Verilator execution with independent Python traces. Exact8 core instructions,16GPR/x0, signed immediates, jalr alias/odd target, little-endian/partial writes, reserved/unaligned rejection and once-only ebreak callback including post-halt probes. |
| E5-M007 | PASS | Actual C11 and Linux Verilator execution with independent Python traces. Exact8 core instructions,16GPR/x0, signed immediates, jalr alias/odd target, little-endian/partial writes, reserved/unaligned rejection and once-only ebreak callback including post-halt probes. |
| E5-M008 | PASS_DOCUMENTED | 按原文7个编号问题回答并核对官方手册图表；指令编码、PC/GPR/x0、字节寻址、EEI/对齐、立即数与旧rs1语义明确。 |
| E5-M009 | PASS | Actual C11 and Linux Verilator execution with independent Python traces. Exact8 core instructions,16GPR/x0, signed immediates, jalr alias/odd target, little-endian/partial writes, reserved/unaligned rejection and once-only ebreak callback including post-halt probes. |
| E5-M010 | PASS | Actual C11 and Linux Verilator execution with independent Python traces. Exact8 core instructions,16GPR/x0, signed immediates, jalr alias/odd target, little-endian/partial writes, reserved/unaligned rejection and once-only ebreak callback including post-halt probes. |
| E5-M011 | PASS | Actual C11 and Linux Verilator execution with independent Python traces. Exact8 core instructions,16GPR/x0, signed immediates, jalr alias/odd target, little-endian/partial writes, reserved/unaligned rejection and once-only ebreak callback including post-halt probes. |
| E5-M012 | PASS | Actual C11 and Linux Verilator execution with independent Python traces. Exact8 core instructions,16GPR/x0, signed immediates, jalr alias/odd target, little-endian/partial writes, reserved/unaligned rejection and once-only ebreak callback including post-halt probes. |
| E5-M013 | PASS | Actual C11 and Linux Verilator execution with independent Python traces. Exact8 core instructions,16GPR/x0, signed immediates, jalr alias/odd target, little-endian/partial writes, reserved/unaligned rejection and once-only ebreak callback including post-halt probes. |
| E5-M014 | PASS | Actual C11 and Linux Verilator execution with independent Python traces. Exact8 core instructions,16GPR/x0, signed immediates, jalr alias/odd target, little-endian/partial writes, reserved/unaligned rejection and once-only ebreak callback including post-halt probes. |
| E5-M015 | PASS | Executed installed Verilator manual DPI add import/example, signed parameters and returns; compiled faulty C implementation rejected. |
| E5-M016 | PASS | Actual C11 and Linux Verilator execution with independent Python traces. Exact8 core instructions,16GPR/x0, signed immediates, jalr alias/odd target, little-endian/partial writes, reserved/unaligned rejection and once-only ebreak callback including post-halt probes. |
| E5-M017 | PASS | Actual C11 and Linux Verilator execution with independent Python traces. Exact8 core instructions,16GPR/x0, signed immediates, jalr alias/odd target, little-endian/partial writes, reserved/unaligned rejection and once-only ebreak callback including post-halt probes. |
| E5-O001 | PASS_DOCUMENTED | 按原文7个编号问题回答并核对官方手册图表；指令编码、PC/GPR/x0、字节寻址、EEI/对齐、立即数与旧rs1语义明确。 |
