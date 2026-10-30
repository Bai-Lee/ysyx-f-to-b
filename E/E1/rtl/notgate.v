// HDL-005 Inverter
// Source: https://hdlbits.01xz.net/wiki/notgate
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire in,
  output wire out
);
assign out = ~in;
endmodule

`default_nettype wire
