`timescale 1ns/1ps
module psram_controller_tb;
 logic clock=0,reset=1;always #5 clock=~clock;
 logic [31:0] in_paddr=0,in_pwdata=0;logic in_psel=0,in_penable=0,in_pwrite=0;
 logic [2:0] in_pprot=0;logic [3:0] in_pstrb=0;
 wire in_pready,in_pslverr,qspi_sck,qspi_ce_n;wire [31:0] in_prdata;wire [3:0] qspi_dio;
 psram_top_apb controller(.*);
 psram #(.MEM_BYTES(4096)) chip(.sck(qspi_sck),.ce_n(qspi_ce_n),.dio(qspi_dio));
 integer cycles=0,checks=0;
 always @(posedge clock)begin cycles++;if(cycles>10000)$fatal(1,"PSRAM_CONTROLLER_TIMEOUT");end
 task automatic access(input bit write_op,input [31:0] address,input [31:0] data,input [3:0] mask,input bit error_expected,output [31:0] result);
  begin
   @(negedge clock);in_psel=1;in_penable=0;in_paddr=address;in_pwdata=data;in_pwrite=write_op;in_pstrb=mask;
   @(negedge clock);in_penable=1;
   do @(posedge clock);while(!in_pready);
   if(in_pslverr!==error_expected)$fatal(1,"PSRAM_CONTROLLER_RESPONSE");result=in_prdata;
   @(negedge clock);in_psel=0;in_penable=0;in_pwrite=0;in_pstrb=0;
  end
 endtask
 logic [31:0] value;
 task automatic wr(input [31:0] address,input [31:0] data,input [3:0] mask,input bit err);
  begin access(1,address,data,mask,err,value);end
 endtask
 task automatic rd(input [31:0] address,input [31:0] expected);
  begin access(0,address,0,0,0,value);if(value!==expected)$fatal(1,"PSRAM_CONTROLLER_DATA addr=%h got=%h expected=%h",address,value,expected);checks++;end
 endtask
 initial begin
  repeat(4)@(negedge clock);reset=0;
  wr(32'h80000020,32'h89abcdef,15,0);rd(32'h80000020,32'h89abcdef);
  wr(32'h80000021,32'h00005500,2,0);rd(32'h80000021,32'h89ab55ef);
  wr(32'h80000022,32'h12340000,12,0);rd(32'h80000022,32'h123455ef);
  wr(32'h80000023,32'hff000000,8,0);rd(32'h80000020,32'hff3455ef);
  wr(32'h80000020,0,0,0);rd(32'h80000020,32'hff3455ef);
  wr(32'h80000020,0,5,1);rd(32'h80000020,32'hff3455ef);
  wr(32'h800003fc,32'h01234567,15,0);wr(32'h80000400,32'h89abcdef,15,0);
  rd(32'h800003fc,32'h01234567);rd(32'h80000400,32'h89abcdef);
  wr(32'h80000ffc,32'h55aa55aa,15,0);rd(32'h80000ffc,32'h55aa55aa);
  // Controller reset must resynchronize a chip that retained QPI mode/data.
  @(negedge clock);reset=1;repeat(4)@(negedge clock);reset=0;
  rd(32'h80000020,32'hff3455ef);rd(32'h80000ffc,32'h55aa55aa);
  $display("PSRAM_CONTROLLER_PASS checks=%0d qpi=%0d",checks,chip.qpi_mode);$finish;
 end
endmodule
