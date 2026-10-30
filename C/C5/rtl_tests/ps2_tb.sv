`timescale 1ns/1ps
module ps2_tb;
  reg clock=0,reset=1;always #5 clock=~clock;
  reg [31:0] in_paddr=0,in_pwdata=0;reg in_psel=0,in_penable=0,in_pwrite=0;
  reg [2:0] in_pprot=0;reg [3:0] in_pstrb=0;wire in_pready,in_pslverr;wire [31:0] in_prdata;
  reg ps2_clk=1,ps2_data=1;ps2_top_apb #(.FRAME_TIMEOUT(100)) dut(.*);
  integer checks=0;
  task send_bit(input bit value);
    begin @(negedge clock);ps2_clk=1;ps2_data=value;repeat(8)@(negedge clock);ps2_clk=0;repeat(8)@(negedge clock);end
  endtask
  task send_byte(input [7:0] value,input bit bad_parity,input bit bad_stop);
    begin
      send_bit(0);for(integer i=0;i<8;i++)send_bit(value[i]);send_bit((~^value)^bad_parity);send_bit(!bad_stop);
      ps2_clk=1;ps2_data=1;repeat(8)@(negedge clock);
    end
  endtask
  task read_byte(input [7:0] expected);
    begin
      @(negedge clock);in_psel=1;in_paddr=0;in_penable=0;@(negedge clock);in_penable=1;
      @(posedge clock);if(!in_pready||in_pslverr||in_prdata!=={24'b0,expected})$fatal(1,"PS2_FIFO_DATA got=%h expected=%h",in_prdata,expected);
      @(negedge clock);in_psel=0;in_penable=0;checks++;
    end
  endtask
  initial begin
    repeat(3)@(negedge clock);reset=0;
    read_byte(0);
    for(integer i=0;i<256;i++)begin send_byte(8'(i),0,0);read_byte(8'(i));read_byte(0);end
    send_byte(8'h45,1,0);send_byte(8'h6d,0,1);read_byte(0);
    send_bit(0);send_bit(1);ps2_clk=1;ps2_data=1;repeat(120)@(negedge clock);send_byte(8'h83,0,0);read_byte(8'h83);
    for(integer i=0;i<17;i++)send_byte(8'h20+8'(i),0,0);
    for(integer i=0;i<16;i++)read_byte(8'h20+8'(i));read_byte(0);
    if(dut.invalid_frames!=3||dut.dropped_frames!=1)$fatal(1,"PS2_ERROR_ACCOUNTING invalid=%d drop=%d",dut.invalid_frames,dut.dropped_frames);
    $display("PS2_APB_PASS checks=%0d",checks);$finish;
  end
endmodule
