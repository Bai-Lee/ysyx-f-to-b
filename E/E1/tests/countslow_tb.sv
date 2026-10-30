`timescale 1ns/1ps
module tb;
reg  v_clk;
reg  v_slowena;
reg  v_reset;
wire [3:0] got_q;reg [3:0] exp_q, mask_q;
reg  scan_clk;
reg  scan_slowena;
reg  scan_reset;
integer file,rc,n=0;top_module dut(.clk(v_clk),.slowena(v_slowena),.reset(v_reset),.q(got_q));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/countslow.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h\n",scan_clk,scan_slowena,scan_reset,exp_q,mask_q);
if(rc!=5)$fatal(2,"vector parse failure");
v_slowena=scan_slowena;
v_reset=scan_reset;
v_clk=scan_clk;
#1;
if(((got_q ^ exp_q) & mask_q) !== 4'd0) begin $display("MISMATCH countslow row=%0d port=q got=%h expected=%h mask=%h",n,got_q,exp_q,mask_q);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=1600)$fatal(2,"wrong case count");
$display("PASS countslow checks=%0d",n);$fclose(file);$finish;end
endmodule
