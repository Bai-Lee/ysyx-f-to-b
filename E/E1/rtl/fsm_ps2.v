// HDL-133 PS/2 packet parser
// Source: https://hdlbits.01xz.net/wiki/fsm_ps2
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire [7:0] in,
  input wire reset,
  output reg done
);
localparam SEEK=0,SECOND=1,THIRD=2;reg[1:0]state;always @(posedge clk)begin if(reset)begin state<=SEEK;done<=0;end else begin done<=0;case(state)
SEEK:if(in[3])begin state<=SECOND;end
SECOND:begin state<=THIRD;end
THIRD:begin state<=SEEK;done<=1;end
default:state<=SEEK;endcase end end
endmodule

`default_nettype wire
