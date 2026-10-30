// HDL-091 Mux and DFF
// Source: https://hdlbits.01xz.net/wiki/mt2015_muxdff
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire L,
  input wire r_in,
  input wire q_in,
  output reg Q
);
always @(posedge clk)Q<=L?r_in:q_in;
endmodule

`default_nettype wire
