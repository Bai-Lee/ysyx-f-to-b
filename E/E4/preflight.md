# E4 preflight

任务：v26.07 E4 的17项核心要求、NJU实验2/3/6/7/8的16个细项（含1个明确高级选做）以及8项约束与3项背景/选做。源资料只读，复制后实现；不使用Logisim computer use。

已核对根AGENTS、工具锁及TOOLCHAIN_READY、E3实际审计。当前宿主可用内存7.55GiB，WSL2上限2GiB、4vCPU、2GiB swap；一次一个编译重任务，Verilator自身源码构建-j1，其余最多-j2，不使用-j0或nproc自动并发。

缺少Linux Verilator和SDL开发依赖；Windows套件仍保留，不能把Windows验收当作Linux验收。按官方安装说明从固定stable Git版本构建私有Linux工具；NVBoard复用已归档官方仓库。WSL没有DISPLAY/WSLg，采用隔离Xvfb显示服务实际运行NVBoard/GTKWave、发送交互事件、保存真实界面截图；这是虚拟显示和虚拟FPGA，非实体上板。

验证：先官方C++示例和正确/错误XOR；组合逻辑穷举、时序逐拍独立参考、PS/2帧及错误帧、VGA完整帧时序及像素检查；sCPU复用F阶段已验证RTL，另写独立C sEMU，与第三方Python模型对照并对GPR/PC分别注错。用lint及Yosys检查锁存器/触发沿，不报告物理PPA或真实亚稳态。

证据位于artifacts/E4，记录命令/cwd/时间/输入快照/哈希/退出码/输出/资源约束和随机种子。所有正式结论待实际运行；本文件不是PASS结论。
