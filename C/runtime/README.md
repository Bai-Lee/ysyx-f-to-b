# C 阶段执行入口

C 公开工程完成，执行边界止于 C。固定原文 101 条：68 项公开核心、2 项项目编号适配、22 条选做/背景、9 条方法提醒。C1/C3 没有独立编程作业，C6 原页建设中。总入口是 [C 报告](../../reports/C_REPORT.md)、[任务清单](../../reports/C_TASKS.md)和[机器审计](../../reports/C_AUDIT.json)。

独立工作台 `/home/USER/c-stage` 从 D 的冻结副本创建，F/E/D 不受修改。主框架、子模块、模型、规范、工具路径及版本分别在章节报告中锁定。初始预检保留当时的 pending 状态，后续实际功能结果和[最终指纹](../../reports/C_toolchain_final.json)是完成依据。

大型综合/生成默认一个重任务。用户于 2026-10-29 授权的并行验收允许一个批次最多 8 个独立仿真，共用 PSS 软上限 6144 MiB，按实时余量自动减少并发；固件构建使用 `-j4`。历史脚本保留其原命令和串行默认值。Windows 可用内存不足 2 GiB 不启动批次，运行中 Windows 低于 1 GiB 或 WSL 低于 512 MiB 则停止并记录 RESOURCE_LIMIT。生成器 JVM 堆上限 4 GiB；WSL 实际容量每次运行前复测。策略及实测见 [并行策略](../../reports/C_performance_policy.json)。

只读核验使用 [Verify-C.ps1](../../scripts/Verify-C.ps1)。[导出脚本](export_final.py)生成一次性冻结包，拒绝覆盖；[最终绑定](final_bindings.py)检查源码、二进制及工具指纹；[离线重放](replay_offline.py)从冻结包中取出程序并实际运行。不要在正式交付后随意运行 setup 脚本覆盖已冻结的工作台。

功能复验按需要选择章节入口：C1 和 C3 的 `run_experiment.py`；C2 的 `nemu_io/`、PA2 与设备脚本；C4 的六模式回归、`rtl_tests/run_fabric.py`、性能和时序脚本；C5 的 `verify_*`、`gui_verify.py` 及 `audit_sdram_coverage.py`。具体命令以已保存的 `artifacts/C*/.../run.json` 为准，包含完整选项、cwd、输入哈希与退出码。原始失败和反例保留在 `attempts`，不能通过更改规格来获得通过。

128 MiB 四颗 SDRAM 的当前入口是 [Start-C5-Full-Sdram.ps1](../../scripts/Start-C5-Full-Sdram.ps1)，内部启动 `run_parallel_sdram_job.py --launch`。它调用 `parallel_sdram.py --bytes 134217728 --jobs 8 --label full128`，每个图样独立复位并完整遍历全范围，全部宽度、图样和参考比较保留。实际并发数受内存余量约束，已完成图样经严格哈希核对后可续用。批次结束后用 `scripts/accept_C_parallel.py --full` 作独立汇总。不要同时启动另一个大批次或大型综合。

本工程没有进入 B，没有把旧 E 物理签核移用于 C CPU/SoC。原题、原图与原课程库不作原地修改。
