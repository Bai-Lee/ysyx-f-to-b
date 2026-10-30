// HDL-094 Create circuit from truth table
// Source: https://hdlbits.01xz.net/wiki/exams/ece241_2013_q7
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire j,
  input wire k,
  output wire Q
);
reg stored,next_d;assign Q=stored;always @* begin case({j,k})2'b00:next_d=stored;2'b01:next_d=0;2'b10:next_d=1;2'b11:next_d=~stored;default:next_d=1'bx;endcase end always @(posedge clk)stored<=next_d;
endmodule

`default_nettype wire
