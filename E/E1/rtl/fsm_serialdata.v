// HDL-136 Serial receiver and datapath
// Source: https://hdlbits.01xz.net/wiki/fsm_serialdata
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire in,
  input wire reset,
  output reg [7:0] out_byte,
  output reg done
);
localparam IDLE=0,DATA=1,PARITY=2,STOP=3,RECOVER=4;reg[2:0]state,bit_index;reg[7:0]payload;always @(posedge clk)begin if(reset)begin state<=IDLE;bit_index<=0;done<=0;end else begin done<=0;case(state)
IDLE:if(!in)begin state<=DATA;bit_index<=0;end
DATA:begin payload[bit_index]<=in;if(bit_index==7)state<=STOP;else bit_index<=bit_index+1'b1;end
STOP:begin if(in)begin state<=IDLE;done<=1;out_byte<=payload;end else state<=RECOVER;end
RECOVER:if(in)state<=IDLE;default:state<=IDLE;endcase end end
endmodule

`default_nettype wire
