// HDL-030 Always blocks (clocked)
// Source: https://hdlbits.01xz.net/wiki/alwaysblock2
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire a,
  input wire b,
  output wire out_assign,
  output reg out_always_comb,
  output reg out_always_ff
);
assign out_assign=a^b;always @* out_always_comb=a^b;always @(posedge clk)out_always_ff<=a^b;
endmodule

`default_nettype wire
