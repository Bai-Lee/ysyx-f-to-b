if {[catch {
read_liberty {/home/USER/tools/icsprout55-e-stage/IP/STD_cell/ics55_LLSC_H7C_V1p10C100/ics55_LLSC_H7CR/liberty/ics55_LLSC_H7CR_typ_tt_1p2_25_nldm.lib}
read_liberty {/home/USER/tools/icsprout55-e-stage/IP/STD_cell/ics55_LLSC_H7C_V1p10C100/ics55_LLSC_H7CL/liberty/ics55_LLSC_H7CL_typ_tt_1p2_25_nldm.lib}
read_verilog {/workspace/projects/ysyx_f_to_b/C/C4/synthesis/axi/mapped.v}
link_design c4_axi_core
read_sdc {/workspace/projects/ysyx_f_to_b/C/C4/synthesis/axi/model.sdc}
check_setup -verbose
puts "C4_SETUP_BEGIN"
report_checks -path_delay max -group_count 1 -endpoint_count 1 -digits 6
report_worst_slack -digits 6
puts "C4_SETUP_END"
puts "C4_HOLD_BEGIN"
report_checks -path_delay min -group_count 1 -endpoint_count 1 -digits 6
puts "C4_HOLD_END"
puts "C4_STA_COMPLETE"
} message]} {puts stderr "C4_STA_ERROR $message"; exit 1}
exit
