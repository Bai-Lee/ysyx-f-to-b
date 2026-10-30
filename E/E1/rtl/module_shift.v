// HDL-023 Three modules
// Source: https://hdlbits.01xz.net/wiki/module_shift
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire d,
  output wire q
);
wire q1,q2;my_dff u0(clk,d,q1);my_dff u1(clk,q1,q2);my_dff u2(clk,q2,q);
endmodule

`default_nettype wire
