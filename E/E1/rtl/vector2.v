// HDL-013 Vector part select
// Source: https://hdlbits.01xz.net/wiki/vector2
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [31:0] in,
  output wire [31:0] out
);
assign out={in[7:0],in[15:8],in[23:16],in[31:24]};
endmodule

`default_nettype wire
