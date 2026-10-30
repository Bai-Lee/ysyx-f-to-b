// HDL-122 Simple FSM 2 (synchronous reset)
// Source: https://hdlbits.01xz.net/wiki/fsm2s
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire reset,
  input wire j,
  input wire k,
  output wire out
);
reg on;assign out=on;always @(posedge clk)if(reset)on<=0;else if(on)begin if(k)on<=0;end else if(j)on<=1;
endmodule

`default_nettype wire
