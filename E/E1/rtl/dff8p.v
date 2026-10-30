// HDL-084 DFF with reset value
// Source: https://hdlbits.01xz.net/wiki/dff8p
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire reset,
  input wire [7:0] d,
  output wire [7:0] q
);
reg[7:0]value;assign q=value;always @(negedge clk)if(reset)value<=8'h34;else value<=d;
endmodule

`default_nettype wire
