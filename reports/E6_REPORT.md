# E6 阶段验收

22 项核心任务和 2 个背景节点已完成本地验收。38 个 riscv-tests、35 个 cpu-tests、21 个 archbench 小规模程序均通过；wrong 和注错 RTL 被正确拒绝。4 组 train 各 20 个程序实际运行，全部保留逐指令差分检查。

[实现说明](../E/E6/NOTES.md) · [机器审计](E6_AUDIT.json) · [官方测试](E6_official_tests.json) · [应用与 benchmark](E6_benchmarks.json) · [性能原始结果](E6_performance.json)

| train 程序 | 主机计时分数 | 100 MHz | 1000 MHz | 综合估计 830 MHz |
|---|---:|---:|---:|---:|
| 100.blockchain | 12 | 265 | 2651 | 2200 |
| 101.igemm | 1 | 7 | 71 | 59 |
| 102.queen | 30 | 622 | 6225 | 5167 |
| 103.dinic | 42 | 810 | 8108 | 6730 |
| 104.malloc | 39 | 771 | 7716 | 6404 |
| 105.bf | 26 | 521 | 5210 | 4324 |
| 106.qsort | 57 | 1143 | 11439 | 9494 |
| 107.stream | 17 | 348 | 3482 | 2890 |
| 108.ntt | 1 | 5 | 57 | 47 |
| 200.genann | 1 | 8 | 84 | 70 |
| 201.jpeg | 8 | 161 | 1616 | 1341 |
| 202.llama2 | 1 | 5 | 51 | 42 |
| 203.rsa | 4 | 92 | 920 | 763 |
| 204.hypergraph | 49 | 998 | 9986 | 8288 |
| 300.bzip3 | 25 | 512 | 5123 | 4252 |
| 301.gsim | 13 | 284 | 2840 | 2357 |
| 302.lua | 28 | 574 | 5741 | 4765 |
| 303.cproc | 48 | 933 | 9332 | 7745 |
| 304.mp3 | 1 | 4 | 43 | 36 |
| 305.h264 | 12 | 254 | 2543 | 2111 |
| 几何平均 | 10.100 | 150.369 | 1526.183 | 1266.614 |

主机计时列反映仿真执行速度。其余三列反映指定频率下的模型时间；830 MHz 是 ICsprout55 R/L、TT、1.2 V、25°C 条件下布局前综合时序估计，不是已布线或实物频率。计时区内的 genann 子测试输出及 LLaMa tokens/s 输出会随频率变化，故指令数并非完全相同；实测时间比例的最大相对偏差为 0.01349%，整数分数舍入另外校验。

| ID | 状态 | 验收依据 |
|---|---|---|
| E6-M001 | PASS | FCEUX native ran original legal homebrew ROM; real SDL framebuffer changed with J and recovered, audio 440/220/440Hz checked from callback PCM; physical speaker is outside automated scope. |
| E6-M002 | PASS | Real cross compilation and NPC image load at0x80000000; originalAM code reaches and remains in the halt symbol range,128MiB model and bounded observation explicit. |
| E6-M003 | PASS | AM embeds a0 result plus ebreak. make uses its just-built binary path; dummyGOOD/exit0, wrongBAD/make-nonzero; error aggregation is verified rather than trusting text alone. |
| E6-M004 | PASS | AM embeds a0 result plus ebreak. make uses its just-built binary path; dummyGOOD/exit0, wrongBAD/make-nonzero; error aggregation is verified rather than trusting text alone. |
| E6-M005 | PASS | AM embeds a0 result plus ebreak. make uses its just-built binary path; dummyGOOD/exit0, wrongBAD/make-nonzero; error aggregation is verified rather than trusting text alone. |
| E6-M006 | PASS | AM embeds a0 result plus ebreak. make uses its just-built binary path; dummyGOOD/exit0, wrongBAD/make-nonzero; error aggregation is verified rather than trusting text alone. |
| E6-M007 | PASS | 38 official tests compiled and executed with every committed instruction checked against independent C reference; exact test list and source defaults retained. |
| E6-M008 | PASS | Actual RTL sign-extension mutant produces first-mismatch PC/instruction/register diagnostic, simulator nonzero and top-level make FAIL; valid control restored and passes. |
| E6-M009 | PASS | 35 official tests compiled and executed with every committed instruction checked against independent C reference; exact test list and source defaults retained. |
| E6-M010 | PASS | Native and RTL hello output checked; random 1/8 readiness and mandatory polling; every load synchronized with independent reference. 100000-sample device and rollover tests passed. |
| E6-M011 | PASS | Dhrystone/CoreMark use course-permitted 2 iterations, microbench uses test; native and RTL runs independently validate; measured host time is not silicon performance. |
| E6-M012 | PASS | Official tiny test model compiled and ran on minirv NPC, emitted Once and passed upstream validation, full differential checking enabled. |
| E6-M013 | PASS | Every pinned archbench directory ran test on native and minirv NPC, including upstream checksum validation and independent per-commit differential comparison. |
| E6-M014 | PASS | Native and RTL hello output checked; random 1/8 readiness and mandatory polling; every load synchronized with independent reference. 100000-sample device and rollover tests passed. |
| E6-M015 | PASS | Official AM t program produced 1/2/3-second lines with host monotonic timer; RTL/C per-commit comparison retained. Timer rollover independently tested. |
| E6-M016 | PASS | Dhrystone/CoreMark use course-permitted 2 iterations, microbench uses test; native and RTL runs independently validate; measured host time is not silicon performance. |
| E6-M017 | PASS | Actual minirv NPC executed upstream FCEUX and two complete ASCII frames, with per-instruction differential checking; bounded semantic stop. |
| E6-M018 | PASS | All 20 official train workloads ran serially with full per-commit differential checks. Per-program process exits, upstream validators, input/output snapshots and arithmetic/geometric means audited. Original upstream script attempt retained separately as interrupted. |
| E6-M019 | PASS | All 20 official train workloads ran serially with full per-commit differential checks. Per-program process exits, upstream validators, input/output snapshots and arithmetic/geometric means audited. Original upstream script attempt retained separately as interrupted. |
| E6-M020 | PASS | All 20 official train workloads ran serially with full per-commit differential checks. Per-program process exits, upstream validators, input/output snapshots and arithmetic/geometric means audited. Original upstream script attempt retained separately as interrupted. |
| E6-M021 | PASS | Real ECC synthesis and TT static timing, with compatible Yosys. Independent LEF pin-name checks pass; timing assumptions and no-layout scope explicit. |
| E6-M022 | PASS | All 20 official train workloads ran serially with full per-commit differential checks. Per-program process exits, upstream validators, input/output snapshots and arithmetic/geometric means audited. Original upstream script attempt retained separately as interrupted. |
| E6-O001 | PASS_DOCUMENTED | Explained why test inputs are not representative performance loads; retained official tool-version compatibility failures and validated working locked versions. |
| E6-O002 | PASS_DOCUMENTED | Explained why test inputs are not representative performance loads; retained official tool-version compatibility failures and validated working locked versions. |

FCEUX 使用自制可再分发 ROM，实际完成画面、按键、PCM 音频及 NPC 字符模式验证。完整 E 阶段交付 ZIP 将在 E7、E8 和 E9 范围审计完成后生成。
