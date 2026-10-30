# B 冻结运行包

`b-final-runtime.tar.gz` 保存 B 的独立工作台源码、最终/历史已记录模拟器配置、NEMU/Spike 参考、Icarus 字节码与程序镜像，共 4,977 个成员。每个普通文件的 SHA 和受限相对符号链接已逐项核对；清单见 [运行包清单（补充包：reports/B_runtime_export.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)。完整累积 ZIP 另外保存原始命令、输入/输出快照和阶段报告。

[离线验收](../../reports/B_offline_replay.json)从这个包提取二进制、参考和镜像到新目录后真实运行：上下文、RT-Thread、microbench test、原 wrong.c、4 KiB 全图样中的一个完整图样、门级 Icarus hello。DUT/REF/程序没有借用原工作台中的活文件；运行所需的 Linux 动态装载器/系统库、锁定 Icarus 与项目资源守卫仍来自已安装环境。完整128MiB的原运行证据按哈希核验，短重放不重复耗时的大容量测试。

当前路径为 `/workspace/projects/ysyx_f_to_b`，WSL 分发为 `YSYX-Linux`，用户为 `ysyx`。Linux 工作台在 `/home/USER/b-stage`。使用 `B/runtime/replay_offline.py --demo` 会再次从包提取到唯一新目录，并将结果写到 `artifacts/B/demo/时间戳`，不覆盖交付验收报告。Windows 上先运行 `scripts/Start-B-HostMemory.ps1`，为资源守卫提供只读原生内存采样；它是有时限的任务进程，不是服务或系统设置。

完整源码重建还需要 [工具指纹](../../reports/B_toolchain_final.json)中的工具、原有编译器/系统依赖和生成器缓存。这里未声称在一台空白机器上离线重建了全部工具链。迁移到其它路径或版本需要重新配置绝对路径并复验。不要把包解压覆盖现有工作台；选择空目录或先保留现有工作。

原官方仓库/递归依赖的固定源归档随累积 F/E/D/C 资料保留，B 的实际覆盖源码在本运行包和 `B/` 中。课程 B1～B5 与所用 PA 原文副本在 `B/*/sources`、`B/runtime/sources/pa`；全量原文、图片、附件和外部阅读链接仍以 `/workspace/YSYX_F_B_Archive` 的独立知识库为准。B2 建设中，B5 明确是索引所链接的 v23.06 页面。

旧交付 ZIP、Git 对象和构建缓存没有嵌套进新 ZIP。旧阶段的最终停点审计应对照其原交付包；当前工作树已进入 B，不能把旧报告的“止于 C/D/E”条件当成当前阶段。
