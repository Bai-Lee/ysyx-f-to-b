// HDL-028 Adder-subtractor
// Source: https://hdlbits.01xz.net/wiki/module_addsub
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [31:0] a,
  input wire [31:0] b,
  input wire sub,
  output wire [31:0] sum
);
wire[31:0]modified_b;wire carry;assign modified_b=b^{32{sub}};add16 lo(a[15:0],modified_b[15:0],sub,sum[15:0],carry);add16 hi(a[31:16],modified_b[31:16],carry,sum[31:16],);
endmodule

`default_nettype wire
