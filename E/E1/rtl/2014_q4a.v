// HDL-092 Mux and DFF
// Source: https://hdlbits.01xz.net/wiki/exams/2014_q4a
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire w,
  input wire R,
  input wire E,
  input wire L,
  output wire Q
);
reg value;assign Q=value;always @(posedge clk)if(L)value<=R;else if(E)value<=w;
endmodule

`default_nettype wire
