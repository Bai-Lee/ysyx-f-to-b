// HDL-042 Generate for-loop: 100-bit binary adder 2
// Source: https://hdlbits.01xz.net/wiki/adder100i
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [99:0] a,
  input wire [99:0] b,
  input wire cin,
  output wire [99:0] cout,
  output wire [99:0] sum
);
wire[100:0]c;assign c[0]=cin;assign cout=c[100:1];genvar n;generate for(n=0;n<100;n=n+1)begin bit_adder f(a[n],b[n],c[n],sum[n],c[n+1]);end endgenerate
endmodule
module bit_adder(input a,b,cin,output s,cout);assign s=a^b^cin;assign cout=(a&b)|(a&cin)|(b&cin);endmodule
`default_nettype wire
