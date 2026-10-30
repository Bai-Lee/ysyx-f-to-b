if {[catch {
read_liberty {/home/USER/tools/icsprout55-e-stage/IP/STD_cell/ics55_LLSC_H7C_V1p10C100/ics55_LLSC_H7CL/liberty/ics55_LLSC_H7CL_typ_tt_1p2_25_nldm.lib}
read_verilog {/workspace/projects/ysyx_f_to_b/C/C4/synthesis/opensta/control.v}
link_design control
create_clock -name clk -period 10 [get_ports clock]
set_load 0.005 [get_ports q]
report_checks -path_delay max -digits 6
report_worst_slack -digits 6
puts "STA_SCRIPT_COMPLETE"
} message]} {puts stderr "STA_SCRIPT_ERROR $message"; exit 1}
exit
