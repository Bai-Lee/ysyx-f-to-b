# E8 验收报告

10 项必做工程任务已完成本地验收。最终 CPU 在 **50 MHz 约束**下通过全流程及签核检查，DRC、LVS 均为 **0 违规**。

完整签核包（原完整交付引用：`../E/E8/signoff/cpu-baseline-signoff.tar.gz`） · [版图（补充包：E/E8/signoff/layout.png）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0) · ECOS 实际界面（原完整交付引用：`../artifacts/E8/gui/dashboard_ready.png`） · 原生二维查看器（原完整交付引用：`../artifacts/E8/gui/native_micrometers.png`） · [方法与限制](../E/E8/NOTES.md)

| 项目 | 结果 |
|---|---:|
| die 面积 | 34596 µm² |
| core 面积 | 33124 µm² |
| 最差 setup WNS | 2.707 ns |
| 最差 hold WNS | 0.085 ns |
| setup / hold TNS | 0 / 0 ns |
| 时序角 | 13 |
| SPEF 文件 | 9 |
| 签核包已核对文件 | 210 |

界面显示的 58 MHz 是工具报告的频率估计；本次实际闭合约束为 50 MHz。最终布线输入网表与已经通过功能仿真的 BALANCE 网表逐字节一致。

完整 microbench 在 Icarus 14 原始 UDP 标准单元模型中以 22,129,163 周期、GOOD_TRAP 结束；同样的程序和周期数也在 RTL 与 Verilator 网表环境中通过。AREA 网表另通过完整 Verilator hello/microbench，用于 E7 策略比较。

签核检查仅保留无宏单元时允许的 `config.macro_locations` 提示，未绕过任何阻塞项。ECOS 原生二维查看器使用工具提供的 CPU 绘制选项，实际查看了全部 20 个图层和 382,252 个绘图对象。

| 工艺库角 | 温度 | RC 角 | setup WNS/ns | hold WNS/ns |
|---|---:|---|---:|---:|
| MAX | 125 | Cworst | 2.707 | 0.259 |
| MAX | 125 | RCworst | 5.094 | 0.255 |
| MIN | -40 | Cbest | 16.236 | 0.085 |
| MIN | -40 | Cworst | 15.768 | 0.086 |
| MIN | -40 | RCbest | 15.992 | 0.085 |
| MIN | -40 | RCworst | 16.168 | 0.085 |
| ML | 125 | Cbest | 15.5 | 0.095 |
| ML | 125 | Cworst | 14.888 | 0.096 |
| ML | 125 | RCbest | 15.188 | 0.096 |
| ML | 125 | RCworst | 15.413 | 0.095 |
| TYP | 25 | TYPICAL | 13.11 | 0.137 |
| WCL | -40 | Cworst | 3.57 | 0.253 |
| WCL | -40 | RCworst | 5.687 | 0.25 |

| ID | 状态 |
|---|---|
| E8-M001 | PASS |
| E8-M002 | PASS |
| E8-M003 | PASS |
| E8-M004 | PASS |
| E8-M005 | PASS |
| E8-M006 | PASS |
| E8-M007 | PASS |
| E8-M008 | PASS |
| E8-M009 | PASS |
| E8-M010 | PASS |
| E8-O001 | NOT_APPLICABLE |
| E8-O002 | NOT_APPLICABLE |
| E8-O003 | NOT_APPLICABLE |
| E8-O004 | NOT_APPLICABLE |
| E8-O005 | NOT_SELECTED_OPTIONAL |
| E8-R001 | PASS_DOCUMENTED |
