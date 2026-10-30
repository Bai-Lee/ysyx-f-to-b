> 历史执行前方案：用户随后已授权并完成安装及轻量验收。当前临时1GB配置与实际状态见[E3检查点报告](E3_REPORT.md)。

# E3 Linux环境待授权方案

当前只读探测：WSL默认版本2，内核文件缺失，没有已安装的发行版。尚未更新WSL、启用系统组件、导入Linux或修改用户.wslconfig。

已下载Canonical官方Ubuntu22.04 amd64 WSL根文件系统：C:\YSYX_WORKSPACE\downloads\ysyx_e3\ubuntu-jammy-wsl-amd64-ubuntu22.04lts.rootfs.tar.gz。大小341,130,963字节；SHA-256=1483cc5c1dce13064f774834cbffdff226559fd522a67a381a8ea77d63fb4109，与同一官方站点发布的SHA256SUMS一致。原始镜像是2025-03快照，导入后要从官方apt源更新，不把旧快照当成已更新系统。

拟执行：更新缺失的WSL2内核及必要组件，将独立发行版YSYX-Linux导入/workspace/tools/wsl/YSYX-Linux。新发行版内安装课程所需编译/调试工具，继续E3。系统组件本身依Windows要求可能留在C盘，发行版及课程数据在D盘。

拟先备份并合并/home/USER/.wslconfig，只设置memory=2GB、processors=4、swap=2GB，以及D盘swapFile；其他设置保持原文。待应用文件见[配置草案](../E/E3/preflight/wslconfig.proposed)。这是全局WSL2资源上限，不是仅单个发行版设置。全局PATH、代理、Windows更新偏好不修改。

不会自动重启Windows。如果必要组件变更要求重启，将保留安装状态并请用户决定时机。开始Linux虚拟机或重编译前重新检测可用内存；低于项目3GiB门槛时不派发重任务，也不关闭用户应用。最近可用内存约2.27GiB。

需要用户授权的原因来自AGENTS.md（原完整交付引用：`/workspace/AGENTS.md`）的明确规则：“WSL/系统组件安装、重启、全局 .wslconfig 变更需用户批准。”下载及方案准备已完成，系统修改尚未执行。

官方依据：[WSL更新/导入命令](https://learn.microsoft.com/en-us/windows/wsl/basic-commands)、[全局资源配置](https://learn.microsoft.com/en-us/windows/wsl/wsl-config)、[Ubuntu WSL安装](https://ubuntu.com/wsl/docs/latest/howto/install-ubuntu-wsl2/)。
