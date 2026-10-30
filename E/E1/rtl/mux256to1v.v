// HDL-065 256-to-1 4-bit multiplexer
// Source: https://hdlbits.01xz.net/wiki/mux256to1v
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [1023:0] in,
  input wire [7:0] sel,
  output wire [3:0] out
);
assign out=in[4*sel+:4];
endmodule

`default_nettype wire
