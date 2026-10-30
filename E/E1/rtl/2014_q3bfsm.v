// HDL-143 Q3b: FSM
// Source: https://hdlbits.01xz.net/wiki/exams/2014_q3bfsm
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire reset,
  input wire x,
  output wire z
);
reg[2:0]state,next_state;always @* begin case(state)0:next_state=x?1:0;1:next_state=x?4:1;2:next_state=x?1:2;3:next_state=x?2:1;4:next_state=x?4:3;default:next_state=0;endcase end always @(posedge clk)if(reset)state<=0;else state<=next_state;assign z=(state==3)||(state==4);
endmodule

`default_nettype wire
