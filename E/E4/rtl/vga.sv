`timescale 1ns/1ns
module vga_timing(input wire clk,reset,output reg [9:0] hc,vc,
 output wire hsync,vsync,valid,output wire [9:0] x,y);
`ifdef FAULT_VGA_TOTAL
  localparam [9:0] H_LAST=10'd798;
`else
  localparam [9:0] H_LAST=10'd799;
`endif
  always @(posedge clk)begin
    if(reset)begin hc<=0;vc<=0;end
    else if(hc==H_LAST)begin hc<=0;vc<=vc==524?10'd0:vc+10'd1;end
    else hc<=hc+10'd1;
  end
  assign hsync=hc>=96;assign vsync=vc>=2;
  assign valid=(hc>=144&&hc<784&&vc>=35&&vc<515);
  assign x=(hc>=144&&hc<784)?hc-10'd144:10'd0;
  assign y=(vc>=35&&vc<515)?vc-10'd35:10'd0;
endmodule
module motion(input wire clk,reset,frame,load,input wire [9:0] seed_x,seed_y,
 input wire seed_dx,seed_dy,input wire [3:0] vx,vy,
 output reg [9:0] x,y,output reg dx,dy);
  wire [10:0] xp={1'b0,x}+{7'b0,vx};wire [10:0] yp={1'b0,y}+{7'b0,vy};
  // Reflected coordinates fit10 bits on the selected collision branches.
  wire [9:0] xr=10'(11'd1152-xp),yr=10'(11'd864-yp);
  always @(posedge clk)begin
    if(reset)begin x<=0;y<=0;dx<=1;dy<=1;end
    else if(load)begin x<=seed_x>576?10'd576:seed_x;y<=seed_y>432?10'd432:seed_y;dx<=seed_dx;dy<=seed_dy;end
    else if(frame)begin
      if(dx)begin
        if(xp>=576)begin x<=xr;dx<=0;end else x<=xp[9:0];
      end else if(x<={6'b0,vx})begin x<={6'b0,vx}-x;dx<=1;end else x<=x-{6'b0,vx};
      if(dy)begin
        if(yp>=432)begin y<=yr;dy<=0;end else y<=yp[9:0];
      end else if(y<={6'b0,vy})begin y<={6'b0,vy}-y;dy<=1;end else y<=y-{6'b0,vy};
    end
  end
endmodule
module vga(input wire clk,reset,moving,input wire [3:0] vx,vy,
 output reg hsync,vsync,valid,output wire [7:0] red,green,blue,
 output reg [9:0] sample_h,sample_v,output wire [9:0] pos_x,pos_y,
 output wire dir_x,dir_y);
  wire [9:0] hc,vc,x,y;wire hs,vs,active;
  vga_timing t(clk,reset,hc,vc,hs,vs,active,x,y);
  wire frame=(hc==799)&&(vc==524);
  motion m(clk,reset,frame,1'b0,10'b0,10'b0,1'b0,1'b0,vx,vy,pos_x,pos_y,dir_x,dir_y);
  reg [11:0] pixels[0:327679];
  initial $readmemh("image.mem",pixels);
  wire inside_image=(x>=pos_x)&&(x<pos_x+10'd64)&&(y>=pos_y)&&(y<pos_y+10'd48);
  wire [9:0] image_x=moving?x-pos_x:x;
  wire [8:0] image_y=moving?y[8:0]-pos_y[8:0]:y[8:0];
  // Column-major, 512 rows per column. Valid addresses are <640*512.
  wire [18:0] address={image_x,image_y};
  reg [11:0] pixel;
  always @(posedge clk)begin
    if(reset)begin hsync<=1;vsync<=1;valid<=0;pixel<=0;sample_h<=0;sample_v<=0;end
    else begin
      hsync<=hs;vsync<=vs;valid<=active;sample_h<=hc;sample_v<=vc;
      pixel<=!active?12'h000:(!moving||inside_image)?pixels[address]:12'h001;
    end
  end
  assign red={pixel[11:8],4'b0};assign green={pixel[7:4],4'b0};assign blue={pixel[3:0],4'b0};
endmodule
