// HDL-010 7458 chip
// Source: https://hdlbits.01xz.net/wiki/7458
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire p1a,
  input wire p1b,
  input wire p1c,
  input wire p1d,
  input wire p1e,
  input wire p1f,
  output wire p1y,
  input wire p2a,
  input wire p2b,
  input wire p2c,
  input wire p2d,
  output wire p2y
);
wire aa,ab,ba,bb;assign aa=p1a&p1b&p1c;assign ab=p1d&p1e&p1f;assign ba=p2a&p2b;assign bb=p2c&p2d;assign p1y=aa|ab;assign p2y=ba|bb;
endmodule

`default_nettype wire
