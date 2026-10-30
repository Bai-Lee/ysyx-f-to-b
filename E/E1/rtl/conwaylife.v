// HDL-118 Conway's Game of Life 16x16
// Source: https://hdlbits.01xz.net/wiki/conwaylife
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire load,
  input wire [255:0] data,
  output wire [255:0] q
);
reg[255:0]cells;wire[255:0]next_cells;assign q=cells;
genvar r,c;generate for(r=0;r<16;r=r+1)begin:rows for(c=0;c<16;c=c+1)begin:cols
wire[3:0]neighbors;
assign neighbors={3'b0,cells[((r+15)%16)*16+(c+15)%16]}+{3'b0,cells[((r+15)%16)*16+c]}+{3'b0,cells[((r+15)%16)*16+(c+1)%16]}+
{3'b0,cells[r*16+(c+15)%16]}+{3'b0,cells[r*16+(c+1)%16]}+
{3'b0,cells[((r+1)%16)*16+(c+15)%16]}+{3'b0,cells[((r+1)%16)*16+c]}+{3'b0,cells[((r+1)%16)*16+(c+1)%16]};
assign next_cells[r*16+c]=(neighbors==3)||((neighbors==2)&&cells[r*16+c]);end end endgenerate
always @(posedge clk)if(load)cells<=data;else cells<=next_cells;
endmodule

`default_nettype wire
