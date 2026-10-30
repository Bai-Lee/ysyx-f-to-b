# E3：Linux、工具及 C 进阶逐题要求

本文件只定义待实施作业；这里引用的命令均是题面，未执行系统安装、用户配置迁移、SSH 授权或公开发布。

Missing Semester 主页目前展示 2026 课程，E3 明列的六个标题与 2020 目录逐一吻合，因此使用 2020 中文版；未把它标成一生一芯 v26.07 原创正文。LCTHW 使用讲义所指译者发布的同一翻译源码，固定提交 331debee3bcd69a1a79cdc99ad5f476d991acfd2；保留署名/许可，未使用题解站。

本地验收统一在隔离练习目录/临时 HOME/专用测试端点完成。原题要求修改个人全局配置、发布 GitHub、Fork/PR 或等待一个月使用习惯的部分，按用户范围明确适配；这些适配不是原课程的原文条件。系统/WSL 等变更仍遵循工作区规则。

## Missing Semester 六个主题

54 个顶层练习；每题内列出的多步/子问完整保留。命令行环境原网页把 SSH 配置代码放在列表外，本清单已把代码归回 MS-05-13。

<a id="ms-01-01"></a>

### MS-01-01 课程概览与 shell

来源：本地原文（原完整交付引用：`<../references/markdown/a54c4ef866690b51.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/course-shell/)

**实现要求**（保留原题的代码、列表及子问）：

- 本课程需要使用类 Unix shell，例如 Bash 或 ZSH。如果您在 Linux 或者 MacOS 上面完成本课程的练习，则不需要做任何特殊的操作。如果您使用的是 Windows，则您不应该使用 cmd 或是 Powershell；您可以使用 [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/) 或者是 Linux 虚拟机。使用 `echo $SHELL` 命令可以查看您的 shell 是否满足要求。如果打印结果为 `/bin/bash` 或 `/usr/bin/zsh` 则是可以的。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：实际 Linux Bash/Zsh 与 echo $SHELL 证据；本轮不因此安装系统组件

归类：E3 指定外部练习（含明确适配）。

<a id="ms-01-02"></a>

### MS-01-02 课程概览与 shell

来源：本地原文（原完整交付引用：`<../references/markdown/a54c4ef866690b51.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/course-shell/)

**实现要求**（保留原题的代码、列表及子问）：

- 在 `/tmp` 下新建一个名为 `missing` 的文件夹。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：目录存在于练习临时目录；不用占用/覆盖其他项目

归类：E3 指定外部练习（含明确适配）。

<a id="ms-01-03"></a>

### MS-01-03 课程概览与 shell

来源：本地原文（原完整交付引用：`<../references/markdown/a54c4ef866690b51.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/course-shell/)

**实现要求**（保留原题的代码、列表及子问）：

- 用 `man` 查看程序 `touch` 的使用手册。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：保存 man touch 中所用选项和说明

归类：E3 指定外部练习（含明确适配）。

<a id="ms-01-04"></a>

### MS-01-04 课程概览与 shell

来源：本地原文（原完整交付引用：`<../references/markdown/a54c4ef866690b51.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/course-shell/)

**实现要求**（保留原题的代码、列表及子问）：

- 用 `touch` 在 `missing` 文件夹中新建一个叫 `semester` 的文件。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：semester 文件创建，路径/类型正确

归类：E3 指定外部练习（含明确适配）。

<a id="ms-01-05"></a>

### MS-01-05 课程概览与 shell

来源：本地原文（原完整交付引用：`<../references/markdown/a54c4ef866690b51.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/course-shell/)

**实现要求**（保留原题的代码、列表及子问）：

- 将以下内容一行一行地写入 `semester` 文件：

  

```
 #!/bin/sh
 curl --head --silent https://missing.csail.mit.edu
```



  第一行可能有点棘手， `#` 在 Bash 中表示注释，而 `!` 即使被双引号（`"`）包裹也具有特殊的含义。
  单引号（`'`）则不一样，此处利用这一点解决输入问题。更多信息请参考 [Bash quoting 手册](https://www.gnu.org/software/bash/manual/html_node/Quoting.html)

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：两行内容逐字与原题一致，解释引号和 shebang

归类：E3 指定外部练习（含明确适配）。

<a id="ms-01-06"></a>

### MS-01-06 课程概览与 shell

来源：本地原文（原完整交付引用：`<../references/markdown/a54c4ef866690b51.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/course-shell/)

**实现要求**（保留原题的代码、列表及子问）：

- 尝试执行这个文件。例如，将该脚本的路径（`./semester`）输入到您的 shell 中并回车。如果程序无法执行，请使用 `ls` 命令来获取信息并理解其不能执行的原因。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：记录执行失败的退出码与 ls 权限并解释

归类：E3 指定外部练习（含明确适配）。

<a id="ms-01-07"></a>

### MS-01-07 课程概览与 shell

来源：本地原文（原完整交付引用：`<../references/markdown/a54c4ef866690b51.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/course-shell/)

**实现要求**（保留原题的代码、列表及子问）：

- 查看 `chmod` 的手册(例如，使用 `man chmod` 命令)

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：给出 chmod 所改位及其作用

归类：E3 指定外部练习（含明确适配）。

<a id="ms-01-08"></a>

### MS-01-08 课程概览与 shell

来源：本地原文（原完整交付引用：`<../references/markdown/a54c4ef866690b51.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/course-shell/)

**实现要求**（保留原题的代码、列表及子问）：

- 使用 `chmod` 命令改变权限，使 `./semester` 能够成功执行，不要使用 `sh semester` 来执行该程序。您的 shell 是如何知晓这个文件需要使用 `sh` 来解析呢？更多信息请参考：[shebang](https://en.wikipedia.org/wiki/Shebang_(Unix))

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：直接 ./semester 成功，解释解释器选择，不能用 sh 绕过可执行权限

归类：E3 指定外部练习（含明确适配）。

<a id="ms-01-09"></a>

### MS-01-09 课程概览与 shell

来源：本地原文（原完整交付引用：`<../references/markdown/a54c4ef866690b51.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/course-shell/)

**实现要求**（保留原题的代码、列表及子问）：

- 使用 `|` 和 `>` ，将 `semester` 文件输出的最后更改日期信息，写入主目录下的 `last-modified.txt` 的文件中

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：管道提取真实响应中的修改日期并写入隔离 HOME 的结果文件；若服务器不发 Last-Modified 如实记录并用固定响应夹具检验提取逻辑

归类：E3 指定外部练习（含明确适配）。

<a id="ms-01-10"></a>

### MS-01-10 课程概览与 shell

来源：本地原文（原完整交付引用：`<../references/markdown/a54c4ef866690b51.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/course-shell/)

**实现要求**（保留原题的代码、列表及子问）：

- 写一段命令来从 `/sys` 中获取笔记本的电量信息，或者台式机 CPU 的温度。注意：macOS 并没有 sysfs，所以 Mac 用户可以跳过这一题。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：只读 sysfs；若虚拟环境未暴露电池/温度，记录证据并用同格式夹具验证解析，不改变电源配置

归类：E3 指定外部练习（含明确适配）。

<a id="ms-02-01"></a>

### MS-02-01 Shell 工具和脚本

来源：本地原文（原完整交付引用：`<../references/markdown/0f2028201d99affb.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/shell-tools/)

**实现要求**（保留原题的代码、列表及子问）：

- 阅读 [`man ls`](https://man7.org/linux/man-pages/man1/ls.1.html) ，然后使用 `ls` 命令进行如下操作：

  - 所有文件（包括隐藏文件）
  - 文件打印以人类可以理解的格式输出 (例如，使用 454M 而不是 454279954)
  - 文件以最近修改顺序排序
  - 以彩色文本显示输出结果

  典型输出如下：

  

```
 -rw-r--r--   1 user group 1.1M Jan 14 09:53 baz
 drwxr-xr-x   5 user group  160 Jan 14 09:53 .
 -rw-r--r--   1 user group  514 Jan 14 06:42 bar
 -rw-r--r--   1 user group 106M Jan 13 12:12 foo
 drwx------+ 47 user group 1.5K Jan 12 18:08 ..
```



**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：同时显示隐藏文件、人类可读大小、时间倒序、颜色；用含隐藏/大文件的夹具检查

归类：E3 指定外部练习（含明确适配）。

<a id="ms-02-02"></a>

### MS-02-02 Shell 工具和脚本

来源：本地原文（原完整交付引用：`<../references/markdown/0f2028201d99affb.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/shell-tools/)

**实现要求**（保留原题的代码、列表及子问）：

- 编写两个 bash 函数 `marco` 和 `polo` 执行下面的操作。
  每当你执行 `marco` 时，当前的工作目录应当以某种形式保存，当执行 `polo` 时，无论现在处在什么目录下，都应当 `cd` 回到当时执行 `marco` 的目录。
  为了方便 debug，你可以把代码写在单独的文件 `marco.sh` 中，并通过 `source marco.sh` 命令，（重新）加载函数。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：多目录、含空格路径中 marco 记录后 polo 确实返回，source 后可复用

归类：E3 指定外部练习（含明确适配）。

<a id="ms-02-03"></a>

### MS-02-03 Shell 工具和脚本

来源：本地原文（原完整交付引用：`<../references/markdown/0f2028201d99affb.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/shell-tools/)

**实现要求**（保留原题的代码、列表及子问）：

- 假设您有一个命令，它很少出错。因此为了在出错时能够对其进行调试，需要花费大量的时间重现错误并捕获输出。
  编写一段 bash 脚本，运行如下的脚本直到它出错，将它的标准输出和标准错误流记录到文件，并在最后输出所有内容。
  加分项：报告脚本在失败前共运行了多少次。

  

```
 #!/usr/bin/env bash

 n=$(( RANDOM % 100 ))

 if [[ n -eq 42 ]]; then
    echo "Something went wrong"
    >&2 echo "The error was using magic numbers"
    exit 1
 fi

 echo "Everything went according to plan"
```



**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：循环在首次非零退出时停止，stdout/stderr 都保留且报告运行次数

归类：E3 指定外部练习（含明确适配）。

<a id="ms-02-04"></a>

### MS-02-04 Shell 工具和脚本

来源：本地原文（原完整交付引用：`<../references/markdown/0f2028201d99affb.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/shell-tools/)

**实现要求**（保留原题的代码、列表及子问）：

- 本节课我们讲解的 `find` 命令中的 `-exec` 参数非常强大，它可以对我们查找的文件进行操作。但是，如果我们要对所有文件进行操作呢？例如创建一个 zip 压缩文件？我们已经知道，命令行可以从参数或标准输入接受输入。在用管道连接命令时，我们将标准输出和标准输入连接起来，但是有些命令，例如 `tar` 则需要从参数接受输入。这里我们可以使用 [`xargs`](https://man7.org/linux/man-pages/man1/xargs.1.html) 命令，它可以使用标准输入中的内容作为参数。
  例如 `ls | xargs rm` 会删除当前目录中的所有文件。

  您的任务是编写一个命令，它可以递归地查找文件夹中所有的 HTML 文件，并将它们压缩成 zip 文件。注意，即使文件名中包含空格，您的命令也应该能够正确执行（提示：查看 `xargs` 的参数 `-d`，译注：MacOS 上的 `xargs` 没有 `-d`，[查看这个 issue](https://github.com/missing-semester/missing-semester/issues/93)）

  如果您使用的是 MacOS，请注意默认的 BSD `find` 与 [GNU coreutils](https://en.wikipedia.org/wiki/List_of_GNU_Core_Utilities_commands) 中的是不一样的。你可以为 `find` 添加 `-print0` 选项，并为 `xargs` 添加 `-0` 选项。作为 Mac 用户，您需要注意 mac 系统自带的命令行工具和 GNU 中对应的工具是有区别的；如果你想使用 GNU 版本的工具，也可以使用 [brew 来安装](https://formulae.brew.sh/formula/coreutils)。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：递归 HTML 筛选及 ZIP 内容完整，文件名含空格/换行的参数传递正确；不执行原文删除文件的示例

归类：E3 指定外部练习（含明确适配）。

<a id="ms-02-05"></a>

### MS-02-05 Shell 工具和脚本

来源：本地原文（原完整交付引用：`<../references/markdown/0f2028201d99affb.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/shell-tools/)

**实现要求**（保留原题的代码、列表及子问）：

- （进阶）编写一个命令或脚本递归的查找文件夹中最近修改的文件。更通用的做法，你可以按照最近的修改时间列出文件吗？

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：按修改时间排序，包含空目录/同时间/含空格路径的测试

归类：E3 指定外部练习（含明确适配）。

<a id="ms-03-01"></a>

### MS-03-01 编辑器 (Vim)

来源：本地原文（原完整交付引用：`<../references/markdown/1b9405df5e13d228.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/editors/)

**实现要求**（保留原题的代码、列表及子问）：

- 完成 `vimtutor`。备注：它在一个
  [80x24](https://en.wikipedia.org/wiki/VT100)（80 列，24 行）
  终端窗口看起来效果最好。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：vimtutor 所有练习有操作记录，不只打开文件

归类：E3 指定外部练习（含明确适配）。

<a id="ms-03-02"></a>

### MS-03-02 编辑器 (Vim)

来源：本地原文（原完整交付引用：`<../references/markdown/1b9405df5e13d228.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/editors/)

**实现要求**（保留原题的代码、列表及子问）：

