# D 阶段离线材料与恢复边界

`d-final-runtime.tar.gz` 保存最终 D 工作台源码、测试输入、AM/klib、NEMU、NPC、共享 REF 及实际使用的五个 Linux 二进制。逐成员内容哈希、符号链接目标和原路径见 [导出清单（补充包：reports/D_runtime_export.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)；最终作者源码与实际工作台的对应见 [最终绑定](../../reports/D_final_bindings.json)。这是最终执行候选的快照，不覆盖 D2 的 PA1 历史快照。

新增原始 NEMU、Capstone 5.0.6、Spike 源码在 `sources`，提交和摘要见 [源码锁定](../../reports/D_offline_sources.json)。AM、am-kernels、archbench、FCEUX、riscv-tests 的规范源码复用累计包中的 [E 源码归档](../../E/offline/README.md)。保留各上游许可证；NEMU REF 的许可证从同一原始 NEMU 补入归档。下载记录区分官方发布摘要与本地记录的 SHA-256。

完整课程原仓库、工具安装包、Ubuntu 系统库与 ICsprout55 PDK 不重复塞入交付包。它们仍位于锁定的 `/workspace/YSYX_F_B_Archive`、`/workspace/tools`、`/workspace/downloads` 及 WSL `/home/USER/tools`；版本和来源见项目 `config/toolchain.json` 与工作区 `config/toolchain.lock.json`。二进制依赖原 Ubuntu glibc、readline、SDL 等环境，本包不是跨系统即用的虚拟机镜像。

只读核验在 PowerShell 调用 `scripts/Verify-D.ps1`；加 `-Archive` 可检查 ZIP、CRC 和全部成员哈希。它核验保留证据，不重新执行仿真或冒充新的可视验收。

如需恢复实验，先在新目录解压快照，保留现有 `/home/USER/d-stage`。归档中的 Makefile 和证据明确记录原绝对路径；在新位置使用前，应逐项调整 `AM_HOME`、`NPC_HOME`、NEMU/REF/Capstone 路径和构建输出，核对源文件后只运行目标测试。Linux 动态库搜索可通过单次命令的 `LD_LIBRARY_PATH` 指向解压后的 `bin`；不改全局 PATH 或系统设置。不要把 ELF 当 Windows 可执行文件。

D2 的 `build_nemu.py`、D3 的 `build_nemu.py`、D5 的 `setup_am.py` 反映各自历史阶段的初始化，会覆盖后续配置，不能在最终工作台按文件名顺序重跑。D2 独立快照在 [manifest.json](../D2/snapshot/manifest.json)；后续最可靠恢复基准是本节最终源码包。复验脚本会保留旧尝试，但运行前仍应检查资源：单重任务、编译 `-j1`，系统可用内存低于 3 GiB 时不派发新重任务。

原来的分配器现场诊断脚本包含当时 PID，只作为历史文本保存在 `artifacts/D8/allocator_diagnosis/diagnose_allocator.py.txt`，不作为可再次执行的入口。
