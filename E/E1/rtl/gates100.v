// HDL-039 Reduction: Even wider gates
// Source: https://hdlbits.01xz.net/wiki/gates100
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [99:0] in,
  output wire out_and,
  output wire out_or,
  output wire out_xor
);
assign out_and=&in;assign out_or=|in;assign out_xor=^in;
endmodule

`default_nettype wire
