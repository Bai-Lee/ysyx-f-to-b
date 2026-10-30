# F阶段交付与验收

**F阶段必做技术任务已完成，最终文件审计PASS。按用户最新指令使用灵活的命令行路线，完成F后停止；E～B没有开始。**

67个黄色源框中，图例/个人流程3项排除，64项技术必做完成；10项选做完成（其中3项为纸面分析），其余选做或背景明确标记。PASS_ADAPTED表示用户已授权的工具/操作方式替代，未降低公开功能规格。

|阶段|状态计数|
|---|---|
|F1|{"EXCLUDED_SCOPE": 3, "PASS": 3}|
|F2|{"PASS": 3, "PASS_ADAPTED": 2}|
|F3|{"PASS": 37}|
|F4|{"PASS": 5, "PASS_ADAPTED": 2}|
|F5|{"PASS_ADAPTED": 7}|
|F6|{"PASS_ADAPTED": 5}|

## 实际执行结果

- 原生结构电路：33个电路、25753向量；包括实际LED/七段组件端口、SR振荡、触发器保持、四位算术和完整一小时分秒状态回绕。最终一次加载只读磁盘字节并检查输入运行前后哈希。
- sCPU：ROM全部256地址；GPR1024写入及16384组读检查；四种基础/增强阶段共32768个任意初态单步样本，覆盖全部256编码。
- 固件：23项正常运行及4类故障拒绝。求和55/奇数和25、增强li/有符号分支、0/255等末项、4种非零按钮、输出保持、12指令电平步进及按下释放步进均实际运行；每周期比较PC/GPR/LED/HEX并保存CSV/VCD。
- 故障拒绝：错误分支符号扩展、错误常量R0、缺输出寄存器、错误li移位均导致非零退出；正常版本通过。另有缺线电路、错误期望值、错误C源码和8类非法汇编操作数对照。
- C程序：本机GCC编译执行z=3/z=42/sum=55；Compiler Explorer真实线上执行同三项并取得source.line汇编映射。
- 选做：16→4优先编码、四种首尾位计数遍历65536输入；两个半加器组成全加器遍历8输入。
- Yosys真实完成ROM MUX映射和增强sCPU结构检查；没有输出缺少工艺/约束支持的PPA结论。

## 逐项64技术必做及排除项

