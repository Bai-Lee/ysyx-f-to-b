// HDL-009 Declaring wires
// Source: https://hdlbits.01xz.net/wiki/wire_decl
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire a,
  input wire b,
  input wire c,
  input wire d,
  output wire out,
  output wire out_n
);
wire ab,cd;assign ab=a&b;assign cd=c&d;assign out=ab|cd;assign out_n=~out;
endmodule

`default_nettype wire
