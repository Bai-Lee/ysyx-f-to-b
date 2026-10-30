// HDL-041 Combinational for-loop: 255-bit population count
// Source: https://hdlbits.01xz.net/wiki/popcount255
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [254:0] in,
  output reg [7:0] out
);
integer n;always @* begin out=8'd0;for(n=0;n<255;n=n+1)out=out+in[n];end
endmodule

`default_nettype wire
