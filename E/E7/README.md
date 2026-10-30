# E7 运行入口

[验收结果](../../reports/E7_REPORT.md) · [方法与推导](NOTES.md) · [原讲义归档](https://ysyx.oscc.cc/docs/2607/e/7.html)

下列入口在 WSL 的 `YSYX-Linux` 发行版、普通用户 `ysyx` 下执行。公共路径固定于本项目的 `E/runtime/common.py`；不是无依赖安装包。已安装工具和原始课程归档的位置见项目锁定清单。

| 入口 | 作用 |
|---|---|
| `build.py --mode valid` | 编译独立的 valid 总线 CPU |
| `build.py --mode soc` | 编译接入提供 SoC 的 CPU |
| `bus_tests.py` | 7 组延迟下的 511 次官方测试和波形检查 |
| `standalone.py` | 3 种结构完整应用/benchmark 回归，包含较长 train 运行 |
| `soc_batch_run.py` | 真实 Flash 启动后依次运行 73 个原测试体，以及独立 wrong 对照 |
| `soc_hello.py` | mainargs、UART16550、时钟比例与两种波特率参数 |
| `gui_verify.py` | 在已有 X11 显示上自动点击 NVBoard 并保存截图 |
| `timer_verify.py --platform npc` | 原始 RTC 测试在隔离 AM 副本上做主机时间校准 |
| `soc_performance.py` | 25/125/75 MHz 三组完整 blockchain train |
| `final_runtime.py` | 构建入口、编译失败传播与默认 NPC 应用复验 |
| `finalize.py` | 检查已完成的结果、冻结快照并生成阶段报告 |

例如从 Windows PowerShell 编译：

```powershell
wsl -d YSYX-Linux -u ysyx --exec python3 /workspace/projects/ysyx_f_to_b/E/E7/build.py --mode valid
```

交互式 NVBoard 需要可用的 Linux 图形显示环境；自动验收使用 Xvfb，截图是实际界面的捕获。`gui_verify.py` 的程序是合法自写 GPIO/CSR 演示，要求先构建 `soc_gui` 并准备对应软件镜像。视觉签收文件与截图哈希绑定，重新生成截图后需重新查看，不能直接复用旧的目视结论。

工作台分为 E6 原工作台、E7 独立 CPU 工作台、SoC AM 副本和 RTC 专用副本。对同一个 SoC AM 修改频率时应串行构建/运行，防止头文件在另一条命令中途变化。`runtime_snapshot` 和 `offline` 是验收后的副本；每次运行的具体输入与输出保存在 `artifacts`。
