// HDL-085 DFF with asynchronous reset
// Source: https://hdlbits.01xz.net/wiki/dff8ar
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire areset,
  input wire [7:0] d,
  output wire [7:0] q
);
reg[7:0]value;assign q=value;always @(posedge clk or posedge areset)if(areset)value<=8'h00;else value<=d;
endmodule

`default_nettype wire
