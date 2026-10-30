`timescale 1ns/1ps
module tb;
reg  v_clk;
reg  v_areset;
reg  v_bump_left;
reg  v_bump_right;
wire  got_walk_left;reg  exp_walk_left, mask_walk_left;
wire  got_walk_right;reg  exp_walk_right, mask_walk_right;
reg  scan_clk;
reg  scan_areset;
reg  scan_bump_left;
reg  scan_bump_right;
integer file,rc,n=0;top_module dut(.clk(v_clk),.areset(v_areset),.bump_left(v_bump_left),.bump_right(v_bump_right),.walk_left(got_walk_left),.walk_right(got_walk_right));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/lemmings1.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h %h\n",scan_clk,scan_areset,scan_bump_left,scan_bump_right,exp_walk_left,mask_walk_left,exp_walk_right,mask_walk_right);
if(rc!=8)$fatal(2,"vector parse failure");
v_areset=scan_areset;
v_bump_left=scan_bump_left;
v_bump_right=scan_bump_right;
v_clk=scan_clk;
#1;
if(((got_walk_left ^ exp_walk_left) & mask_walk_left) !== 1'd0) begin $display("MISMATCH lemmings1 row=%0d port=walk_left got=%h expected=%h mask=%h",n,got_walk_left,exp_walk_left,mask_walk_left);$fatal(1,"behavior mismatch");end
if(((got_walk_right ^ exp_walk_right) & mask_walk_right) !== 1'd0) begin $display("MISMATCH lemmings1 row=%0d port=walk_right got=%h expected=%h mask=%h",n,got_walk_right,exp_walk_right,mask_walk_right);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=3512)$fatal(2,"wrong case count");
$display("PASS lemmings1 checks=%0d",n);$fclose(file);$finish;end
endmodule
