`timescale 1ns/1ps
module tb;
reg  v_clk;
reg  v_areset;
reg  v_x;
wire  got_z;reg  exp_z, mask_z;
reg  scan_clk;
reg  scan_areset;
reg  scan_x;
integer file,rc,n=0;top_module dut(.clk(v_clk),.areset(v_areset),.x(v_x),.z(got_z));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/ece241_2014_q5b.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h\n",scan_clk,scan_areset,scan_x,exp_z,mask_z);
if(rc!=5)$fatal(2,"vector parse failure");
v_areset=scan_areset;
v_x=scan_x;
v_clk=scan_clk;
#1;
if(((got_z ^ exp_z) & mask_z) !== 1'd0) begin $display("MISMATCH ece241_2014_q5b row=%0d port=z got=%h expected=%h mask=%h",n,got_z,exp_z,mask_z);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=5764)$fatal(2,"wrong case count");
$display("PASS ece241_2014_q5b checks=%0d",n);$fclose(file);$finish;end
endmodule
