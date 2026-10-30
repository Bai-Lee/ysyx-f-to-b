# E3：Missing Semester 2020 实作与范围

对应指定的六个主题，共 54 条冻结条目，逐条状态见 [结果](../../../reports/E3_MS_results.json)，原文见 [course_specs.json（补充包：E/E3/course_specs.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)。此处是实际实现解释，非官方答案。专用 Linux 用户 ysyx，不读取或上传用户浏览器、真实 SSH 私钥或 GitHub 账号内容。

## Shell 与脚本

真实创建 `/tmp/missing` 并用标记确认归属，写入 shebang 脚本；无执行位直接调用返回 126，chmod 后可执行。curl HEAD 获取 MIT 站点响应并保存 Last-Modified，不编造服务器日期。WSL 不提供物理电池 sysfs，因此用 Windows Win32Battery 只读查询得到一条真实电池记录，明确为平台替代。

marco 记录当前位置，polo 用带引号的 cd 回去，路径含空格时同样工作；子进程不能修改父 shell 的目录，因此用 source 加载函数。原随机脚本反复运行至真实失败，保存失败前次数和 stdout/stderr，最大 10000 次只是保护上限。`find -print0` 与 `xargs -0` 保护空格、换行和前导短横线文件名，ZIP 成员由 Python 独立核对。时间排序也保留 NUL 分隔；不要用 `for f in $(ls)` 破坏文件名边界。

## 编辑器与数据整理

Vim 使用实际二进制，保存普通/插入/可视、删除/复制/粘贴、搜索/替换/重复等命令家族的执行与断言；采用脚本和 PTY 自动化，不宣称真人做完 30 分钟 vimtutor。课程 vimrc、CtrlP 与 commentary 使用固定提交；Ctrl-P 通过真实 PTY 选中文件，XML 用 Vim 宏转换后与 ElementTree 的每个人物记录对照。宏阅读过课程提示，没有冒称全程无提示。FizzBuzz 的 1、3、5、15、30 与独立预期比较；Bash 设置 vi 编辑模式。一个月日常使用属于个人时间，不伪造。

RegexOne 下载页面，首个 abc 示例来自页面，其余正则概念用本地自编边界用例执行；没有网页登录进度。字典命令统计至少三个 a 且非 `'s` 结尾的词、尾部二字母出现频次、缺失组合，并与 Python 集合/Counter 独立复算。`sed ... file > file` 会先截空输入，故只能在自有临时文件示范；修复用 sed -i/安全临时文件。

WSL 的 PID1 是 init，journalctl 没有持久化启动日志，Windows 相应性能事件查询也没有可用记录，所以无法产生“最近十次真实启动耗时”及“最近三次启动差异”。用明确标记 synthetic 的十次/三次固定输入验收解析算法，两个条目仍标 UNAVAILABLE_HISTORY_METHOD_TESTED；合成值不进入真实系统性能结论。

下载 [UCI Iris](https://archive.ics.uci.edu/dataset/53/iris) 的真实 150 行数据，用 awk 计算每列范围及差值累计，与 Python Decimal 独立比较。来源 DOI `10.24432/C56C76`，CC BY 4.0，原数据与校验值一同导出。

## 终端、进程、配置与远程连接

实际 PTY 执行 Ctrl-Z、bg、pgrep、pkill，只针对自己创建的 sleep；另有真实 sleep 60 等待，并演示另一个 shell 的 wait 不能等待非子进程，kill -0 轮询仅反映该 PID 此刻存在/可探测。alias dc 和历史统计来自这次真实交互命令，不声称拥有一周个人历史。

tmux 使用独立 socket，创建 session/window/pane、发送命令、抓取输出、修改前缀并清理；不触碰用户现有 tmux。dotfiles 将专用账户配置先备份再链接，版本库有提交记录，重复安装幂等；另在新 Linux 账户 ysyx-dotcheck 实跑恢复。这是干净账户替代另一台虚拟机，隔离强度不同。GitHub 公开发布属于用户账号行为，未发布。

SSH 服务只监听本机回环地址 22222，使用本次生成的临时 Ed25519 密钥。实际执行 ssh-copy-id、严格 hostkey 核验、密钥登录、8888→9999 本地转发、ControlMaster 检查/退出。`-N` 不执行远端命令，`-f` 在认证后转后台。Vim 实改隔离 sshd 配置，再加载并检查 PasswordAuthentication=no、PermitRootLogin=no，密钥登录继续有效，纯密码方式被拒绝。验收后停止专用服务，未部署互联网服务器，私钥不打包。

实际 mosh server/client 经专用 UDP 中继连通，丢弃双向数据包 3 秒，恢复后看到由远端执行产生的 token。输入用十六进制编码避免终端本地回显冒充远端响应。该实验替代关闭系统网卡，证明本次连接能从指定丢包窗口恢复，不证明所有网络场景。session key 只留进程内存，日志脱敏，子进程清理。[Mosh 官方说明](https://mosh.org/)

## Git 与个人流程边界

完整拉取课程仓库历史，实际 log、blame、show；另建专用实验仓库演示文件从历史中移除，修改的是自建仓库，未改课程上游历史。stash/pop 前后文件完全一致，Git alias 与全局 ignore 只属于新建 Linux 学习账户。

文字修改生成本地 patch，未发送 PR；dotfiles 也未上传。两者不是下载失败，而是未实施账号发布行为。用户已排除本人相关流程，本阶段保留可审阅材料，不把它们标成已公开提交。

这些实作允许 AI 工程测试继续推进；不能等同于官方对真人长期使用习惯、真实多次开机记录或账号发布记录的全部字面要求均通过。
