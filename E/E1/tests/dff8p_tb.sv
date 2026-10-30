`timescale 1ns/1ps
module tb;
reg  v_clk;
reg  v_reset;
reg [7:0] v_d;
wire [7:0] got_q;reg [7:0] exp_q, mask_q;
reg  scan_clk;
reg  scan_reset;
reg [7:0] scan_d;
integer file,rc,n=0;top_module dut(.clk(v_clk),.reset(v_reset),.d(v_d),.q(got_q));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/dff8p.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h\n",scan_clk,scan_reset,scan_d,exp_q,mask_q);
if(rc!=5)$fatal(2,"vector parse failure");
v_reset=scan_reset;
v_d=scan_d;
v_clk=scan_clk;
#1;
if(((got_q ^ exp_q) & mask_q) !== 8'd0) begin $display("MISMATCH dff8p row=%0d port=q got=%h expected=%h mask=%h",n,got_q,exp_q,mask_q);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=1200)$fatal(2,"wrong case count");
$display("PASS dff8p checks=%0d",n);$fclose(file);$finish;end
endmodule
