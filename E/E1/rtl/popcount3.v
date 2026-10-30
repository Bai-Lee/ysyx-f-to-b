// HDL-058 3-bit population count
// Source: https://hdlbits.01xz.net/wiki/popcount3
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [2:0] in,
  output wire [1:0] out
);
assign out={1'b0,in[0]}+{1'b0,in[1]}+{1'b0,in[2]};
endmodule

`default_nettype wire
