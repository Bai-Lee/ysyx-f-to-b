// HDL-141 Q5b: Serial two's complementer (Mealy FSM)
// Source: https://hdlbits.01xz.net/wiki/exams/ece241_2014_q5b
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire areset,
  input wire x,
  output wire z
);
localparam A=2'b01,B=2'b10;reg[1:0]state,next_state;
always @* begin next_state[0]=state[0]&~x;next_state[1]=state[1]|(state[0]&x);end
always @(posedge clk or posedge areset)if(areset)state<=A;else state<=next_state;
assign z=(state[0]&x)|(state[1]&~x);
endmodule

`default_nettype wire
