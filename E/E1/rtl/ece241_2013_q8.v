// HDL-139 Q8: Design a Mealy FSM
// Source: https://hdlbits.01xz.net/wiki/exams/ece241_2013_q8
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire aresetn,
  input wire x,
  output wire z
);
localparam EMPTY=0,ONE=1,ONE_ZERO=2;reg[1:0]state,next_state;
always @* begin case(state)EMPTY:next_state=x?ONE:EMPTY;ONE:next_state=x?ONE:ONE_ZERO;
ONE_ZERO:next_state=x?ONE:EMPTY;default:next_state=EMPTY;endcase end
always @(posedge clk or negedge aresetn)if(!aresetn)state<=EMPTY;else state<=next_state;
assign z=(state==ONE_ZERO)&&x;
endmodule

`default_nettype wire
