# C1：ELF 文件与链接

本章原文明确“暂无编程内容”，因此对应 **C1-O001 背景记录，核心编程任务数为 0**。这里阅读了固定版本的 [C1 原文](sources/C1.md)及 v23.06 ELF/链接课件（原完整交付引用：`/workspace/YSYX_F_B_Archive/slides/markdown/2306/580e82b43f0b9820.md`），并增加一个小型作者实验帮助理解。没有声称看完全部视频，也没有把这组示例改称课程新增必做题。

## 看到链接错误时，先判断文件里还缺什么

一个 `.o` 已经包含机器指令，但它通常还不知道外部函数和变量的最终地址。编译器可以把“调用 add_to_counter”翻译成调用指令的形状，留下需要链接器处理的位置；这个位置及处理方式记录在重定位表中。链接器随后完成两类工作：把引用与定义关联，再安排最终地址并修补对应引用。

这解释了两种不同错误：`undefined reference` 是引用还找不到定义；`multiple definition` 是本例中同一个全局名称有多个不允许并存的定义。随便换一个编译选项可能使某次错误消失，却不一定解决接口设计问题。先检查名称、可见性、文件是否实际参与链接，再检查库的顺序和链接脚本。

| 要回答的问题 | 观察位置/命令 | 不能据此直接推断的内容 |
| --- | --- | --- |
| 文件面向哪种机器、是目标文件还是可执行映像？ | `readelf -h` | ELF 文件一定能在当前宿主运行 |
| 代码、数据、零初始化对象放在哪里？ | `readelf -SW` | 所有内存数据都逐字节存放在文件中 |
| 哪个名字已定义，哪个仍为 UND？ | `readelf -sW`、`nm` | 普通符号表能够完整检查 C 类型一致性 |
| 哪些地址需要重填？ | `readelf -rW`、`objdump -dr` | 可以把所有重定位当成同一种整数写入 |
| 操作系统将装载哪些区域？ | `readelf -lW` | 节表与程序头表可以混用 |
| 是否还需要动态库？ | `readelf -dW`、INTERP 程序头 | 链入一个 `.a` 就使整个程序成为完全静态程序 |

ELF 的节主要服务于链接、组织和调试；程序头中的段描述装载需要的范围与属性。`.bss` 常为 `NOBITS`：它需要运行时空间，但不需要在文件中存放等长的零字节。本机加载器能按装载信息建立零初始化空间，裸机启动代码则必须自行履行相应约定。C5 将程序从 Flash 搬到 RAM 时，这个区别会直接影响 `.data` 搬运和 `.bss` 清零。

## 一个实际执行的小实验

[src](src) 中，`main.c` 引用另一文件定义的函数、`counter`、`zero_counter` 和字符串；`producer.c` 定义它们，并有只在本文件使用的 `static bias`。`unused.c` 仅提供一个不会调用的函数。

构建流程是：分别生成 `.o`，把 `producer.o` 与 `unused.o` 放进 `liblesson.a`，再按 `main.o liblesson.a` 的顺序链接。实际 GCC 为本地 11.4.0；版本、文件哈希和原始命令见 [C1_experiment.json](../../reports/C1_experiment.json)及 命令证据（原完整交付引用：`../../artifacts/C1/elf`）。

实测结果如下：

1. `main.o` 为 `ET_REL`，`add_to_counter` 仍是 UND，并有 `R_X86_64_PLT32` 等重定位。这里是宿主 x86-64 实验。
2. 正确链接后运行得到 `ELF_LINK_PASS counter=15 zero=0`。`counter` 是 GLOBAL 符号，`bias` 是 LOCAL 符号。
3. `unused_archive_member` 不在最终符号表中，说明这个未被需要的归档成员没有被取出。实验没有依靠 `--gc-sections` 隐藏它；归档成员选择和链接后的节垃圾回收是不同步骤。
4. 把库放到 `main.o` 前面，真实链接失败，诊断含 `undefined reference` 与 `add_to_counter`。在本次 GNU 链接流程扫描库时，还没有后面的未解析引用，因此没有取出需要的成员。循环库依赖可研究链接器的分组重扫描选项，但不要无差别地给所有库加分组。
5. 再链接一个定义 `counter=100` 的文件，真实报告 `multiple definition`。同一套源码的正确链接与这两个负例都保留。
6. 最终 ELF 是 `ET_EXEC`，同时有 INTERP 和对 `libc.so.6` 的 NEEDED 项：本例的业务库以静态归档方式链接，宿主 libc 仍是动态依赖。

