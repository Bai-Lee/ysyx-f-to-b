// HDL-014 Bitwise operators
// Source: https://hdlbits.01xz.net/wiki/vectorgates
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [2:0] a,
  input wire [2:0] b,
  output wire [2:0] out_or_bitwise,
  output wire out_or_logical,
  output wire [5:0] out_not
);
assign out_or_bitwise=a|b;assign out_or_logical=a||b;assign out_not={~b,~a};
endmodule

`default_nettype wire
