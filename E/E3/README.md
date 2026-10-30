# E3 课程工程交付

[当前报告](../../reports/E3_REPORT.md)、[234项清单](../../reports/E3_TASKS.md)、[冻结课程要求（补充包：E/E3/course_specs.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)、[机器审计](../../reports/E3_AUDIT.json)是当前入口。F/E1/E2 保留原阶段证据；下一项为 E4。

## 文件与来源

- `lcthw/original`：32章原始代码块，源文件/提交/摘要见 course_specs.json；只在派生目录修复。
- `lcthw/solutions/continued`：本轮C实现、错误变体、构建文件和测试；0–9实现也保留在lcthw目录中。
- `lcthw/notes`：逐章解释、源码错误、指针与所有权约定、教学卡片。
- `lcthw/figures`：16组实测性能CSV、PNG、SVG。
- `ms`：实际Shell、Vim/PTY、Git、tmux、SSH、mosh、数据整理脚本与说明。
- `offline`：公开输入、配置副本、课程Git历史bundle、插件源码快照；manifest.json包含来源和SHA-256。没有SSH私钥。
- `../../artifacts/E3`：真实命令、输入、stdout/stderr、退出码、超时、PTY、core、证据快照；attempts保留诊断中的失败。

原讲义库仍在 `/workspace/YSYX_F_B_Archive`，当前工程ZIP不重复携带整个原资料库或WSL虚拟磁盘。课程实现与公开实验输入可离线审阅；运行依赖已经装好的Ubuntu工具链，包版本和工具指纹见[离线验收报告](../../reports/E3_offline_verification.json)。

## 已执行与复验

本轮所有成绩来自真实执行。当前[Run-E3.ps1](../../scripts/Run-E3.ps1)默认重新核验输入快照、源文件/日志和任务覆盖，再生成并逐成员校验ZIP；`-VerifyOffline` 额外在全新的Linux目录从本地bundle恢复并重新编译数据库、链表及构建骨架。此选项不是重复全部234项，也不会重新安装系统或改变WSL资源配置。

Linux发行版 `YSYX-Linux`，普通用户 `ysyx`，工程挂载路径 `/workspace/projects/ysyx_f_to_b`。授权预算2GiB/4vCPU/2GiB swap；源码编译最多-j2，一次一个重任务。新的编译复验在Windows可用内存不足3GiB时先停止。`Run-E3-Light.ps1`只代表旧1GB检查点，已加防误用保护。

详细批次入口按依赖顺序为：middle、middle_extra、database、functions_stack、objects、macros_scope、types、io_variadic、libraries、debugger、lists、defensive、supplement，各文件位于lcthw目录，以Linux python3执行。它们包含断言，异常即停止；原始故障例程序必须使用各脚本规定的隔离目录、资源上限和预期失败状态，不要从讲义中任意整段执行命令。Valgrind源码构建另在 `scripts/e3/build_valgrind.py`，源码包在D盘downloads。

MS的SSH配置、root服务辅助脚本和个人配置操作仅用于本次专用Linux实验用户；完整重做需按已有日志中的准备/启动/登录/重载/停止次序，不能把脚本指向用户真实服务器。当前默认复验不启动这些服务，原始实验已通过且监听端口已关闭。

输入快照分两类：执行时保存，或之后从当前/冻结源码按已记录SHA-256逐字节匹配重建。后者明确登记于[快照恢复清单](../../reports/E3_input_recovery.json)，不冒充当时捕获。原运行记录不修改；即使生成器后来覆写了派生路径，原编译输入仍可检查。

## 状态解释

PASS 是在记录范围内通过；PASS_ADAPTED 明确含平台或原例修复；PASS_DOCUMENTED 是原题要求的研究/说明，有文献与说明但不假称运行GUI；PASS_REVIEW_NO_CONFIRMED_BUG表示完成有限代码复查且未发现应提交的确定新缺陷。六项长期个人练习/公开发布/真实启动历史例外全部保留非PASS状态，不隐去。工程范围完成不等于官方闭卷考核、流片或所有字面课程条件已完成。
