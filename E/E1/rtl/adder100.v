// HDL-071 100-bit binary adder
// Source: https://hdlbits.01xz.net/wiki/adder100
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [99:0] a,
  input wire [99:0] b,
  input wire cin,
  output wire cout,
  output wire [99:0] sum
);
assign {cout,sum}={1'b0,a}+{1'b0,b}+cin;
endmodule

`default_nettype wire
