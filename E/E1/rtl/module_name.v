// HDL-022 Connecting ports by name
// Source: https://hdlbits.01xz.net/wiki/module_name
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire a,
  input wire b,
  input wire c,
  input wire d,
  output wire out1,
  output wire out2
);
mod_a u(.in4(d),.out2(out2),.in1(a),.in3(c),.out1(out1),.in2(b));
endmodule

`default_nettype wire