- 下载我们提供的 [vimrc](https://missing-semester-cn.github.io/2020/files/vimrc)，然后把它保存到 `~/.vimrc`。 通读这个注释详细的文件
  （用 Vim!）， 然后观察 Vim 在这个新的设置下看起来和使用起来有哪些细微的区别。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：在隔离 HOME 或 Vim -u 测试配置，解释各设置变化，不覆盖用户现有 vimrc

归类：E3 指定外部练习（含明确适配）。

<a id="ms-03-03"></a>

### MS-03-03 编辑器 (Vim)

来源：本地原文（原完整交付引用：`<../references/markdown/1b9405df5e13d228.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/editors/)

**实现要求**（保留原题的代码、列表及子问）：

- 安装和配置一个插件：
  [ctrlp.vim](https://github.com/ctrlpvim/ctrlp.vim).
  1. 用 `mkdir -p ~/.vim/pack/vendor/start` 创建插件文件夹
  2. 下载这个插件： `cd ~/.vim/pack/vendor/start; git clone https://github.com/ctrlpvim/ctrlp.vim`
  3. 阅读这个插件的
     [文档](https://github.com/ctrlpvim/ctrlp.vim/blob/master/readme.md)。
     尝试用 CtrlP 来在一个工程文件夹里定位一个文件，打开 Vim, 然后用 Vim 命令控制行开始
     `:CtrlP`.
  4. 自定义 CtrlP：添加
     [configuration](https://github.com/ctrlpvim/ctrlp.vim/blob/master/readme.md#basic-options)
     到你的 `~/.vimrc` 来用按 Ctrl-P 打开 CtrlP

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：插件可定位文件，文档/自定配置/快捷键四个步骤有结果；安装在实验配置目录

归类：E3 指定外部练习（含明确适配）。

<a id="ms-03-04"></a>

### MS-03-04 编辑器 (Vim)

来源：本地原文（原完整交付引用：`<../references/markdown/1b9405df5e13d228.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/editors/)

**实现要求**（保留原题的代码、列表及子问）：

- 练习使用 Vim, 在你自己的机器上重做 [演示](#demo)。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：原文 demo 的编辑操作可用录制或前后文本核对

归类：E3 指定外部练习（含明确适配）。

<a id="ms-03-05"></a>

### MS-03-05 编辑器 (Vim)

来源：本地原文（原完整交付引用：`<../references/markdown/1b9405df5e13d228.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/editors/)

**实现要求**（保留原题的代码、列表及子问）：

- 下个月用 Vim 完成 *所有的* 文件编辑。每当不够高效的时候，或者你感觉 “一定有一个更好的方式”时，
  尝试求助搜索引擎，很有可能有一个更好的方式。如果你遇到难题，可以来我们的答疑时间或者给我们发邮件。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：原文一个月使用属于个人习惯训练；适配为 Vim 编辑操作演练，不把等待一个月列为工程阻塞

归类：E3 指定外部练习（含明确适配）。

<a id="ms-03-06"></a>

### MS-03-06 编辑器 (Vim)

来源：本地原文（原完整交付引用：`<../references/markdown/1b9405df5e13d228.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/editors/)

**实现要求**（保留原题的代码、列表及子问）：

- 在其他工具中设置 Vim 快捷键 （见上面的操作指南）。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：在隔离工具配置中演示 Vim 键位，不改用户当前工具偏好

归类：E3 指定外部练习（含明确适配）。

<a id="ms-03-07"></a>

### MS-03-07 编辑器 (Vim)

来源：本地原文（原完整交付引用：`<../references/markdown/1b9405df5e13d228.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/editors/)

**实现要求**（保留原题的代码、列表及子问）：

- 进一步自定义你的 `~/.vimrc` 和安装更多插件。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：记录新增设置/插件的效果和来源，配置可复现

归类：E3 指定外部练习（含明确适配）。

<a id="ms-03-08"></a>

### MS-03-08 编辑器 (Vim)

来源：本地原文（原完整交付引用：`<../references/markdown/1b9405df5e13d228.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/editors/)

**实现要求**（保留原题的代码、列表及子问）：

- （高阶）用 Vim 宏将 XML 转换到 JSON ([例子文件](https://missing-semester-cn.github.io/2020/files/example-data.xml))。
  尝试着先完全自己做，但是在你卡住的时候可以查看上面 [宏](#macros) 章节。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：宏把原 XML 例子变成等价且可解析 JSON，所有记录/转义正确

归类：E3 指定外部练习（含明确适配）。

<a id="ms-04-01"></a>

### MS-04-01 数据整理

来源：本地原文（原完整交付引用：`<../references/markdown/646dc88b3ca704da.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/data-wrangling/)

**实现要求**（保留原题的代码、列表及子问）：

- 学习一下这篇简短的 [交互式正则表达式教程](https://regexone.com/).

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：正则练习覆盖匹配/字符组/重复/捕获等题目；可本地复现题面样例，在线成绩非必要

归类：E3 指定外部练习（含明确适配）。

<a id="ms-04-02"></a>

### MS-04-02 数据整理

来源：本地原文（原完整交付引用：`<../references/markdown/646dc88b3ca704da.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/data-wrangling/)

**实现要求**（保留原题的代码、列表及子问）：

- 统计 words 文件 (`/usr/share/dict/words`) 中包含至少三个 `a` 且不以 `'s` 结尾的单词个数。这些单词中，出现频率前三的末尾两个字母是什么？ `sed` 的 `y` 命令，或者 `tr` 程序也许可以帮你解决大小写的问题。共存在多少种词尾两字母组合？还有一个很 有挑战性的问题：哪个组合从未出现过？

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：以锁定 words 文件核算所有子问，大小写归一和词尾排除条件正确

归类：E3 指定外部练习（含明确适配）。

<a id="ms-04-03"></a>

### MS-04-03 数据整理

来源：本地原文（原完整交付引用：`<../references/markdown/646dc88b3ca704da.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/data-wrangling/)

**实现要求**（保留原题的代码、列表及子问）：

- 进行原地替换听上去很有诱惑力，例如：
  `sed s/REGEX/SUBSTITUTION/ input.txt > input.txt`。但是这并不是一个明智的做法，为什么呢？还是说只有 `sed` 是这样的? 查看 `man sed` 来完成这个问题

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：用可丢弃副本说明重定向先截断的问题；保留原输入，不在资料原件试验

归类：E3 指定外部练习（含明确适配）。

<a id="ms-04-04"></a>

### MS-04-04 数据整理

来源：本地原文（原完整交付引用：`<../references/markdown/646dc88b3ca704da.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/data-wrangling/)

**实现要求**（保留原题的代码、列表及子问）：

- 找出您最近十次开机的开机时间平均数、中位数和最长时间。在 Linux 上需要用到 `journalctl` ，而在 macOS 上使用 `log show`。找到每次起到开始和结束时的时间戳。在 Linux 上类似这样操作：

  

```
Logs begin at ...
```



  和

  

```
systemd[577]: Startup finished in ...
```



  在 macOS 上, [查找](https://eclecticlight.co/2018/03/21/macos-unified-log-3-finding-your-way/):

  

```
=== system boot:
```



  和

  

```
Previous shutdown cause: 5
```



**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：十次启动时间抽取、均值/中位数/最大值可复算；历史不足用明确标记的日志夹具补技术练习

归类：E3 指定外部练习（含明确适配）。

<a id="ms-04-05"></a>

### MS-04-05 数据整理

来源：本地原文（原完整交付引用：`<../references/markdown/646dc88b3ca704da.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/data-wrangling/)

**实现要求**（保留原题的代码、列表及子问）：

- 查看之前三次重启启动信息中不同的部分(参见 `journalctl` 的 `-b` 选项)。将这一任务分为几个步骤，首先获取之前三次启动的启动日志，也许获取启动日志的命令就有合适的选项可以帮助您提取前三次启动的日志，亦或者您可以使用 `sed '0,/STRING/d'` 来删除 `STRING` 匹配到的字符串前面的全部内容。然后，过滤掉每次都不相同的部分，例如时间戳。下一步，重复记录输入行并对其计数(可以使用 `uniq` )。最后，删除所有出现过 3 次的内容（因为这些内容是三次启动日志中的重复部分）。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：三次启动日志归一/去共有项的结果正确，原始日志保留；数据不足不编造本机历史

归类：E3 指定外部练习（含明确适配）。

<a id="ms-04-06"></a>

### MS-04-06 数据整理

来源：本地原文（原完整交付引用：`<../references/markdown/646dc88b3ca704da.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/data-wrangling/)

**实现要求**（保留原题的代码、列表及子问）：

- 在网上找一个类似 [这个](https://stats.wikimedia.org/EN/TablesWikipediaZZ.htm) 或者 [这个](https://ucr.fbi.gov/crime-in-the-u.s/2016/crime-in-the-u.s.-2016/topic-pages/tables/table-1) 的数据集。或者从 [这里](https://www.springboard.com/blog/free-public-data-sets-data-science-project/) 找一些。使用 `curl` 获取数据集并提取其中两列数据，如果您想要获取的是 HTML 数据，那么 [`pup`](https://github.com/EricChiang/pup) 可能会更有帮助。对于 JSON 类型的数据，可以试试 [`jq`](https://stedolan.github.io/jq/)。请使用一条指令来找出其中一列的最大值和最小值，用另外一条指令计算两列之间差的总和。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：下载一个合法公开数据集，固定来源/哈希，提取两列并计算所选统计/图；不是只打印网页

归类：E3 指定外部练习（含明确适配）。

<a id="ms-05-01"></a>

### MS-05-01 命令行环境 / 任务控制

来源：本地原文（原完整交付引用：`<../references/markdown/9dc7805f098cb580.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/command-line/)

**实现要求**（保留原题的代码、列表及子问）：

- 我们可以使用类似 `ps aux | grep` 这样的命令来获取任务的 pid ，然后您可以基于 pid 来结束这些进程。但我们其实有更好的方法来做这件事。在终端中执行 `sleep 10000` 这个任务。然后用 `Ctrl-Z` 将其切换到后台并使用 `bg` 来继续运行它。现在，使用 [`pgrep`](https://www.man7.org/linux/man-pages/man1/pgrep.1.html) 来查找 pid 并使用 [`pkill`](https://www.man7.org/linux/man-pages/man1/pgrep.1.html) 结束进程而不需要手动输入 pid。(提示：: 使用 `-af` 标记)。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：只管理自己启动的 sleep 进程；Ctrl-Z/bg/pgrep/pkill 状态与退出证据齐全

归类：E3 指定外部练习（含明确适配）。

<a id="ms-05-02"></a>

### MS-05-02 命令行环境 / 任务控制

来源：本地原文（原完整交付引用：`<../references/markdown/9dc7805f098cb580.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/command-line/)

**实现要求**（保留原题的代码、列表及子问）：

- 如果您希望某个进程结束后再开始另外一个进程， 应该如何实现呢？在这个练习中，我们使用 `sleep 60 &` 作为先执行的程序。一种方法是使用 [`wait`](http://man7.org/linux/man-pages/man1/wait.1p.html) 命令。尝试启动这个休眠命令，然后待其结束后再执行 `ls` 命令。

  但是，如果我们在不同的 bash 会话中进行操作，则上述方法就不起作用了。因为 `wait` 只能对子进程起作用。之前我们没有提过的一个特性是，`kill` 命令成功退出时其状态码为 0 ，其他状态则是非 0。`kill -0` 则不会发送信号，但是会在进程不存在时返回一个不为 0 的状态码。请编写一个 bash 函数 `pidwait` ，它接受一个 pid 作为输入参数，然后一直等待直到该进程结束。您需要使用 `sleep` 来避免浪费 CPU 性能。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：wait 的子进程限制和 pidwait 的跨会话等待均验证，轮询含 sleep

归类：E3 指定外部练习（含明确适配）。

<a id="ms-05-03"></a>

### MS-05-03 命令行环境 / 终端多路复用

来源：本地原文（原完整交付引用：`<../references/markdown/9dc7805f098cb580.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/command-line/)

**实现要求**（保留原题的代码、列表及子问）：

- 请完成这个 `tmux` [教程](https://www.hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/) 参考 [这些步骤](https://www.hamvocke.com/blog/a-guide-to-customizing-your-tmux-conf/) 来学习如何自定义 `tmux`。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：tmux 会话/窗口/分屏/恢复和自定配置能演示，配置隔离

归类：E3 指定外部练习（含明确适配）。

<a id="ms-05-04"></a>

### MS-05-04 命令行环境 / 别名

来源：本地原文（原完整交付引用：`<../references/markdown/9dc7805f098cb580.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/command-line/)

**实现要求**（保留原题的代码、列表及子问）：

- 创建一个 `dc` 别名，它的功能是当我们错误的将 `cd` 输入为 `dc` 时也能正确执行。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：临时 shell 中 dc 的行为与 cd 一致

归类：E3 指定外部练习（含明确适配）。

<a id="ms-05-05"></a>

### MS-05-05 命令行环境 / 别名

来源：本地原文（原完整交付引用：`<../references/markdown/9dc7805f098cb580.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/command-line/)

**实现要求**（保留原题的代码、列表及子问）：

- 执行 `history | awk '{$1="";print substr($0,2)}' | sort | uniq -c | sort -n | tail -n 10` 来获取您最常用的十条命令，尝试为它们创建别名。注意：这个命令只在 Bash 中生效，如果您使用 ZSH，使用 `history 1` 替换 `history`。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：使用练习会话历史统计十条高频命令并创建有效别名，不导出用户敏感历史

归类：E3 指定外部练习（含明确适配）。

<a id="ms-05-06"></a>

### MS-05-06 命令行环境 / 配置文件

来源：本地原文（原完整交付引用：`<../references/markdown/9dc7805f098cb580.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/command-line/)

**实现要求**（保留原题的代码、列表及子问）：

- 为您的配置文件新建一个文件夹，并设置好版本控制

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：实验 dotfiles 目录是独立 Git 仓库，提交可回溯

归类：E3 指定外部练习（含明确适配）。

<a id="ms-05-07"></a>

### MS-05-07 命令行环境 / 配置文件

来源：本地原文（原完整交付引用：`<../references/markdown/9dc7805f098cb580.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/command-line/)

**实现要求**（保留原题的代码、列表及子问）：

- 在其中添加至少一个配置文件，比如说您的 shell，在其中包含一些自定义设置（可以从设置 `$PS1` 开始）。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：至少一份实验配置含自定设置且可实际加载

归类：E3 指定外部练习（含明确适配）。

<a id="ms-05-08"></a>

### MS-05-08 命令行环境 / 配置文件

来源：本地原文（原完整交付引用：`<../references/markdown/9dc7805f098cb580.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/command-line/)

**实现要求**（保留原题的代码、列表及子问）：

- 建立一种在新设备进行快速安装配置的方法（无需手动操作）。最简单的方法是写一个 shell 脚本对每个文件使用 `ln -s`，也可以使用 [专用工具](https://dotfiles.github.io/utilities/)

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：安装脚本在临时 HOME 建链接，可重复运行且处理已有文件不破坏内容

归类：E3 指定外部练习（含明确适配）。

<a id="ms-05-09"></a>

### MS-05-09 命令行环境 / 配置文件

来源：本地原文（原完整交付引用：`<../references/markdown/9dc7805f098cb580.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/command-line/)

**实现要求**（保留原题的代码、列表及子问）：

- 在新的虚拟机上测试该安装脚本。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：在隔离 Linux 测试用户/目录或可用虚拟机验证脚本，不擅自新装系统组件

归类：E3 指定外部练习（含明确适配）。

<a id="ms-05-10"></a>

### MS-05-10 命令行环境 / 配置文件

来源：本地原文（原完整交付引用：`<../references/markdown/9dc7805f098cb580.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/command-line/)

**实现要求**（保留原题的代码、列表及子问）：

- 将您现有的所有配置文件移动到项目仓库里。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：只复制/链接实验配置，保留原件；不迁移用户所有真实配置

归类：E3 指定外部练习（含明确适配）。

<a id="ms-05-11"></a>

### MS-05-11 命令行环境 / 配置文件

来源：本地原文（原完整交付引用：`<../references/markdown/9dc7805f098cb580.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/command-line/)

**实现要求**（保留原题的代码、列表及子问）：

- 将项目发布到 GitHub。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：个人 GitHub 发布按用户范围排除；本地仓库/提交验证发布前内容即可，不执行公网发布

归类：E3 指定外部练习（含明确适配）。

<a id="ms-05-12"></a>

### MS-05-12 命令行环境 / 远端设备

来源：本地原文（原完整交付引用：`<../references/markdown/9dc7805f098cb580.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/command-line/)

**实现要求**（保留原题的代码、列表及子问）：

- 前往 `~/.ssh/` 并查看是否已经存在 SSH 密钥对。如果不存在，请使用 `ssh-keygen -o -a 100 -t ed25519` 来创建一个。建议为密钥设置密码然后使用 `ssh-agent`，更多信息可以参考 [这里](https://www.ssh.com/ssh/agent)；

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：只在隔离实验 HOME 使用专用测试密钥；不读取/输出个人私钥

归类：E3 指定外部练习（含明确适配）。

<a id="ms-05-13"></a>

### MS-05-13 命令行环境 / 远端设备

来源：本地原文（原完整交付引用：`<../references/markdown/9dc7805f098cb580.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/command-line/)

**实现要求**（保留原题的代码、列表及子问）：

- 在 `.ssh/config` 加入下面内容：



```
Host vm
    User username_goes_here
    HostName ip_goes_here
    IdentityFile ~/.ssh/id_ed25519
    LocalForward 9999 localhost:8888
```



**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：在实验配置填测试用户名/地址/专用密钥，LocalForward 9999→8888 与实际连接一致

归类：E3 指定外部练习（含明确适配）。

<a id="ms-05-14"></a>

### MS-05-14 命令行环境 / 远端设备

来源：本地原文（原完整交付引用：`<../references/markdown/9dc7805f098cb580.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/command-line/)

