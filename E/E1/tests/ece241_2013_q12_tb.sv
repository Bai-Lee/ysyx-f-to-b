`timescale 1ns/1ps
module tb;
reg  v_clk;
reg  v_enable;
reg  v_S;
reg  v_A;
reg  v_B;
reg  v_C;
wire  got_Z;reg  exp_Z, mask_Z;
reg  scan_clk;
reg  scan_enable;
reg  scan_S;
reg  scan_A;
reg  scan_B;
reg  scan_C;
integer file,rc,n=0;top_module dut(.clk(v_clk),.enable(v_enable),.S(v_S),.A(v_A),.B(v_B),.C(v_C),.Z(got_Z));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/ece241_2013_q12.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h %h\n",scan_clk,scan_enable,scan_S,scan_A,scan_B,scan_C,exp_Z,mask_Z);
if(rc!=8)$fatal(2,"vector parse failure");
v_enable=scan_enable;
v_S=scan_S;
v_A=scan_A;
v_B=scan_B;
v_C=scan_C;
v_clk=scan_clk;
#1;
if(((got_Z ^ exp_Z) & mask_Z) !== 1'd0) begin $display("MISMATCH ece241_2013_q12 row=%0d port=Z got=%h expected=%h mask=%h",n,got_Z,exp_Z,mask_Z);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=8192)$fatal(2,"wrong case count");
$display("PASS ece241_2013_q12 checks=%0d",n);$fclose(file);$finish;end
endmodule
