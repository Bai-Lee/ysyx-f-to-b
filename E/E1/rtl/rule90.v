// HDL-116 Rule 90
// Source: https://hdlbits.01xz.net/wiki/rule90
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire load,
  input wire [511:0] data,
  output wire [511:0] q
);
reg[511:0]cells;assign q=cells;always @(posedge clk)if(load)cells<=data;else cells<={1'b0,cells[511:1]}^{cells[510:0],1'b0};
endmodule

`default_nettype wire