**实现要求**（保留原题的代码、列表及子问）：

- 使用 `ssh-copy-id vm` 将您的 ssh 密钥拷贝到服务器。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：仅对自有测试 SSH 端点配置测试公钥；不改用户实际服务器授权

归类：E3 指定外部练习（含明确适配）。

<a id="ms-05-15"></a>

### MS-05-15 命令行环境 / 远端设备

来源：本地原文（原完整交付引用：`<../references/markdown/9dc7805f098cb580.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/command-line/)

**实现要求**（保留原题的代码、列表及子问）：

- 使用 `python -m http.server 8888` 在您的虚拟机中启动一个 Web 服务器并通过本机的 `http://localhost:9999` 访问虚拟机上的 Web 服务器

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：8888 测试 HTTP 服务经 9999 转发访问，能核对响应来源

归类：E3 指定外部练习（含明确适配）。

<a id="ms-05-16"></a>

### MS-05-16 命令行环境 / 远端设备

来源：本地原文（原完整交付引用：`<../references/markdown/9dc7805f098cb580.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/command-line/)

**实现要求**（保留原题的代码、列表及子问）：

- 使用 `sudo vim /etc/ssh/sshd_config` 编辑 SSH 服务器配置，通过修改 `PasswordAuthentication` 的值来禁用密码验证。通过修改 `PermitRootLogin` 的值来禁用 root 登录。然后使用 `sudo service sshd restart` 重启 `ssh` 服务器，然后重新尝试。

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：仅在隔离测试 SSH 服务中验证关闭密码/root 登录，不修改宿主或用户真实 SSH 服务；当前为待实施

归类：E3 指定外部练习（含明确适配）。

<a id="ms-05-17"></a>

### MS-05-17 命令行环境 / 远端设备

来源：本地原文（原完整交付引用：`<../references/markdown/9dc7805f098cb580.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/command-line/)

**实现要求**（保留原题的代码、列表及子问）：

- (附加题) 在虚拟机中安装 [`mosh`](https://mosh.org/) 并启动连接。然后断开服务器/虚拟机的网络适配器。mosh 可以恢复连接吗？

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：附加题：隔离测试连接中断/恢复，记录 mosh 实际行为，无网络适配器全局改动

归类：E3 指定外部练习（含明确适配）。

<a id="ms-05-18"></a>

### MS-05-18 命令行环境 / 远端设备

来源：本地原文（原完整交付引用：`<../references/markdown/9dc7805f098cb580.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/command-line/)

**实现要求**（保留原题的代码、列表及子问）：

- (附加题) 查看 `ssh` 的 `-N` 和 `-f` 选项的作用，找出在后台进行端口转发的命令是什么？

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：附加题：解释并在测试端点验证 -N/-f 及后台转发，结束自建进程

归类：E3 指定外部练习（含明确适配）。

<a id="ms-06-01"></a>

### MS-06-01 版本控制(Git)

来源：本地原文（原完整交付引用：`<../references/markdown/9e05a05994e7d0b7.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/version-control/)

**实现要求**（保留原题的代码、列表及子问）：

- 如果您之前从来没有用过 Git，推荐您阅读 [Pro Git](https://git-scm.com/book/en/v2) 的前几章，或者完成像 [Learn Git Branching](https://learngitbranching.js.org/) 这样的教程。重点关注 Git 命令和数据模型相关内容；

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：Git 对象/分支/工作区/暂存区关系能用实验仓库命令说明

归类：E3 指定外部练习（含明确适配）。

<a id="ms-06-02"></a>

### MS-06-02 版本控制(Git)

来源：本地原文（原完整交付引用：`<../references/markdown/9e05a05994e7d0b7.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/version-control/)

**实现要求**（保留原题的代码、列表及子问）：

- 克隆 [本课程网站的仓库](https://github.com/missing-semester-cn/missing-semester-cn.github.io.git)
  1. 将版本历史可视化并进行探索
  2. 是谁最后修改了 `README.md` 文件？（提示：使用 `git log` 命令并添加合适的参数）
  3. 最后一次修改 `_config.yml` 文件中 `collections:` 行时的提交信息是什么？（提示：使用 `git blame` 和 `git show`）

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：仓库历史图、README 最后修改者、collections 行提交信息三个子问逐项有命令证据

归类：E3 指定外部练习（含明确适配）。

<a id="ms-06-03"></a>

### MS-06-03 版本控制(Git)

来源：本地原文（原完整交付引用：`<../references/markdown/9e05a05994e7d0b7.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/version-control/)

**实现要求**（保留原题的代码、列表及子问）：

- 使用 Git 时的一个常见错误是提交本不应该由 Git 管理的大文件，或是将含有敏感信息的文件提交给 Git 。尝试向仓库中添加一个文件并添加提交信息，然后将其从历史中删除 ( [这篇文章也许会有帮助](https://help.github.com/articles/removing-sensitive-data-from-a-repository/))；

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：在可丢弃实验仓库用虚构非敏感文件演示历史清理，不重写用户仓库历史

归类：E3 指定外部练习（含明确适配）。

<a id="ms-06-04"></a>

### MS-06-04 版本控制(Git)

来源：本地原文（原完整交付引用：`<../references/markdown/9e05a05994e7d0b7.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/version-control/)

**实现要求**（保留原题的代码、列表及子问）：

- 从 GitHub 上克隆某个仓库，修改一些文件。当您使用 `git stash` 会发生什么？当您执行 `git log --all --oneline` 时会显示什么？通过 `git stash pop` 命令来撤销 `git stash` 操作，什么时候会用到这一技巧？

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：stash/log --all/stash pop 的对象与工作区状态符合预期，演示冲突处理

归类：E3 指定外部练习（含明确适配）。

<a id="ms-06-05"></a>

### MS-06-05 版本控制(Git)

来源：本地原文（原完整交付引用：`<../references/markdown/9e05a05994e7d0b7.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/version-control/)

**实现要求**（保留原题的代码、列表及子问）：

- 与其他的命令行工具一样，Git 也提供了一个名为 `~/.gitconfig` 配置文件 (或 dotfile)。请在 `~/.gitconfig` 中创建一个别名，使您在运行 `git graph` 时，您可以得到 `git log --all --graph --decorate --oneline` 的输出结果；

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：仓库局部配置或隔离 HOME 的 graph 别名输出对应 graph 命令

归类：E3 指定外部练习（含明确适配）。

<a id="ms-06-06"></a>

### MS-06-06 版本控制(Git)

来源：本地原文（原完整交付引用：`<../references/markdown/9e05a05994e7d0b7.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/version-control/)

**实现要求**（保留原题的代码、列表及子问）：

- 您可以通过执行 `git config --global core.excludesfile ~/.gitignore_global` 来设置全局忽略文件的位置，这会告诉 Git 使用该文件，但您仍需要手动在该路径创建 `~/.gitignore_global` 文件。配置您的全局 gitignore 文件来自动忽略系统或编辑器的临时文件，例如 `.DS_Store`；

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：仅设置隔离 HOME 的忽略规则，临时文件被忽略且正常源码仍被追踪，不改用户全局 Git 配置

归类：E3 指定外部练习（含明确适配）。

<a id="ms-06-07"></a>

### MS-06-07 版本控制(Git)

来源：本地原文（原完整交付引用：`<../references/markdown/9e05a05994e7d0b7.md>`） · [Missing Semester 2020 Chinese translation; selected by exact six E3 titles 在线原文](https://missing-semester-cn.github.io/2020/version-control/)

**实现要求**（保留原题的代码、列表及子问）：

- Fork [本课程网站的仓库](https://github.com/missing-semester-cn/missing-semester-cn.github.io.git)，找找有没有错别字或其他可以改进的地方，在 GitHub 上发起拉取请求（Pull Request)；

**交付物**：脚本/练习文件/必要配置副本、操作记录、输入与输出、返回码；不保存个人私钥或无关历史。

**验收条件**（自验）：Fork/PR 是公开协作练习但涉及个人账号和外部写入，本轮范围排除；保留本地修改与 patch，不发布 PR

归类：E3 指定外部练习（含明确适配）。

## LCTHW 指定 32 章

每章原例和理解任务列 BASE；“如何使它崩溃”列 BREAK；每条附加题列 Xnn。共 180 条，它们从属于 E3-M004，不是额外增加 180 个课程节点。破坏例子应保留失败和修复的对照；故意 UB 的结果不要求跨编译器恒定。

<a id="lct-00-base"></a>

### LCT-00-BASE 练习0：准备

来源：本地原文（原完整交付引用：`<../references/markdown/5f37f2a6b92e28e7.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex0.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习0：准备”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：编译器/Make/编辑器/调试器路径和版本可用，运行最小 C 例证实环境；复用已有工具

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-01-base"></a>

### LCT-01-BASE 练习1：启用编译器

来源：本地原文（原完整交付引用：`<../references/markdown/a747a105cc16c790.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex1.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习1：启用编译器”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：源码可编译执行，警告开关实际生效，返回码和文本正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-01-break"></a>

### LCT-01-BREAK 如何使它崩溃

来源：本地原文（原完整交付引用：`<../references/markdown/a747a105cc16c790.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex1.md)

**实现要求**（保留原题的代码、列表及子问）：

在这本书中我会添加一个小节，关于如何使程序崩溃。我会让你对程序做一些奇怪的事情，以奇怪的方式运行，或者修改代码，以便让你看到崩溃和编译器错误。

对于这个程序，打开所有编译警告重新构建它：



```
$ rm ex1
$ CFLAGS="-Wall" make ex1
cc -Wall    ex1.c   -o ex1
ex1.c: In function 'main':
ex1.c:3: warning: implicit declaration of function 'puts'
$ ./ex1
Hello world.
$
```



现在你会得到一个警告，说`puts`函数是隐式声明的。C语言的编译器很智能，它能够理解你想要什么。但是如果可以的话，你应该去除所有编译器警告。把下面一行添加到`ex1.c`文件的最上面，之后重新编译来去除它：



```
#include <stdio.h>
```



现在像刚才一样重新执行make命令，你会看到所有警告都消失了。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：在可丢弃练习副本复现所列破坏行为，保存诊断/退出码，解释原因并提交修复版；不把故意 UB 的随机表现作为唯一预期。章级交叉检查：源码可编译执行，警告开关实际生效，返回码和文本正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-01-x01"></a>

### LCT-01-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/a747a105cc16c790.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex1.md)

**实现要求**（保留原题的代码、列表及子问）：

- 在你的文本编辑器中打开`ex1`文件，随机修改或删除一部分，之后运行它看看发生了什么。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：源码可编译执行，警告开关实际生效，返回码和文本正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-01-x02"></a>

### LCT-01-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/a747a105cc16c790.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex1.md)

**实现要求**（保留原题的代码、列表及子问）：

- 再多打印5行文本或者其它比`"Hello world."`更复杂的东西。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：源码可编译执行，警告开关实际生效，返回码和文本正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-01-x03"></a>

### LCT-01-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/a747a105cc16c790.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex1.md)

**实现要求**（保留原题的代码、列表及子问）：

- 执行`man 3 puts`来阅读这个函数和其它函数的文档。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：源码可编译执行，警告开关实际生效，返回码和文本正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-02-base"></a>

### LCT-02-BASE 练习2：用Make来代替Python

来源：本地原文（原完整交付引用：`<../references/markdown/2b37c45be674cd46.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex2.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习2：用Make来代替Python”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：make 隐式规则/CFLAGS/clean 生效，故意语法错误能使构建失败

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-02-break"></a>

### LCT-02-BREAK 如何使它崩溃

来源：本地原文（原完整交付引用：`<../references/markdown/2b37c45be674cd46.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex2.md)

**实现要求**（保留原题的代码、列表及子问）：

上面那些已经足够让你起步了，但是让我们以一种特定的方式来破坏make文件，以便你可以看到发生了什么。找到`rm -f ex1`的那一行并去掉缩进（让它左移），之后你可以看到发生了什么。再次运行`make clean`，你就会得到下面的信息：



```
$ make clean
Makefile:4: *** missing separator.  Stop.
```



永远记住要缩进，以及如果你得到了像这种奇奇怪怪的错误，应该复查你是否都使用了 TAB 字符，由于一些make的变种十分挑剔。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：在可丢弃练习副本复现所列破坏行为，保存诊断/退出码，解释原因并提交修复版；不把故意 UB 的随机表现作为唯一预期。章级交叉检查：make 隐式规则/CFLAGS/clean 生效，故意语法错误能使构建失败

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-02-x01"></a>

### LCT-02-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/2b37c45be674cd46.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex2.md)

**实现要求**（保留原题的代码、列表及子问）：

- 创建目标`all:ex1`，可以以单个命令`make`构建`ex1`。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：make 隐式规则/CFLAGS/clean 生效，故意语法错误能使构建失败

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-02-x02"></a>

### LCT-02-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/2b37c45be674cd46.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex2.md)

**实现要求**（保留原题的代码、列表及子问）：

- 阅读`man make`来了解关于如何执行它的更多信息。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：make 隐式规则/CFLAGS/clean 生效，故意语法错误能使构建失败

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-02-x03"></a>

### LCT-02-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/2b37c45be674cd46.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex2.md)

**实现要求**（保留原题的代码、列表及子问）：

- 阅读`man cc`来了解关于`-Wall`和`-g`行为的更多信息。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：make 隐式规则/CFLAGS/clean 生效，故意语法错误能使构建失败

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-02-x04"></a>

### LCT-02-X04 附加题 / 4

来源：本地原文（原完整交付引用：`<../references/markdown/2b37c45be674cd46.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex2.md)

**实现要求**（保留原题的代码、列表及子问）：

- 在互联网上搜索Makefile文件，看看你是否能改进你的文件。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：make 隐式规则/CFLAGS/clean 生效，故意语法错误能使构建失败

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-02-x05"></a>

### LCT-02-X05 附加题 / 5

来源：本地原文（原完整交付引用：`<../references/markdown/2b37c45be674cd46.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex2.md)

**实现要求**（保留原题的代码、列表及子问）：

- 在另一个C语言项目中找到`Makefile`文件，并且尝试理解它做了什么。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：make 隐式规则/CFLAGS/clean 生效，故意语法错误能使构建失败

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-03-base"></a>

### LCT-03-BASE 练习3：格式化输出

来源：本地原文（原完整交付引用：`<../references/markdown/da2647729188776b.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex3.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习3：格式化输出”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：格式化类型与参数匹配，逐字段输出符合原例，编译警告不被吞掉

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-03-break"></a>

### LCT-03-BREAK 如何使它崩溃

来源：本地原文（原完整交付引用：`<../references/markdown/da2647729188776b.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex3.md)

**实现要求**（保留原题的代码、列表及子问）：

尝试下面的一些东西来使你的程序崩溃，在你的电脑上它们可能会崩溃，也可能不会。

- 从第一个`printf`中去掉`age`并重新编译，你应该会得到一大串的警告。
- 运行新的程序，它会崩溃，或者打印出奇怪的年龄。
- 将`printf`恢复原样，并且去掉`age`的初值，将那一行改为`int age;`，之后重新构建并运行。



