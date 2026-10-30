// HDL-031 If statement
// Source: https://hdlbits.01xz.net/wiki/always_if
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire a,
  input wire b,
  input wire sel_b1,
  input wire sel_b2,
  output wire out_assign,
  output reg out_always
);
assign out_assign=(sel_b1&&sel_b2)?b:a;always @* begin if(sel_b1&&sel_b2)out_always=b;else out_always=a;end
endmodule

`default_nettype wire
