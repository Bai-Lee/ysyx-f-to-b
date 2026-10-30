// HDL-020 Modules
// Source: https://hdlbits.01xz.net/wiki/module
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire a,
  input wire b,
  output wire out
);
mod_a u(.in1(a),.in2(b),.out(out));
endmodule

`default_nettype wire
