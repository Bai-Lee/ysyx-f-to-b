# E3 运行依赖

实际Ubuntu安装版本；未打包整个系统。工具绝对路径和SHA-256见[E3_offline_verification.json](E3_offline_verification.json)。

| 包 | 版本 | 架构 |
|---|---|---|
| curl | 7.81.0-1ubuntu1.20 | amd64 |
| gcc | 4:11.2.0-1ubuntu1 | amd64 |
| gdb | 12.1-0ubuntu1~22.04.2 | amd64 |
| git | 1:2.34.1-1ubuntu1.12 | amd64 |
| make | 4.3-4.1build1 | amd64 |
| man-db | 2.10.2-1 | amd64 |
| manpages-dev | 5.10-1ubuntu1 | all |
| mosh | 1.3.2-2.1ubuntu1 | amd64 |
| openssh-server | 1:8.9p1-3ubuntu0.18 | amd64 |
| python3 | 3.10.6-1~22.04.1 | amd64 |
| tmux | 3.2a-4ubuntu0.2 | amd64 |
| unzip | 6.0-26ubuntu3.2 | amd64 |
| valgrind | 1:3.18.1-1ubuntu2 | amd64 |
| vim | 2:8.2.3995-1ubuntu2.23 | amd64 |
| wamerican | 2020.12.07-2 | all |
| zip | 3.0-12build2 | amd64 |

源码构建Valgrind另在 `/home/USER/tools/valgrind-3.18.1-source`，构建限制AMD64。Python编排主要使用Ubuntu Python3标准库；Windows审计/打包复用 `/workspace/YSYX_F_B_Archive/.venv/Scripts/python.exe`；绘图复用 `/workspace/.venv/Scripts/python.exe` 的matplotlib。

公开插件、课程Git完整历史、数据和配置副本的来源/固定提交/摘要见[离线清单](../E/E3/offline/manifest.json)。OS根文件系统、内核安装器和Valgrind源码原包继续保存在既有D盘downloads/tools中，原下载校验报告保留。
