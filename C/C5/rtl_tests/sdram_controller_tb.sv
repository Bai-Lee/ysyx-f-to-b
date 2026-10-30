`timescale 1ns/1ps
module sdram_controller_tb;
  localparam integer WIDTH=`C5_SDRAM_DQ,RANKS=`C5_SDRAM_RANKS;
  reg clock=0,reset=1;always #5 clock=~clock;
  reg [31:0] in_paddr=0,in_pwdata=0;reg in_psel=0,in_penable=0,in_pwrite=0;
  reg [2:0] in_pprot=0;reg [3:0] in_pstrb=0;
  wire in_pready,in_pslverr;wire [31:0] in_prdata;
  wire sdram_clk,sdram_cke,sdram_ras,sdram_cas,sdram_we;
  wire [RANKS-1:0] sdram_cs;wire [12:0] sdram_a;wire [1:0] sdram_ba;
  wire [WIDTH/8-1:0] sdram_dqm;wire [WIDTH-1:0] sdram_dq;
  sdram_top_apb dut(.*);
  for(genvar r=0;r<RANKS;r++)begin:ranks
    for(genvar lane=0;lane<WIDTH/16;lane++)begin:lanes
      c5_sdram_chip #(.ROW_BITS(3),.CHIP_ID(r*2+lane)) chip(
        .clk(sdram_clk),.cke(sdram_cke),.cs(sdram_cs[r]),.ras(sdram_ras),.cas(sdram_cas),.we(sdram_we),
        .a(sdram_a),.ba(sdram_ba),.dqm(sdram_dqm[lane*2+:2]),.dq(sdram_dq[lane*16+:16]));
    end
  end
  integer checks=0,access_cycles=0,commands=0;
  reg [31:0] addresses[0:19],golden[0:19],value;
  integer naddresses;
  always @(posedge sdram_clk)if(sdram_cke && sdram_cs!={RANKS{1'b1}} && {sdram_ras,sdram_cas,sdram_we}==3'b000)begin
    if(sdram_a[6:4]!==3'd2 || sdram_a[2:0]!=(WIDTH==16?1:0))$fatal(1,"SDRAM_CONTROLLER_MODE");
  end
  always @(posedge sdram_clk)if(sdram_cke && sdram_cs!={RANKS{1'b1}} && !sdram_cas && sdram_ras)commands++;
  task access(input bit writing,input [31:0] address,input [31:0] data,input [3:0] mask,output [31:0] result);
    integer count;
    begin
      @(negedge clock);in_psel=1;in_penable=0;in_pwrite=writing;in_paddr=address;in_pwdata=data;in_pstrb=mask;
      @(negedge clock);in_penable=1;count=0;
      begin:wait_ready
        forever begin
          @(posedge clock);count++;
          if(in_pready===1)disable wait_ready;
          if(count>20000)$fatal(1,"SDRAM_APB_TIMEOUT");
        end
      end
      if(in_pslverr!==0)$fatal(1,"SDRAM_APB_ERROR");result=in_prdata;access_cycles+=count;
      @(negedge clock);in_psel=0;in_penable=0;in_pstrb=0;
      @(negedge clock);
    end
  endtask
  task check_read(input [31:0] address,input [31:0] expected);
    begin access(0,address,0,0,value);if(value!==expected)$fatal(1,"SDRAM_CONTROLLER_READ address=%h got=%h expected=%h",address,value,expected);checks++;end
  endtask
  initial begin
    repeat(5)@(negedge clock);reset=0;
    naddresses=8;
    addresses[0]=32'ha0000000;addresses[1]=32'ha0000004;addresses[2]=32'ha00003fc;addresses[3]=32'ha0000400;
    addresses[4]=32'ha0000800;addresses[5]=32'ha0000c00;addresses[6]=32'ha0001000;
    addresses[7]=WIDTH==16?32'ha0007ffc:32'ha000fffc;
    if(RANKS==2)begin for(integer i=0;i<8;i++)addresses[i+8]=addresses[i]+32'h04000000;naddresses=16;end
    for(integer i=0;i<naddresses;i++)begin golden[i]=32'h81426375^(32'(i)*32'h1020304);access(1,addresses[i],golden[i],15,value);end
    for(integer i=naddresses-1;i>=0;i--)check_read(addresses[i],golden[i]);
    for(integer i=0;i<naddresses;i++)begin
      access(1,addresses[i]+1,32'h0000aa00,4'b0010,value);golden[i][15:8]=8'haa;check_read(addresses[i],golden[i]);
      access(1,addresses[i]+2,32'h5c6d0000,4'b1100,value);golden[i][31:16]=16'h5c6d;check_read(addresses[i],golden[i]);
    end
    // Revisit after periodic refresh and after controller-only warm reset.
    repeat(1800)@(negedge clock);
    for(integer i=0;i<naddresses;i++)check_read(addresses[i],golden[i]);
    reset=1;repeat(5)@(negedge clock);reset=0;
    for(integer i=0;i<naddresses;i++)check_read(addresses[i],golden[i]);
    $display("SDRAM_CONTROLLER_PASS width=%0d ranks=%0d checks=%0d commands=%0d access_cycles=%0d",WIDTH,RANKS,checks,commands,access_cycles);$finish;
  end
  initial begin #5000000;$fatal(1,"SDRAM_CONTROLLER_TEST_TIMEOUT");end
endmodule
