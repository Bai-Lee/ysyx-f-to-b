// HDL-115 3-input LUT
// Source: https://hdlbits.01xz.net/wiki/exams/ece241_2013_q12
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire enable,
  input wire S,
  input wire A,
  input wire B,
  input wire C,
  output wire Z
);
reg[7:0]storage;always @(posedge clk)if(enable)storage<={storage[6:0],S};assign Z=storage[{A,B,C}];
endmodule

`default_nettype wire
