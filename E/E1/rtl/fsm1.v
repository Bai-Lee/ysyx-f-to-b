// HDL-119 Simple FSM 1 (asynchronous reset)
// Source: https://hdlbits.01xz.net/wiki/fsm1
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire areset,
  input wire in,
  output wire out
);
reg state;assign out=state;always @(posedge clk or posedge areset)if(areset)state<=1'b1;else if(!in)state<=~state;
endmodule

`default_nettype wire