还将不依赖宿主头文件的 `producer.c` 单独编译成 RV32E/ILP32E 对象，检查了 RVE 标志、ISA attributes、`R_RISCV_HI20` 与 `R_RISCV_LO12_*`。结果在 [rv32e-relocations.txt](results/rv32e-relocations.txt)。这个对象只做编译和检查，没有在此处运行 NPC；宿主程序的执行不能充当 RV32E 执行证据。

## 地址是怎样落定的

链接脚本决定各输出节放在哪里、对齐到哪里，以及 `_start`、堆栈边界等符号的值。把输入对象中的 `.text*` 合并后，符号相对整个映像的位置会改变；链接器根据每种重定位类型计算编码所需的值。以 PC 相对调用为例，目标地址、调用位置和位移必须一致，再按 ISA 指令字段编码。

RISC-V 的 `lui`/`addi`、`auipc`/`jalr` 涉及高低部分及符号扩展，不能简单地“把一个 32 位地址塞进指令”。链接器松弛还可能把较长的调用序列缩为 `jal`，从而继续改变后续地址。课件中的寻址范围表是概括；具体限制取决于 XLEN、对齐、重定位类型和 code model。本实验没有逐一验证所有 code model 或松弛变体。

在 C5 中还会区分 **VMA（运行时地址）** 与 **LMA（镜像存放地址）**。例如变量运行时在 SRAM，但它的初值字节先存在 Flash。链接器让代码引用 SRAM 地址，启动加载器则根据链接符号把初值从 Flash 搬过去。只把二进制复制到另一个位置，不保证所有绝对引用自动改变。

## 阅读课件时需要保留的限定

课件将字符串表作为一种设计思路介绍；实际 ELF 通常把**节名称**放在 `.shstrtab`，由 ELF 头的 `e_shstrndx` 指出这张表；普通符号名称通常在 `.strtab`，动态符号另有 `.dynstr`。这些名字是常见约定，真正关联依靠表的索引字段。本例头部索引为 36，对应实际 `.shstrtab`，见 [linked-elf.txt](results/linked-elf.txt)。

普通非 LTO 链接流程并不等同于完整的 C 类型检查：两个文件若把同一外部对象分别声明成不同类型，名称可能关联成功，却不代表程序满足语言规则。共享头文件能让编译器检查一致的声明；C/C++ 接口还要留意名称修饰。`extern "C"` 主要规定语言链接，不能自动修复错误的参数布局、位宽或调用约定。

课件关于 `-fno-common` 报错“违反 C 标准”的表述不能直接沿用。N1570 的 §6.9 第 5 段约束整个程序中的外部定义数量；§6.9.2 第 2 段描述一个翻译单元内的试探性定义。两个翻译单元各写一个 `int a;`，并不能据此推出标准要求链接器把它们合并。GNU `-fcommon` 的 COMMON 合并属于工具行为，跨文件共享对象更稳妥的写法是在头文件声明 `extern`，只在一个源文件中给出定义。

本次只读核对了 N1570 原 PDF（原完整交付引用：`/workspace/YSYX_F_B_Archive/assets/offline/www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf`）物理页 173、176，并查看第 173 页完整渲染；对应印刷页为 155、158。[提取文本](results/n1570-excerpts.txt)保留上下文。这里没有重新实验 `-fcommon` 的所有兼容变体，也不把课件中不同类型声明的运行结果当成可移植保证。

## 实际入口与验证范围

在 PowerShell 中运行：

```powershell
wsl.exe -d YSYX-Linux -u ysyx -- python3 /workspace/projects/ysyx_f_to_b/C/C1/run_experiment.py
```

构建和输出只位于本章目录，记录由 `C/runtime/common.py` 写入 `artifacts/C1`。命令、输入、输出及日志哈希完全相同时脚本会复用原证据；复用不表示再次执行。初次标准文本定位因 PDF 换行而失败，诊断及当时脚本保留在 `artifacts/C1/standard/parser_initial_failure.json`；修复的是定位方法，没有改 PDF 或语言约束。

本章结果是“固定课件阅读与有界演示完成”，不是课程学习掌握证明、所有 ELF 实现认证或 C1 新增核心题验收。