|ID|实现要求|验收状态|具体结果与证据|
|---|---|---|---|
|F1-M001|识别黄色框图例，无作业|EXCLUDED_SCOPE|LEGEND<br>|
|F1-M002|通识问卷、报名与入学资格|EXCLUDED_SCOPE|USER_EXCLUDED_PERSONAL<br>|
|F1-M003|保留学习过程的工程证据；不创建个人学习表|PASS|Actual commands/failed attempts/input snapshots and hashes maintained in artifacts; local Git project initialized.<br>[preflight_F.json](../reports/preflight_F.json)、[F1_工程方法与记录.md](../F/notes/F1_工程方法与记录.md)|
|F1-M004|个人提问指南与模板|EXCLUDED_SCOPE|USER_EXCLUDED_PERSONAL<br>|
|F1-M005|理解搜索、查阅手册与阅读源码的作用|PASS|STFW/RTFM/RTFSC applied to Pin invalidation, model port geometry, DipSwitch documentation and autosave recovery.<br>[preflight_F.json](../reports/preflight_F.json)、[F1_工程方法与记录.md](../F/notes/F1_工程方法与记录.md)|
|F1-M006|阅读 AI 时代学习信，理解原创实现与理解能力要求|PASS|Read source letter; engineering reflection and independent verification method delivered; no personal biography invented.<br>[preflight_F.json](../reports/preflight_F.json)、[F1_工程方法与记录.md](../F/notes/F1_工程方法与记录.md)|
|F2-M001|安装或复用 Logisim-evolution 并打开|PASS|Required technical deliverable and its checks completed.<br>[F2_results.json](../reports/F2_results.json)、[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F2_工具与教程.md](../F/notes/F2_工具与教程.md)|
|F2-M002|完成官方入门教程全部六部分并跟做|PASS_ADAPTED|Native Logisim tutorial_xor: 4 vectors, zero mismatches; input bytes unchanged.<br>[F2_results.json](../reports/F2_results.json)、[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F2_工具与教程.md](../F/notes/F2_工具与教程.md)|
|F2-M003|阅读图形界面与菜单参考|PASS_ADAPTED|Actual execution/evidence complete under user-authorized non-GUI workflow.<br>[F2_results.json](../reports/F2_results.json)、[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F2_工具与教程.md](../F/notes/F2_工具与教程.md)|
|F2-M004|阅读 Input/Output library 元件功能|PASS|Required technical deliverable and its checks completed.<br>[F2_results.json](../reports/F2_results.json)、[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F2_工具与教程.md](../F/notes/F2_工具与教程.md)|
|F2-M005|自行设计一个感兴趣的数字电路并仿真|PASS|Native Logisim parity_alarm: 16 vectors, zero mismatches; input bytes unchanged.<br>[F2_results.json](../reports/F2_results.json)、[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F2_工具与教程.md](../F/notes/F2_工具与教程.md)|
|F3-M001|分析原图的晶体管门电路|PASS|Source transistor topology identified as NOR; four ideal-switch input combinations checked.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M002|画出或门的晶体管结构|PASS|OR drawn as NOR plus inverter; all six device/net identities cross-checked and four outputs verified.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M003|用其他逻辑门搭建 XOR 并计算晶体管数|PASS|Native Logisim xor_nand4: 4 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M004|用门搭建 XNOR|PASS|Native Logisim xnor: 4 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M005|按对等设计原则分析 AND、NOR、OR、传输门面积|PASS|NOT/NAND/AND/NOR/OR/TG equal-drive area formulas derived; physical device count distinguished from area units.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M006|分别从门级和晶体管级构建 N 输入 NAND|PASS|NAND N(N+1) versus specified gate chain 8N-10 derived for N>=2, checked at 31 integer sizes.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M007|用门实现 2→4 译码器，不能用现成译码元件代替|PASS|Native Logisim decoder2to4: 4 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M008|把自建译码器封装成子电路|PASS|Native Logisim decoder2to4: 4 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M009|通过若干 2→4 译码器与少量门扩成 3→8|PASS|Native Logisim decoder3to8: 8 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M010|4 位输入、8 位输出的十进制七段译码器|PASS|Native Logisim sevenseg_decimal: 16 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M011|增加十六进制 A,b,C,d,E,F 显示|PASS|Native Logisim sevenseg_hex: 16 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M012|门级 16→4 编码器接十六进制数码管|PASS|Native Logisim encoder16to4: 16 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M013|4→2 优先编码器，列逻辑式并比较面积|PASS|Native Logisim priority4to2: 16 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M014|门级 1 位 2 选 1 MUX|PASS|Native Logisim mux2: 8 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M015|门级 3 位 4 选 1 MUX，画结构|PASS|Native Logisim mux4x3: 16384 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M016|5 开关控制十/十六进制七段显示|PASS|Native Logisim select_display: 32 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M017|4 位相等比较器，结果驱动 LED|PASS|Native Logisim equal4: 256 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M018|门级 1 位全加器并列真值表|PASS|Native Logisim full_adder: 8 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M019|4 位加法器，两个输入与结果十六进制显示、LED 显示进位|PASS|Native Logisim add4: 256 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M020|4 位减法器与借位显示|PASS|Native Logisim sub4: 256 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M021|4 位原码加法器，负结果额外显示负号|PASS|Native Logisim signmag4: 256 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M022|4 位反码加法器|PASS|Native Logisim ones4: 256 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M023|补全补码溢出表并实现检测|PASS|Native Logisim signed_overflow4: 256 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M024|门级 SR 锁存器，观察非法状态释放和仿真振荡|PASS|Native Logisim sr_latch: 6 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M025|分析原图第一种 D 锁存器|PASS|Native Logisim dlatch_nor: 6 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M026|分析原图另一种 D 锁存器|PASS|Native Logisim dlatch_nand: 6 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M027|门级搭建 D 锁存器|PASS|Native Logisim dlatch_nor: 6 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M028|给 D 锁存器加复位至 0|PASS|Native Logisim dlatch_reset: 9 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M029|输出取反反馈到 D 锁存器，解释振荡|PASS|Native Logisim latch_oscillator: 2 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M030|主从式 D 触发器，用按钮时钟观察|PASS|Native Logisim dff: 8 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M031|为 D 触发器加复位至 0|PASS|Native Logisim dff_reset: 120 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M032|D 触发器反馈取反实现翻转并比较锁存器|PASS|Native Logisim toggle: 66 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M033|带使能的 D 触发器|PASS|Native Logisim dff_enable: 120 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M034|4 位带复位寄存器，拨码输入、数码输出|PASS|Native Logisim reg4: 36 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M035|4 位循环计数器|PASS|Native Logisim counter4: 68 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M036|寄存器与加法器实现 1+…+10|PASS|Native Logisim sum10: 30 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F3-M037|实现有分、秒的电子时钟|PASS|Native Logisim clock_mmss: 7204 vectors, zero mismatches; input bytes unchanged.<br>[F_circuit_results.json（补充包：reports/F_circuit_results.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[F_theory_results.json](../reports/F_theory_results.json)、[F3_逻辑与时序分析.md](../F/notes/F3_逻辑与时序分析.md)|
|F4-M001|继续执行讲义 sISA 求和程序，记录寄存器状态|PASS|Real RTL trace reaches PC7 and R2=55, then retains the self-loop state.<br>[F4_results.json](../reports/F4_results.json)、[F4_状态机与编译.md](../F/notes/F4_状态机与编译.md)、[c_to_assembly.md](../F/analysis/c_to_assembly.md)|
|F4-M002|用 sISA 求 1+3+5+7+9|PASS|Independent odd-sum firmware reaches PC7 and R2=25 on the same hardware.<br>[F4_results.json](../reports/F4_results.json)、[F4_状态机与编译.md](../F/notes/F4_状态机与编译.md)、[c_to_assembly.md](../F/analysis/c_to_assembly.md)|
|F4-M003|在 Compiler Explorer 运行示例 C 并修改观察|PASS_ADAPTED|Compiler Explorer cg151 actually executes z=3; modified z=42 and native GCC executions also pass.<br>[F4_results.json](../reports/F4_results.json)、[F4_状态机与编译.md](../F/notes/F4_状态机与编译.md)、[c_to_assembly.md](../F/analysis/c_to_assembly.md)|
|F4-M004|继续执行原 C 程序并记状态|PASS|Source-level x/y/z state sequence and END explained; actual output3 confirmed.<br>[F4_results.json](../reports/F4_results.json)、[F4_状态机与编译.md](../F/notes/F4_状态机与编译.md)、[c_to_assembly.md](../F/analysis/c_to_assembly.md)|
|F4-M005|从状态机解释 F3 求和电路|PASS|Dedicated i/sum states0..10 tabulated and checked against native per-vector assertions.<br>[F4_results.json](../reports/F4_results.json)、[F4_状态机与编译.md](../F/notes/F4_状态机与编译.md)、[c_to_assembly.md](../F/analysis/c_to_assembly.md)|
|F4-M006|解释 C 求和与指令序列的编译对应|PASS|Real loop-boundary commits satisfy sum=i(i+1)/2; intermediate ISA states distinguished from one dedicated clock.<br>[F4_results.json](../reports/F4_results.json)、[F4_状态机与编译.md](../F/notes/F4_状态机与编译.md)、[c_to_assembly.md](../F/analysis/c_to_assembly.md)|
|F4-M007|在 Compiler Explorer 对照 C 与汇编|PASS_ADAPTED|Real Compiler Explorer source.line mappings preserved; replaces GUI color highlighting by user-authorized API.<br>[F4_results.json](../reports/F4_results.json)、[F4_状态机与编译.md](../F/notes/F4_状态机与编译.md)、[c_to_assembly.md](../F/analysis/c_to_assembly.md)|
|F5-M001|用 MUX 构建存求和指令的 ROM，并由 PC 取指|PASS_ADAPTED|256 ROM addresses compared; real Yosys maps byte selection into a MUX network.<br>[F_cpu_results.json](../reports/F_cpu_results.json)、[scpu.sv](../F/rtl/scpu.sv)、[F5_结构与程序.md](../F/notes/F5_结构与程序.md)|
|F5-M002|用寄存器和译码构建可写 GPR|PASS_ADAPTED|GPR4x8 passes1024 writes,16384 address-pair reads,1024 hold checks and reset; R0 writable.<br>[F_cpu_results.json](../reports/F_cpu_results.json)、[scpu.sv](../F/rtl/scpu.sv)、[F5_结构与程序.md](../F/notes/F5_结构与程序.md)|
|F5-M003|实现 li 指令周期及 PC 更新|PASS_ADAPTED|STAGE0 li-only executes first4 initialization instructions with expected PC/GPR.<br>[F_cpu_results.json](../reports/F_cpu_results.json)、[scpu.sv](../F/rtl/scpu.sv)、[F5_结构与程序.md](../F/notes/F5_结构与程序.md)|
|F5-M004|增加 add 指令|PASS_ADAPTED|STAGE1 adds add; first6 instructions end with R1=1,R2=1.<br>[F_cpu_results.json](../reports/F_cpu_results.json)、[scpu.sv](../F/rtl/scpu.sv)、[F5_结构与程序.md](../F/notes/F5_结构与程序.md)|
|F5-M005|增加 bner0，运行完整求和程序|PASS_ADAPTED|STAGE2 complete program gives PC7,R2=55 and self-loop hold.<br>[F_cpu_results.json](../reports/F_cpu_results.json)、[scpu.sv](../F/rtl/scpu.sv)、[F5_结构与程序.md](../F/notes/F5_结构与程序.md)|
|F5-M006|比较专用求和电路与存储程序处理器|PASS_ADAPTED|Dedicated versus stored-program comparison includes10 versus34 update steps and explicitly avoids unsupported PPA.<br>[F_cpu_results.json](../reports/F_cpu_results.json)、[scpu.sv](../F/rtl/scpu.sv)、[F5_结构与程序.md](../F/notes/F5_结构与程序.md)|
|F5-M007|仅改指令序列求奇数和|PASS_ADAPTED|Only firmware image changes; same core computes odd sum25.<br>[F_cpu_results.json](../reports/F_cpu_results.json)、[scpu.sv](../F/rtl/scpu.sv)、[F5_结构与程序.md](../F/notes/F5_结构与程序.md)|
|F6-M001|增强 li 移位立即数和 bner0 的 4 位有符号相对偏移|PASS_ADAPTED|Enhanced li shift and signed PC-relative branch pass8192 arbitrary-state encoding cases and sum55 firmware.<br>[F_cpu_results.json](../reports/F_cpu_results.json)、[F_assembler_results.json](../reports/F_assembler_results.json)、[scpu.sv](../F/rtl/scpu.sv)、[F6_增强指令与输入输出.md](../F/notes/F6_增强指令与输入输出.md)|
|F6-M002|增加 io，结果输出到 8 位 LED|PASS_ADAPTED|Output register drives LED data55=0x37 and remains stable after source GPR changes.<br>[F_cpu_results.json](../reports/F_cpu_results.json)、[F_assembler_results.json](../reports/F_assembler_results.json)、[scpu.sv](../F/rtl/scpu.sv)、[F6_增强指令与输入输出.md](../F/notes/F6_增强指令与输入输出.md)|
|F6-M003|io 输出到两个十六进制数码管|PASS_ADAPTED|Independent HEX register and high/low segment decoders show37 for decimal55; source-overwrite hold checked.<br>[F_cpu_results.json](../reports/F_cpu_results.json)、[F_assembler_results.json](../reports/F_assembler_results.json)、[scpu.sv](../F/rtl/scpu.sv)、[F6_增强指令与输入输出.md](../F/notes/F6_增强指令与输入输出.md)|
|F6-M004|io 从拨码读入数列末项|PASS_ADAPTED|Switch limits0,1,2,10,22,23,31,127,255 actually run; overflow and zero-limit behavior documented.<br>[F_cpu_results.json](../reports/F_cpu_results.json)、[F_assembler_results.json](../reports/F_assembler_results.json)、[scpu.sv](../F/rtl/scpu.sv)、[F6_增强指令与输入输出.md](../F/notes/F6_增强指令与输入输出.md)|
|F6-M005|循环输出当前项，求和完成后轮询按钮再显示结果|PASS_ADAPTED|No-button display hold and four nonzero button values checked; current-term LED remains held.<br>[F_cpu_results.json](../reports/F_cpu_results.json)、[F_assembler_results.json](../reports/F_assembler_results.json)、[scpu.sv](../F/rtl/scpu.sv)、[F6_增强指令与输入输出.md](../F/notes/F6_增强指令与输入输出.md)|

## 选做与范围

已完成：F3-O011, F3-O012, F3-O013, F3-O014, F3-O017, F3-O015, F5-O001, F6-O001, F6-O002, F6-O003。

未选做：F3-O003, F3-O004, F3-O006, F3-O007, F3-O018, F3-O019。未选项不记PASS。F7建设中按用户指令忽略，无公开技术作业可验收。

## 验证边界

这是按公开功能要求的自验，未申请官方身份、考核或认证。数字仿真振荡不证明模拟亚稳态；理想晶体管开关和面积单位不等同PDK/真实PPA；32768个任意初态是抽样而非全状态证明；没有设计或验证RISC-V、E阶段框架及后端流片流程。

## 给GPT-6 Astra的接续入口

先读项目README、config/execution_policy.json、config/task_status.json和本报告，然后从E1开始。F5/F6是8位sISA，不可当RISC-V：R0可写、PC每指令+1；后续RISC-V的x0/指令宽度/寄存器组必须重新按手册实现。原归档保持只读，使用固定提交的官方框架，不能把其中现成代码冒充独立实现。

E目录当前为空；现有Icarus/Yosys/Verilator来自工作区锁定工具。只发现WSL入口，没有注册Linux发行版；后续E3需要实际Linux验证，系统/WSL组件变更遵循根AGENTS规则。此轮没有安装系统组件、改全局PATH、填写个人表格或发消息给外部人员。


最终审计：`F_final_audit.json`，所有检查PASS；已停止在F，等待用户更换模型。
