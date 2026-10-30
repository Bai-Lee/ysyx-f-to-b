`timescale 1ns/1ps
module tb;
reg  v_clk;
reg  v_reset;
wire [4:0] got_q;reg [4:0] exp_q, mask_q;
reg  scan_clk;
reg  scan_reset;
integer file,rc,n=0;top_module dut(.clk(v_clk),.reset(v_reset),.q(got_q));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/lfsr5.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h\n",scan_clk,scan_reset,exp_q,mask_q);
if(rc!=4)$fatal(2,"vector parse failure");
v_reset=scan_reset;
v_clk=scan_clk;
#1;
if(((got_q ^ exp_q) & mask_q) !== 5'd0) begin $display("MISMATCH lfsr5 row=%0d port=q got=%h expected=%h mask=%h",n,got_q,exp_q,mask_q);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=420)$fatal(2,"wrong case count");
$display("PASS lfsr5 checks=%0d",n);$fclose(file);$finish;end
endmodule
