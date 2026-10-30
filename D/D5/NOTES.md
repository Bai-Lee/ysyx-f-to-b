# D5：AM、运行时和独立 klib

范围来自 [D5 原文](sources/D5.md) 与 [PA2.3](../runtime/sources/pa/212fcff6a122de75.md)。同一 C 程序能够跨平台运行，依赖编译器的 ISA/ABI 选择，以及 AM 对启动、输出、计时、堆和退出的约定；并不意味着各平台二进制可以互换。

## 从 ELF 到 GOOD TRAP

Makefile 根据 ARCH 选择头文件、汇编启动代码、平台实现和编译参数；各源文件编成目标文件，再把 AM、klib 和程序链接起来。链接脚本安排入口、代码、只读数据、数据、BSS 和堆栈。objcopy 提取装载镜像，NEMU 将它装到复位地址。启动代码建立栈后进入运行时，再调用 main。main 的返回值传给 halt，最终由 a0 和 EBREAK 通知宿主。

`native` 由 GNU/Linux 启动和 glibc 承担一部分工作；`riscv32-nemu` 是 freestanding，不依赖宿主 RV32 Linux libc。本机交叉编译器缺少 `gnu/stubs-ilp32.h`，本工程只为无宿主环境提供了任务局部的空桩头，并实测 `__STDC_HOSTED__==0`、指针与 uint32_t 均为 4 字节。不把这一处理说成安装了可用的 RV32 Linux libc。

## klib 的边界和算法

`string.c` 实现了长度、复制、拼接、比较和内存操作。比较时按 unsigned char 解释字节；strncpy 在源串结束后补零；memcpy 的输入不得重叠；memmove 根据相对地址决定从前往后还是从后往前复制。返回值、末尾 NUL 以及目标区间两侧的哨兵字节都要检查，不能只看最终字符串“像不像”。

`stdio.c` 通过一个输出目标抽象复用格式解析：输出到 putch 或有限缓冲区。支持整数、字符、字符串、指针、百分号，以及 flags、宽度、精度和 hh/h/l/ll/z/t/j。snprintf 返回本应输出的长度，同时在容量允许时结束为 NUL；容量为 0 时不写目标。负数转为无符号幅值后输出，避免对最小有符号数取负导致 UB。没有声称支持浮点格式或 `%n`；超出一百万的宽度/精度按资源约束拒绝。

裸机分配器按 16 字节对齐，在空闲块链表中采用 first-fit，另外维护物理相邻块关系；分裂更新两套链表，释放时只与左右邻块合并。calloc 检查乘法溢出并清零；realloc 失败时保留原块，成功时保持旧内容，也支持合并右侧空闲块原位增长。原生平台启动过程也会调用分配器，因此 native-klib 明确通过锁定 glibc 的 `__libc_*` 接口桥接宿主分配；裸机分配器另在受控内存区单独验证。这不是一种可移植到任意 libc 的承诺。

初版按物理链表扫描分配/合并，在 D8 的 train 图划分测试中出现严重性能问题。只读 GDB 快照确认 11518 个块、242 个空闲块，物理链表仍完整，采样热点在 malloc/free。当前改为仅扫描空闲块和局部合并，未删断言或改应用校验；新增 512 块碎片与原位增长场景，保留原 10000 次随机操作。故意使 calloc 返回非零内容的 mutant 被同一断言拒绝。旧版本、停止原因和失败尝试保留在 `D8/upstream/alloc-before-freelist.c` 与 `artifacts/D8/allocator_diagnosis`。

stdarg 的宏由编译器结合 ABI 实现，负责参数保存区、栈位置、类型大小和对齐。取可变参数还要考虑默认提升，例如 char/short 以 int 传递、float 以 double 传递；不能把 va_list 普遍当成“每次加 4 的指针”。本工程使用编译器提供的 va_start/va_arg/va_copy，分别在 native、RV32IM 和 RV32E 下编译和测试。

## 把软件与模拟器错误分开

同一份 `portable_tests.c` 先在 native/glibc 执行，再在 native/自写 klib 执行，最后在 RV32IM NEMU 上执行并逐指令与 Spike 比较。三个平台各做 5007 项检查。另有 [21199 次主机比较](../../reports/D5_host_klib.json)与 [10000 次分配器操作](../../reports/D5_allocator.json)，均启用 ASAN/UBSAN。故意漏写字符串终止符的 mutant 被相同断言拒绝。

D8 应用还需要读取由 AM `gen-ramdisk.py` 嵌入的输入文件，新增 `fileio.c` 提供受限的内存文件 API：读、写、定位、EOF/error、整数格式扫描和控制台格式输出。它使用生成器相同的 `struct file` 布局，写入时采用副本，保持镜像内原始数据不变；不模拟宿主文件系统或 glibc FILE 内部结构。64 个文件、29 个普通打开流、单文件 64 MiB 等上限明确检查；浮点扫描及其他未实现格式报错。与 glibc 的主机对照及错误 EOF mutant 见 `D8_fileio.json`，随后 21 个 archbench 程序实际验证。这个补充没有改变原始输入或预期 checksum。

[三平台结果](../../reports/D5_portable.json)中，NEMU 运行 6253853 条指令，6253821 条参与比较，32 条显式跳过：31 次 UART 输出及最终 EBREAK。跳过设备访问意味着该条的结果以 DUT 为准，不能把它算作独立参考验证。

native-klib 使用宏改变头文件声明及库构建条件，再把自写符号放进实际链接产物。为了避免构建缓存混用，单独使用 `native-klib` 架构名和产物路径。早期将 native 的 exit 再转到 halt，形成递归退出环；已经修复为 native 仍用宿主 exit，裸机走 AM halt。该次超时前主动终止的记录保留，未记成通过。

退出码还分层传播：测试程序非零 → 子 make 失败 → 测试聚合 Makefile 非零。已修复上游聚合器中吞掉失败的管道，并用原始 wrong 程序验证。因此一行 PASS 必须有对应运行报告，不能只搜索终端的颜色。

复验见 `verify_host.py`、`verify_allocator.py`、`run_portable.py` 和 `artifacts/D5`。保留原始 AM 与测试来源快照；后续 D8 继续复用这里的 klib 源码，而不回用 E 阶段预编译的 miniRV klib。
