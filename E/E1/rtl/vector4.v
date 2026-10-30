// HDL-018 Replication operator
// Source: https://hdlbits.01xz.net/wiki/vector4
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [7:0] in,
  output wire [31:0] out
);
assign out={{24{in[7]}},in};
endmodule

`default_nettype wire
