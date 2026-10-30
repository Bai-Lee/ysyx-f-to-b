// HDL-021 Connecting ports by position
// Source: https://hdlbits.01xz.net/wiki/module_pos
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire a,
  input wire b,
  input wire c,
  input wire d,
  output wire out1,
  output wire out2
);
mod_a u(out1,out2,a,b,c,d);
endmodule

`default_nettype wire
