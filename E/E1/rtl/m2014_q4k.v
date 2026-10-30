// HDL-113 Shift register
// Source: https://hdlbits.01xz.net/wiki/exams/m2014_q4k
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire resetn,
  input wire in,
  output wire out
);
reg[3:0]stages;assign out=stages[3];always @(posedge clk)if(!resetn)stages<=4'b0;else stages<={stages[2:0],in};
endmodule

`default_nettype wire
