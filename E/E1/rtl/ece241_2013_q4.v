// HDL-127 Design a Moore FSM
// Source: https://hdlbits.01xz.net/wiki/exams/ece241_2013_q4
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire reset,
  input wire [3:1] s,
  output wire fr3,
  output wire fr2,
  output wire fr1,
  output wire dfr
);
localparam LOW=0,M1UP=1,M1DOWN=2,M2UP=3,M2DOWN=4,HIGH=5;
reg[2:0]state,next_state;
always @* begin next_state=state;case(s)
3'b000:next_state=LOW;3'b111:next_state=HIGH;
3'b001:if(state==LOW)next_state=M1UP;else if(state!=M1UP && state!=M1DOWN)next_state=M1DOWN;
3'b011:if(state==HIGH)next_state=M2DOWN;else if(state!=M2UP && state!=M2DOWN)next_state=M2UP;
default:next_state=state;endcase end
always @(posedge clk)if(reset)state<=LOW;else state<=next_state;
assign fr3=(state==LOW);assign fr2=(state==LOW)||(state==M1UP)||(state==M1DOWN);
assign fr1=(state!=HIGH);assign dfr=(state==LOW)||(state==M1DOWN)||(state==M2DOWN);
endmodule

`default_nettype wire
