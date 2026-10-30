// HDL-102 Slow decade counter
// Source: https://hdlbits.01xz.net/wiki/countslow
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire slowena,
  input wire reset,
  output wire [3:0] q
);
reg[3:0]count;assign q=count;always @(posedge clk)if(reset)count<=4'd0;else if(slowena) count <= (count == 4'd9) ? 4'd0 : count + 4'd1;
endmodule

`default_nettype wire
