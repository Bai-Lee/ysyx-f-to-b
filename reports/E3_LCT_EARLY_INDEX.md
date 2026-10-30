# 历史1GiB检查点：LCTHW 0–9逐项验收

本文件保留早期部分结果；当前完整结果见 [E3_TASKS.md](E3_TASKS.md)。LCT-04-BASE源码构建现已完成，旧RESOURCE_LIMIT不代表当前状态。

共54项：PASS 48，PASS_ADAPTED 5，RESOURCE_LIMIT 1。剩余章节126项未执行。

每条需求全文在[E3冻结清单（补充包：E/E3/course_specs.json）](https://github.com/Bai-Lee/ysyx-f-to-b/releases/tag/v1.0.0)，[实现说明与勘误](../E/E3/lcthw/notes/00-09.md)逐章解释。PASS在故意错误实验中表示错误得到正确复现/记录，不表示错误程序正确。

| 项目 | 实现要求（原文首段） | 交付物与验收 | 状态 |
|---|---|---|
| LCT-00-BASE | 阅读并理解“练习0：准备”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-01-BASE | 阅读并理解“练习1：启用编译器”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-01-BREAK | 在这本书中我会添加一个小节，关于如何使程序崩溃。我会让你对程序做一些奇怪的事情，以奇怪的方式运行，或者修改代码，以便让你看到崩溃和编译器错误。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-01-X01 | - 在你的文本编辑器中打开`ex1`文件，随机修改或删除一部分，之后运行它看看发生了什么。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-01-X02 | - 再多打印5行文本或者其它比`"Hello world."`更复杂的东西。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-01-X03 | - 执行`man 3 puts`来阅读这个函数和其它函数的文档。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-02-BASE | 阅读并理解“练习2：用Make来代替Python”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-02-BREAK | 上面那些已经足够让你起步了，但是让我们以一种特定的方式来破坏make文件，以便你可以看到发生了什么。找到`rm -f ex1`的那一行并去掉缩进（让它左移），之后你可以看到发生了什么。再次运行`make clean`，你就会得到下面的信息： | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-02-X01 | - 创建目标`all:ex1`，可以以单个命令`make`构建`ex1`。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-02-X02 | - 阅读`man make`来了解关于如何执行它的更多信息。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-02-X03 | - 阅读`man cc`来了解关于`-Wall`和`-g`行为的更多信息。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-02-X04 | - 在互联网上搜索Makefile文件，看看你是否能改进你的文件。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-02-X05 | - 在另一个C语言项目中找到`Makefile`文件，并且尝试理解它做了什么。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-03-BASE | 阅读并理解“练习3：格式化输出”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-03-BREAK | 尝试下面的一些东西来使你的程序崩溃，在你的电脑上它们可能会崩溃，也可能不会。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-03-X01 | - 找到尽可能多的方法使`ex3`崩溃。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-03-X02 | - 执行`man 3 printf`来阅读其它可用的'%'格式化占位符。如果你在其它语言中使用过它们，应该看着非常熟悉（它们来源于`printf`）。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-03-X03 | - 将`ex3`添加到你的`Makefile`的`all`列表中。到目前为止，可以使用`make clean all`来构建你所有的练习。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-03-X04 | - 将`ex3`添加到你的`Makefile`的`clean`列表中。当你需要的时候使用`make clean`可以删除它。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-04-BASE | 阅读并理解“练习4：Valgrind 介绍”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。 | 例程及修复已运行；Valgrind完整源码构建暂缓；见[证据索引](E3_LCT_early_task_status.json) | RESOURCE_LIMIT |
| LCT-04-X01 | - 按照上面的指导，使用`Valgrind`和编译器修复这个程序。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-04-X02 | - 在互联网上查询`Valgrind`相关的资料。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-04-X03 | - 下载另一个程序并手动构建它。尝试一些你已经使用，但从来没有手动构建的程序。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-04-X04 | - 看看`Valgrind`的源码是如何在目录下组织的，并且阅读它的Makefile文件。不要担心，这对我来说没有任何意义。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-05-BASE | 阅读并理解“练习5：一个C程序的结构”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-05-X01 | - 对于每一行，写出你不理解的符号，并且看看是否能猜出它们的意思。在纸上写下你的猜测，你可以在以后检查它，看看是否正确。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS_ADAPTED |
| LCT-05-X02 | - 回头去看之前几个练习的源代码，并且像这样分解代码，来看看你是否了解它们。写下你不了解和不能自己解释的东西。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-06-BASE | 阅读并理解“练习6：变量类型”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS_ADAPTED |
| LCT-06-BREAK | 你可以通过向`printf`传递错误的参数来轻易使这个程序崩溃。例如，如果你找到打印我的名字的那行，把`initial`放到`first_name`前面，你就制造了一个bug。执行上述修改编译器就会向你报错，之后运行的时候你可能会得到一个“段错误”，就像这样： | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-06-X01 | - 寻找其他通过修改`printf`使这段C代码崩溃的方法。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-06-X02 | - 搜索“`printf`格式化”，试着使用一些高级的占位符。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-06-X03 | - 研究可以用几种方法打印数字。尝试以八进制或十六进制打印，或者其它你找到的方法。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-06-X04 | - 试着打印空字符串，即`""`。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-07-BASE | 阅读并理解“练习7：更多变量和一些算术”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS_ADAPTED |
| LCT-07-BREAK | 像之前一样，向`printf`传入错误的参数来使它崩溃。对比`%c`，看看当你使用`%s`来打印`nul_byte`变量时会发生什么。做完这些之后，在`Valgrind`下运行它看看关于你的这次尝试会输出什么。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-07-X01 | - 把为`universe_of_defects`赋值的数改为不同的大小，观察编译器的警告。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-07-X02 | - 这些巨大的数字实际上打印成了什么？ | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-07-X03 | - 将`long`改为`unsigned long`，并试着找到对它来说太大的数字。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-07-X04 | - 上网搜索`unsigned`做了什么。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-07-X05 | - 试着自己解释（在下个练习之前）为什么`char`可以和`int`相乘。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-08-BASE | 阅读并理解“练习8：大小和数组”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS_ADAPTED |
| LCT-08-BREAK | 使这个程序崩溃非常容易，只需要尝试下面这些事情： | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-08-X01 | - 尝试使用`areas[0] = 100;`以及相似的操作对`areas`的元素赋值。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-08-X02 | - 尝试对`name`和`full_name`的元素赋值。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-08-X03 | - 尝试将`areas`的一个元素赋值为`name`中的字符。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-08-X04 | - 上网搜索在不同的CPU上整数所占的不同大小。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-09-BASE | 阅读并理解“练习9：数组和字符串”，在 Linux 编译运行原例，核对“你会看到什么”，解释代码及所用工具。没有代码的章节完成对应环境/方法操作。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-09-BREAK | C中所有bug的大多数来源都是忘了预留出足够的空间，或者忘了在字符串末尾加上一个`'\0'`。事实上，这些bug是非常普遍并且难以改正的，大部分优秀的C代码都不会使用C风格字符串。下一个练习中我们会学到如何彻底避免C风格字符串。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-09-X01 | - 将一些字符赋给`numbers`的元素，之后用`printf`一次打印一个字符，你会得到什么编译器警告？ | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-09-X02 | - 对`names`执行上述的相反操作，把`names`当成`int`数组，并一次打印一个`int`，`Valgrind`会提示什么？ | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-09-X03 | - 有多少种其它的方式可以用来打印它？ | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-09-X04 | - 如果一个字符数组占四个字节，一个整数也占4个字节，你可以像整数一样使用整个`name`吗？你如何用黑魔法实现它？ | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
| LCT-09-X05 | - 拿出一张纸，将每个数组画成一排方框，之后在纸上画出代码中的操作，看看是否正确。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS_ADAPTED |
| LCT-09-X06 | - 将`name`转换成`another`的形式，看看代码是否能正常工作。 | 原始/派生C、真实日志、独立预期或错误诊断、逐章解释；见[证据索引](E3_LCT_early_task_status.json) | PASS |
