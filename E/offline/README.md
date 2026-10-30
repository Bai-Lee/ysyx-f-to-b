# E 阶段离线材料

本目录提供已经验收的源代码与运行副本，配合[总报告](../../reports/E_REPORT.md)、工具清单（原完整交付引用：`../../config/toolchain.json`）和[最终工具指纹](../../reports/E_toolchain_final.json)使用。

- `sources/`：8 个固定提交的顶层仓库归档，以及实际使用的官方 klib。导出时关闭 Git 的自动换行转换；原始完整仓库及其子模块继续保存在课程归档目录。
- `patched-runtime.tar.gz`：NPC、AM、SoC 外设接口、NVBoard 资源和选定运行产物，共 726 个逐项校验成员。补丁后的代码保留上游许可证。
- [运行副本清单](../../reports/E_runtime_export.json)和[源码清单](../../reports/E_offline_sources.json)记录来源、文件名及 SHA-256。
- E7 的独立测试对象和调度代码另见批处理归档（原完整交付引用：`../E7/batch/objects-and-dispatch.tar.gz`）；E8 的版图、网表、约束与寄生文件见签核包（原完整交付引用：`../E8/signoff/cpu-baseline-signoff.tar.gz`）。

这些材料不包含 WSL 操作系统安装器和全部已安装工具。编译器、仿真器、ECC/ECOS、PDK 资产使用锁定清单中现有的 D 盘与 Linux 路径。顶层源码归档不是包含所有子模块的完整 Git 克隆；现有实验使用已归档的生成后 SoC RTL，无需重新生成 Chisel。

在本机运行 `scripts/Verify-E.ps1` 可只读检查阶段记录、冻结副本、归档成员与文档链接。增加 `-External` 会核对外部课程原件；增加 `-Archive <完整ZIP路径>` 会读取交付包的全部成员并检查 CRC 与 SHA-256。这个入口不重新运行长时仿真，也不改写验收结果。

需要重跑功能测试时使用各阶段 README 和报告列出的入口。复验会在 `artifacts` 保存新结果和历史尝试；较长的程序、四值网表和物理设计必须串行调度并复核可用内存。E5、E6 的冻结副本用于追溯旧阶段，不应被后续 AM 或仿真器修改覆盖。
