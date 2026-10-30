// HDL-146 Q6c: FSM one-hot next-state logic
// Source: https://hdlbits.01xz.net/wiki/exams/m2014_q6c
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [6:1] y,
  input wire w,
  output wire Y2,
  output wire Y4
);
assign Y2=~w&y[1];assign Y4=w&(y[2]|y[3]|y[5]|y[6]);
endmodule

`default_nettype wire
