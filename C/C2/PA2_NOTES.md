# PA2.5：NEMU I/O 实现与六组必答题

原题冻结在 [PA2.5](../runtime/sources/pa/c513b8fe1d21123b.md)，其中 17 条必做和 31 条扩展/说明的范围见 [嵌套清单](../runtime/nested_scope_review.json)。本节解释当前 C 副本的真实行为；D 的既有源码和快照保持原状。运行证据见 [功能程序](../../reports/C2_nemu_functional.json)、[设备驱动](../../reports/C2_nemu_host_drivers.json)、[窗口与应用](../../reports/C2_nemu_gui.json)、[性能](../../reports/C2_nemu_benchmarks.json)和[编译链接实验](../../reports/C2_pa2_compiler.json)。

## 1. 串口、printf 与设备地址

本机采用 RISC-V MMIO。guest 的 store/load 先由指令实现计算有效地址，经过虚拟地址到物理地址的当前直通映射，再由物理内存层区分 RAM 和 MMIO。MMIO 在已注册的设备区间中查找 IOMap，检查整个访问跨度，然后调用设备回调。没有实现无关的 x86 in/out 指令。

NEMU 串口在 `0xa00003f8`。AM 的 putch 写这个寄存器，宿主 serial 模型再输出一个字节。hello 是在 AM/TRM 上运行的裸机程序，与通常通过操作系统系统调用输出的宿主 hello 层次不同。当前真实 hello 及 ALU 程序都使用独立 Spike 比较普通指令，报告列出显式跳过的设备访问。原始 wrong 程序仍触发 BAD_TRAP 和非零退出。

printf/sprintf/snprintf 复用同一个格式解析和输出核心，只更换“输出到 putch”或“输出到缓冲区”的目标。已经实现的整数、字符、字符串、指针、宽度/精度等契约见 [D5 的实现解释](../../D/D5/NOTES.md)；C 使用同一已验证实现，并把 5007 项便携测试重新编译到当前 NEMU 执行。浮点格式、`%n` 等未实现范围不算 ISO C 全部 stdio 支持。ALU 测试成功时没有 PASS 文本，而是返回累计的 exit_code=0；因此验收依据真实 GOOD_TRAP，而非寻找不存在的提示字符串。

## 2. RTC 的顺序为何重要

NEMU 的两个 RTC 寄存器分别在 `0xa0000048`、`0xa000004c`。当前原始设备回调在读取**高字**时同时更新两个 32 位字，因此 C 的 AM 驱动先读高、再读低，然后拼成 uint64，并减去 IOE 初始化时的基准值。

如果先读旧低字，再读高字触发新快照，在低位回绕附近便可能把不同时间的两半拼在一起。C 的宿主测试既对 AM 驱动构造 300 次回绕边界，也直接编译真实 NEMU RTC 回调；低字先读的错误版本确实被拒绝。这里的正确顺序属于这个设备协议，不能推广成所有 64 位设备都应高字先读；D 的 NPC 模型采用低字读取锁存高字，是另一个明确的协议。

真实 `t` 测试已观察到 1、2、3 秒输出。日历 RTC 尚未实现，返回原约定的 1900 占位日期；不以此宣称拥有实时时钟日期功能。性能构建使用原 NEMU 的 `CLOCK_MONOTONIC_COARSE`，有粗粒度量化，短程序的计分不宜过度解读。

## 3. 键盘、显存与同步

键盘寄存器 `0xa0000060` 的低位是 AM 键码，bit15 表示按下；没有事件返回 AM_KEY_NONE。SDL 事件先进入 NEMU 的键盘队列，guest 读取时弹出一次，AM 再拆出 keycode/keydown。实际窗口收到 J=49 和 LEFT=75 的按下、释放；宿主测试覆盖无事件。多键状态应在应用中维护集合，按下加入、释放移除，不能用“最后一个事件”替代全部当前状态。

显示控制寄存器低地址给出 `(width<<16)|height`，显存从 `0xa1000000` 开始。像素 `(x,y)` 的字节地址是 `FB_ADDR+4*(y*screen_width+x)`。FBDRAW 的源数据按传入矩形宽度逐行排列，目的行距则是屏幕宽度；裁剪目的矩形时必须保留原来的源行距。驱动检查负尺寸、空指针，允许零尺寸的单纯同步请求。

