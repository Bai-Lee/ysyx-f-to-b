// HDL-070 Signed addition overflow
// Source: https://hdlbits.01xz.net/wiki/exams/ece241_2014_q1c
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [7:0] a,
  input wire [7:0] b,
  output wire [7:0] s,
  output wire overflow
);
assign s=a+b;assign overflow=(~(a[7]^b[7]))&(a[7]^s[7]);
endmodule

`default_nettype wire
