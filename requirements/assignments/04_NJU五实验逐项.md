# E4：NJU 五个实验逐项要求

E4 明确允许将 NVBoard 当作实验板使用。本清单采用 RTL 仿真＋NVBoard；若没有实际 FPGA 上板，不标为“实体上板 PASS”。原文的图、引脚、代码、表格见每项链接。除标明选做的组合键扩展，其余是实验实施/思考清单。

<a id="nju-02-01"></a>

### NJU-02-01 实验 2

来源：本地原文（原完整交付引用：`<../references/markdown/d29ffff00a654fdd.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://nju-projectn.github.io/dlco-lecture-note/exp/02.html)

**实现要求**：门级/RTL 实现 2→4、3→8 译码与普通编码示例

**交付物**：RTL、独立组合 TB、波形

**验收条件**（自验）：独热输入输出及使能条件穷举；普通编码器不把多热未定义当优先编码

归类：E4 指定实验。

<a id="nju-02-02"></a>

### NJU-02-02 实验 2

来源：本地原文（原完整交付引用：`<../references/markdown/d29ffff00a654fdd.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://nju-projectn.github.io/dlco-lecture-note/exp/02.html)

**实现要求**：8→3 高位优先编码、有效指示与十进制七段显示

**交付物**：编码器/七段 RTL、NVBoard 引脚

**验收条件**（自验）：256 输入穷举；全零 valid=0，多热取最高位，00001110→3；LED 与数码一致

归类：E4 指定实验。

<a id="nju-02-03"></a>

### NJU-02-03 实验 2

来源：本地原文（原完整交付引用：`<../references/markdown/d29ffff00a654fdd.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://nju-projectn.github.io/dlco-lecture-note/exp/02.html)

**实现要求**：理解 casex/casez 并讨论优先编码实现

**交付物**：语言规则/示例对照

**验收条件**（自验）：区分 X/Z 与通配，不能因过度匹配掩盖未知输入；功能对照参考

归类：E4 指定实验。

<a id="nju-03-01"></a>

### NJU-03-01 实验 3

来源：本地原文（原完整交付引用：`<../references/markdown/1a5b5cc32fc96bd9.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://nju-projectn.github.io/dlco-lecture-note/exp/03.html)

**实现要求**：全加器、串行进位及可加减的补码加法器

**交付物**：RTL、运算/进位/溢出/零检测 TB

**验收条件**（自验）：穷举四位 -8…7；最小负数相减与两种 Overflow 公式反例；进位/借位定义明确

归类：E4 指定实验。

<a id="nju-03-02"></a>

### NJU-03-02 实验 3

来源：本地原文（原完整交付引用：`<../references/markdown/1a5b5cc32fc96bd9.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://nju-projectn.github.io/dlco-lecture-note/exp/03.html)

**实现要求**：实现表 4 的四位 ALU 八种功能

**交付物**：ALU、选择表、NVBoard 交互

**验收条件**（自验）：000加/001减/010非/011与/100或/101异或/110有符号小于/111相等；运算标志正确，逻辑不强求溢出

归类：E4 指定实验。

<a id="nju-03-03"></a>

### NJU-03-03 实验 3

来源：本地原文（原完整交付引用：`<../references/markdown/1a5b5cc32fc96bd9.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://nju-projectn.github.io/dlco-lecture-note/exp/03.html)

**实现要求**：解释有符号/无符号比较由减法标志实现

**交付物**：公式、边界用例和独立参考

**验收条件**（自验）：-8、7、0、同数与溢出对照，不能直接取减法符号而忽略溢出

归类：E4 指定实验。

<a id="nju-06-01"></a>

### NJU-06-01 实验 6

来源：本地原文（原完整交付引用：`<../references/markdown/fc7e85498e5708ad.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://nju-projectn.github.io/dlco-lecture-note/exp/06.html)

**实现要求**：八位移位寄存器实现表 6 八种模式

**交付物**：RTL、串/并输入 TB

**验收条件**（自验）：000清零/001置数/010逻辑右/011逻辑左/100算术右/101串入/110循环右/111循环左；逐拍核对

归类：E4 指定实验。

<a id="nju-06-02"></a>

### NJU-06-02 实验 6

来源：本地原文（原完整交付引用：`<../references/markdown/fc7e85498e5708ad.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://nju-projectn.github.io/dlco-lecture-note/exp/06.html)

**实现要求**：八位组合桶形移位器及 RV32I 32 位推广思考

**交付物**：分级 MUX RTL、参考模型、结构解释

