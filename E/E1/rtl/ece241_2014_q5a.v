// HDL-140 Q5a: Serial two's complementer (Moore FSM)
// Source: https://hdlbits.01xz.net/wiki/exams/ece241_2014_q5a
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire areset,
  input wire x,
  output wire z
);
localparam BEFORE_ONE=0,OUT_ONE=1,OUT_ZERO=2;reg[1:0]state,next_state;
always @* begin case(state)BEFORE_ONE:next_state=x?OUT_ONE:BEFORE_ONE;
OUT_ONE,OUT_ZERO:next_state=x?OUT_ZERO:OUT_ONE;default:next_state=BEFORE_ONE;endcase end
always @(posedge clk or posedge areset)if(areset)state<=BEFORE_ONE;else state<=next_state;
assign z=(state==OUT_ONE);
endmodule

`default_nettype wire
