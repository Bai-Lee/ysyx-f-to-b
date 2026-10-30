// HDL-012 Vectors in more detail
// Source: https://hdlbits.01xz.net/wiki/vector1
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [15:0] in,
  output wire [7:0] out_hi,
  output wire [7:0] out_lo
);
assign out_hi=in[15:8];assign out_lo=in[7:0];
endmodule

`default_nettype wire
