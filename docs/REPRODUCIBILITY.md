# 复现范围和外部依赖

最小仿真只依赖 Python 与 Icarus，入口见 [SIMULATION.md](SIMULATION.md)。其输入来自最终 B 版本的既有 RTL、网表和四值测试平台；便携脚本和小程序是本次整理时新增的。

完整 F～B 历史工程还依赖 Logisim、Verilator、C/C++ 和 RISC-V 交叉编译器、NEMU、AM、课程 SoC、RT-Thread，以及相应阶段的模型与 EDA 工具。这些依赖不由最小入口偷偷下载或安装。

## 重要固定来源

| 依赖 | 原工程使用的来源/提交 |
|---|---|
| ysyxSoC 兼容框架 | [OSCPU/ysyxSoC](https://github.com/OSCPU/ysyxSoC)，`ysyx6`，`bcdcbc3e8d97a11c07d3007e14f33c6147c02a8e` |
| NEMU | [NJU-ProjectN/nemu](https://github.com/NJU-ProjectN/nemu)，ics2024，`8e7a0fecc95b5b5d2c1f6be0ec1b703da93356c0`，再应用阶段改动 |
| AbstractMachine | [NJU-ProjectN/abstract-machine](https://github.com/NJU-ProjectN/abstract-machine)，ics2026，`9bc0a93c52c928a6de970f39a507be94cfb63a9f` |
| AM Kernels | [NJU-ProjectN/am-kernels](https://github.com/NJU-ProjectN/am-kernels)，ics2026，`9c433f7cf4b4e05d09543bf7e269b23502d1b2b6` |
| RT-Thread AM | [NJU-ProjectN/rt-thread-am](https://github.com/NJU-ProjectN/rt-thread-am)，`72ba231bb79db53f1c07920f2642ef20679faeff` |
| NVBoard | [NJU-ProjectN/nvboard](https://github.com/NJU-ProjectN/nvboard)，`b5f49b68a85f4a1a185086cbd6532fff3ecda454` |

任务文本版本与兼容框架分支分别锁定；不能把 `ysyx6` 构建称为 `2607` 分支的原样构建。递归依赖与来源证据见 [C5 来源锁](../reports/C5_source_lock.json)和[上游清单](../THIRD_PARTY_SOURCES.md)。历史二进制版本见各阶段 `*_toolchain*.json`，工具版本字符串本身不是通过证明。

## 历史脚本和报告

旧脚本围绕阶段工作台、锁定工具和本地证据布局编写。脱敏用占位路径替换了本机绝对路径、Windows 用户名和主机名。复现这些脚本需显式配置自己的目录、依赖与资源预算；不要运行旧环境安装/系统配置脚本来尝试最小演示。

历史停止点核验器仍描述当时状态，例如“尚未进入下一阶段”。它们不应直接覆盖最终 B 状态。历史清单中的哈希描述原始文件；公开副本的当前哈希见 `publication/FILES.sha256`，两者不同的原因记录在 `publication/provenance.json`。

体积较大的文本输出和图示以 Release 补充包交付。补充包恢复原相对目录；不包含原电脑凭据、整个工具安装、WSL 磁盘、重复交付 ZIP 或完整第三方仓库。

## 建议资源

小演示顺序执行即可。完整构建建议从 `-j4` 开始，一次只运行一个大型构建/综合；先测小样本再运行长基准。原工作台的 128 MiB 全容量验证是长任务，不能把短演示或稀疏功能 RAM 的成功当作它的重跑。

