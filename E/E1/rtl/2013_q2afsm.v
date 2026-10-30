// HDL-150 Q2a: FSM
// Source: https://hdlbits.01xz.net/wiki/exams/2013_q2afsm
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire resetn,
  input wire [3:1] r,
  output wire [3:1] g
);
localparam IDLE=0,G1=1,G2=2,G3=3;reg[1:0]state,next_state;
always @* begin next_state=state;case(state)
IDLE:if(r[1])next_state=G1;else if(r[2])next_state=G2;else if(r[3])next_state=G3;
G1:if(!r[1])next_state=IDLE;G2:if(!r[2])next_state=IDLE;G3:if(!r[3])next_state=IDLE;endcase end
always @(posedge clk)if(!resetn)state<=IDLE;else state<=next_state;
assign g[1]=(state==G1);assign g[2]=(state==G2);assign g[3]=(state==G3);
endmodule

`default_nettype wire
