// HDL-029 Always blocks (combinational)
// Source: https://hdlbits.01xz.net/wiki/alwaysblock1
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire a,
  input wire b,
  output wire out_assign,
  output reg out_alwaysblock
);
assign out_assign=a&b;always @* out_alwaysblock=a&b;
endmodule

`default_nettype wire
