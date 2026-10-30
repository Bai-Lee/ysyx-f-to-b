set_units -time ns -capacitance pF
create_clock -name clk -period 10.0 [get_ports clock]
set_clock_transition 0.1 [get_clocks clk]
set data_inputs {}
foreach p [all_inputs] {if {[get_full_name $p] ne "clock"} {lappend data_inputs $p}}
set_input_delay -clock clk -max 1.0 $data_inputs
set_input_delay -clock clk -min 0.1 $data_inputs
set_input_transition 0.1 $data_inputs
set_output_delay -clock clk -max 1.0 [all_outputs]
set_output_delay -clock clk -min 0.0 [all_outputs]
set_load 0.005 [all_outputs]
