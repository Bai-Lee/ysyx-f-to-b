`timescale 1ns/1ps
module tb;
reg  v_clk;
reg  v_j;
reg  v_k;
wire  got_Q;reg  exp_Q, mask_Q;
reg  scan_clk;
reg  scan_j;
reg  scan_k;
integer file,rc,n=0;top_module dut(.clk(v_clk),.j(v_j),.k(v_k),.Q(got_Q));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/ece241_2013_q7.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h\n",scan_clk,scan_j,scan_k,exp_Q,mask_Q);
if(rc!=5)$fatal(2,"vector parse failure");
v_j=scan_j;
v_k=scan_k;
v_clk=scan_clk;
#1;
if(((got_Q ^ exp_Q) & mask_Q) !== 1'd0) begin $display("MISMATCH ece241_2013_q7 row=%0d port=Q got=%h expected=%h mask=%h",n,got_Q,exp_Q,mask_Q);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=242)$fatal(2,"wrong case count");
$display("PASS ece241_2013_q7 checks=%0d",n);$fclose(file);$finish;end
endmodule
