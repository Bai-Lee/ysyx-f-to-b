// HDL-054 Simple circuit B
// Source: https://hdlbits.01xz.net/wiki/mt2015_q4b
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire x,
  input wire y,
  output wire z
);
assign z=~(x^y);
endmodule

`default_nettype wire
