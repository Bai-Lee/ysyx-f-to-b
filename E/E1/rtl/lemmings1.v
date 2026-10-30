// HDL-128 Lemmings 1
// Source: https://hdlbits.01xz.net/wiki/lemmings1
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire areset,
  input wire bump_left,
  input wire bump_right,
  output wire walk_left,
  output wire walk_right
);
reg right;always @(posedge clk or posedge areset)if(areset)right<=0;else if(right?bump_right:bump_left)right<=~right;assign walk_left=~right;assign walk_right=right;
endmodule

`default_nettype wire
