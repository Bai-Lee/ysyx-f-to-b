`timescale 1ns/1ps
module tb;
reg A=0,B=0,C=0,D=0,E=0,CK=0;wire n,nl,o,ol,ai,ail,co,s,col,sl,q,qn,ql,qnl;
NAND2X1H7L_sw g1(A,B,n);NAND2X1H7L_lib l1(A,B,nl);
OAI22X1H7L_sw g2(A,B,C,D,o);OAI22X1H7L_lib l2(A,B,C,D,ol);
AOI221X1H7L_sw g3(A,B,C,D,E,ai);AOI221X1H7L_lib l3(A,B,C,D,E,ail);
ADDFX1H7L_sw g4(A,B,C,co,s);ADDFX1H7L_lib l4(A,B,C,col,sl);
DFFX1H7L_sw g5(CK,A,q,qn);DFFX1H7L_lib l5(CK,A,ql,qnl);
integer i;
initial begin
 for(i=0;i<32;i=i+1)begin
 {A,B,C,D,E}=i;CK=0;#2;
 if(n!==!(A&B) || n!==nl)$fatal(1,"NAND");
 if(o!==!((A|B)&(C|D)) || o!==ol)$fatal(1,"OAI22");
 if(ai!==!((A&B)|(C&D)|E) || ai!==ail)$fatal(1,"AOI221");
 if({co,s}!==({1'b0,A}+B+C) || {co,s}!=={col,sl})$fatal(1,"ADDF");
 CK=1;#2;if(q!==A || q!==ql || qn!==~A || qn!==qnl)begin
 $display("DFF nodes CKP=%b CKN=%b net33=%b net46=%b net25=%b net9=%b",g5.CKP,g5.CKN,g5.net33,g5.net46,g5.net25,g5.net9);
 $fatal(1,"DFF sample i=%0d q=%b qn=%b expected=%b",i,q,qn,A);end
 A=~A;#2;if(q!==ql || qn!==qnl)$fatal(1,"DFF hold");
 end
 $display("CDL_PASS 32 combinational cases and 32 DFF capture/hold cases");$finish;
end endmodule
