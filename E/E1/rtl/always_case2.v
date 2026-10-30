// HDL-034 Priority encoder
// Source: https://hdlbits.01xz.net/wiki/always_case2
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [3:0] in,
  output reg [1:0] pos
);
always @* begin case(in)4'b0001,4'b0011,4'b0101,4'b0111,4'b1001,4'b1011,4'b1101,4'b1111:pos=0;4'b0010,4'b0110,4'b1010,4'b1110:pos=1;4'b0100,4'b1100:pos=2;4'b1000:pos=3;default:pos=0;endcase end
endmodule

`default_nettype wire
