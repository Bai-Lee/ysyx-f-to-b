create_clock -name clk -period 3.076923076923 [get_ports clock]
set_clock_transition 0.02 [get_clocks clk]
set inputs {}
foreach p [all_inputs] {if {[get_full_name $p] ne "clock"} {lappend inputs $p}}
set_input_delay -clock clk -max 0.1 $inputs
set_input_delay -clock clk -min 0.05 $inputs
set_input_transition 0.02 $inputs
set_output_delay -clock clk -max 0.1 [all_outputs]
set_output_delay -clock clk -min 0 [all_outputs]
set_load 5 [all_outputs]
