// HDL-017 Vector reversal 1
// Source: https://hdlbits.01xz.net/wiki/vectorr
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [7:0] in,
  output wire [7:0] out
);
genvar i;generate for(i=0;i<8;i=i+1)begin assign out[i]=in[7-i];end endgenerate
endmodule

`default_nettype wire
