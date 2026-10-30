// HDL-003 Simple wire
// Source: https://hdlbits.01xz.net/wiki/wire
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire in,
  output wire out
);
assign out = in;
endmodule

`default_nettype wire
