// HDL-051 Truth tables
// Source: https://hdlbits.01xz.net/wiki/truthtable1
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire x3,
  input wire x2,
  input wire x1,
  output wire f
);
assign f=(~x3 & x2) | (x3 & x1);
endmodule

`default_nettype wire
