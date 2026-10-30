// HDL-097 Edge capture register
// Source: https://hdlbits.01xz.net/wiki/edgecapture
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire reset,
  input wire [31:0] in,
  output wire [31:0] out
);
reg[31:0]previous,captured;assign out=captured;always @(posedge clk)begin previous<=in;if(reset)captured<=32'b0;else captured<=captured|(previous&~in);end
endmodule

`default_nettype wire