**验收条件**（自验）：shamt 0–7、左右/算逻所有组合；纯组合无时钟等待，32 位推广需五级/五位移量

归类：E4 指定实验。

<a id="nju-06-03"></a>

### NJU-06-03 实验 6

来源：本地原文（原完整交付引用：`<../references/markdown/fc7e85498e5708ad.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://nju-projectn.github.io/dlco-lecture-note/exp/06.html)

**实现要求**：八位 LFSR 伪随机发生器与十六进制显示

**交付物**：LFSR RTL、状态序列、NVBoard 映射

**验收条件**（自验）：新高位=x4⊕x3⊕x2⊕x0；非零种子周期255、255状态不重复，零态处理；源例九位拼写不得机械照抄

归类：E4 指定实验。

<a id="nju-06-04"></a>

### NJU-06-04 实验 6

来源：本地原文（原完整交付引用：`<../references/markdown/fc7e85498e5708ad.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://nju-projectn.github.io/dlco-lecture-note/exp/06.html)

**实现要求**：思考更复杂伪随机序列方法

**交付物**：方案及周期/统计性质说明

**验收条件**（自验）：区分确定性 LFSR 和真随机；不以看起来随机宣称密码安全

归类：E4 指定实验。

<a id="nju-07-01"></a>

### NJU-07-01 实验 7

来源：本地原文（原完整交付引用：`<../references/markdown/c203ed4c183393ac.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://nju-projectn.github.io/dlco-lecture-note/exp/07.html)

**实现要求**：四个连续 0 或 1 检测 FSM，允许重叠；比较编码/Moore/Mealy

**交付物**：二进制编码 RTL、TB、编码对照

**验收条件**（自验）：四/五连续位的第4/5拍 z=1；交替输入为0，低有效同步复位；说明 one-hot/Mealy 取舍

归类：E4 指定实验。

<a id="nju-07-02"></a>

### NJU-07-02 实验 7

来源：本地原文（原完整交付引用：`<../references/markdown/c203ed4c183393ac.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://nju-projectn.github.io/dlco-lecture-note/exp/07.html)

**实现要求**：实现 PS/2 帧接收、键码转 ASCII、按键次数与七段显示

**交付物**：PS2 接收/扫描码状态机、ASCII ROM、TB、NVBoard

**验收条件**（自验）：11位帧；字符和数字键；按下低两位键码/中两位ASCII，释放低四位灭；高两位累计，按住不重复计数；不要求组合键/小键盘

归类：E4 指定实验。

<a id="nju-07-03"></a>

### NJU-07-03 实验 7

来源：本地原文（原完整交付引用：`<../references/markdown/c203ed4c183393ac.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://nju-projectn.github.io/dlco-lecture-note/exp/07.html)

**实现要求**：高级选做：Shift/CTRL 状态、组合输入及大写 ASCII

**交付物**：扩展状态机、键序列用例

**验收条件**（自验）：修饰键与字符不冲突，按下释放次序正确，LED 状态正确；明确选做

归类：选做。

<a id="nju-08-01"></a>

### NJU-08-01 实验 8

来源：本地原文（原完整交付引用：`<../references/markdown/8eb56251b0d9d092.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://nju-projectn.github.io/dlco-lecture-note/exp/08.html)

**实现要求**：VGA 行场同步控制器

**交付物**：RTL、像素/同步波形、引脚约束

**验收条件**（自验）：640×480有效区，行800像素/场525行、25MHz；消隐/同步宽度与源时序表一致

归类：E4 指定实验。

<a id="nju-08-02"></a>

### NJU-08-02 实验 8

来源：本地原文（原完整交付引用：`<../references/markdown/8eb56251b0d9d092.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://nju-projectn.github.io/dlco-lecture-note/exp/08.html)

**实现要求**：图像转 MIF 并显示静态图

**交付物**：自有/合法图像、转换脚本、MIF、帧截图

**验收条件**（自验）：像素布局/颜色/地址互相一致，保留源文列优先和640×512的建议；不强制采用有歧义的19位拼接描述

归类：E4 指定实验。

<a id="nju-08-03"></a>

### NJU-08-03 实验 8

来源：本地原文（原完整交付引用：`<../references/markdown/8eb56251b0d9d092.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://nju-projectn.github.io/dlco-lecture-note/exp/08.html)

**实现要求**：小图在屏幕内移动，触边弹性反射

**交付物**：动画 RTL/程序、边界 TB、NVBoard 画面

**验收条件**（自验）：图像不越界；四边和角同时碰撞正确，x/y速度参数及方向可观察

归类：E4 指定实验。