```
# edit ex3.c to break printf
$ make ex3
cc -Wall -g    ex3.c   -o ex3
ex3.c: In function 'main':
ex3.c:8: warning: too few arguments for format
ex3.c:5: warning: unused variable 'age'
$ ./ex3
I am -919092456 years old.
I am 72 inches tall.
# edit ex3.c again to fix printf, but don't init age
$ make ex3
cc -Wall -g    ex3.c   -o ex3
ex3.c: In function 'main':
ex3.c:8: warning: 'age' is used uninitialized in this function
$ ./ex3
I am 0 years old.
I am 72 inches tall.
$
```



**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：在可丢弃练习副本复现所列破坏行为，保存诊断/退出码，解释原因并提交修复版；不把故意 UB 的随机表现作为唯一预期。章级交叉检查：格式化类型与参数匹配，逐字段输出符合原例，编译警告不被吞掉

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-03-x01"></a>

### LCT-03-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/da2647729188776b.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex3.md)

**实现要求**（保留原题的代码、列表及子问）：

- 找到尽可能多的方法使`ex3`崩溃。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：格式化类型与参数匹配，逐字段输出符合原例，编译警告不被吞掉

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-03-x02"></a>

### LCT-03-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/da2647729188776b.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex3.md)

**实现要求**（保留原题的代码、列表及子问）：

- 执行`man 3 printf`来阅读其它可用的'%'格式化占位符。如果你在其它语言中使用过它们，应该看着非常熟悉（它们来源于`printf`）。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：格式化类型与参数匹配，逐字段输出符合原例，编译警告不被吞掉

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-03-x03"></a>

### LCT-03-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/da2647729188776b.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex3.md)

**实现要求**（保留原题的代码、列表及子问）：

- 将`ex3`添加到你的`Makefile`的`all`列表中。到目前为止，可以使用`make clean all`来构建你所有的练习。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：格式化类型与参数匹配，逐字段输出符合原例，编译警告不被吞掉

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-03-x04"></a>

### LCT-03-X04 附加题 / 4

来源：本地原文（原完整交付引用：`<../references/markdown/da2647729188776b.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex3.md)

**实现要求**（保留原题的代码、列表及子问）：

- 将`ex3`添加到你的`Makefile`的`clean`列表中。当你需要的时候使用`make clean`可以删除它。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：格式化类型与参数匹配，逐字段输出符合原例，编译警告不被吞掉

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-04-base"></a>

### LCT-04-BASE 练习4：Valgrind 介绍

来源：本地原文（原完整交付引用：`<../references/markdown/77178c8a62cf6913.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex4.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习4：Valgrind 介绍”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：Valgrind 真正捕获原错误；修复版错误消失，保留两组日志

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-04-x01"></a>

### LCT-04-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/77178c8a62cf6913.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex4.md)

**实现要求**（保留原题的代码、列表及子问）：

- 按照上面的指导，使用`Valgrind`和编译器修复这个程序。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：Valgrind 真正捕获原错误；修复版错误消失，保留两组日志

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-04-x02"></a>

### LCT-04-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/77178c8a62cf6913.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex4.md)

**实现要求**（保留原题的代码、列表及子问）：

- 在互联网上查询`Valgrind`相关的资料。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：Valgrind 真正捕获原错误；修复版错误消失，保留两组日志

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-04-x03"></a>

### LCT-04-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/77178c8a62cf6913.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex4.md)

**实现要求**（保留原题的代码、列表及子问）：

- 下载另一个程序并手动构建它。尝试一些你已经使用，但从来没有手动构建的程序。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：Valgrind 真正捕获原错误；修复版错误消失，保留两组日志

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-04-x04"></a>

### LCT-04-X04 附加题 / 4

来源：本地原文（原完整交付引用：`<../references/markdown/77178c8a62cf6913.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex4.md)

**实现要求**（保留原题的代码、列表及子问）：

- 看看`Valgrind`的源码是如何在目录下组织的，并且阅读它的Makefile文件。不要担心，这对我来说没有任何意义。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：Valgrind 真正捕获原错误；修复版错误消失，保留两组日志

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-05-base"></a>

### LCT-05-BASE 练习5：一个C程序的结构

来源：本地原文（原完整交付引用：`<../references/markdown/10185bd9e2bed32a.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex5.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习5：一个C程序的结构”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：解释预处理/main/语句/返回，删除构件产生的诊断可复现

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-05-x01"></a>

### LCT-05-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/10185bd9e2bed32a.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex5.md)

**实现要求**（保留原题的代码、列表及子问）：

- 对于每一行，写出你不理解的符号，并且看看是否能猜出它们的意思。在纸上写下你的猜测，你可以在以后检查它，看看是否正确。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：解释预处理/main/语句/返回，删除构件产生的诊断可复现

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-05-x02"></a>

### LCT-05-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/10185bd9e2bed32a.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex5.md)

**实现要求**（保留原题的代码、列表及子问）：

- 回头去看之前几个练习的源代码，并且像这样分解代码，来看看你是否了解它们。写下你不了解和不能自己解释的东西。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：解释预处理/main/语句/返回，删除构件产生的诊断可复现

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-06-base"></a>

### LCT-06-BASE 练习6：变量类型

来源：本地原文（原完整交付引用：`<../references/markdown/8adfce49ddd1851f.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex6.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习6：变量类型”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：各类型/格式说明符正确，平台宽度实际记录

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-06-break"></a>

### LCT-06-BREAK 如何使它崩溃

来源：本地原文（原完整交付引用：`<../references/markdown/8adfce49ddd1851f.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex6.md)

**实现要求**（保留原题的代码、列表及子问）：

你可以通过向`printf`传递错误的参数来轻易使这个程序崩溃。例如，如果你找到打印我的名字的那行，把`initial`放到`first_name`前面，你就制造了一个bug。执行上述修改编译器就会向你报错，之后运行的时候你可能会得到一个“段错误”，就像这样：



```
$ make ex6
cc -Wall -g    ex6.c   -o ex6
ex6.c: In function 'main':
ex6.c:19: warning: format '%s' expects type 'char *', but argument 2 has type 'int'
ex6.c:19: warning: format '%c' expects type 'int', but argument 3 has type 'char *'
$ ./ex6
You are 100 miles away.
You have 2.345000 levels of power.
You have 56789.453125 awesome super powers.
I have an initial A.
I have a first name Zed.
I have a last name Shaw.
Segmentation fault
$
```



在`Valgrind`下运行修改后的程序，来观察它会告诉你什么关于错误“Invalid read of size 1”的事情。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：在可丢弃练习副本复现所列破坏行为，保存诊断/退出码，解释原因并提交修复版；不把故意 UB 的随机表现作为唯一预期。章级交叉检查：各类型/格式说明符正确，平台宽度实际记录

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-06-x01"></a>

### LCT-06-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/8adfce49ddd1851f.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex6.md)

**实现要求**（保留原题的代码、列表及子问）：

- 寻找其他通过修改`printf`使这段C代码崩溃的方法。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：各类型/格式说明符正确，平台宽度实际记录

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-06-x02"></a>

### LCT-06-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/8adfce49ddd1851f.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex6.md)

**实现要求**（保留原题的代码、列表及子问）：

- 搜索“`printf`格式化”，试着使用一些高级的占位符。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：各类型/格式说明符正确，平台宽度实际记录

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-06-x03"></a>

### LCT-06-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/8adfce49ddd1851f.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex6.md)

**实现要求**（保留原题的代码、列表及子问）：

- 研究可以用几种方法打印数字。尝试以八进制或十六进制打印，或者其它你找到的方法。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：各类型/格式说明符正确，平台宽度实际记录

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-06-x04"></a>

### LCT-06-X04 附加题 / 4

来源：本地原文（原完整交付引用：`<../references/markdown/8adfce49ddd1851f.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex6.md)

**实现要求**（保留原题的代码、列表及子问）：

- 试着打印空字符串，即`""`。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：各类型/格式说明符正确，平台宽度实际记录

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-07-base"></a>

### LCT-07-BASE 练习7：更多变量和一些算术

来源：本地原文（原完整交付引用：`<../references/markdown/4033b3de1454e235.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex7.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习7：更多变量和一些算术”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：运算及溢出/转换条件解释，结果与该平台类型语义一致

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-07-break"></a>

### LCT-07-BREAK 如何使它崩溃

来源：本地原文（原完整交付引用：`<../references/markdown/4033b3de1454e235.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex7.md)

**实现要求**（保留原题的代码、列表及子问）：

像之前一样，向`printf`传入错误的参数来使它崩溃。对比`%c`，看看当你使用`%s`来打印`nul_byte`变量时会发生什么。做完这些之后，在`Valgrind`下运行它看看关于你的这次尝试会输出什么。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：在可丢弃练习副本复现所列破坏行为，保存诊断/退出码，解释原因并提交修复版；不把故意 UB 的随机表现作为唯一预期。章级交叉检查：运算及溢出/转换条件解释，结果与该平台类型语义一致

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-07-x01"></a>

### LCT-07-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/4033b3de1454e235.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex7.md)

**实现要求**（保留原题的代码、列表及子问）：

- 把为`universe_of_defects`赋值的数改为不同的大小，观察编译器的警告。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：运算及溢出/转换条件解释，结果与该平台类型语义一致

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-07-x02"></a>

### LCT-07-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/4033b3de1454e235.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex7.md)

**实现要求**（保留原题的代码、列表及子问）：

- 这些巨大的数字实际上打印成了什么？

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：运算及溢出/转换条件解释，结果与该平台类型语义一致

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-07-x03"></a>

### LCT-07-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/4033b3de1454e235.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex7.md)

**实现要求**（保留原题的代码、列表及子问）：

- 将`long`改为`unsigned long`，并试着找到对它来说太大的数字。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：运算及溢出/转换条件解释，结果与该平台类型语义一致

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-07-x04"></a>

### LCT-07-X04 附加题 / 4

来源：本地原文（原完整交付引用：`<../references/markdown/4033b3de1454e235.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex7.md)

**实现要求**（保留原题的代码、列表及子问）：

- 上网搜索`unsigned`做了什么。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：运算及溢出/转换条件解释，结果与该平台类型语义一致

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-07-x05"></a>

### LCT-07-X05 附加题 / 5

来源：本地原文（原完整交付引用：`<../references/markdown/4033b3de1454e235.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex7.md)

**实现要求**（保留原题的代码、列表及子问）：

- 试着自己解释（在下个练习之前）为什么`char`可以和`int`相乘。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：运算及溢出/转换条件解释，结果与该平台类型语义一致

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-08-base"></a>

### LCT-08-BASE 练习8：大小和数组

来源：本地原文（原完整交付引用：`<../references/markdown/779314100c36ef32.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex8.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习8：大小和数组”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：sizeof 与数组/字符串长度区别正确，越界实验隔离

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-08-break"></a>

### LCT-08-BREAK 如何使它崩溃

来源：本地原文（原完整交付引用：`<../references/markdown/779314100c36ef32.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex8.md)

**实现要求**（保留原题的代码、列表及子问）：

使这个程序崩溃非常容易，只需要尝试下面这些事情：

- 将`full_name`最后的`'\0'`去掉，并重新运行它，在`valgrind`下再运行一遍。现在将`full_name`的定义从`main`函数中移到它的上面，尝试在`Valgrind`下运行它来看看是否能得到一些新的错误。有些情况下，你会足够幸运，不会得到任何错误。
- 将`areas[0]`改为`areas[10]`并打印，来看看`Valgrind`会输出什么。
- 尝试上述操作的不同变式，也对`name`和`full_name`执行一遍。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：在可丢弃练习副本复现所列破坏行为，保存诊断/退出码，解释原因并提交修复版；不把故意 UB 的随机表现作为唯一预期。章级交叉检查：sizeof 与数组/字符串长度区别正确，越界实验隔离

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-08-x01"></a>

### LCT-08-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/779314100c36ef32.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex8.md)

**实现要求**（保留原题的代码、列表及子问）：

- 尝试使用`areas[0] = 100;`以及相似的操作对`areas`的元素赋值。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：sizeof 与数组/字符串长度区别正确，越界实验隔离

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-08-x02"></a>

### LCT-08-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/779314100c36ef32.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex8.md)

**实现要求**（保留原题的代码、列表及子问）：

- 尝试对`name`和`full_name`的元素赋值。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：sizeof 与数组/字符串长度区别正确，越界实验隔离

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-08-x03"></a>

### LCT-08-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/779314100c36ef32.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex8.md)

**实现要求**（保留原题的代码、列表及子问）：

- 尝试将`areas`的一个元素赋值为`name`中的字符。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：sizeof 与数组/字符串长度区别正确，越界实验隔离

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-08-x04"></a>

### LCT-08-X04 附加题 / 4

来源：本地原文（原完整交付引用：`<../references/markdown/779314100c36ef32.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex8.md)

**实现要求**（保留原题的代码、列表及子问）：

- 上网搜索在不同的CPU上整数所占的不同大小。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：sizeof 与数组/字符串长度区别正确，越界实验隔离

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-09-base"></a>

### LCT-09-BASE 练习9：数组和字符串

来源：本地原文（原完整交付引用：`<../references/markdown/9a7ce42510816e43.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex9.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习9：数组和字符串”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：NUL 终止、字符数组和字符串打印边界正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-09-break"></a>

### LCT-09-BREAK 如何使它崩溃

来源：本地原文（原完整交付引用：`<../references/markdown/9a7ce42510816e43.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex9.md)

**实现要求**（保留原题的代码、列表及子问）：

C中所有bug的大多数来源都是忘了预留出足够的空间，或者忘了在字符串末尾加上一个`'\0'`。事实上，这些bug是非常普遍并且难以改正的，大部分优秀的C代码都不会使用C风格字符串。下一个练习中我们会学到如何彻底避免C风格字符串。

使这个程序崩溃的的关键就是拿掉字符串结尾的`'\0'`。下面是实现它的一些途径：

- 删掉`name`的初始化表达式。
- 无意中设置`name[3] = 'A'`，于是它就没有终止字符了。
- 将初始化表达式设置为`{'a','a','a','a'}`，于是就有过多的`'a'`字符，没有办法给`'\0'`留出位置。

试着想出一些其它的办法让它崩溃，并且在`Valgrind`下像往常一样运行这个程序，你可以看到具体发生了什么，以及错误叫什么名字。有时`Valgrind`并不能发现你犯的错误，则需要移动声明这些变量的地方看看是否能找出错误。这是C的黑魔法的一部分，有时变量的位置会改变bug。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：在可丢弃练习副本复现所列破坏行为，保存诊断/退出码，解释原因并提交修复版；不把故意 UB 的随机表现作为唯一预期。章级交叉检查：NUL 终止、字符数组和字符串打印边界正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-09-x01"></a>

### LCT-09-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/9a7ce42510816e43.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex9.md)

**实现要求**（保留原题的代码、列表及子问）：

- 将一些字符赋给`numbers`的元素，之后用`printf`一次打印一个字符，你会得到什么编译器警告？

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：NUL 终止、字符数组和字符串打印边界正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-09-x02"></a>

### LCT-09-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/9a7ce42510816e43.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex9.md)

**实现要求**（保留原题的代码、列表及子问）：

- 对`names`执行上述的相反操作，把`names`当成`int`数组，并一次打印一个`int`，`Valgrind`会提示什么？

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：NUL 终止、字符数组和字符串打印边界正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-09-x03"></a>

### LCT-09-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/9a7ce42510816e43.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex9.md)

**实现要求**（保留原题的代码、列表及子问）：

- 有多少种其它的方式可以用来打印它？

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：NUL 终止、字符数组和字符串打印边界正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-09-x04"></a>

### LCT-09-X04 附加题 / 4

