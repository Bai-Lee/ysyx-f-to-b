// HDL-104 Counter 1000
// Source: https://hdlbits.01xz.net/wiki/exams/ece241_2014_q7b
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire reset,
  output wire OneHertz,
  output wire [2:0] c_enable
);
wire[3:0]u,t,h;assign c_enable[0]=1'b1;assign c_enable[1]=(u==9);assign c_enable[2]=(u==9)&&(t==9);assign OneHertz=(u==9)&&(t==9)&&(h==9);bcdcount low(clk,reset,c_enable[0],u);bcdcount middle(clk,reset,c_enable[1],t);bcdcount high(clk,reset,c_enable[2],h);
endmodule

`default_nettype wire
