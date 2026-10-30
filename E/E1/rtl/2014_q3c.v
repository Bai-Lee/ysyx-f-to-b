// HDL-144 Q3c: FSM logic
// Source: https://hdlbits.01xz.net/wiki/exams/2014_q3c
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire [2:0] y,
  input wire x,
  output wire Y0,
  output wire z
);
wire[2:0]state=y;reg[2:0]next_state;always @* begin case(state)0:next_state=x?1:0;1:next_state=x?4:1;2:next_state=x?1:2;3:next_state=x?2:1;4:next_state=x?4:3;default:next_state=0;endcase end assign Y0=next_state[0];assign z=(y==3)||(y==4);
endmodule

`default_nettype wire
