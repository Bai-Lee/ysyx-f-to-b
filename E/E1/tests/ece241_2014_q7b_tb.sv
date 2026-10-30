`timescale 1ns/1ps
module tb;
reg  v_clk;
reg  v_reset;
wire  got_OneHertz;reg  exp_OneHertz, mask_OneHertz;
wire [2:0] got_c_enable;reg [2:0] exp_c_enable, mask_c_enable;
reg  scan_clk;
reg  scan_reset;
integer file,rc,n=0;top_module dut(.clk(v_clk),.reset(v_reset),.OneHertz(got_OneHertz),.c_enable(got_c_enable));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/ece241_2014_q7b.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h\n",scan_clk,scan_reset,exp_OneHertz,mask_OneHertz,exp_c_enable,mask_c_enable);
if(rc!=6)$fatal(2,"vector parse failure");
v_reset=scan_reset;
v_clk=scan_clk;
#1;
if(((got_OneHertz ^ exp_OneHertz) & mask_OneHertz) !== 1'd0) begin $display("MISMATCH ece241_2014_q7b row=%0d port=OneHertz got=%h expected=%h mask=%h",n,got_OneHertz,exp_OneHertz,mask_OneHertz);$fatal(1,"behavior mismatch");end
if(((got_c_enable ^ exp_c_enable) & mask_c_enable) !== 3'd0) begin $display("MISMATCH ece241_2014_q7b row=%0d port=c_enable got=%h expected=%h mask=%h",n,got_c_enable,exp_c_enable,mask_c_enable);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=9010)$fatal(2,"wrong case count");
$display("PASS ece241_2014_q7b checks=%0d",n);$fclose(file);$finish;end
endmodule
