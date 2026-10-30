// HDL-145 Q6b: FSM next-state logic
// Source: https://hdlbits.01xz.net/wiki/exams/m2014_q6b
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [3:1] y,
  input wire w,
  output wire Y2
);
reg[2:0]next_state;always @* begin case(y)0:next_state=w?0:1;1:next_state=w?3:2;2:next_state=w?3:4;3:next_state=w?0:5;4:next_state=w?3:4;5:next_state=w?3:2;default:next_state=0;endcase end assign Y2=next_state[1];
endmodule

`default_nettype wire
