// HDL-037 Conditional ternary operator
// Source: https://hdlbits.01xz.net/wiki/conditional
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [7:0] a,
  input wire [7:0] b,
  input wire [7:0] c,
  input wire [7:0] d,
  output wire [7:0] min
);
wire[7:0]m0,m1;assign m0=a<b?a:b;assign m1=c<d?c:d;assign min=m0<m1?m0:m1;
endmodule

`default_nettype wire
