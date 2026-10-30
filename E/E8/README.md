# E8 复验入口

[验收报告](../../reports/E8_REPORT.md) · [方法说明](NOTES.md) · 签核包（原完整交付引用：`signoff/cpu-baseline-signoff.tar.gz`） · [版图（补充包：E/E8/signoff/layout.png）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)

最终候选为 BALANCE 3 综合网表，顶层 `ysyx_00000000`，物理目标 50 MHz。完整软件的 RTL、Verilator 网表和 Icarus 四值结果，以及所有后端约束、输入和签核检查分别留存。

| 入口 | 验证内容 |
|---|---|
| `front_audit.py` | 当前 RTL 与综合输入一致、正沿时钟、无锁存器、严格 lint、前端回归来源 |
| `preflight.py` / `icarus14_controls.py` | VPI 示例、插件缺失、不定态参数和漏复位负对照 |
| `rtl_icarus_programs.py` | 原始 hello 和完整 microbench 的四值 RTL 运行 |
| `mapped_final.py` | 最终基线网表的完整 Icarus 14 运行，原始 UDP 库模型 |
| `area_functional.py` | 面积策略网表完整 Verilator 程序验证 |
| `physical_run.py --name cpu_baseline --isolate-steps` | 用官方 `--only` 命令按步骤续跑，每步结束释放工具内存 |
| `export_signoff.py` | 实际签核检查、导出及全部清单成员的 SHA-256/大小验证 |
| `gui_session.py` / `gui_action.py` | 实际 ECOS 窗口与只读原生二维查看器的审阅环境 |
| `finalize.py` | 汇总 13 个时序角、9 个 SPEF、质量门槛与视觉证据 |

Linux 运行环境为 `YSYX-Linux`、用户 `ysyx`。WSL 内存上限已获授权调整为 4 GiB；物理流程限制为两个逻辑核，并监测进程组内存。每步独立启动保留完整物理流程与所有质量检查，避免工具跨步骤累积内存。

ECOS 的导出首先写入 Linux 工作目录，再逐字节复制到本项目。直接写入 Windows 挂载目录曾因复制文件元数据返回 `Operation not permitted`；原失败记录保留，未更改挂载权限或系统安全设置。

原生查看器需要的两项 X11 运行库以官方 Ubuntu 包便携解包，使用进程级库路径。二维查看采用上游提供的 `ECOS_GPU_CANVAS=0`，无需安装 CUDA 或修改全局驱动。内置 AI 代理与三维查看不属于本次验收范围。视觉验收与实际截图哈希绑定，重生成图片后应重新查看。

`signoff/cpu-baseline-signoff.tar.gz` 是工具产生的正式格式本地签核包；`native-run-evidence.tar.gz` 补充原生日志、配置及质量分析。这里的签核是锁定 PDK、SDC 和寄生模型下的本地结果，不表示已经实际生产芯片或通过个人课程认证。
