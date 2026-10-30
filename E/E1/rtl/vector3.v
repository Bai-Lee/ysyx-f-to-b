// HDL-016 Vector concatenation operator
// Source: https://hdlbits.01xz.net/wiki/vector3
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [4:0] a,
  input wire [4:0] b,
  input wire [4:0] c,
  input wire [4:0] d,
  input wire [4:0] e,
  input wire [4:0] f,
  output wire [7:0] w,
  output wire [7:0] x,
  output wire [7:0] y,
  output wire [7:0] z
);
assign {w,x,y,z}={a,b,c,d,e,f,2'b11};
endmodule

`default_nettype wire