初始化教学小例通过单独的链接包装，在 GPU 初始化时执行 `fb[i]=i`，随后同步。它没有修改最终通用驱动；实际捕获的全部 480000 个放大后像素，与 400×300 原图的二倍最近邻展开完全相同。随后使用完整 FBDRAW 驱动运行官方 video 动画。160 组独立矩形预期、边界哨兵、错误行距 mutant 与实际 SDL 画面共同检查了这条路径。

同步是协议，不是画一个 SVG：guest 写 `VGACTL+4=1` 后，NEMU 的 `device_update` 到达更新时机，才把 framebuffer 上传给 SDL，之后把同步寄存器清零。若不请求同步，显存可以已经改变而窗口仍显示旧帧；若每写一个像素就强制刷新，则会出现大量不必要的刷新和中间画面。

集成时发现 AM 的真实 `klib-macros.h` 不声明 assert，而最初的宿主测试桩错误地替它声明了。已在驱动中显式包含 `klib.h`，修正测试桩并重跑宿主、交叉编译与 GUI 检查。该失败记录保留，说明主机桩测试不能代替目标平台集成。

## 4. dtrace 与性能配置

dtrace 以 `map->name` 输出设备名、PC、方向、地址、长度和数据，环境变量 `C_DTRACE_FILE` 指定文件，`C_DTRACE_FILTER` 按完整设备名筛选，`C_DTRACE_LIMIT` 限制条数。实际串口用例只保留 8 条 serial 写记录和一行上限提示；反向筛选保留 RTC 时，纯串口程序的 trace 为空；非法负上限被明确拒绝。完整访问跨度也被检查，不能只确认起始字节在映射内：实际从 `0xa10752fe` 执行 4 字节 load，起始字节在显存映射内但末尾越界，NEMU 在宿主访问前拒绝，见 [MMIO 负对照](../../reports/C2_nemu_mmio_boundary.json)。

功能版和性能版是两个不同的 ELF/输出目录。性能版真实关闭 TRACE、WATCHPOINT、DIFFTEST 和 CC_DEBUG，并通过符号表确认继承的 trace hooks 未进入执行产物。关闭调试仅用于明确标注的性能测试，功能验收仍保留正常调试能力。

| 程序 | 输入 | 动态指令 | 本次宿主运行秒 | 原程序报告 |
| --- | --- | ---: | ---: | --- |
| Dhrystone | 原始 500000 次 | 217015843 | 4.322 | 216 Marks |
| CoreMark | 原始 1000 次 | 305955038 | 5.619 | 542 Marks |
| MicroBench | test | 363730 | 0.236 | PASS |
| MicroBench | ref | 1867103714 | 33.336 | 664 Marks |

三个 benchmark 的原始输入/校验逻辑均保留；D 的最小演示迭代数在 C 的性能专用副本中恢复为官方原值。MicroBench ref 没有因堆不足跳过项目。表中是这台笔记本、WSL、当前模拟器和计时源的结果，不是芯片 PPA，也不是官方 CoreMark 认证成绩；CoreMark 这一轮报告用时约 5.39 秒，未达到标准认证常用的 10 秒时长。

## 5. 程序演示的实际边界

已实际运行 slider、typing-game、demo 中的兰顿蚂蚁、Bad Apple、snake、LiteNES、FCEUX。slider 有相隔五秒的不同图片；打字/贪吃蛇有真实输入与画面变化；Bad Apple 从原 MP4 转换为原程序要求的 80×25 帧并观察多帧字符输出；无效媒体输入被 FFmpeg 拒绝。便携 FFmpeg 来自 Ubuntu 官方包并核对了发布摘要，没有系统安装。

LiteNES 和 FCEUX 采用项目 CC0 ROM，经独立构建清单选择；原来的商业 ROM 源文件保留但不链接进该测试。实际控制器事件使画面蓝→红→蓝。LiteNES 在本轮功能构建中很慢，因此等待实际颜色状态，固定睡眠结束不算通过。所有无限循环演示在取得规定观察后，以普通 SDL 关闭事件退出，记录为 QUIT/有界观察，不伪装成程序自然完成或无限期稳定。

