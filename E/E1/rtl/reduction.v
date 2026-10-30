// HDL-038 Reduction operators
// Source: https://hdlbits.01xz.net/wiki/reduction
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [7:0] in,
  output wire parity
);
assign parity=^in;
endmodule

`default_nettype wire
