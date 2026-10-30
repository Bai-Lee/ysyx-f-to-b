// HDL-149 Q2b: One-hot FSM equations
// Source: https://hdlbits.01xz.net/wiki/exams/2012_q2b
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [5:0] y,
  input wire w,
  output wire Y1,
  output wire Y3
);
assign Y1=w&y[0];assign Y3=~w&(y[1]|y[2]|y[4]|y[5]);
endmodule

`default_nettype wire
