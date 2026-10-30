// HDL-098 Dual-edge triggered flip-flop
// Source: https://hdlbits.01xz.net/wiki/dualedge
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire d,
  output wire q
);
reg rising,falling;always @(posedge clk)rising<=d;always @(negedge clk)falling<=d;assign q=clk?rising:falling;
endmodule

`default_nettype wire
