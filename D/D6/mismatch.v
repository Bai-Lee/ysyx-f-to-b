`timescale 1ns/1ps
module tb;
reg a=0,b=0;reg incomplete,temporary,ywrong;wire ycorrect=a&b;
always @(a) incomplete=a&b;
always @(a or b) begin ywrong=temporary; temporary=a&b;end
reg [1:0] select;reg cx,cz;wire delayed;assign #2 delayed=a;
always @* casex(select) 2'b1?:cx=1;default:cx=0;endcase
always @* casez(select) 2'b1?:cz=1;default:cz=0;endcase
initial begin
 a=1;#3;b=1;#1;
 if(incomplete!==0 || ycorrect!==1 || ywrong!==0)$fatal(1,"missing expected mismatch");
 select=2'bx0;#1;if(cx!==1 || cz!==0)$fatal(1,"casex/casez X distinction");
 select=2'bz0;#1;if(cz!==1)$fatal(1,"casez Z wildcard");
 a=0;#1;if(delayed!==1)$fatal(1,"delay expected");#2;if(delayed!==0)$fatal(1,"settled delay");
 $display("MISMATCH_PASS sensitivity temporary casex casez delay");$finish;
end endmodule
