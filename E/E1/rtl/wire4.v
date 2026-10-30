// HDL-004 Four wires
// Source: https://hdlbits.01xz.net/wiki/wire4
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire a,
  input wire b,
  input wire c,
  output wire w,
  output wire x,
  output wire y,
  output wire z
);
assign w=a;assign x=b;assign y=b;assign z=c;
endmodule

`default_nettype wire
