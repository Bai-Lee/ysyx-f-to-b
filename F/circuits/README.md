# F阶段电路文件

- `fundamentals.circ`：33个已验证电路，最终批量运行25753向量；以 `config/F_circuit_jobs.json` 的电路名/任务ID映射为准。
- `preflight.circ`、`hierarchy_control.circ`：工具的正反对照、分线器及自定义层次端口预检。
- `tutorial_reference_complete.circ`：紧凑XOR参考交付，四种输入实际验证。
- `tutorial_missing_output_fault.circ`：故意缺输出线，预期失败；用于确认检查器能拒绝错误电路。
- `tutorial_gui_unfinished.circ`：早期GUI工作副本，后来被工具恢复了GUI自动存档；文件名不能作为其状态依据。它不参与最终33电路生产验收。严格验证器现在只读指定字节，禁用自动恢复路径。

用户已要求停止computer-use操作Logisim。后续不需要打开GUI；命令行批量重放约数秒。F5/F6处理器交付在 `F/rtl`，采用用户允许的RTL路线。
