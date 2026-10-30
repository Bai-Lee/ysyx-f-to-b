// HDL-081 D flip-flop
// Source: https://hdlbits.01xz.net/wiki/dff
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire d,
  output reg q
);
always @(posedge clk)q<=d;
endmodule

`default_nettype wire
