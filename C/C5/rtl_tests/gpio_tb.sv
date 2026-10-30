`timescale 1ns/1ps
module gpio_tb;
  reg clock=0,reset=1;always #5 clock=~clock;
  reg [31:0] in_paddr=0,in_pwdata=0;reg in_psel=0,in_penable=0,in_pwrite=0;
  reg [2:0] in_pprot=0;reg [3:0] in_pstrb=0;wire in_pready,in_pslverr;wire [31:0] in_prdata;
  reg [15:0] gpio_in=0;wire [15:0] gpio_out;wire [7:0] gpio_seg_0,gpio_seg_1,gpio_seg_2,gpio_seg_3,gpio_seg_4,gpio_seg_5,gpio_seg_6,gpio_seg_7;
  gpio_top_apb dut(.*);
  reg [7:0] golden[0:15];integer checks=0;
  task write_reg(input [3:0] address,input [31:0] value,input [3:0] mask);
    begin
      @(negedge clock);in_paddr=address;in_pwdata=value;in_pstrb=mask;in_pwrite=1;in_psel=1;
      @(negedge clock);in_penable=1;@(posedge clock);if(!in_pready||in_pslverr)$fatal(1,"GPIO_APB_WRITE");
      @(negedge clock);in_psel=0;in_penable=0;in_pwrite=0;
    end
  endtask
  initial begin
    golden[0]=8'hc0;golden[1]=8'hf9;golden[2]=8'ha4;golden[3]=8'hb0;golden[4]=8'h99;golden[5]=8'h92;golden[6]=8'h82;golden[7]=8'hf8;
    golden[8]=8'h80;golden[9]=8'h90;golden[10]=8'h88;golden[11]=8'h83;golden[12]=8'hc6;golden[13]=8'ha1;golden[14]=8'h86;golden[15]=8'h8e;
    repeat(3)@(negedge clock);reset=0;
    for(integer i=0;i<16;i++)begin write_reg(0,32'(1<<i),15);if(gpio_out!==(16'b1<<i))$fatal(1,"GPIO_LED_WALK");checks++;end
    write_reg(0,32'ha55a,15);write_reg(1,32'hcc,1);if(gpio_out!==16'ha5cc)$fatal(1,"GPIO_LOW_MASK");
    write_reg(2,32'hbb00,2);if(gpio_out!==16'hbbcc)$fatal(1,"GPIO_HIGH_MASK");
    write_reg(0,0,12);if(gpio_out!==16'hbbcc)$fatal(1,"GPIO_UNUSED_MASK");
    for(integer i=0;i<16;i++)begin
      write_reg(8,32'h11111111*32'(i),15);
      if({gpio_seg_7,gpio_seg_6,gpio_seg_5,gpio_seg_4,gpio_seg_3,gpio_seg_2,gpio_seg_1,gpio_seg_0}!=={8{golden[i]}})$fatal(1,"GPIO_SEGMENTS");checks+=8;
    end
    in_paddr=4;
    for(integer i=0;i<65536;i++)begin gpio_in=16'(i);repeat(3)@(negedge clock);if(in_prdata!==32'(i))$fatal(1,"GPIO_INPUT_MAPPING");checks++;end
    reset=1;repeat(3)@(negedge clock);if(gpio_out!==0)$fatal(1,"GPIO_RESET");
    $display("GPIO_APB_PASS checks=%0d",checks);$finish;
  end
endmodule
