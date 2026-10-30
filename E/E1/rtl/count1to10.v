// HDL-101 Decade counter again
// Source: https://hdlbits.01xz.net/wiki/count1to10
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire reset,
  output wire [3:0] q
);
reg[3:0]count;assign q=count;always @(posedge clk)if(reset)count<=4'd1;else  count <= (count == 4'd10) ? 4'd1 : count + 4'd1;
endmodule

`default_nettype wire
