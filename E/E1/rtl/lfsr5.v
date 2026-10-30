// HDL-110 5-bit LFSR
// Source: https://hdlbits.01xz.net/wiki/lfsr5
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire reset,
  output wire [4:0] q
);
reg[4:0]value;assign q=value;always @(posedge clk)if(reset)value<=5'b00001;else value<={value[0],value[4],value[3]^value[0],value[2:1]};
endmodule

`default_nettype wire
