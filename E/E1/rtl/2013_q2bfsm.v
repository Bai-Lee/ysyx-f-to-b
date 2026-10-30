// HDL-151 Q2b: Another FSM
// Source: https://hdlbits.01xz.net/wiki/exams/2013_q2bfsm
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire resetn,
  input wire x,
  input wire y,
  output wire f,
  output wire g
);
localparam A=0,B=1,C=2,D=3,E=4,F=5,G=6,H=7,I=8;reg[3:0]state,next_state;
always @* begin case(state)
A:next_state=B;B:next_state=C;C:next_state=x?D:C;D:next_state=x?D:E;E:next_state=x?F:C;
F:next_state=y?H:G;G:next_state=y?H:I;H:next_state=H;I:next_state=I;default:next_state=A;endcase end
always @(posedge clk)if(!resetn)state<=A;else state<=next_state;
assign f=(state==B);assign g=(state==F)||(state==G)||(state==H);
endmodule

`default_nettype wire
