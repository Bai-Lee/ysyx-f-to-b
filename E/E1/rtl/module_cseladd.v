// HDL-027 Carry-select adder
// Source: https://hdlbits.01xz.net/wiki/module_cseladd
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [31:0] a,
  input wire [31:0] b,
  output wire [31:0] sum
);
wire carry;wire[15:0]s0,s1;add16 lo(a[15:0],b[15:0],1'b0,sum[15:0],carry);add16 hi0(a[31:16],b[31:16],1'b0,s0,);add16 hi1(a[31:16],b[31:16],1'b1,s1,);assign sum[31:16]=carry?s1:s0;
endmodule

`default_nettype wire
