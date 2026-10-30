// HDL-096 Detect both edges
// Source: https://hdlbits.01xz.net/wiki/edgedetect2
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire [7:0] in,
  output wire [7:0] anyedge
);
reg[7:0]previous,result;assign anyedge=result;always @(posedge clk)begin previous<=in;result<=in^previous;end
endmodule

`default_nettype wire