来源：本地原文（原完整交付引用：`<../references/markdown/9a7ce42510816e43.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex9.md)

**实现要求**（保留原题的代码、列表及子问）：

- 如果一个字符数组占四个字节，一个整数也占4个字节，你可以像整数一样使用整个`name`吗？你如何用黑魔法实现它？

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：NUL 终止、字符数组和字符串打印边界正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-09-x05"></a>

### LCT-09-X05 附加题 / 5

来源：本地原文（原完整交付引用：`<../references/markdown/9a7ce42510816e43.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex9.md)

**实现要求**（保留原题的代码、列表及子问）：

- 拿出一张纸，将每个数组画成一排方框，之后在纸上画出代码中的操作，看看是否正确。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：NUL 终止、字符数组和字符串打印边界正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-09-x06"></a>

### LCT-09-X06 附加题 / 6

来源：本地原文（原完整交付引用：`<../references/markdown/9a7ce42510816e43.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex9.md)

**实现要求**（保留原题的代码、列表及子问）：

- 将`name`转换成`another`的形式，看看代码是否能正常工作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：NUL 终止、字符数组和字符串打印边界正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-10-base"></a>

### LCT-10-BASE 练习10：字符串数组和循环

来源：本地原文（原完整交付引用：`<../references/markdown/c52acddad54ae603.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex10.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习10：字符串数组和循环”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：argv 数量/遍历范围/字符串数组访问正确，覆盖空参数及多参数

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-10-break"></a>

### LCT-10-BREAK 如何使它崩溃

来源：本地原文（原完整交付引用：`<../references/markdown/c52acddad54ae603.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex10.md)

**实现要求**（保留原题的代码、列表及子问）：

- 使用你喜欢的另一种语言，来写这个程序。传入尽可能多的命令行参数，看看是否能通过传入过多参数使其崩溃。
- 将`i`初始化为0看看会发生什么。是否也需要改动`argc`，不改动的话它能正常工作吗？为什么下标从0开始可以正常工作？
- 将`num_states`改为错误的值使它变大，来看看会发生什么。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：在可丢弃练习副本复现所列破坏行为，保存诊断/退出码，解释原因并提交修复版；不把故意 UB 的随机表现作为唯一预期。章级交叉检查：argv 数量/遍历范围/字符串数组访问正确，覆盖空参数及多参数

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-10-x01"></a>

### LCT-10-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/c52acddad54ae603.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex10.md)

**实现要求**（保留原题的代码、列表及子问）：

- 弄清楚在`for`循环的每一部分你都可以放置什么样的代码。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：argv 数量/遍历范围/字符串数组访问正确，覆盖空参数及多参数

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-10-x02"></a>

### LCT-10-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/c52acddad54ae603.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex10.md)

**实现要求**（保留原题的代码、列表及子问）：

- 查询如何使用`','`（逗号）字符来在`for`循环的每一部分中，`';'`（分号）之间分隔多条语句。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：argv 数量/遍历范围/字符串数组访问正确，覆盖空参数及多参数

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-10-x03"></a>

### LCT-10-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/c52acddad54ae603.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex10.md)

**实现要求**（保留原题的代码、列表及子问）：

- 查询`NULL`是什么东西，尝试将它用做`states`的一个元素，看看它会打印出什么。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：argv 数量/遍历范围/字符串数组访问正确，覆盖空参数及多参数

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-10-x04"></a>

### LCT-10-X04 附加题 / 4

来源：本地原文（原完整交付引用：`<../references/markdown/c52acddad54ae603.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex10.md)

**实现要求**（保留原题的代码、列表及子问）：

- 看看你是否能在打印之前将`states`的一个元素赋值给`argv`中的元素，再试试相反的操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：argv 数量/遍历范围/字符串数组访问正确，覆盖空参数及多参数

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-11-base"></a>

### LCT-11-BASE 练习11：While循环和布尔表达式

来源：本地原文（原完整交付引用：`<../references/markdown/3bd60e222566eeab.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex11.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习11：While循环和布尔表达式”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：while 的边界、更新、终止条件可解释，正反例有记录

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-11-break"></a>

### LCT-11-BREAK 如何使它崩溃

来源：本地原文（原完整交付引用：`<../references/markdown/3bd60e222566eeab.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex11.md)

**实现要求**（保留原题的代码、列表及子问）：

在你自己的代码中，应优先选择`for`循环而不是`while`循环，因为`for`循环不容易崩溃。下面是几点普遍的原因：

- 忘记初始化`int i`，使循环发生错误。
- 忘记初始化第二个循环的`i`，于是`i`还保留着第一个循环结束时的值。你的第二个循环可能执行也可能不会执行。
- 忘记在最后执行`i++`自增，你会得到一个“死循环”，它是在你开始编程的第一个或前两个十年中，最可怕的问题之一。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：在可丢弃练习副本复现所列破坏行为，保存诊断/退出码，解释原因并提交修复版；不把故意 UB 的随机表现作为唯一预期。章级交叉检查：while 的边界、更新、终止条件可解释，正反例有记录

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-11-x01"></a>

### LCT-11-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/3bd60e222566eeab.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex11.md)

**实现要求**（保留原题的代码、列表及子问）：

- 让这些循环倒序执行，通过使用`i--`从`argc`开始递减直到0。你可能需要做一些算数操作让数组的下标正常工作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：while 的边界、更新、终止条件可解释，正反例有记录

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-11-x02"></a>

### LCT-11-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/3bd60e222566eeab.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex11.md)

**实现要求**（保留原题的代码、列表及子问）：

- 使用`while`循环将`argv`中的值复制到`states`。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：while 的边界、更新、终止条件可解释，正反例有记录

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-11-x03"></a>

### LCT-11-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/3bd60e222566eeab.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex11.md)

**实现要求**（保留原题的代码、列表及子问）：

- 让这个复制循环不会执行失败，即使`argv`之中有很多元素也不会全部放进`states`。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：while 的边界、更新、终止条件可解释，正反例有记录

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-11-x04"></a>

### LCT-11-X04 附加题 / 4

来源：本地原文（原完整交付引用：`<../references/markdown/3bd60e222566eeab.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex11.md)

**实现要求**（保留原题的代码、列表及子问）：

- 研究你是否真正复制了这些字符串。答案可能会让你感到意外和困惑。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：while 的边界、更新、终止条件可解释，正反例有记录

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-12-base"></a>

### LCT-12-BASE 练习12：If，Else If，Else

来源：本地原文（原完整交付引用：`<../references/markdown/43ae397b343b31af.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex12.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习12：If，Else If，Else”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：if/else 分支覆盖，条件改动前后结果可解释

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-12-break"></a>

### LCT-12-BREAK 如何使它崩溃

来源：本地原文（原完整交付引用：`<../references/markdown/43ae397b343b31af.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex12.md)

**实现要求**（保留原题的代码、列表及子问）：

使这段代码崩溃并不容易，因为它太简单了。尝试把`if`语句的测试表达式搞乱：

- 移除`else`部分，使它不能处理边界情况。
- 将`&&`改为`||`，于是你会把“与”操作变成“或”操作，并且看看会发生什么。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：在可丢弃练习副本复现所列破坏行为，保存诊断/退出码，解释原因并提交修复版；不把故意 UB 的随机表现作为唯一预期。章级交叉检查：if/else 分支覆盖，条件改动前后结果可解释

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-12-x01"></a>

### LCT-12-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/43ae397b343b31af.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex12.md)

**实现要求**（保留原题的代码、列表及子问）：

- 我已经向你简短地介绍了`&&`，它执行“与”操作。上网搜索与之不同的“布尔运算符”。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：if/else 分支覆盖，条件改动前后结果可解释

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-12-x02"></a>

### LCT-12-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/43ae397b343b31af.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex12.md)

**实现要求**（保留原题的代码、列表及子问）：

- 为这个程序编写更多的测试用例，看看你会写出什么。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：if/else 分支覆盖，条件改动前后结果可解释

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-12-x03"></a>

### LCT-12-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/43ae397b343b31af.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex12.md)

**实现要求**（保留原题的代码、列表及子问）：

- 回到练习10和11，使用`if`语句使循环提前退出。你需要`break`语句来实现它，搜索它的有关资料。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：if/else 分支覆盖，条件改动前后结果可解释

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-12-x04"></a>

### LCT-12-X04 附加题 / 4

来源：本地原文（原完整交付引用：`<../references/markdown/43ae397b343b31af.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex12.md)

**实现要求**（保留原题的代码、列表及子问）：

- 第一个判断所输出的话真的正确吗？由于你的“第一个参数”不是用户输入的第一个参数，把它改正。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：if/else 分支覆盖，条件改动前后结果可解释

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-13-base"></a>

### LCT-13-BASE 练习13：Switch语句

来源：本地原文（原完整交付引用：`<../references/markdown/be75e8603b58711e.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex13.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习13：Switch语句”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：switch 的 case/default/break 路径覆盖并解释贯穿

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-13-break"></a>

### LCT-13-BREAK 如何使它崩溃

来源：本地原文（原完整交付引用：`<../references/markdown/be75e8603b58711e.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex13.md)

**实现要求**（保留原题的代码、列表及子问）：

破坏一个`switch`语句块太容易了。下面是一些方法，你可以挑一个来用：

- 忘记写`break`，程序就会运行两个或多个代码块，这些都是你不想运行的。
- 忘记写`default`，程序会在静默中忽略你所忘记的值。
- 无意中将一些带有预料之外的值的变量放入`switch`中，比如带有奇怪的值的`int`。
- 在`switch`中是否未初始化的值。

你也可以使用一些别的方法使这个程序崩溃。试着看你能不能自己做到它。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：在可丢弃练习副本复现所列破坏行为，保存诊断/退出码，解释原因并提交修复版；不把故意 UB 的随机表现作为唯一预期。章级交叉检查：switch 的 case/default/break 路径覆盖并解释贯穿

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-13-x01"></a>

### LCT-13-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/be75e8603b58711e.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex13.md)

**实现要求**（保留原题的代码、列表及子问）：

- 编写另一个程序，在字母上做算术运算将它们转换为小写，并且在`switch`中移除所有额外的大写字母。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：switch 的 case/default/break 路径覆盖并解释贯穿

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-13-x02"></a>

### LCT-13-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/be75e8603b58711e.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex13.md)

**实现要求**（保留原题的代码、列表及子问）：

- 使用`','`（逗号）在`for`循环中初始化`letter`。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：switch 的 case/default/break 路径覆盖并解释贯穿

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-13-x03"></a>

### LCT-13-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/be75e8603b58711e.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex13.md)

**实现要求**（保留原题的代码、列表及子问）：

- 使用另一个`for`循环来让它处理你传入的所有命令行参数。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：switch 的 case/default/break 路径覆盖并解释贯穿

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-13-x04"></a>

### LCT-13-X04 附加题 / 4

来源：本地原文（原完整交付引用：`<../references/markdown/be75e8603b58711e.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex13.md)

**实现要求**（保留原题的代码、列表及子问）：

- 将这个`switch`语句转为`if`语句，你更喜欢哪个呢？

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：switch 的 case/default/break 路径覆盖并解释贯穿

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-13-x05"></a>

### LCT-13-X05 附加题 / 5

来源：本地原文（原完整交付引用：`<../references/markdown/be75e8603b58711e.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex13.md)

**实现要求**（保留原题的代码、列表及子问）：

- 在“Y”的例子中，我在`if`代码块外面写了个`break`。这样会产生什么效果？如果把它移进`if`代码块，会发生什么？自己试着解答它，并证明你是正确的。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：switch 的 case/default/break 路径覆盖并解释贯穿

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-14-base"></a>

### LCT-14-BASE 练习14：编写并使用函数

来源：本地原文（原完整交付引用：`<../references/markdown/4526f0a1b3776083.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex14.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习14：编写并使用函数”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：函数声明/参数/返回正确，命令行样例和错误输入都测

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-14-break"></a>

### LCT-14-BREAK 如何使它崩溃

来源：本地原文（原完整交付引用：`<../references/markdown/4526f0a1b3776083.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex14.md)

**实现要求**（保留原题的代码、列表及子问）：

下面是使它崩溃的两种不同的方法：

- 通过移除前向声明来把编译器搞晕。它会报告`can_print_it` 和 `print_letters`的错误。
- 当你在`main`中调用`print_arguments`时，试着使`argc`加1，于是它会越过`argv`数组的最后一个元素。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：在可丢弃练习副本复现所列破坏行为，保存诊断/退出码，解释原因并提交修复版；不把故意 UB 的随机表现作为唯一预期。章级交叉检查：函数声明/参数/返回正确，命令行样例和错误输入都测

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-14-x01"></a>

### LCT-14-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/4526f0a1b3776083.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex14.md)

**实现要求**（保留原题的代码、列表及子问）：

- 重新编写这些函数，使它们的数量减少。比如，你真的需要`can_print_it`吗？

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：函数声明/参数/返回正确，命令行样例和错误输入都测

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-14-x02"></a>

### LCT-14-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/4526f0a1b3776083.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex14.md)

**实现要求**（保留原题的代码、列表及子问）：

- 使用`strlen`函数，让`print_arguments`知道每个字符串参数都有多长，之后将长度传入`print_letters`。然后重写`print_letters`，让它只处理固定的长度，不按照`'\0'`终止符。你需要`#include <string.h>`来实现它。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：函数声明/参数/返回正确，命令行样例和错误输入都测

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-14-x03"></a>

### LCT-14-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/4526f0a1b3776083.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex14.md)

**实现要求**（保留原题的代码、列表及子问）：

- 使用`man`来查询`isalpha`和`isblank`的信息。使用其它相似的函数来只打印出数字或者其它字符。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：函数声明/参数/返回正确，命令行样例和错误输入都测

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-14-x04"></a>

### LCT-14-X04 附加题 / 4

来源：本地原文（原完整交付引用：`<../references/markdown/4526f0a1b3776083.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex14.md)

**实现要求**（保留原题的代码、列表及子问）：

- 上网浏览不同的人喜欢什么样的函数格式。永远不要使用“K&R”语法，因为它过时了，而且容易使人混乱，但是当你碰到一些人使用这种格式时，要理解代码做了什么。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：函数声明/参数/返回正确，命令行样例和错误输入都测

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-15-base"></a>

### LCT-15-BASE 练习15：指针，可怕的指针

来源：本地原文（原完整交付引用：`<../references/markdown/821276b1076ae8ff.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex15.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习15：指针，可怕的指针”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：数组下标/指针递增的对应及越界风险可画图说明

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-15-break"></a>

### LCT-15-BREAK 如何使它崩溃

来源：本地原文（原完整交付引用：`<../references/markdown/821276b1076ae8ff.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex15.md)

**实现要求**（保留原题的代码、列表及子问）：

你可以通过将指针指向错误的位置来使程序崩溃：

- 试着将`cur_age`指向`names`。可以需要C风格转换来强制执行，试着查阅相关资料把它弄明白。
- 在最后的`for`循环中，用一些古怪的方式使计算发生错误。
- 试着重写循环，让它们从数组的最后一个元素开始遍历到首个元素。这比看上去要困难。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：在可丢弃练习副本复现所列破坏行为，保存诊断/退出码，解释原因并提交修复版；不把故意 UB 的随机表现作为唯一预期。章级交叉检查：数组下标/指针递增的对应及越界风险可画图说明

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-15-x01"></a>

### LCT-15-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/821276b1076ae8ff.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex15.md)

**实现要求**（保留原题的代码、列表及子问）：

- 使用访问指针的方式重写所有使用数组的地方。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：数组下标/指针递增的对应及越界风险可画图说明

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-15-x02"></a>

### LCT-15-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/821276b1076ae8ff.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex15.md)

**实现要求**（保留原题的代码、列表及子问）：

- 使用访问数组的方式重写所有使用指针的地方。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：数组下标/指针递增的对应及越界风险可画图说明

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-15-x03"></a>

### LCT-15-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/821276b1076ae8ff.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex15.md)

**实现要求**（保留原题的代码、列表及子问）：

- 在其它程序中使用指针来代替数组访问。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：数组下标/指针递增的对应及越界风险可画图说明

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-15-x04"></a>

### LCT-15-X04 附加题 / 4

来源：本地原文（原完整交付引用：`<../references/markdown/821276b1076ae8ff.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex15.md)

