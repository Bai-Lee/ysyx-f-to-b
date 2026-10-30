`timescale 1ns/1ps
module tb;
reg  v_x3;
reg  v_x2;
reg  v_x1;
wire  got_f;reg  exp_f, mask_f;
reg  scan_x3;
reg  scan_x2;
reg  scan_x1;
integer file,rc,n=0;top_module dut(.x3(v_x3),.x2(v_x2),.x1(v_x1),.f(got_f));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/truthtable1.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h\n",scan_x3,scan_x2,scan_x1,exp_f,mask_f);
if(rc!=5)$fatal(2,"vector parse failure");
v_x3=scan_x3;
v_x2=scan_x2;
v_x1=scan_x1;
#1;
if(((got_f ^ exp_f) & mask_f) !== 1'd0) begin $display("MISMATCH truthtable1 row=%0d port=f got=%h expected=%h mask=%h",n,got_f,exp_f,mask_f);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=8)$fatal(2,"wrong case count");
$display("PASS truthtable1 checks=%0d",n);$fclose(file);$finish;end
endmodule
