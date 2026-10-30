// HDL-008 XNOR gate
// Source: https://hdlbits.01xz.net/wiki/xnorgate
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire a,
  input wire b,
  output wire out
);
assign out = ~(a ^ b);
endmodule

`default_nettype wire
