read_liberty {/workspace/projects/ysyx_f_to_b/C/C4/models/nangate45/NangateOpenCellLibrary_typical.lib}
read_verilog {/workspace/projects/ysyx_f_to_b/C/C4/synthesis/nangate/control.v}
link_design control
create_clock -name clk -period 0.001 [get_ports clock]
set_input_delay -clock clk 1 [get_ports a]
set_output_delay -clock clk 1 [get_ports y]
report_worst_slack -digits 6
puts "NANGATE_CONTROL_DONE"
exit
