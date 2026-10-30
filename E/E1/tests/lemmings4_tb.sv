`timescale 1ns/1ps
module tb;
reg  v_clk;
reg  v_areset;
reg  v_bump_left;
reg  v_bump_right;
reg  v_ground;
reg  v_dig;
wire  got_walk_left;reg  exp_walk_left, mask_walk_left;
wire  got_walk_right;reg  exp_walk_right, mask_walk_right;
wire  got_aaah;reg  exp_aaah, mask_aaah;
wire  got_digging;reg  exp_digging, mask_digging;
reg  scan_clk;
reg  scan_areset;
reg  scan_bump_left;
reg  scan_bump_right;
reg  scan_ground;
reg  scan_dig;
integer file,rc,n=0;top_module dut(.clk(v_clk),.areset(v_areset),.bump_left(v_bump_left),.bump_right(v_bump_right),.ground(v_ground),.dig(v_dig),.walk_left(got_walk_left),.walk_right(got_walk_right),.aaah(got_aaah),.digging(got_digging));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/lemmings4.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h %h %h %h %h %h %h %h\n",scan_clk,scan_areset,scan_bump_left,scan_bump_right,scan_ground,scan_dig,exp_walk_left,mask_walk_left,exp_walk_right,mask_walk_right,exp_aaah,mask_aaah,exp_digging,mask_digging);
if(rc!=14)$fatal(2,"vector parse failure");
v_areset=scan_areset;
v_bump_left=scan_bump_left;
v_bump_right=scan_bump_right;
v_ground=scan_ground;
v_dig=scan_dig;
v_clk=scan_clk;
#1;
if(((got_walk_left ^ exp_walk_left) & mask_walk_left) !== 1'd0) begin $display("MISMATCH lemmings4 row=%0d port=walk_left got=%h expected=%h mask=%h",n,got_walk_left,exp_walk_left,mask_walk_left);$fatal(1,"behavior mismatch");end
if(((got_walk_right ^ exp_walk_right) & mask_walk_right) !== 1'd0) begin $display("MISMATCH lemmings4 row=%0d port=walk_right got=%h expected=%h mask=%h",n,got_walk_right,exp_walk_right,mask_walk_right);$fatal(1,"behavior mismatch");end
if(((got_aaah ^ exp_aaah) & mask_aaah) !== 1'd0) begin $display("MISMATCH lemmings4 row=%0d port=aaah got=%h expected=%h mask=%h",n,got_aaah,exp_aaah,mask_aaah);$fatal(1,"behavior mismatch");end
if(((got_digging ^ exp_digging) & mask_digging) !== 1'd0) begin $display("MISMATCH lemmings4 row=%0d port=digging got=%h expected=%h mask=%h",n,got_digging,exp_digging,mask_digging);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=49960)$fatal(2,"wrong case count");
$display("PASS lemmings4 checks=%0d",n);$fclose(file);$finish;end
endmodule
