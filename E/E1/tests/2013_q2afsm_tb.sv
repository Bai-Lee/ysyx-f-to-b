`timescale 1ns/1ps
module tb;
reg  v_clk;
reg  v_resetn;
reg [3:1] v_r;
wire [3:1] got_g;reg [3:1] exp_g, mask_g;
reg  scan_clk;
reg  scan_resetn;
reg [3:1] scan_r;
integer file,rc,n=0;top_module dut(.clk(v_clk),.resetn(v_resetn),.r(v_r),.g(got_g));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/2013_q2afsm.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h\n",scan_clk,scan_resetn,scan_r,exp_g,mask_g);
if(rc!=5)$fatal(2,"vector parse failure");
v_resetn=scan_resetn;
v_r=scan_r;
v_clk=scan_clk;
#1;
if(((got_g ^ exp_g) & mask_g) !== 3'd0) begin $display("MISMATCH 2013_q2afsm row=%0d port=g got=%h expected=%h mask=%h",n,got_g,exp_g,mask_g);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=42960)$fatal(2,"wrong case count");
$display("PASS 2013_q2afsm checks=%0d",n);$fclose(file);$finish;end
endmodule
