`timescale 1ns/1ps
module tb;
reg  v_clk;
reg  v_w;
reg  v_R;
reg  v_E;
reg  v_L;
wire  got_Q;reg  exp_Q, mask_Q;
reg  scan_clk;
reg  scan_w;
reg  scan_R;
reg  scan_E;
reg  scan_L;
integer file,rc,n=0;top_module dut(.clk(v_clk),.w(v_w),.R(v_R),.E(v_E),.L(v_L),.Q(got_Q));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/2014_q4a.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h\n",scan_clk,scan_w,scan_R,scan_E,scan_L,exp_Q,mask_Q);
if(rc!=7)$fatal(2,"vector parse failure");
v_w=scan_w;
v_R=scan_R;
v_E=scan_E;
v_L=scan_L;
v_clk=scan_clk;
#1;
if(((got_Q ^ exp_Q) & mask_Q) !== 1'd0) begin $display("MISMATCH 2014_q4a row=%0d port=Q got=%h expected=%h mask=%h",n,got_Q,exp_Q,mask_Q);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=642)$fatal(2,"wrong case count");
$display("PASS 2014_q4a checks=%0d",n);$fclose(file);$finish;end
endmodule
