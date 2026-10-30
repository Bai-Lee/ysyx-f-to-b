// HDL-032 If statement latches
// Source: https://hdlbits.01xz.net/wiki/always_if2
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire cpu_overheated,
  output reg shut_off_computer,
  input wire arrived,
  input wire gas_tank_empty,
  output reg keep_driving
);
always @* begin if(cpu_overheated)shut_off_computer=1;else shut_off_computer=0;if(!arrived && !gas_tank_empty)keep_driving=1;else keep_driving=0;end
endmodule

`default_nettype wire
