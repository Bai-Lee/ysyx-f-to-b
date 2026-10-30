// HDL-123 Simple state transitions 3
// Source: https://hdlbits.01xz.net/wiki/fsm3comb
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire in,
  input wire [1:0] state,
  output reg [1:0] next_state,
  output wire out
);
localparam A=2'd0,B=2'd1,C=2'd2,D=2'd3;always @* begin case(state)A:next_state=in?B:A;B:next_state=in?B:C;C:next_state=in?D:A;D:next_state=in?B:C;default:next_state=A;endcase end assign out=(state==D);
endmodule

`default_nettype wire
