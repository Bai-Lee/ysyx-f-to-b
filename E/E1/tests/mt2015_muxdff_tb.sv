`timescale 1ns/1ps
module tb;
reg  v_clk;
reg  v_L;
reg  v_r_in;
reg  v_q_in;
wire  got_Q;reg  exp_Q, mask_Q;
reg  scan_clk;
reg  scan_L;
reg  scan_r_in;
reg  scan_q_in;
integer file,rc,n=0;top_module dut(.clk(v_clk),.L(v_L),.r_in(v_r_in),.q_in(v_q_in),.Q(got_Q));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/mt2015_muxdff.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h\n",scan_clk,scan_L,scan_r_in,scan_q_in,exp_Q,mask_Q);
if(rc!=6)$fatal(2,"vector parse failure");
v_L=scan_L;
v_r_in=scan_r_in;
v_q_in=scan_q_in;
v_clk=scan_clk;
#1;
if(((got_Q ^ exp_Q) & mask_Q) !== 1'd0) begin $display("MISMATCH mt2015_muxdff row=%0d port=Q got=%h expected=%h mask=%h",n,got_Q,exp_Q,mask_Q);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=320)$fatal(2,"wrong case count");
$display("PASS mt2015_muxdff checks=%0d",n);$fclose(file);$finish;end
endmodule
