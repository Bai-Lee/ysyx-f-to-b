// HDL-117 Rule 110
// Source: https://hdlbits.01xz.net/wiki/rule110
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire load,
  input wire [511:0] data,
  output wire [511:0] q
);
reg[511:0]cells;wire[511:0]next_cells;assign q=cells;
function next_bit;input l,c,r;begin case({l,c,r})3'b001,3'b010,3'b011,3'b101,3'b110:next_bit=1;default:next_bit=0;endcase end endfunction
genvar n;generate for(n=0;n<512;n=n+1)begin
if(n==0)assign next_cells[n]=next_bit(cells[n+1],cells[n],1'b0);
else if(n==511)assign next_cells[n]=next_bit(1'b0,cells[n],cells[n-1]);
else assign next_cells[n]=next_bit(cells[n+1],cells[n],cells[n-1]);end endgenerate
always @(posedge clk)if(load)cells<=data;else cells<=next_cells;
endmodule

`default_nettype wire
