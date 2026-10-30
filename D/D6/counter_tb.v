`timescale 1ns/1ps
module tb;
reg clk=0,rst=1,en=0;wire [1:0] refq,mapq;reg[1:0] expected;integer i;
counter original(clk,rst,en,refq);
counter_mapped mapped(.clk(clk),.rst(rst),.en(en),.\count[0] (mapq[0]),.\count[1] (mapq[1]));
initial begin
 expected=0;
 for(i=0;i<4096;i=i+1) begin
   clk=0;rst=(i%17==0);en=((i*13+3)%7<4);#1;
   if(rst)expected=0;else if(en)expected=expected+1;
   clk=1;#1;
   if(refq!==expected || mapq!==expected)$fatal(1,"COUNT_MISMATCH cycle=%d expected=%d ref=%d mapped=%d",i,expected,refq,mapq);
 end
 $display("COUNTER_PASS 4096 cycles");$finish;
end endmodule
