# Remaining E-stage preflight

用户要求继续完成E阶段全部剩余工作，范围E5–E9：96个清单节点。E1–E4历史证据保留，E9个人报名/答辩材料按既有授权排除。目标包含真实minirv执行、AM测试、SimpleBus/官方SoC、综合及公开物理设计流程；当前不宣称任何新任务已通过。

已重新读取根AGENTS、工具锁、TOOLCHAIN_READY和E4审计；E4的Linux工具指纹和运行目录核对通过。WSL2维持2GiB/4vCPU/2GiB swap；当前宿主可用3.52GiB，重任务串行、编译默认-j1或-j2。低于3GiB时暂停新重任务，不杀用户其他程序。使用PDF技能读取已有官方ISA手册，不改原文件。

已有：Verilator5.052、Icarus、GCC/G++、GTKWave、NVBoard、Windows Yosys等。新需要：官方RISC-V交叉工具、ECC/ECOS及与讲义一致的标准单元数据。安装/下载只用官方源；GitHub连接器用于版本/资产元数据，二进制通过官方资产URL下载并比较其发布摘要。尽量使用D盘，Linux文件位于D盘WSL磁盘中。

架构边界：E5为16个32位GPR、8条核心minirv指令及测试终止ebreak，不能添加别的指令替代编译转换。仿真包装层与可综合DUT分开。E7才加入所需CSR；所有32位地址对外可达。同步状态只用posedge，复位与提交边界明确。

验证分层：手工边界程序→独立C/Python参考→RTL逐提交DiffTest与注错→官方程序集→延迟/SoC→综合网表二/四态→物理工具实际检查。运行时墙钟、假设CPU频率、库/约束下STA及后端结果分别报告，不将生成GDS等同于制造成功。
