// HDL-026 Adder 2
// Source: https://hdlbits.01xz.net/wiki/module_fadd
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [31:0] a,
  input wire [31:0] b,
  output wire [31:0] sum
);
wire carry;add16 lo(.a(a[15:0]),.b(b[15:0]),.cin(1'b0),.sum(sum[15:0]),.cout(carry));add16 hi(.a(a[31:16]),.b(b[31:16]),.cin(carry),.sum(sum[31:16]),.cout());
endmodule
module add1(input a,b,cin,output sum,cout);assign sum=a^b^cin;assign cout=(a&b)|(a&cin)|(b&cin);endmodule
`default_nettype wire
