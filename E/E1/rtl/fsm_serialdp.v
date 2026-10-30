// HDL-137 Serial receiver with parity checking
// Source: https://hdlbits.01xz.net/wiki/fsm_serialdp
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire in,
  input wire reset,
  output reg [7:0] out_byte,
  output reg done
);
localparam IDLE=0,DATA=1,PARITY=2,STOP=3,RECOVER=4;reg[2:0]state,bit_index;reg[7:0]payload;wire odd;wire parity_reset=reset || (state!=DATA && state!=PARITY);parity parity_accumulator(clk,parity_reset,in,odd);always @(posedge clk)begin if(reset)begin state<=IDLE;bit_index<=0;done<=0;end else begin done<=0;case(state)
IDLE:if(!in)begin state<=DATA;bit_index<=0;end
DATA:begin payload[bit_index]<=in;if(bit_index==7)state<=PARITY;else bit_index<=bit_index+1'b1;end
PARITY:state<=STOP;
STOP:begin if(in)begin state<=IDLE;if(odd)begin done<=1;out_byte<=payload;end end else state<=RECOVER;end
RECOVER:if(in)state<=IDLE;default:state<=IDLE;endcase end end
endmodule

`default_nettype wire
