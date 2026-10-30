`timescale 1ns/1ps
module tb;reg X,Y;wire Z;integer i;xor_from_circ dut(X,Y,Z);
initial begin
for(i=0;i<4;i=i+1)begin {X,Y}=i;#1;if(Z!==(X!=Y))$fatal(1,"MISMATCH tutorial_export row=%0d got=%b",i,Z);end
$display("PASS tutorial_export checks=4");$finish;end endmodule
