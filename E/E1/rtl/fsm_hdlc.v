// HDL-138 Sequence recognition
// Source: https://hdlbits.01xz.net/wiki/fsm_hdlc
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire reset,
  input wire in,
  output wire disc,
  output wire flag,
  output wire err
);
reg[3:0]state,next_state;
always @* begin case(state)
0:next_state=in?1:0;1:next_state=in?2:0;2:next_state=in?3:0;3:next_state=in?4:0;
4:next_state=in?5:0;5:next_state=in?6:8;6:next_state=in?7:9;
7:next_state=in?7:0;8:next_state=in?1:0;9:next_state=in?1:0;default:next_state=0;endcase end
always @(posedge clk)if(reset)state<=0;else state<=next_state;
assign disc=(state==8);assign flag=(state==9);assign err=(state==7);
endmodule

`default_nettype wire
