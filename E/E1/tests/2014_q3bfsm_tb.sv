`timescale 1ns/1ps
module tb;
reg  v_clk;
reg  v_reset;
reg  v_x;
wire  got_z;reg  exp_z, mask_z;
reg  scan_clk;
reg  scan_reset;
reg  scan_x;
integer file,rc,n=0;top_module dut(.clk(v_clk),.reset(v_reset),.x(v_x),.z(got_z));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/2014_q3bfsm.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h\n",scan_clk,scan_reset,scan_x,exp_z,mask_z);
if(rc!=5)$fatal(2,"vector parse failure");
v_reset=scan_reset;
v_x=scan_x;
v_clk=scan_clk;
#1;
if(((got_z ^ exp_z) & mask_z) !== 1'd0) begin $display("MISMATCH 2014_q3bfsm row=%0d port=z got=%h expected=%h mask=%h",n,got_z,exp_z,mask_z);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=2100)$fatal(2,"wrong case count");
$display("PASS 2014_q3bfsm checks=%0d",n);$fclose(file);$finish;end
endmodule
