// HDL-109 Left/right arithmetic shift by 1 or 8
// Source: https://hdlbits.01xz.net/wiki/shift18
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire load,
  input wire ena,
  input wire [1:0] amount,
  input wire [63:0] data,
  output reg [63:0] q
);
always @(posedge clk)begin if(load)q<=data;else if(ena)case(amount)2'b00:q<=q<<1;2'b01:q<=q<<8;2'b10:q<=$signed(q)>>>1;2'b11:q<=$signed(q)>>>8;endcase end
endmodule

`default_nettype wire
