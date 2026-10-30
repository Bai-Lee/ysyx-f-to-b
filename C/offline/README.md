# C 阶段离线材料

`c-final-runtime.tar.gz` 保存 C 的最终运行工作台、AM/NEMU/RT-Thread/NVBoard、两种 SoC 生成器副本、记录的 C4/C5 模拟器二进制和主要固件。逐成员类型、源路径和 SHA-256 的对应关系见 [冻结清单（补充包：reports/C_runtime_export.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)，Linux 权限保存在 tar 内。链接保留为相对路径；原生成器指向外部 firtool 的绝对链接已作为锁定工具文件实体保存。

`sources/` 保存 C 新增的固定 SoC 主仓库、递归依赖和补充资料原包，见[来源清单](../../reports/C_offline_sources.json)。完整旧课程库和大部分已安装工具不重复打包；F/E/D 的原始源包与冻结运行包仍在累积交付树中。C2 的独立 NEMU I/O 快照在 [C2 snapshot](../C2/snapshot/manifest.json)，其中含 feature/performance 二进制、Capstone 和 Spike 参考库。

包中 `bin/C5/<配置>/sim` 的旧配置分别对应各自验收时的源输入；不能拿最新共享 runner 的时间戳推断所有旧二进制都已重建。每个构建的输入快照、命令和选项保留在 `artifacts/C5/build`。最终源码与软件覆盖文件的关系见[绑定检查](../../reports/C_final_bindings.json)。

## 已执行的离线重放

[重放报告](../../reports/C_offline_replay.json)记录从 tar 中实际解出的模拟器、固件和参考库，重新运行 MicroBench、脚本化 RT-Thread、ChipLink 正例及远端读数据损坏反例。正常结果、周期、退休指令、寄存器、UART 和适用的覆盖计数与原验收一致。重放使用已安装 Linux 的动态加载器/系统库，没有重新编译，也不代表在一台全新离线机器上重新构建所有工具。

在原工作区使用现有发行版/普通用户复跑，命令为：

```powershell
wsl -d YSYX-Linux -u ysyx -- python3 /workspace/projects/ysyx_f_to_b/C/runtime/replay_offline.py
```

它会创建新的隔离解包目录，沿用单重任务预算并保存独立运行记录。再次运行不会覆盖原验收输入，但会更新重放报告和当前证据槽，因此正式交付后重跑会使当前文件与旧 ZIP 的一致性检查如实失败；原 ZIP 是不变的交付快照。

## 只读完整性核验

```powershell
& C:\YSYX_WORKSPACE\projects\ysyx_f_to_b\scripts\Verify-C.ps1
& C:\YSYX_WORKSPACE\projects\ysyx_f_to_b\scripts\Verify-C.ps1 -External -Archive C:\YSYX_WORKSPACE\projects\ysyx_f_to_b\YSYX_C_DELIVERY.zip
```

第一条检查范围、结果、快照、冻结运行包、报告链接及历史文件。第二条额外核对原始课程副本和原 D ZIP，并检查交付 ZIP 的全部成员及旁置 `.sha256`。默认不运行长仿真；Python 核验器只使用标准库，可在解压后的工程根目录执行 `python scripts/verify_C_delivery.py`。PowerShell 包装器仍指向本项目已有解释器。

完整功能重建入口位于各章脚本和[执行说明](../runtime/README.md)。多小时的全容量遍历需要单独运行；不要以几十 KiB 的预跑替代完整容量。GUI 复验依赖 SDL、Xvfb、xdotool、scrot 及锁定 NVBoard；综合/生成依赖锁定 Verilator/Yosys/OpenSTA/单元库/JDK/Mill/firtool 和已有 Maven 缓存。安装资产/版本证据见[最终工具锁](../../reports/C_toolchain_final.json)，本包不承诺完全自包含的系统工具环境。

旧 F/E/D 原包保留在工作区，未嵌套到 `YSYX_C_DELIVERY.zip`。它们的旧终点断言仍以当时阶段为准，不能在 C 账本下直接运行旧阶段的完整“停点”核验来判断 C。C 核验器使用历史成员哈希检查保护。
