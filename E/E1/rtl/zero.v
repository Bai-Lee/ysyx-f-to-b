// HDL-002 Output Zero
// Source: https://hdlbits.01xz.net/wiki/zero
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  output wire zero
);
assign zero = 1'b0;
endmodule

`default_nettype wire
