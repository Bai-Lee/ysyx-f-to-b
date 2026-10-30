// HDL-040 Combinational for-loop: Vector reversal 2
// Source: https://hdlbits.01xz.net/wiki/vector100r
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [99:0] in,
  output wire [99:0] out
);
genvar n;generate for(n=0;n<100;n=n+1)begin assign out[n]=in[99-n];end endgenerate
endmodule

`default_nettype wire
