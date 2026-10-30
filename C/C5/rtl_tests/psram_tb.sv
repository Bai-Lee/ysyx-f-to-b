`timescale 1ns/1ps
module psram_tb;
 parameter bit BAD_DATA=0;
 parameter integer SCENARIO=0;
 logic sck=0,ce_n=1;
 logic [3:0] host_data=0,host_enable=0;
 wire [3:0] dio;
 for(genvar i=0;i<4;i++)assign dio[i]=host_enable[i]?host_data[i]:1'bz;
 psram #(.MEM_BYTES(4096),.FAULT_BAD_DATA(BAD_DATA)) dut(.*);
 logic qpi=0;
 integer checks=0;
 task automatic rise;
  begin #2;sck=1;#2;end
 endtask
 task automatic fall;
  begin sck=0;#2;end
 endtask
 task automatic send_nibble(input [3:0] value,input [3:0] enable);
  begin host_enable=enable;host_data=value;rise();if((dio&enable)!==(value&enable))$fatal(1,"HOST_BUS_CONTENTION");fall();end
 endtask
 task automatic deselect;
  begin ce_n=1;host_enable=0;sck=0;#2;if(dio!==4'bzzzz)$fatal(1,"PSRAM_NOT_HIGH_Z");end
 endtask
 task automatic command(input [7:0] value);
  begin
   deselect();ce_n=0;#2;
   if(qpi)begin send_nibble(value[7:4],15);send_nibble(value[3:0],15);end
   else for(integer i=7;i>=0;i--)send_nibble({3'b0,value[i]},1);
  end
 endtask
 task automatic send_address(input [23:0] value);
  begin for(integer i=5;i>=0;i--)send_nibble(value[i*4+:4],15);end
 endtask
 task automatic write_bytes(input [23:0] address,input integer n,input [31:0] value);
  begin
   command(8'h38);send_address(address);
   for(integer i=0;i<n;i++)begin send_nibble(value[i*8+4+:4],15);send_nibble(value[i*8+:4],15);end
   deselect();
  end
 endtask
 task automatic read_bytes(input [23:0] address,input integer n,input [31:0] expected);
  logic [31:0] value;
  begin
   command(8'heb);send_address(address);host_enable=0;
   for(integer i=0;i<6;i++)begin
    #1;if(dio!==4'bzzzz)$fatal(1,"DUMMY_CYCLE_DIRECTION_OR_COUNT");rise();fall();
   end
   value=0;
   if(SCENARIO==3)begin host_enable=15;host_data=15;end
   for(integer i=0;i<n;i++)begin
    rise();value[i*8+4+:4]=dio;fall();rise();value[i*8+:4]=dio;fall();
   end
   deselect();
   if(value!==expected)$fatal(1,"PSRAM_READ_DATA address=%h got=%h expected=%h",address,value,expected);
   checks++;
  end
 endtask
 initial begin
  #1;ce_n=0;#1;ce_n=1;#2;
  if(SCENARIO!=1)begin rise();fall();end
  if(SCENARIO==2)begin command(8'h38);send_address(24'h1000);$fatal(1,"RANGE_NOT_REJECTED");end
  if(SCENARIO==4)begin command(8'hff);$fatal(1,"COMMAND_NOT_REJECTED");end
  write_bytes(24'h20,4,32'h5af03c96);read_bytes(24'h20,4,32'h5af03c96);
  for(integer i=0;i<256;i++)begin write_bytes(24'h100+i,1,32'(i));read_bytes(24'h100+i,1,32'(i));end
  write_bytes(24'h3fe,4,32'h44332211);read_bytes(24'h3fe,4,32'h44332211);read_bytes(0,2,32'h4433);
  write_bytes(24'hfff,2,32'haa55);read_bytes(24'hfff,2,32'haa55);read_bytes(24'hc00,1,32'haa);
  command(8'h35);deselect();qpi=1;
  write_bytes(24'h280,4,32'h01234567);read_bytes(24'h280,4,32'h01234567);
  command(8'hf5);deselect();qpi=0;read_bytes(24'h20,4,32'h5af03c96);
  write_bytes(24'h380,1,32'h5a);
  command(8'h38);send_address(24'h380);send_nibble(15,15);deselect();
  read_bytes(24'h380,1,32'h5a);
  command(8'h38);send_nibble(10,15);deselect();read_bytes(24'h380,1,32'h5a);
  $display("PSRAM_PIN_PROTOCOL_PASS checks=%0d",checks);$finish;
 end
endmodule
