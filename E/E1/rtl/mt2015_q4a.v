// HDL-053 Simple circuit A
// Source: https://hdlbits.01xz.net/wiki/mt2015_q4a
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire x,
  input wire y,
  output wire z
);
assign z=(x^y)&x;
endmodule

`default_nettype wire
