// HDL-086 DFF with byte enable
// Source: https://hdlbits.01xz.net/wiki/dff16e
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire resetn,
  input wire [1:0] byteena,
  input wire [15:0] d,
  output wire [15:0] q
);
reg[15:0]value;assign q=value;always @(posedge clk)begin if(!resetn)value<=16'h0;else begin if(byteena[0])value[7:0]<=d[7:0];if(byteena[1])value[15:8]<=d[15:8];end end
endmodule

`default_nettype wire