这些 GUI 会话为控制成本关闭了独立 ISA DiffTest；它们验证的是设备及应用集成。普通指令的当前正确性由另行启用 Spike 的 hello、alu-tests、klib、负程序检查支撑。NEMU 声卡仍为原文选做，未实现；原生 FCEUX 的真实音频回调验收在 [C2 说明](NOTES.md)，两者不得混淆。内存嵌套 NEMU、暴力优化 LiteNES、额外小游戏及全部外链阅读未冒充已完成。

## 6. 必答题 Q01：YEMU 状态机

采用原文真实字节序列：`e6 04 e5 11 f7 10 21 00`。其中 M[5]=16、M[6]=33、M[7]=0。状态至少包含 PC、寄存器组、内存和 halt；不能只跟踪最后的和。[原始代码加观察语句的运行](../../reports/C2_pa2_yemu.json)如下：

| 执行后 PC | 刚执行的含义 | R0 | R1 | M[7] | halt |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | load 6 | 33 | 0 | 0 | 0 |
| 2 | mov r1,r0 | 33 | 33 | 0 | 0 |
| 3 | load 5 | 16 | 33 | 0 | 0 |
| 4 | add r0,r1 | 49 | 33 | 0 | 0 |
| 5 | store 7 | 49 | 33 | 49 | 0 |
| 6 | 把数据 0x10 当作 add r0,r0 | 98 | 33 | 49 | 0 |
| 7 | 数据 0x21 的操作码 2 非法 | 98 | 33 | 49 | 1 |

关键细节是原程序没有在 store 后直接停止；它继续取到数据区，最终因非法操作码停机，所以输出 M[7] 仍为 49，但最后 R0 已是 98。取指 `M[pc]` 后，用操作码选择分支，再按格式解析寄存器/地址，修改状态，最后 pc++。原教学代码使用 C bit-field，位域布局不是跨编译器统一的 ISA 规范；本次实际 GCC 验证了此样例的布局。

## 7. 必答题 Q02：一条 NEMU 指令如何执行

以 `lw a0,4(sp)` 为例：SDB 的 c/si 调用 cpu_exec，循环中的 exec_once 设置当前 PC、顺序 PC；isa_exec_once 经 inst_fetch/vaddr_ifetch/paddr_read 取得 32 位编码并推进顺序地址。译码提取 rs1、rd、funct3 和符号扩展立即数，计算地址 sp+4，再由 vaddr_read/paddr_read 判断 RAM 或 MMIO，取得字并写 a0。设置下一 PC 后更新架构 PC，进行 trace、DiffTest、监视点检查和设备推进。

这几个 PC 概念不能混淆：当前 PC 标识正在执行的指令，顺序 PC 是 pc+4，动态下一 PC 可以被分支或跳转改写。x0 在写回后保持零。执行 EBREAK 时将 a0 传给结束状态，不等于实现了完整特权异常。相关文件在 C 工作台的 `src/cpu/cpu-exec.c`、`src/isa/riscv32/inst.c`、`src/memory/paddr.c`、`src/device/io/map.c`；原文 RTFSC 问题和 D 的完整 RV32IM 解释继续见 [D3](../../D/D3/NOTES.md)。

## 8. 必答题 Q03：打字游戏如何从按键更新画面

宿主 SDL 收到按键 → NEMU device_update/send_key 将 AM 键码和按下位入队 → guest 读取键盘 MMIO → AM_INPUT_KEYBRD 拆成事件 → 游戏判断是否 keydown、字母是否命中当前字符 → 修改游戏状态/分数 → 按状态生成像素 → AM_GPU_FBDRAW 写显存并请求同步 → NEMU/SDL 显示下一帧。

游戏逻辑只看 AM 事件，不应依赖宿主 SDL 扫描码；AM 驱动只负责硬件接口解释，不应决定“玩家命中”。键盘读取改变设备队列状态，不能当成可无限重复的普通 RAM 读取。矩形绘制也不等于显示器已经刷新，同步寄存器是最后一层交接。这样拆层后，键码错先检查设备/驱动，命中判定错检查游戏状态，颜色/位置错检查像素格式和行距，避免从全部波形里盲找。

