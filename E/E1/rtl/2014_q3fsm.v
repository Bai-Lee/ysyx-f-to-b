// HDL-142 Q3a: FSM
// Source: https://hdlbits.01xz.net/wiki/exams/2014_q3fsm
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire reset,
  input wire s,
  input wire w,
  output wire z
);
localparam A=0,B=1,C=2,D=3,E=4,F=5,G=6,H=7;reg[2:0]state,next_state;
always @* begin case(state)
A:next_state=s?B:A;B,H:next_state=w?D:C;C:next_state=w?F:E;D:next_state=w?G:F;
E:next_state=B;F:next_state=w?H:B;G:next_state=w?B:H;default:next_state=A;endcase end
always @(posedge clk)if(reset)state<=A;else state<=next_state;
assign z=(state==H);
endmodule

`default_nettype wire
