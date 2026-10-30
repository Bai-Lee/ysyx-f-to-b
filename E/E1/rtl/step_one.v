// HDL-001 Getting Started
// Source: https://hdlbits.01xz.net/wiki/step_one
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  output wire one
);
assign one = 1'b1;
endmodule

`default_nettype wire
