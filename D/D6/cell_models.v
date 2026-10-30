module BUF(input A,output Y);assign Y=A;endmodule
module NOT(input A,output Y);assign Y=~A;endmodule
module NAND(input A,B,output Y);assign Y=~(A&B);endmodule
module NOR(input A,B,output Y);assign Y=~(A|B);endmodule
module DFF(input C,D,output reg Q);always @(posedge C)Q<=D;endmodule
