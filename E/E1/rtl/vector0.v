// HDL-011 Vectors
// Source: https://hdlbits.01xz.net/wiki/vector0
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [2:0] vec,
  output wire [2:0] outv,
  output wire o2,
  output wire o1,
  output wire o0
);
assign outv=vec;assign {o2,o1,o0}=vec;
endmodule

`default_nettype wire
