`timescale 1ns/1ps
module sdram_tb;
  parameter integer SCENARIO=0;
  reg clk=0,cke=1,cs=1,ras=1,cas=1,we=1;
  reg [12:0] a=0;reg [1:0] ba=0,dqm=0;
  reg host_enable=0;reg [15:0] host_data=0;wire [15:0] dq;
  assign dq=host_enable?host_data:16'bz;
  c5_sdram_chip #(.ROW_BITS(3)) dut(.*);
  integer checks=0;
  task tick(input [3:0] command,input [12:0] address,input [1:0] bank,input [1:0] mask,input integer drive,input [15:0] value);
    begin
      clk=0;{cs,ras,cas,we}=command;a=address;ba=bank;dqm=mask;host_enable=drive!=0;host_data=value;
      #3;clk=1;#2;
    end
  endtask
  task nop;begin tick(4'b0111,0,0,0,0,0);end endtask
  task mode(input integer blcode,input integer cl,input integer interleave);
    begin tick(4'b0000,13'((cl<<4)|(interleave<<3)|blcode),0,0,0,0);nop();end
  endtask
  task active(input integer bank,input integer rowno);
    begin tick(4'b0011,13'(rowno),2'(bank),0,0,0);nop();end
  endtask
  task expect_data(input [15:0] value);
    begin if(dq!==value)$fatal(1,"SDRAM_READ_DATA got=%h expected=%h",dq,value);checks++;end
  endtask
  task read_one(input integer bank,input integer col,input integer cl,input [15:0] expected);
    begin
      tick(4'b0101,13'(col),2'(bank),0,0,0);
      if(dq!==16'bz)$fatal(1,"SDRAM_READ_TOO_EARLY");
      for(integer n=1;n<cl;n++)begin nop();if(n<cl-1&&dq!==16'bz)$fatal(1,"SDRAM_LATENCY");end
      expect_data(expected);nop();if(dq!==16'bz)$fatal(1,"SDRAM_NOT_HIGH_Z");
    end
  endtask
  initial begin
    nop();mode(0,2,0);
    if(SCENARIO==1)begin tick(4'b0101,0,0,0,0,0);$fatal(1,"MISSING_ACTIVE_ACCEPTED");end
    if(SCENARIO==2)begin mode(1,0,0);$fatal(1,"BAD_MODE_ACCEPTED");end
    if(SCENARIO==3)begin active(0,0);tick(4'b0100,0,0,0,0,0);$fatal(1,"FLOATING_WRITE_ACCEPTED");end
    for(integer cl=2;cl<=3;cl++)begin
      for(integer il=0;il<2;il++)begin
        for(integer code=0;code<4;code++)begin
          integer length;length=1<<code;
          mode(code,cl,il);active(3,7);
          tick(4'b0100,13'd511,3,0,1,16'h5a00);
          for(integer n=1;n<length;n++)tick(4'b0111,0,0,0,1,16'h5a00^(16'(n)*16'h2d));
          nop();nop();
          tick(4'b0101,13'd511,3,0,0,0);
          for(integer n=1;n<cl;n++)begin nop();if(n<cl-1&&dq!==16'bz)$fatal(1,"SDRAM_LATENCY");end
          for(integer n=0;n<length;n++)begin expect_data(16'h5a00^(16'(n)*16'h2d));if(n+1<length)nop();end
          nop();if(dq!==16'bz)$fatal(1,"SDRAM_NOT_HIGH_Z");
          mode(0,cl,0);
          for(integer n=0;n<length;n++)begin
            integer col;col=il?(511^n):512-length+((length-1+n)%length);
            read_one(3,col,cl,16'h5a00^(16'(n)*16'h2d));
          end
        end
      end
    end
    mode(0,2,0);
    for(integer bank=0;bank<4;bank++)begin
      active(bank,bank);tick(4'b0100,13'd17,2'(bank),0,1,16'hc100+16'(bank));nop();
    end
    for(integer bank=0;bank<4;bank++)read_one(bank,17,2,16'hc100+16'(bank));
    tick(4'b0100,13'd17,0,2'b10,1,16'hab5e);nop();read_one(0,17,2,16'hc15e);
    tick(4'b0100,13'd17,0,2'b01,1,16'h6d22);nop();read_one(0,17,2,16'h6d5e);
    tick(4'b0100,13'd17,0,2'b11,1,16'hffff);nop();read_one(0,17,2,16'h6d5e);
    // Mask at READ edge suppresses the data valid two edges later.
    tick(4'b0101,13'd17,0,3,0,0);nop();if(dq!==16'bz)$fatal(1,"SDRAM_READ_DQM_LATENCY");nop();
    // CKE suspends command sampling; a disabled write does not change memory.
    cke=0;tick(4'b0100,13'd17,0,0,1,16'hffff);tick(4'b0111,0,0,0,0,0);cke=1;nop();read_one(0,17,2,16'h6d5e);
    tick(4'b0010,13'h400,0,0,0,0);tick(4'b0001,0,0,0,0,0);active(0,0);read_one(0,17,2,16'h6d5e);
    $display("SDRAM_PIN_PROTOCOL_PASS checks=%0d",checks);$finish;
  end
endmodule
