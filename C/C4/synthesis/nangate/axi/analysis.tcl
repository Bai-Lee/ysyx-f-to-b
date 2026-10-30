read_liberty {/workspace/projects/ysyx_f_to_b/C/C4/models/nangate45/NangateOpenCellLibrary_typical.lib}
read_verilog {/workspace/projects/ysyx_f_to_b/C/C4/synthesis/nangate/axi/sta-netlist.v}
link_design c4_axi_core
read_sdc {/workspace/projects/ysyx_f_to_b/C/C4/synthesis/nangate/axi/model.sdc}
check_setup -verbose
report_checks -path_delay max -group_count 1 -digits 6
report_worst_slack -digits 6
puts "HOLD_BEGIN"
report_checks -path_delay min -group_count 1 -digits 6
puts "TRANSITION_BEGIN"
report_check_types -max_transition -all_violators -no_line_splits -digits 6
puts "NANGATE_STA_DONE"
exit
