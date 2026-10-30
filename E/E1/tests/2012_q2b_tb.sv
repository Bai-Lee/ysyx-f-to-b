`timescale 1ns/1ps
module tb;
reg [5:0] v_y;
reg  v_w;
wire  got_Y1;reg  exp_Y1, mask_Y1;
wire  got_Y3;reg  exp_Y3, mask_Y3;
reg [5:0] scan_y;
reg  scan_w;
integer file,rc,n=0;top_module dut(.y(v_y),.w(v_w),.Y1(got_Y1),.Y3(got_Y3));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/2012_q2b.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h\n",scan_y,scan_w,exp_Y1,mask_Y1,exp_Y3,mask_Y3);
if(rc!=6)$fatal(2,"vector parse failure");
v_y=scan_y;
v_w=scan_w;
#1;
if(((got_Y1 ^ exp_Y1) & mask_Y1) !== 1'd0) begin $display("MISMATCH 2012_q2b row=%0d port=Y1 got=%h expected=%h mask=%h",n,got_Y1,exp_Y1,mask_Y1);$fatal(1,"behavior mismatch");end
if(((got_Y3 ^ exp_Y3) & mask_Y3) !== 1'd0) begin $display("MISMATCH 2012_q2b row=%0d port=Y3 got=%h expected=%h mask=%h",n,got_Y3,exp_Y3,mask_Y3);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=128)$fatal(2,"wrong case count");
$display("PASS 2012_q2b checks=%0d",n);$fclose(file);$finish;end
endmodule
