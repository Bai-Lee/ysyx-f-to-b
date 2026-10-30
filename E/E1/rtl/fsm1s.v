// HDL-120 Simple FSM 1 (synchronous reset)
// Source: https://hdlbits.01xz.net/wiki/fsm1s
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire reset,
  input wire in,
  output wire out
);
reg state;assign out=state;always @(posedge clk)if(reset)state<=1'b1;else if(!in)state<=~state;
endmodule

`default_nettype wire
