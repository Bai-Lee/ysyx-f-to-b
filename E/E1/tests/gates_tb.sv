`timescale 1ns/1ps
module tb;
reg  v_a;
reg  v_b;
wire  got_out_and;reg  exp_out_and, mask_out_and;
wire  got_out_or;reg  exp_out_or, mask_out_or;
wire  got_out_xor;reg  exp_out_xor, mask_out_xor;
wire  got_out_nand;reg  exp_out_nand, mask_out_nand;
wire  got_out_nor;reg  exp_out_nor, mask_out_nor;
wire  got_out_xnor;reg  exp_out_xnor, mask_out_xnor;
wire  got_out_anotb;reg  exp_out_anotb, mask_out_anotb;
reg  scan_a;
reg  scan_b;
integer file,rc,n=0;top_module dut(.a(v_a),.b(v_b),.out_and(got_out_and),.out_or(got_out_or),.out_xor(got_out_xor),.out_nand(got_out_nand),.out_nor(got_out_nor),.out_xnor(got_out_xnor),.out_anotb(got_out_anotb));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/gates.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h\n",scan_a,scan_b,exp_out_and,mask_out_and,exp_out_or,mask_out_or,exp_out_xor,mask_out_xor,exp_out_nand,mask_out_nand,exp_out_nor,mask_out_nor,exp_out_xnor,mask_out_xnor,exp_out_anotb,mask_out_anotb);
if(rc!=16)$fatal(2,"vector parse failure");
v_a=scan_a;
v_b=scan_b;
#1;
if(((got_out_and ^ exp_out_and) & mask_out_and) !== 1'd0) begin $display("MISMATCH gates row=%0d port=out_and got=%h expected=%h mask=%h",n,got_out_and,exp_out_and,mask_out_and);$fatal(1,"behavior mismatch");end
if(((got_out_or ^ exp_out_or) & mask_out_or) !== 1'd0) begin $display("MISMATCH gates row=%0d port=out_or got=%h expected=%h mask=%h",n,got_out_or,exp_out_or,mask_out_or);$fatal(1,"behavior mismatch");end
if(((got_out_xor ^ exp_out_xor) & mask_out_xor) !== 1'd0) begin $display("MISMATCH gates row=%0d port=out_xor got=%h expected=%h mask=%h",n,got_out_xor,exp_out_xor,mask_out_xor);$fatal(1,"behavior mismatch");end
if(((got_out_nand ^ exp_out_nand) & mask_out_nand) !== 1'd0) begin $display("MISMATCH gates row=%0d port=out_nand got=%h expected=%h mask=%h",n,got_out_nand,exp_out_nand,mask_out_nand);$fatal(1,"behavior mismatch");end
if(((got_out_nor ^ exp_out_nor) & mask_out_nor) !== 1'd0) begin $display("MISMATCH gates row=%0d port=out_nor got=%h expected=%h mask=%h",n,got_out_nor,exp_out_nor,mask_out_nor);$fatal(1,"behavior mismatch");end
if(((got_out_xnor ^ exp_out_xnor) & mask_out_xnor) !== 1'd0) begin $display("MISMATCH gates row=%0d port=out_xnor got=%h expected=%h mask=%h",n,got_out_xnor,exp_out_xnor,mask_out_xnor);$fatal(1,"behavior mismatch");end
if(((got_out_anotb ^ exp_out_anotb) & mask_out_anotb) !== 1'd0) begin $display("MISMATCH gates row=%0d port=out_anotb got=%h expected=%h mask=%h",n,got_out_anotb,exp_out_anotb,mask_out_anotb);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=4)$fatal(2,"wrong case count");
$display("PASS gates checks=%0d",n);$fclose(file);$finish;end
endmodule