**实现要求**（保留原题的代码、列表及子问）：

- 使用指针来处理命令行参数，就像处理`names`那样。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：数组下标/指针递增的对应及越界风险可画图说明

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-15-x05"></a>

### LCT-15-X05 附加题 / 5

来源：本地原文（原完整交付引用：`<../references/markdown/821276b1076ae8ff.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex15.md)

**实现要求**（保留原题的代码、列表及子问）：

- 将获取值和获取地址组合到一起。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：数组下标/指针递增的对应及越界风险可画图说明

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-15-x06"></a>

### LCT-15-X06 附加题 / 6

来源：本地原文（原完整交付引用：`<../references/markdown/821276b1076ae8ff.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex15.md)

**实现要求**（保留原题的代码、列表及子问）：

- 在程序末尾添加一个`for`循环，打印出这些指针所指向的地址。你需要在`printf`中使用`%p`。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：数组下标/指针递增的对应及越界风险可画图说明

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-15-x07"></a>

### LCT-15-X07 附加题 / 7

来源：本地原文（原完整交付引用：`<../references/markdown/821276b1076ae8ff.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex15.md)

**实现要求**（保留原题的代码、列表及子问）：

- 对于每一种打印数组的方法，使用函数来重写程序。试着向函数传递指针来处理数据。记住你可以声明接受指针的函数，但是可以像数组那样用它。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：数组下标/指针递增的对应及越界风险可画图说明

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-15-x08"></a>

### LCT-15-X08 附加题 / 8

来源：本地原文（原完整交付引用：`<../references/markdown/821276b1076ae8ff.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex15.md)

**实现要求**（保留原题的代码、列表及子问）：

- 将`for`循环改为`while`循环，并且观察对于每种指针用法哪种循环更方便。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：数组下标/指针递增的对应及越界风险可画图说明

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-16-base"></a>

### LCT-16-BASE 练习16：结构体和指向它们的指针

来源：本地原文（原完整交付引用：`<../references/markdown/778867275188b07f.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex16.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习16：结构体和指向它们的指针”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：结构体创建/访问/释放正确；分配失败与重复释放风险被检查

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-16-break"></a>

### LCT-16-BREAK 如何使它崩溃

来源：本地原文（原完整交付引用：`<../references/markdown/778867275188b07f.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex16.md)

**实现要求**（保留原题的代码、列表及子问）：

使这个程序崩溃的办法涉及到使用指针和`malloc`系统的方法：

- 试着传递`NULL`给`Person_destroy`来看看会发生什么。如果它没有崩溃，你必须移除Makefile的`CFLAGS`中的`-g`选项。
- 在结尾处忘记调用`Person_destroy`，在`Valgrind`下运行程序，你会看到它报告出你忘记释放内存。弄清楚你应该向`valgrind`传递什么参数来让它向你报告内存如何泄露。
- 忘记在`Person_destroy`中释放`who->name`，并且对比两次的输出。同时，使用正确的选项来让`Valgrind`告诉你哪里错了。
- 这一次，向`Person_print`传递`NULL`，并且观察`Valgrind`会输出什么。
- 你应该明白了`NULL`是个使程序崩溃的快速方法。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：在可丢弃练习副本复现所列破坏行为，保存诊断/退出码，解释原因并提交修复版；不把故意 UB 的随机表现作为唯一预期。章级交叉检查：结构体创建/访问/释放正确；分配失败与重复释放风险被检查

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-16-x01"></a>

### LCT-16-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/778867275188b07f.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex16.md)

**实现要求**（保留原题的代码、列表及子问）：

在这个练习的附加题中我想让你尝试一些有难度的东西：将这个程序改为不用指针和`malloc`的版本。这可能很困难，所以你需要研究下面这些东西：

- 如何在栈上创建结构体，就像你创建任何其它变量那样。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：结构体创建/访问/释放正确；分配失败与重复释放风险被检查

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-16-x02"></a>

### LCT-16-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/778867275188b07f.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex16.md)

**实现要求**（保留原题的代码、列表及子问）：

- 如何使用`x.y`而不是`x->y`来初始化结构体。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：结构体创建/访问/释放正确；分配失败与重复释放风险被检查

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-16-x03"></a>

### LCT-16-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/778867275188b07f.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex16.md)

**实现要求**（保留原题的代码、列表及子问）：

- 如何不使用指针来将结构体传给其它函数。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：结构体创建/访问/释放正确；分配失败与重复释放风险被检查

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-17-base"></a>

### LCT-17-BASE 练习17：堆和栈的内存分配

来源：本地原文（原完整交付引用：`<../references/markdown/7f6ae09d26223fcc.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex17.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习17：堆和栈的内存分配”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：数据库 create/get/set/delete/list 等原例动作均测，文件保存重开与错误路径正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-17-break"></a>

### LCT-17-BREAK 如何使它崩溃

来源：本地原文（原完整交付引用：`<../references/markdown/7f6ae09d26223fcc.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex17.md)

**实现要求**（保留原题的代码、列表及子问）：

这个程序有很多可以使之崩溃的地方，尝试下面这些东西，同时也想出自己的办法。

- 最经典的方法是移除一些安全检查，你就可以传入任意数据。例如，第160行的检查防止你传入任何记录序号。
- 你也可以尝试弄乱数据文件。使用任何编辑器打开它并且随机修改几个字节并关闭。
- 你也可以寻找在运行中向程序传递非法参数的办法。例如将文件参数放到动作后面，就会创建一个以动作命名的文件，并且按照文件名的第一个字符执行动作。
- 这个程序中有个bug，因为`strncpy`有设计缺陷。查询`strncpy`的相关资料，然后试着弄清楚如果`name`或者`address`超过512个字节会发生什么。可以通过简单把最后一个字符设置成`'\0'`来修复它，你应该无论如何都这样做（这也是函数原本应该做的）。
- 在附加题中我会让你传递参数来创建任意大小的数据库。在你造成程序退出或`malloc`的内存不足之前，尝试找出最大的数据库尺寸是多少。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：在可丢弃练习副本复现所列破坏行为，保存诊断/退出码，解释原因并提交修复版；不把故意 UB 的随机表现作为唯一预期。章级交叉检查：数据库 create/get/set/delete/list 等原例动作均测，文件保存重开与错误路径正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-17-x01"></a>

### LCT-17-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/7f6ae09d26223fcc.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex17.md)

**实现要求**（保留原题的代码、列表及子问）：

- `die`函数需要接收`conn`变量作为参数，以便执行清理并关闭它。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：数据库 create/get/set/delete/list 等原例动作均测，文件保存重开与错误路径正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-17-x02"></a>

### LCT-17-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/7f6ae09d26223fcc.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex17.md)

**实现要求**（保留原题的代码、列表及子问）：

- 修改代码，使其接收参数作为`MAX_DATA`和`MAX_ROWS`，将它们储存在`Database`结构体中，并且将它们写到文件。这样就可以创建任意大小的数据库。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：数据库 create/get/set/delete/list 等原例动作均测，文件保存重开与错误路径正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-17-x03"></a>

### LCT-17-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/7f6ae09d26223fcc.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex17.md)

**实现要求**（保留原题的代码、列表及子问）：

- 向数据库添加更多操作，比如`find`。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：数据库 create/get/set/delete/list 等原例动作均测，文件保存重开与错误路径正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-17-x04"></a>

### LCT-17-X04 附加题 / 4

来源：本地原文（原完整交付引用：`<../references/markdown/7f6ae09d26223fcc.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex17.md)

**实现要求**（保留原题的代码、列表及子问）：

- 查询C如何打包结构体，并且试着弄清楚为什么你的文件是相应的大小。看看你是否可以计算出结构体添加一些字段之后的新大小。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：数据库 create/get/set/delete/list 等原例动作均测，文件保存重开与错误路径正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-17-x05"></a>

### LCT-17-X05 附加题 / 5

来源：本地原文（原完整交付引用：`<../references/markdown/7f6ae09d26223fcc.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex17.md)

**实现要求**（保留原题的代码、列表及子问）：

- 向`Address`添加一些字段，使它们可被搜索。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：数据库 create/get/set/delete/list 等原例动作均测，文件保存重开与错误路径正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-17-x06"></a>

### LCT-17-X06 附加题 / 6

来源：本地原文（原完整交付引用：`<../references/markdown/7f6ae09d26223fcc.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex17.md)

**实现要求**（保留原题的代码、列表及子问）：

- 编写一个shell脚本来通过以正确顺序运行命令执行自动化测试。提示：在`bash`顶端使用使用`set -e`，使之在任何命令发生错误时退出。
  > 译者注：使用Python编写多行脚本或许更方便一些。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：数据库 create/get/set/delete/list 等原例动作均测，文件保存重开与错误路径正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-17-x07"></a>

### LCT-17-X07 附加题 / 7

来源：本地原文（原完整交付引用：`<../references/markdown/7f6ae09d26223fcc.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex17.md)

**实现要求**（保留原题的代码、列表及子问）：

- 尝试重构程序，使用单一的全局变量来储存数据库连接。这个新版本和旧版本比起来如何？

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：数据库 create/get/set/delete/list 等原例动作均测，文件保存重开与错误路径正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-17-x08"></a>

### LCT-17-X08 附加题 / 8

来源：本地原文（原完整交付引用：`<../references/markdown/7f6ae09d26223fcc.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex17.md)

**实现要求**（保留原题的代码、列表及子问）：

- 搜索“栈数据结构”，并且在你最喜欢的语言中实现它，然后尝试在C中实现。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：数据库 create/get/set/delete/list 等原例动作均测，文件保存重开与错误路径正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-18-base"></a>

### LCT-18-BASE 练习18：函数指针

来源：本地原文（原完整交付引用：`<../references/markdown/b1f61c31b6762fcc.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex18.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习18：函数指针”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：函数指针回调/排序行为正确，不能只把指针强转到任意类型

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-18-break"></a>

### LCT-18-BREAK 如何使它崩溃

来源：本地原文（原完整交付引用：`<../references/markdown/b1f61c31b6762fcc.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex18.md)

**实现要求**（保留原题的代码、列表及子问）：

我打算让你做一些奇怪的事情来使它崩溃，这些函数指针都是类似于其它指针的指针，他们都指向内存的一块区域。C中可以将一种指针的指针转换为另一种，以便以不同方式处理数据。这些通常是不必要的，但是为了想你展示如何侵入你的电脑，我希望你把这段代码添加在`test_sorting`下面：



```
unsigned char *data = (unsigned char *)cmp;

for(i = 0; i < 25; i++) {
    printf("%02x:", data[i]);
}

printf("\n");
```



这个循环将你的函数转换成字符串，并且打印出来它的内容。这并不会中断你的程序，除非CPU和OS在执行过程中遇到了问题。在它打印排序过的数组之后，你所看到的是一个十六进制数字的字符串：



```
55:48:89:e5:89:7d:fc:89:75:f8:8b:55:fc:8b:45:f8:29:d0:c9:c3:55:48:89:e5:89:
```



这就应该是函数的原始的汇编字节码了，你应该能看到它们有相同的起始和不同的结尾。也有可能这个循环并没有获得函数的全部，或者获得了过多的代码而跑到程序的另外一片空间。这些不通过更多分析是不可能知道的。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：在可丢弃练习副本复现所列破坏行为，保存诊断/退出码，解释原因并提交修复版；不把故意 UB 的随机表现作为唯一预期。章级交叉检查：函数指针回调/排序行为正确，不能只把指针强转到任意类型

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-18-x01"></a>

### LCT-18-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/b1f61c31b6762fcc.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex18.md)

**实现要求**（保留原题的代码、列表及子问）：

- 用十六进制编辑器打开`ex18`，接着找到函数起始处的十六进制代码序列，看看是否能在原始程序中找到函数。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：函数指针回调/排序行为正确，不能只把指针强转到任意类型

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-18-x02"></a>

### LCT-18-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/b1f61c31b6762fcc.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex18.md)

**实现要求**（保留原题的代码、列表及子问）：

- 在你的十六进制编辑器中找到更多随机出现的东西并修改它们。重新运行你的程序看看发生了什么。字符串是你最容易修改的东西。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：函数指针回调/排序行为正确，不能只把指针强转到任意类型

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-18-x03"></a>

### LCT-18-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/b1f61c31b6762fcc.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex18.md)

**实现要求**（保留原题的代码、列表及子问）：

- 将错误的函数传给`compare_cb`，并看看C编辑器会报告什么错误。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：函数指针回调/排序行为正确，不能只把指针强转到任意类型

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-18-x04"></a>

### LCT-18-X04 附加题 / 4

来源：本地原文（原完整交付引用：`<../references/markdown/b1f61c31b6762fcc.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex18.md)

**实现要求**（保留原题的代码、列表及子问）：

- 将`NULL`传给它，看看程序中会发生什么。然后运行`Valgrind`来看看它会报告什么。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：函数指针回调/排序行为正确，不能只把指针强转到任意类型

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-18-x05"></a>

### LCT-18-X05 附加题 / 5

来源：本地原文（原完整交付引用：`<../references/markdown/b1f61c31b6762fcc.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex18.md)

**实现要求**（保留原题的代码、列表及子问）：

- 编写另一个排序算法，修改`test_sorting`使它接收任意的排序函数和排序函数的比较回调。并使用它来测试两种排序算法。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：函数指针回调/排序行为正确，不能只把指针强转到任意类型

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-19-base"></a>

### LCT-19-BASE 练习19：一个简单的对象系统

来源：本地原文（原完整交付引用：`<../references/markdown/2c03a44e10bc0f59.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex19.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习19：一个简单的对象系统”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：原例对象/继承/回调行为对应，内存生命周期完整，无方法表错误

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-19-x01"></a>

### LCT-19-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/2c03a44e10bc0f59.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex19.md)

**实现要求**（保留原题的代码、列表及子问）：

- 修改`Makefile`文件，使之在执行`make clean`时能够同时清理`object.o`。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：原例对象/继承/回调行为对应，内存生命周期完整，无方法表错误

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-19-x02"></a>

### LCT-19-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/2c03a44e10bc0f59.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex19.md)

**实现要求**（保留原题的代码、列表及子问）：

- 编写一个测试脚本，能够以多种方式来调用该游戏，并且扩展`Makefile`使之能够通过运行`make test`来测试该游戏。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：原例对象/继承/回调行为对应，内存生命周期完整，无方法表错误

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-19-x03"></a>

### LCT-19-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/2c03a44e10bc0f59.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex19.md)

**实现要求**（保留原题的代码、列表及子问）：

- 在游戏中添加更多房间和怪物。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：原例对象/继承/回调行为对应，内存生命周期完整，无方法表错误

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-19-x04"></a>

### LCT-19-X04 附加题 / 4

