// HDL-134 PS/2 packet parser and datapath
// Source: https://hdlbits.01xz.net/wiki/fsm_ps2data
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire [7:0] in,
  input wire reset,
  output reg [23:0] out_bytes,
  output reg done
);
localparam SEEK=0,SECOND=1,THIRD=2;reg[1:0]state;reg[7:0]first,second;always @(posedge clk)begin if(reset)begin state<=SEEK;done<=0;end else begin done<=0;case(state)
SEEK:if(in[3])begin state<=SECOND;first<=in;end
SECOND:begin state<=THIRD;second<=in;end
THIRD:begin state<=SEEK;done<=1;out_bytes<={first,second,in};end
default:state<=SEEK;endcase end end
endmodule

`default_nettype wire
