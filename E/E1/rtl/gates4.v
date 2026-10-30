// HDL-015 Four-input gates
// Source: https://hdlbits.01xz.net/wiki/gates4
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [3:0] in,
  output wire out_and,
  output wire out_or,
  output wire out_xor
);
assign out_and=&in;assign out_or=|in;assign out_xor=^in;
endmodule

`default_nettype wire
