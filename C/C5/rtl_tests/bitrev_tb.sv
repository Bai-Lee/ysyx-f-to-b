`timescale 1ns/1ps
module bitrev_tb;
 parameter bit BAD=0;
 logic sck=0,ss=0,mosi=0;wire miso;
 bitrev #(.FAULT_ECHO(BAD)) dut(.*);
 task automatic transfer(input [7:0] value);
  logic [7:0] result,expected;
  begin
   ss=1;sck=0;#2;if(miso!==1)$fatal(1,"DESELECTED_MISO");
   result=0;expected=0;
   for(integer i=0;i<8;i++)expected={expected[6:0],value[i]};
   ss=0;
   for(integer i=15;i>=0;i--)begin
    mosi=i>=8?value[i-8]:1'b0;#2;sck=1;#1;
    if(i<8)result={result[6:0],miso};
    #1;sck=0;#2;
   end
   ss=1;#2;
   if(result!==expected)$fatal(1,"BIT_REVERSE value=%h actual=%h expected=%h",value,result,expected);
  end
 endtask
 initial begin
  #1;ss=1;#2;
  for(integer i=0;i<256;i++)transfer(8'(i));
  // Abort a partial transaction and ensure chip-select resets all state.
  ss=0;mosi=1;repeat(3)begin #2;sck=1;#2;sck=0;end
  ss=1;#2;transfer(8'ha3);
  $display("BITREV_ALL256_AND_ABORT_RESET_PASS");$finish;
 end
endmodule
