// HDL-061 2-to-1 multiplexer
// Source: https://hdlbits.01xz.net/wiki/mux2to1
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire a,
  input wire b,
  input wire sel,
  output wire out
);
assign out=sel?b:a;
endmodule

`default_nettype wire
