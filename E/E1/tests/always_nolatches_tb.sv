`timescale 1ns/1ps
module tb;
reg [15:0] v_scancode;
wire  got_left;reg  exp_left, mask_left;
wire  got_down;reg  exp_down, mask_down;
wire  got_right;reg  exp_right, mask_right;
wire  got_up;reg  exp_up, mask_up;
reg [15:0] scan_scancode;
integer file,rc,n=0;top_module dut(.scancode(v_scancode),.left(got_left),.down(got_down),.right(got_right),.up(got_up));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/always_nolatches.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h %h %h\n",scan_scancode,exp_left,mask_left,exp_down,mask_down,exp_right,mask_right,exp_up,mask_up);
if(rc!=9)$fatal(2,"vector parse failure");
v_scancode=scan_scancode;
#1;
if(((got_left ^ exp_left) & mask_left) !== 1'd0) begin $display("MISMATCH always_nolatches row=%0d port=left got=%h expected=%h mask=%h",n,got_left,exp_left,mask_left);$fatal(1,"behavior mismatch");end
if(((got_down ^ exp_down) & mask_down) !== 1'd0) begin $display("MISMATCH always_nolatches row=%0d port=down got=%h expected=%h mask=%h",n,got_down,exp_down,mask_down);$fatal(1,"behavior mismatch");end
if(((got_right ^ exp_right) & mask_right) !== 1'd0) begin $display("MISMATCH always_nolatches row=%0d port=right got=%h expected=%h mask=%h",n,got_right,exp_right,mask_right);$fatal(1,"behavior mismatch");end
if(((got_up ^ exp_up) & mask_up) !== 1'd0) begin $display("MISMATCH always_nolatches row=%0d port=up got=%h expected=%h mask=%h",n,got_up,exp_up,mask_up);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=65536)$fatal(2,"wrong case count");
$display("PASS always_nolatches checks=%0d",n);$fclose(file);$finish;end
endmodule