来源：本地原文（原完整交付引用：`<../references/markdown/2c03a44e10bc0f59.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex19.md)

**实现要求**（保留原题的代码、列表及子问）：

- 把游戏的逻辑放在其它文件中，并把它编译为`.o`。然后，使用它来编写另一个小游戏。如果你正确编写的话，你会在新游戏中创建新的`Map`和`main`函数。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：原例对象/继承/回调行为对应，内存生命周期完整，无方法表错误

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-20-base"></a>

### LCT-20-BASE 练习20：Zed的强大的调试宏

来源：本地原文（原完整交付引用：`<../references/markdown/bb3d0d4aafa01516.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex20.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习20：Zed的强大的调试宏”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：dbg 宏的正常/error 路径和编译开关都测，能追溯实际控制流

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-20-x01"></a>

### LCT-20-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/bb3d0d4aafa01516.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex20.md)

**实现要求**（保留原题的代码、列表及子问）：

- 将`#define NDEBUG`放在文件顶端来消除所有调试信息。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：dbg 宏的正常/error 路径和编译开关都测，能追溯实际控制流

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-20-x02"></a>

### LCT-20-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/bb3d0d4aafa01516.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex20.md)

**实现要求**（保留原题的代码、列表及子问）：

- 撤销上面添加的一行，并在`MakeFile`顶端将`-D NDEBUG`添加到`CFLAGS`，之后重新编译来达到同样效果。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：dbg 宏的正常/error 路径和编译开关都测，能追溯实际控制流

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-20-x03"></a>

### LCT-20-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/bb3d0d4aafa01516.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex20.md)

**实现要求**（保留原题的代码、列表及子问）：

- 修改日志宏，使之包含函数名称和`file:line`。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：dbg 宏的正常/error 路径和编译开关都测，能追溯实际控制流

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-21-base"></a>

### LCT-21-BASE 练习21：高级数据类型和控制结构

来源：本地原文（原完整交付引用：`<../references/markdown/2a1317882cbcfa3a.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex21.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习21：高级数据类型和控制结构”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：类型/存储/控制结构知识点分别举例，区分平台相关与标准语义

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-21-x01"></a>

### LCT-21-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/2a1317882cbcfa3a.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex21.md)

**实现要求**（保留原题的代码、列表及子问）：

- 阅读`stdint.h`或它的描述，写出所有可能出现的大小定义。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：类型/存储/控制结构知识点分别举例，区分平台相关与标准语义

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-21-x02"></a>

### LCT-21-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/2a1317882cbcfa3a.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex21.md)

**实现要求**（保留原题的代码、列表及子问）：

- 查询本练习的每一项，写出它在代码中的作用。上网浏览资料来研究它如何正确使用。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：类型/存储/控制结构知识点分别举例，区分平台相关与标准语义

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-21-x03"></a>

### LCT-21-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/2a1317882cbcfa3a.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex21.md)

**实现要求**（保留原题的代码、列表及子问）：

- 将这些信息做成教学卡片，每天看上15分钟来记住它们。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：类型/存储/控制结构知识点分别举例，区分平台相关与标准语义

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-21-x04"></a>

### LCT-21-X04 附加题 / 4

来源：本地原文（原完整交付引用：`<../references/markdown/2a1317882cbcfa3a.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex21.md)

**实现要求**（保留原题的代码、列表及子问）：

- 创建一个程序，打印出每个类型的示例，并验证你的研究结果是否正确。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：类型/存储/控制结构知识点分别举例，区分平台相关与标准语义

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-22-base"></a>

### LCT-22-BASE 练习22：栈、作用域和全局

来源：本地原文（原完整交付引用：`<../references/markdown/8ad38a07208504a7.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex22.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习22：栈、作用域和全局”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：栈/全局/静态/作用域/extern 的链接及生命周期可解释，故意破坏的多文件例子能诊断

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-22-break"></a>

### LCT-22-BREAK 如何使它崩溃

来源：本地原文（原完整交付引用：`<../references/markdown/8ad38a07208504a7.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex22.md)

**实现要求**（保留原题的代码、列表及子问）：

对于这个练习，崩溃这个程序涉及到尝试访问或修改你不能访问的东西。

- 试着从`ex22_main.c`直接访问`ex22.c`中的你不能访问变量。例如，你能不能获取`update_ratio`中的`ratio`？如果你用一个指针指向它会发生什么？
- 移除`ex22.h`的`extern`声明，来观察会得到什么错误或警告。
- 对不同变量添加`static`或者`const`限定符，之后尝试修改它们。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：在可丢弃练习副本复现所列破坏行为，保存诊断/退出码，解释原因并提交修复版；不把故意 UB 的随机表现作为唯一预期。章级交叉检查：栈/全局/静态/作用域/extern 的链接及生命周期可解释，故意破坏的多文件例子能诊断

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-22-x01"></a>

### LCT-22-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/8ad38a07208504a7.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex22.md)

**实现要求**（保留原题的代码、列表及子问）：

- 研究“值传递”和“引用传递”的差异，并且为二者编写示例。（译者注：C中没有引用传递，你可以搜索“指针传递”。）

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：栈/全局/静态/作用域/extern 的链接及生命周期可解释，故意破坏的多文件例子能诊断

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-22-x02"></a>

### LCT-22-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/8ad38a07208504a7.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex22.md)

**实现要求**（保留原题的代码、列表及子问）：

- 使用指针来访问原本不能访问的变量。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：栈/全局/静态/作用域/extern 的链接及生命周期可解释，故意破坏的多文件例子能诊断

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-22-x03"></a>

### LCT-22-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/8ad38a07208504a7.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex22.md)

**实现要求**（保留原题的代码、列表及子问）：

- 使用`Valgrind`来观察错误的访问是什么样子。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：栈/全局/静态/作用域/extern 的链接及生命周期可解释，故意破坏的多文件例子能诊断

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-22-x04"></a>

### LCT-22-X04 附加题 / 4

来源：本地原文（原完整交付引用：`<../references/markdown/8ad38a07208504a7.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex22.md)

**实现要求**（保留原题的代码、列表及子问）：

- 编写一个递归调用并导致栈溢出的函数。如果不知道递归函数是什么的话，试着在`scope_demo`底部调用`scope_demo`本身，会形成一种循环。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：栈/全局/静态/作用域/extern 的链接及生命周期可解释，故意破坏的多文件例子能诊断

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-22-x05"></a>

### LCT-22-X05 附加题 / 5

来源：本地原文（原完整交付引用：`<../references/markdown/8ad38a07208504a7.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex22.md)

**实现要求**（保留原题的代码、列表及子问）：

- 重新编写`Makefile`使之能够构建这些文件。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：栈/全局/静态/作用域/extern 的链接及生命周期可解释，故意破坏的多文件例子能诊断

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-24-base"></a>

### LCT-24-BASE 练习24：输入输出和文件

来源：本地原文（原完整交付引用：`<../references/markdown/d879b51dc361cbc5.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex24.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习24：输入输出和文件”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：scanf/fgets 的合法/格式错误/长输入/EOF 路径均记录，缓冲区终止正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-24-break"></a>

### LCT-24-BREAK 如何使它崩溃

来源：本地原文（原完整交付引用：`<../references/markdown/d879b51dc361cbc5.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex24.md)

**实现要求**（保留原题的代码、列表及子问）：

这个程序非常不错，但是这个练习中真正重要的部分是，`scanf`如何发生错误。对于简单的数值转换没有问题，但是对于字符串会出现问题，因为`scanf`在你读取之前并不知道缓冲区有多大。类似于`gets`的函数（并不是`fgets`，不带`f`的版本）也有一个我们已经避免的问题。它并不是道输入缓冲区有多大，并且可能会使你的程序崩溃。

要演示`fscanf`和字符串的这一问题，需要修改使用`fgets`的那一行，使它变成`fscanf(stdin, "%50s", you.first_name)`，并且尝试再次运行。你会注意到，它读取了过多的内容，并且吃掉了你的回车键。这并不是你期望它所做的，你应该使用`fgets`而不是去解决古怪的`scanf`问题。

接下来，将`fgets`改为`gets`，接着使用`valgrind`来执行`valgrind ./ex24 < /dev/urandom`，往你的程序中输入一些垃圾字符串。这叫做对你的程序进行“模糊测试”，它是一种不错的方法来发现输入错误。这个例子中，你需要从`/dev/urandom`文件来输入一些垃圾，并且观察它如何崩溃。在一些平台上你需要执行数次，或者修改`MAX_DATA`来使其变小。

`gets`函数非常糟糕，以至于一些平台在程序运行时会警告你使用了`gets`。你应该永远避免使用这个函数。

最后，找到`you.eyes`输入的地方，并移除对其是否在正确范围内的检查。然后，为它输入一个错误的数值，比如-1或者1000。在`Valgrind`执行这些操作，来观察会发生什么。

> 译者注：根据最新的C11标准，对于输入函数，你应该总是使用`_s`后缀的安全版本。对于向字符串的输出函数，应该总是使用C99中新增的带`n`的版本，例如`snprintf`。如果你的编译器支持新版本，就不应该使用旧版本的不安全函数。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：在可丢弃练习副本复现所列破坏行为，保存诊断/退出码，解释原因并提交修复版；不把故意 UB 的随机表现作为唯一预期。章级交叉检查：scanf/fgets 的合法/格式错误/长输入/EOF 路径均记录，缓冲区终止正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-24-x01"></a>

### LCT-24-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/d879b51dc361cbc5.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex24.md)

**实现要求**（保留原题的代码、列表及子问）：

- 将这个程序重写为不需要`fscanf`的版本。你需要使用类似于`atoi`的函数来将输入的字符串转换为数值。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：scanf/fgets 的合法/格式错误/长输入/EOF 路径均记录，缓冲区终止正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-24-x02"></a>

### LCT-24-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/d879b51dc361cbc5.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex24.md)

**实现要求**（保留原题的代码、列表及子问）：

- 修改这个程序，使用`scanf`来代替`fscanf`，并观察有什么不同。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：scanf/fgets 的合法/格式错误/长输入/EOF 路径均记录，缓冲区终止正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-24-x03"></a>

### LCT-24-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/d879b51dc361cbc5.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex24.md)

**实现要求**（保留原题的代码、列表及子问）：

- 修改程序，是输入的名字不包含任何换行符和空白字符。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：scanf/fgets 的合法/格式错误/长输入/EOF 路径均记录，缓冲区终止正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-24-x04"></a>

### LCT-24-X04 附加题 / 4

来源：本地原文（原完整交付引用：`<../references/markdown/d879b51dc361cbc5.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex24.md)

**实现要求**（保留原题的代码、列表及子问）：

- 使用`scanf`编写函数，按照文件名读取文件内容，每次读取单个字符，但是不要越过（文件和缓冲区的）末尾。使这个函数接受字符串大小来更加通用，并且确保无论什么情况下字符串都以`'\0'`结尾。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：scanf/fgets 的合法/格式错误/长输入/EOF 路径均记录，缓冲区终止正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-25-base"></a>

### LCT-25-BASE 练习25：变参函数

来源：本地原文（原完整交付引用：`<../references/markdown/e279218544f09774.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex25.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习25：变参函数”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：va_list/va_start/va_arg/va_end 类型与数量匹配，正常和错误格式/输入均验证

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-25-break"></a>

### LCT-25-BREAK 如何使它崩溃

来源：本地原文（原完整交付引用：`<../references/markdown/e279218544f09774.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex25.md)

**实现要求**（保留原题的代码、列表及子问）：

这个程序对缓冲区溢出更加健壮，但是和`scanf`一样，它不能够处理输入的格式错误。为了使它崩溃，试着修改代码，把首先传入用于`'%s'`格式的尺寸去掉。同时试着传入多于`MAX_DATA`的数据，之后找到在`read_string`中不使用`calloc`的方法，并且修改它的工作方式。最后还有个问题是`fgets`会吃掉换行符，所以试着使用`fgetc`修复它，要注意字符串结尾应为`'\0'`。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：在可丢弃练习副本复现所列破坏行为，保存诊断/退出码，解释原因并提交修复版；不把故意 UB 的随机表现作为唯一预期。章级交叉检查：va_list/va_start/va_arg/va_end 类型与数量匹配，正常和错误格式/输入均验证

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-25-x01"></a>

### LCT-25-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/e279218544f09774.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex25.md)

**实现要求**（保留原题的代码、列表及子问）：

- 再三检查确保你明白了每个`out_`变量的作用。最重要的是`out_string`，并且它是指针的指针。所以，理清当你设置时获取到的是指针还是内容尤为重要。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：va_list/va_start/va_arg/va_end 类型与数量匹配，正常和错误格式/输入均验证

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-25-x02"></a>

### LCT-25-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/e279218544f09774.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex25.md)

**实现要求**（保留原题的代码、列表及子问）：

- 使用变参系统编写一个和`printf`相似的函数，重新编写`main`来使用它。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：va_list/va_start/va_arg/va_end 类型与数量匹配，正常和错误格式/输入均验证

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-25-x03"></a>

### LCT-25-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/e279218544f09774.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex25.md)

**实现要求**（保留原题的代码、列表及子问）：

- 像往常一样，阅读这些函数/宏的手册页，确保知道了它在你的平台做了什么，一些平台会使用宏而其它平台会使用函数，还有一些平台会让它们不起作用。这完全取决于你所用的编译器和平台。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：va_list/va_start/va_arg/va_end 类型与数量匹配，正常和错误格式/输入均验证

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-27-base"></a>

### LCT-27-BASE 练习27：创造性和防御性编程

来源：本地原文（原完整交付引用：`<../references/markdown/1cc97495fdc24dd0.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex27.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习27：创造性和防御性编程”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：防御性检查能捕获预设故障，断言前提不依赖 UB，说明各策略取舍

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-27-x01"></a>

### LCT-27-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/1cc97495fdc24dd0.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex27.md)

**实现要求**（保留原题的代码、列表及子问）：

- 到现在为止（以及以后）书中的代码都可能违反这些规则。回退并挑选一个练习，将你学到的应用在它上面，来看看你能不能改进它或发现bug。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：防御性检查能捕获预设故障，断言前提不依赖 UB，说明各策略取舍

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-27-x02"></a>

### LCT-27-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/1cc97495fdc24dd0.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex27.md)

**实现要求**（保留原题的代码、列表及子问）：

- 寻找一个开源项目，对其中一些文件进行类似的代码复查。如果你发现了bug，提交一个补丁来修复它。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：防御性检查能捕获预设故障，断言前提不依赖 UB，说明各策略取舍

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-28-base"></a>

### LCT-28-BASE 练习28：Makefile 进阶

来源：本地原文（原完整交付引用：`<../references/markdown/55c7b2897cde101b.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex28.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习28：Makefile 进阶”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：原项目目录/依赖/构建/clean 规则可干净重复执行

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-28-x01"></a>

### LCT-28-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/55c7b2897cde101b.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex28.md)

**实现要求**（保留原题的代码、列表及子问）：

- 尝试通过将源文件和头文件添加进`src/`，来使`Makefile`真正起作用，并且构建出库文件。在源文件中不应该需要`main`函数。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：原项目目录/依赖/构建/clean 规则可干净重复执行

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-28-x02"></a>

### LCT-28-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/55c7b2897cde101b.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex28.md)

**实现要求**（保留原题的代码、列表及子问）：

- 研究`check:`目标会使用`BADFUNCS`的正则表达式来寻找什么函数。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：原项目目录/依赖/构建/clean 规则可干净重复执行

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-28-x03"></a>

### LCT-28-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/55c7b2897cde101b.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex28.md)

**实现要求**（保留原题的代码、列表及子问）：

- 如果你没有做过自动化测试，查询有关资料为以后做准备。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：原项目目录/依赖/构建/clean 规则可干净重复执行

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-29-base"></a>

### LCT-29-BASE 练习29：库和链接

来源：本地原文（原完整交付引用：`<../references/markdown/585a5b80564720bd.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex29.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习29：库和链接”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：静态库/共享库符号与链接/装载路径正确，故意缺库能产生预期失败

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-29-break"></a>

