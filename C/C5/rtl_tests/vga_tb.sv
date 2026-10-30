`timescale 1ns/1ps
module vga_tb;
  reg clock=0,reset=1;always #5 clock=~clock;
  reg [31:0] in_paddr=0,in_pwdata=0;reg in_psel=0,in_penable=0,in_pwrite=0;
  reg [2:0] in_pprot=0;reg [3:0] in_pstrb=0;wire in_pready,in_pslverr;wire [31:0] in_prdata;
  wire [7:0] vga_r,vga_g,vga_b;wire vga_hsync,vga_vsync,vga_valid;
  vga_top_apb dut(.*);integer pixels=0;
  function automatic [31:0] color(input integer x,input integer y);
    color=(((x*3)&255)<<16)|(((y*5)&255)<<8)|((x^y)&255);
  endfunction
  task write_pixel(input integer index,input [31:0] value,input [3:0] mask);
    begin
      @(negedge clock);in_psel=1;in_penable=0;in_pwrite=1;in_paddr=32'h21000000+32'(index*4);in_pwdata=value;in_pstrb=mask;
      @(negedge clock);in_penable=1;@(posedge clock);if(!in_pready||in_pslverr)$fatal(1,"VGA_APB_WRITE");
      @(negedge clock);in_psel=0;in_penable=0;in_pwrite=0;
    end
  endtask
  initial begin
    repeat(3)@(negedge clock);reset=0;
    for(integer y=0;y<480;y++)for(integer x=0;x<640;x++)write_pixel(y*640+x,color(x,y),15);
    write_pixel(0,32'h00aa0000,4'b0100);write_pixel(307199,32'h0000005a,4'b0001);
    in_paddr=32'h2112bffc;#1;if(in_prdata!==(color(639,479)&32'hffffff00|32'h5a))$fatal(1,"VGA_LAST_PIXEL");
    in_paddr=32'h2112c000;in_psel=1;in_penable=1;#1;if(!in_pslverr)$fatal(1,"VGA_OUT_OF_RANGE");in_psel=0;in_penable=0;
    // Synchronize using only external VSYNC, then independently score a whole frame.
    while(!vga_vsync)@(negedge clock);while(vga_vsync)@(negedge clock);
    for(integer n=0;n<800*525;n++)begin
      integer h,v,x,y;reg valid;reg [31:0] expected;
      h=n%800;v=n/800;valid=h>=144&&h<784&&v>=35&&v<515;
      if(vga_hsync!==(h>=96)||vga_vsync!==(v>=2)||vga_valid!==valid)$fatal(1,"VGA_TIMING n=%0d",n);
      expected=0;
      if(valid)begin
        x=h-144;y=v-35;expected=color(x,y);
        if(x==0&&y==0)expected=32'h00aa0000;
        if(x==639&&y==479)expected=(expected&32'hffffff00)|32'h5a;
        pixels++;
      end
      if({vga_r,vga_g,vga_b}!==expected[23:0])$fatal(1,"VGA_PIXEL_DATA n=%0d got=%h expected=%h",n,{vga_r,vga_g,vga_b},expected[23:0]);
      @(negedge clock);
    end
    if(pixels!=307200)$fatal(1,"VGA_FRAME_PIXEL_COUNT");
    reset=1;repeat(3)@(negedge clock);in_paddr=32'h21000000;#1;if(in_prdata!==32'h00aa0000)$fatal(1,"VGA_WARM_RESET_RETENTION");
    $display("VGA_FULL_FRAME_PASS pixels=%0d",pixels);$finish;
  end
endmodule
