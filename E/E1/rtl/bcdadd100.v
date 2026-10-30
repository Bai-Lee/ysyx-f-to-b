// HDL-043 Generate for-loop: 100-digit BCD adder
// Source: https://hdlbits.01xz.net/wiki/bcdadd100
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [399:0] a,
  input wire [399:0] b,
  input wire cin,
  output wire cout,
  output wire [399:0] sum
);
wire[100:0]c;assign c[0]=cin;assign cout=c[100];genvar n;generate for(n=0;n<100;n=n+1)begin bcd_fadd f(a[4*n+:4],b[4*n+:4],c[n],c[n+1],sum[4*n+:4]);end endgenerate
endmodule

`default_nettype wire