### LCT-29-BREAK 如何使它崩溃

来源：本地原文（原完整交付引用：`<../references/markdown/585a5b80564720bd.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex29.md)

**实现要求**（保留原题的代码、列表及子问）：

打开`lbex29.so`，并且使用能够处理二进制的编辑器编辑它。修改一些字节，然后关闭。看看你是否能使用`dlopen`函数来打开它，即使你修改了它。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：在可丢弃练习副本复现所列破坏行为，保存诊断/退出码，解释原因并提交修复版；不把故意 UB 的随机表现作为唯一预期。章级交叉检查：静态库/共享库符号与链接/装载路径正确，故意缺库能产生预期失败

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-29-x01"></a>

### LCT-29-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/585a5b80564720bd.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex29.md)

**实现要求**（保留原题的代码、列表及子问）：

- 你注意到我在`libex29.c`中写的不良代码了吗？我使用了一个`for`循环来检查`'\0'`的结尾，修改它们使这些函数总是接收字符串长度，并在函数内部使用。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：静态库/共享库符号与链接/装载路径正确，故意缺库能产生预期失败

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-29-x02"></a>

### LCT-29-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/585a5b80564720bd.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex29.md)

**实现要求**（保留原题的代码、列表及子问）：

- 使用项目框架目录，来为这个练习创建新的项目。将`libex29.c`放入`src/`目录，修改`Makefile`使它能够构建`build/libex29.so`。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：静态库/共享库符号与链接/装载路径正确，故意缺库能产生预期失败

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-29-x03"></a>

### LCT-29-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/585a5b80564720bd.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex29.md)

**实现要求**（保留原题的代码、列表及子问）：

- 将`ex29.c`改为`tests/ex29_tests.c`，使它做为单元测试执行。使它能够正常工作，意思是你需要修改它让它加载`build/libex29.so`文件，并且运行上面我手写的测试。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：静态库/共享库符号与链接/装载路径正确，故意缺库能产生预期失败

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-29-x04"></a>

### LCT-29-X04 附加题 / 4

来源：本地原文（原完整交付引用：`<../references/markdown/585a5b80564720bd.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex29.md)

**实现要求**（保留原题的代码、列表及子问）：

- 阅读`man dlopen`文档，并且查询所有有关函数。尝试`dlopen`的其它选项，比如`RTLD_NOW`。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：静态库/共享库符号与链接/装载路径正确，故意缺库能产生预期失败

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-30-base"></a>

### LCT-30-BASE 练习30：自动化测试

来源：本地原文（原完整交付引用：`<../references/markdown/bee2e9921b51461d.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex30.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习30：自动化测试”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：自动化测试有正确/错误对照，失败测试确实使命令返回失败

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-30-x01"></a>

### LCT-30-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/bee2e9921b51461d.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex30.md)

**实现要求**（保留原题的代码、列表及子问）：

- 这段代码能起作用，但是可能有点乱。清理框架目录，是它包含所有这些文件，但是移除任何和练习29有关的代码。你应该能够复制这个目录并且无需很多编辑操作就能开始新的项目。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：自动化测试有正确/错误对照，失败测试确实使命令返回失败

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-30-x02"></a>

### LCT-30-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/bee2e9921b51461d.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex30.md)

**实现要求**（保留原题的代码、列表及子问）：

- 研究`runtests.sh`，并且查询有关`bash`语法的资料，来弄懂它的作用。你能够编写这个脚本的C版本吗？

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：自动化测试有正确/错误对照，失败测试确实使命令返回失败

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-31-base"></a>

### LCT-31-BASE 练习31：代码调试

来源：本地原文（原完整交付引用：`<../references/markdown/265509af28439f32.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex31.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习31：代码调试”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：GDB/Valgrind 等实用调试命令定位原例故障，修复后重跑原用例

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-31-x01"></a>

### LCT-31-X01 附加到进程

来源：本地原文（原完整交付引用：`<../references/markdown/265509af28439f32.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex31.md)

**实现要求**（保留原题的代码、列表及子问）：

`gdb`最实用的功能就是附加到运行中的程序，并且就地调试它的能力。当你拥有一个崩溃的服务器或GUI程序，你通常不需要像之前那样在`gdb`下运行它。而是可以直接启动它，希望它不要马上崩溃，之后附加到它并设置断点。练习的这一部分中我会向你展示怎么做。

当你退出`gdb`之后，如果你停止了`ex31`我希望你重启它，之后开启另一个中断窗口以便于启动`gdb`并附加。进程附加就是你让`gdb`连接到已经运行的程序，以便于你实时监测它。它会挂起程序来让你单步执行，当你执行完之后程序会像往常一样恢复运行。

下面是一段会话，我对`ex31`做了上述事情，单步执行它，之后修改`while`循环并使它退出。



```
$ ps ax | grep ex31
10026 s000  S+     0:00.11 ./ex31
10036 s001  R+     0:00.00 grep ex31

$ gdb ./ex31 10026
GNU gdb 6.3.50-20050815 (Apple version gdb-1705) (Fri Jul  1 10:50:06 UTC 2011)
Copyright 2004 Free Software Foundation, Inc.
GDB is free software, covered by the GNU General Public License, and you are
welcome to change it and/or distribute copies of it under certain conditions.
Type "show copying" to see the conditions.
There is absolutely no warranty for GDB.  Type "show warranty" for details.
This GDB was configured as "x86_64-apple-darwin"...Reading symbols for shared libraries .. done

/Users/zedshaw/projects/books/learn-c-the-hard-way/code/10026: No such file or directory
Attaching to program: `/Users/zedshaw/projects/books/learn-c-the-hard-way/code/ex31', process 10026.
Reading symbols for shared libraries + done
Reading symbols for shared libraries ++........................ done
Reading symbols for shared libraries + done
0x00007fff862c9e42 in __semwait_signal ()

(gdb) break 8
Breakpoint 1 at 0x107babf14: file ex31.c, line 8.

(gdb) break ex31.c:11
Breakpoint 2 at 0x107babf1c: file ex31.c, line 12.

(gdb) cont
Continuing.

Breakpoint 1, main (argc=1, argv=0x7fff677aabd8) at ex31.c:8
8      while(i < 100) {

(gdb) p i
$1 = 0

(gdb) cont
Continuing.

Breakpoint 1, main (argc=1, argv=0x7fff677aabd8) at ex31.c:8
8      while(i < 100) {

(gdb) p i
$2 = 0

(gdb) list
3  
4  int main(int argc, char *argv[])
5  {
6      int i = 0;
7  
8      while(i < 100) {
9          usleep(3000);
10     }
11
12     return 0;

(gdb) set var i = 200

(gdb) p i
$3 = 200

(gdb) next

Breakpoint 2, main (argc=1, argv=0x7fff677aabd8) at ex31.c:12
12     return 0;

(gdb) cont
Continuing.

Program exited normally.
(gdb) quit
$
```


> 注

> 在OSX上你可能会看到输入root密码的GUI输入框，并且即使你输入了密码还是会得到来自`gdb`的“Unable to access task for process-id XXX: (os/kern) failure.”的错误。这种情况下，你需要停止`gdb`和`ex31`程序，并重新启动程序使它工作，只要你成功输入了root密码。

我会遍历整个会话，并且解释我做了什么：

gdb:1

使用`ps`来寻找我想要附加的`ex31`的进程ID。

gdb:5

我使用`gdb ./ex31 PID`来附加到进程，其中`PID`替换为我所拥有的进程ID。

gdb:6-19

`gdb`打印出了一堆关于协议的信息，接着它读取了所有东西。

gdb:21

程序被附加，并且在当前执行点上停止。所以现在我在文件中的第8行使用`break`设置了断点。我假设我这么做的时候，已经在这个我想中断的文件中了。

gdb:24

执行`break`的更好方式，是提供`file.c line`的格式，便于你确保定位到了正确的地方。我在这个`break`中这样做。

gdb:27

我使用`cont`来继续运行，直到我命中了断点。

gdb:30-31

我已到达断点，于是`gdb`打印出我需要了解的变量（`argc`和`argv`），以及停下来的位置，之后打印出断点的行号。

gdb:33-34

我使用`print`的缩写`p`来打印出`i`变量的值，它是0。

gdb:36

继续运行来查看`i`是否改变。

gdb:42

再次打印出`i`，显然它没有变化。

gdb:45-55

使用`list`来查看代码是什么，之后我意识到它不可能退出，因为我没有自增`i`。

gdb:57

确认我的假设是正确的，即`i`需要使用`set`命令来修改为`i = 200`。这是`gdb`最优秀的特性之一，让你“修改”程序来让你快速知道你是否正确。

gdb:59

打印`i`来确保它已改变。

gdb:62

使用`next`来移到下一段代码，并且我发现命中了`ex31.c:12`的断点，所以这意味着`while`循环已退出。我的假设正确，我需要修改`i`。

gdb:67

使用`cont`来继续运行，程序像往常一样退出。

gdb:71

最后我使用`quit`来退出`gdb`。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：GDB/Valgrind 等实用调试命令定位原例故障，修复后重跑原用例

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-31-x02"></a>

### LCT-31-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/265509af28439f32.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex31.md)

**实现要求**（保留原题的代码、列表及子问）：

- 找到一个图形化的调试器，将它与原始的`gdb`相比。它们在本地调试程序时非常有用，但是对于在服务器上调试没有任何意义。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：GDB/Valgrind 等实用调试命令定位原例故障，修复后重跑原用例

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-31-x03"></a>

### LCT-31-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/265509af28439f32.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex31.md)

**实现要求**（保留原题的代码、列表及子问）：

- 你可以开启OS上的“核心转储”，当程序崩溃时你会得到一个核心文件。这个核心文件就像是对程序的解剖，便于你了解崩溃时发生了什么，以及由什么原因导致。修改`ex31.c`使它在几个迭代之后崩溃，之后尝试得到它的核心转储并分析。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：GDB/Valgrind 等实用调试命令定位原例故障，修复后重跑原用例

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-32-base"></a>

### LCT-32-BASE 练习32：双向链表

来源：本地原文（原完整交付引用：`<../references/markdown/1434800391620f1d.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex32.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习32：双向链表”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：双向链表 push/pop/shift/unshift/remove 等操作及空链/首尾/单节点不变量正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-32-x01"></a>

### LCT-32-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/1434800391620f1d.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex32.md)

**实现要求**（保留原题的代码、列表及子问）：

- 研究双向和单向链表，以及什么情况下其中一种优于另一种。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：双向链表 push/pop/shift/unshift/remove 等操作及空链/首尾/单节点不变量正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-32-x02"></a>

### LCT-32-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/1434800391620f1d.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex32.md)

**实现要求**（保留原题的代码、列表及子问）：

- 研究双向链表的限制。例如，虽然它们对于插入和删除元素很高效，但是对于变量元素比较慢。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：双向链表 push/pop/shift/unshift/remove 等操作及空链/首尾/单节点不变量正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-32-x03"></a>

### LCT-32-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/1434800391620f1d.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex32.md)

**实现要求**（保留原题的代码、列表及子问）：

- 还缺少什么你能想到的操作？比如复制、连接、分割等等。实现这些操作，并且为它们编写单元测试。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：双向链表 push/pop/shift/unshift/remove 等操作及空链/首尾/单节点不变量正确

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-33-base"></a>

### LCT-33-BASE 练习33：链表算法

来源：本地原文（原完整交付引用：`<../references/markdown/72876ab4a5a374d8.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex33.md)

**实现要求**（保留原题的代码、列表及子问）：

阅读并理解“练习33：链表算法”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：链表排序/搜索等原例算法与独立参考一致，比较复杂度与数据结构限制

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-33-x01"></a>

### LCT-33-X01 附加题 / 1

来源：本地原文（原完整交付引用：`<../references/markdown/72876ab4a5a374d8.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex33.md)

**实现要求**（保留原题的代码、列表及子问）：

- 创建单元测试来比较这两个算法的性能。你需要`man 3 time`来查询基本的时间函数，并且需要运行足够的迭代次数，至少以几秒钟作为样本。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：链表排序/搜索等原例算法与独立参考一致，比较复杂度与数据结构限制

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-33-x02"></a>

### LCT-33-X02 附加题 / 2

来源：本地原文（原完整交付引用：`<../references/markdown/72876ab4a5a374d8.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex33.md)

**实现要求**（保留原题的代码、列表及子问）：

- 改变需要排序的链表中的数据总量，看看耗时如何变化。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：链表排序/搜索等原例算法与独立参考一致，比较复杂度与数据结构限制

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-33-x03"></a>

### LCT-33-X03 附加题 / 3

来源：本地原文（原完整交付引用：`<../references/markdown/72876ab4a5a374d8.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex33.md)

**实现要求**（保留原题的代码、列表及子问）：

- 寻找方法来创建不同长度的随机链表，并且测量需要多少时间，之后将它可视化并与算法的描述对比。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：链表排序/搜索等原例算法与独立参考一致，比较复杂度与数据结构限制

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-33-x04"></a>

### LCT-33-X04 附加题 / 4

来源：本地原文（原完整交付引用：`<../references/markdown/72876ab4a5a374d8.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex33.md)

**实现要求**（保留原题的代码、列表及子问）：

- 尝试解释为什么对链表排序十分麻烦。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：链表排序/搜索等原例算法与独立参考一致，比较复杂度与数据结构限制

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-33-x05"></a>

### LCT-33-X05 附加题 / 5

来源：本地原文（原完整交付引用：`<../references/markdown/72876ab4a5a374d8.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex33.md)

**实现要求**（保留原题的代码、列表及子问）：

- 实现`List_insert_sorted`（有序链表），它使用`List_compare`，接收一个值，将其插入到正确的位置，使链表有序。它与创建链表后再进行排序相比怎么样？

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：链表排序/搜索等原例算法与独立参考一致，比较复杂度与数据结构限制

归类：E3 指定，附加题也按 E3 要求纳入。

<a id="lct-33-x06"></a>

### LCT-33-X06 附加题 / 6

来源：本地原文（原完整交付引用：`<../references/markdown/72876ab4a5a374d8.md>`） · [translator-published GitBook source; commit 331debee3bcd69a1a79cdc99ad5f476d991acfd2 在线原文](https://raw.githubusercontent.com/wizardforcel/lcthw-zh/331debee3bcd69a1a79cdc99ad5f476d991acfd2/ex33.md)

**实现要求**（保留原题的代码、列表及子问）：

- 尝试实现维基百科上“自底向上”的归并排序。上面的代码已经是C写的了，所以很容易重新创建，但是要试着理解它的工作原理，并与这里的低效版本对比。

**交付物**：本题 C/头文件/Makefile 或分析笔记；Linux 编译、运行、GDB/Valgrind 等本项所需日志；原例与变体分开保存。

**验收条件**（自验）：逐条完成本项原题所有子问；比较原例与修改版，给可复现实验、错误输入/边界及理由。章级交叉检查：链表排序/搜索等原例算法与独立参考一致，比较复杂度与数据结构限制

归类：E3 指定，附加题也按 E3 要求纳入。
