// HDL-108 Left/right rotator
// Source: https://hdlbits.01xz.net/wiki/rotate100
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire load,
  input wire [1:0] ena,
  input wire [99:0] data,
  output reg [99:0] q
);
always @(posedge clk)begin if(load)q<=data;else case(ena)2'b01:q<={q[0],q[99:1]};2'b10:q<={q[98:0],q[99]};default:q<=q;endcase end
endmodule

`default_nettype wire
