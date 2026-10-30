// HDL-129 Lemmings 2
// Source: https://hdlbits.01xz.net/wiki/lemmings2
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire areset,
  input wire bump_left,
  input wire bump_right,
  input wire ground,
  output wire walk_left,
  output wire walk_right,
  output wire aaah
);
localparam LEFT=0,RIGHT=1,FLEFT=2,FRIGHT=3,DLEFT=4,DRIGHT=5,DEAD=6;reg[2:0]state,next_state;always @* begin next_state=state;case(state)
LEFT:if(!ground)next_state=FLEFT;else if(bump_left)next_state=RIGHT;
RIGHT:if(!ground)next_state=FRIGHT;else if(bump_right)next_state=LEFT;
FLEFT:if(ground)next_state=LEFT;
FRIGHT:if(ground)next_state=RIGHT;
default:next_state=state;endcase end
always @(posedge clk or posedge areset)if(areset)state<=LEFT;else state<=next_state;
assign walk_left=(state==LEFT);assign walk_right=(state==RIGHT);assign aaah=(state==FLEFT)||(state==FRIGHT);
endmodule

`default_nettype wire
