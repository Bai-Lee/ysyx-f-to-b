// HDL-125 Simple FSM 3 (asynchronous reset)
// Source: https://hdlbits.01xz.net/wiki/fsm3
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire in,
  input wire areset,
  output wire out
);
localparam A=2'd0,B=2'd1,C=2'd2,D=2'd3;reg[1:0]state,next_state;assign out=(state==D);always @* begin case(state)A:next_state=in?B:A;B:next_state=in?B:C;C:next_state=in?D:A;D:next_state=in?B:C;default:next_state=A;endcase end always @(posedge clk or posedge areset)if(areset)state<=A;else state<=next_state;
endmodule

`default_nettype wire