## 9. 必答题 Q04：static/inline 编译与链接

在独立的真实 NEMU 副本中改变 ifetch.h，保留全部变体与链接诊断：

| 定义方式 | 优化 | 实际结果 |
| --- | --- | --- |
| static inline | -O2 | 通过 |
| inline（去 static） | -O2 | 通过；调用被优化展开 |
| static（去 inline） | -O2 | 通过；编译器仍可选择展开 |
| 无 static/inline | -O2 | 链接失败，inst.c 与 hostcall.c 产生多个外部定义 |
| inline（去 static） | -O0 | 链接失败，留下 inst_fetch 的未定义外部引用 |

static 决定内部链接，每个翻译单元有自己的定义；inline 并不保证机器码一定展开，也不能代替外部定义的链接规则。普通非 static 函数定义放在头文件中，被两个翻译单元包含，就会出现多个同名外部定义。仅 inline 的 C 定义在这里没有提供供未展开调用使用的外部定义，-O0 的实际链接失败验证了这一点。不能只凭 -O2 没报错推定该写法始终可链接。

## 10. 必答题 Q05：两处 dummy 为什么仍是 30 个

在本次记录的 RV32IM/性能配置、GCC 11.4 下，只在 common.h 加 `volatile static int dummy;`，最终 ELF 的 `nm -a -S` 找到 30 个独立的局部 BSS 对象。再在 debug.h 加相同语句，仍然是 30 个。数量来自实际参与编译的翻译单元及优化行为，不是所有 NEMU 配置固定为 30。

原因是头文件被文本包含进各个翻译单元。static 让不同翻译单元里的名字彼此独立；但同一个翻译单元内，同类型、同链接的多次暂定定义在翻译单元末尾合成一个对象。因此两个头文件并不自动把实体数翻倍。

把两处都改成 `volatile static int dummy = 0;` 后，两处都成为带初始化的定义，同一个翻译单元出现重定义，编译器明确拒绝。volatile 改变访问的可观察性要求，不会允许重复的带初始化定义。所有修改仅发生在隔离副本，实验结束恢复了该副本的原始头文件；活动 NEMU 的头文件未被修改。

## 11. 必答题 Q06：make 如何生成 hello ELF

hello 的 Makefile 指定 NAME 与 SRCS，再包含 AM 的公共 Makefile。ARCH=riscv32-nemu 选择架构头文件、交叉编译器、ISA/ABI 参数和 NEMU 平台源文件。公共规则先把 hello.c 与依赖头文件编成对象，递归构建 AM/klib 归档，然后用链接脚本安排启动入口、代码、数据、BSS、堆栈及 `_pmem_start=0x80000000`，最后链接生成 ELF。

ELF 保留节、段和符号信息；objcopy 再生成装载用 bin，insert-arg 把指定 mainargs 写入预留区域。run 目标随后调用 NEMU，并传入镜像、日志和报告路径。编译生成 `.d` 依赖文件，使头文件变化也能触发对应对象重建；对象和归档的依赖关系由规则决定，不能把一次完整命令行等同于 make 的全部机制。

已保存真实 `make -n -B -j1 ARCH=riscv32-nemu` 展开结果于 [hello.make-plan.txt](nemu_io/compiler/hello.make-plan.txt)。-n 打印将执行的命令，不声称自己完成了编译；实际编译/执行另有 hello 的 run.json 和 ELF/镜像哈希。

## 范围与复验

正常功能：`nemu_io/build.py`、`run_programs.py`、`gui_programs.py`；性能：`run_programs.py --benchmarks`；必答题编译实验：`compiler_questions.py`、`yemu_check.py`。这些入口只操作 C 专用目录。图形测试启动隔离 Xvfb，普通关闭后留下真实退出码、NEMU 报告和图像；没有操作用户桌面的窗口。

本工程没有替用户填写学号、生成官方提交身份或运行 make submit。声卡、在 NEMU 中嵌套 NEMU、优化 LiteNES 等原选做项目保留范围说明；未观看的完整视频和外部文章也不记为完成。所有源码/测试错误、下载失败、等待条件过短的失败均保存，不以删断言或改应用校验来获得 PASS。
