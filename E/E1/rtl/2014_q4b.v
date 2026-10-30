// HDL-114 Shift register
// Source: https://hdlbits.01xz.net/wiki/exams/2014_q4b
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [3:0] SW,
  input wire [3:0] KEY,
  output wire [3:0] LEDR
);
MUXDFF u3(KEY[0],KEY[3],SW[3],KEY[1],KEY[2],LEDR[3]);MUXDFF u2(KEY[0],LEDR[3],SW[2],KEY[1],KEY[2],LEDR[2]);MUXDFF u1(KEY[0],LEDR[2],SW[1],KEY[1],KEY[2],LEDR[1]);MUXDFF u0(KEY[0],LEDR[1],SW[0],KEY[1],KEY[2],LEDR[0]);
endmodule
module MUXDFF(input clk,w,R,E,L,output reg Q);always @(posedge clk)if(L)Q<=R;else if(E)Q<=w;endmodule
`default_nettype wire
