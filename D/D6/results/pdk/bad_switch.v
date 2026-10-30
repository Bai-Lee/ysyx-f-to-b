`timescale 1ns/1ps
module NAND2X1H7L_sw(A,B,Y);
input A,B; output Y; supply1 VDD;supply0 VSS;
wire net6;
pmos MMN0(Y,net6,B);
nmos MMN1(net6,VSS,A);
pmos MMP1(Y,VDD,B);
pmos MMP0(Y,VDD,A);
endmodule
module NAND2X1H7L_lib(A,B,Y);
input A,B;output Y;
assign Y=(!A) | (!B);
endmodule
module OAI22X1H7L_sw(A0,A1,B0,B1,Y);
input A0,A1,B0,B1; output Y; supply1 VDD;supply0 VSS;
wire net046,net049,net8;
nmos MNM4(net8,VSS,A1);
nmos MNM3(net8,VSS,A0);
nmos MMN5(Y,net8,B0);
nmos MNM5(Y,net8,B1);
pmos MMP5(Y,net046,A1);
pmos MPM3(net046,VDD,A0);
pmos MPM5(Y,net049,B1);
pmos MPM4(net049,VDD,B0);
endmodule
module OAI22X1H7L_lib(A0,A1,B0,B1,Y);
input A0,A1,B0,B1;output Y;
assign Y=(!A0 & !A1) | (!B0 & !B1);
endmodule
module AOI221X1H7L_sw(A0,A1,B0,B1,C0,Y);
input A0,A1,B0,B1,C0; output Y; supply1 VDD;supply0 VSS;
wire net1,net16,net17,net8;
nmos MMNM4(Y,VSS,C0);
nmos MMNM3(net16,VSS,B0);
nmos MMNM2(Y,net16,B1);
nmos MMNM1(net17,VSS,A0);
nmos MMNM0(Y,net17,A1);
pmos MMPM4(Y,net1,C0);
pmos MMPM3(net1,net8,B1);
pmos MMPM2(net1,net8,B0);
pmos MMPM1(net8,VDD,A1);
pmos MMPM0(net8,VDD,A0);
endmodule
module AOI221X1H7L_lib(A0,A1,B0,B1,C0,Y);
input A0,A1,B0,B1,C0;output Y;
assign Y=(!A0 & !B0 & !C0) | (!A0 & !B1 & !C0) | (!A1 & !B0 & !C0) | (!A1 & !B1 & !C0);
endmodule
module ADDFX1H7L_sw(A,B,CI,CO,S);
input A,B,CI; output CO,S; supply1 VDD;supply0 VSS;
wire net102,net110,net25,net29,net49,net53,net62,net66,net77,net9,net90,net93;
pmos MMM12(net90,net29,A);
pmos MMM10(net29,VDD,net62);
pmos MMM2(net9,VDD,B);
pmos MMM11(net90,net29,B);
pmos MMM6(net25,VDD,CI);
pmos MMM13(net90,net29,CI);
pmos MMM7(net62,net25,A);
pmos MMM8(net62,net25,B);
pmos MMM25(net49,VDD,B);
pmos MMM23(net90,net53,A);
pmos MMM0(net62,net9,A);
pmos MMM22(net53,net49,CI);
nmos MMM20(net102,net110,CI);
nmos MMM3(net66,VSS,B);
nmos MMM24(net110,VSS,B);
nmos MMM5(net62,net77,A);
nmos MMM14(net93,VSS,net62);
nmos MMM16(net90,net93,A);
nmos MMM1(net62,net66,A);
nmos MMM17(net90,net93,CI);
nmos MMM15(net90,net93,B);
nmos MMM9(net62,net77,B);
nmos MMM21(net90,net102,A);
nmos MMM4(net77,VSS,CI);
nmos XI2_MMN0(S,VSS,net90);
pmos XI2_MMP0(S,VDD,net90);
nmos XXI2_MMN0(CO,VSS,net62);
pmos XXI2_MMP0(CO,VDD,net62);
endmodule
module ADDFX1H7L_lib(A,B,CI,CO,S);
input A,B,CI;output CO,S;
assign CO=(A & B) | (A & CI) | (B & CI);
assign S=(A & B & CI) | (A & !B & !CI) | (!A & B & !CI) | (!A & !B & CI);
endmodule
module DFFX1H7L_sw(CK,D,Q,QN);
input CK,D; output Q,QN; supply1 VDD;supply0 VSS;
wire CKN,CKP,XI2_net024,XI2_net18,XI3_net024,XI3_net18,XI4_net024,XI4_net18,XXI6_net024,XXI6_net18,net25,net33,net46,net9;
rnmos XI2_MMN0(net33,XI2_net18,CKP);
rnmos XI2_MMN1(XI2_net18,VSS,net46);
rpmos XI2_MMP1(XI2_net024,VDD,net46);
rpmos XI2_MMP0(net33,XI2_net024,CKN);
nmos XXI6_MMN0(net33,XXI6_net18,CKN);
nmos XXI6_MMN1(XXI6_net18,VSS,D);
pmos XXI6_MMP1(XXI6_net024,VDD,D);
pmos XXI6_MMP0(net33,XXI6_net024,CKP);
nmos XI3_MMN0(net25,XI3_net18,CKP);
nmos XI3_MMN1(XI3_net18,VSS,net46);
pmos XI3_MMP1(XI3_net024,VDD,net46);
pmos XI3_MMP0(net25,XI3_net024,CKN);
rnmos XI4_MMN0(net25,XI4_net18,CKN);
rnmos XI4_MMN1(XI4_net18,VSS,net9);
rpmos XI4_MMP1(XI4_net024,VDD,net9);
rpmos XI4_MMP0(net25,XI4_net024,CKP);
nmos XI1_MMN0(net46,VSS,net33);
pmos XI1_MMP0(net46,VDD,net33);
nmos XI0_MMN0(CKP,VSS,CKN);
pmos XI0_MMP0(CKP,VDD,CKN);
nmos XXI12_MMN0(Q,VSS,net25);
pmos XXI12_MMP0(Q,VDD,net25);
nmos XXI10_MMN0(net9,VSS,net25);
pmos XXI10_MMP0(net9,VDD,net25);
nmos XI5_MMN0(QN,VSS,net9);
pmos XI5_MMP0(QN,VDD,net9);
nmos XXI4_MMN0(CKN,VSS,CK);
pmos XXI4_MMP0(CKN,VDD,CK);
endmodule
module DFFX1H7L_lib(CK,D,Q,QN);
input CK,D;output Q,QN;
reg q;always @(posedge CK)q<=D;assign Q=q;assign QN=~q;
endmodule
module DFFX1H7L_phase(input CK,D,output Q,QN);
reg master,slave;
always @* if(!CK)master=D;
always @* if(CK)slave=master;
assign Q=slave;assign QN=~slave;
endmodule
