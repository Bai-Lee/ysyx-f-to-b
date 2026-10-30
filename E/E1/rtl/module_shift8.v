// HDL-024 Modules and vectors
// Source: https://hdlbits.01xz.net/wiki/module_shift8
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire [7:0] d,
  input wire [1:0] sel,
  output wire [7:0] q
);
wire[7:0]q1,q2,q3;my_dff8 u0(clk,d,q1);my_dff8 u1(clk,q1,q2);my_dff8 u2(clk,q2,q3);assign q=sel==0?d:sel==1?q1:sel==2?q2:q3;
endmodule

`default_nettype wire
