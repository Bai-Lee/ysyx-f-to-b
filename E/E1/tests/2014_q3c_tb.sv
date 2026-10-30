`timescale 1ns/1ps
module tb;
reg  v_clk;
reg [2:0] v_y;
reg  v_x;
wire  got_Y0;reg  exp_Y0, mask_Y0;
wire  got_z;reg  exp_z, mask_z;
reg  scan_clk;
reg [2:0] scan_y;
reg  scan_x;
integer file,rc,n=0;top_module dut(.clk(v_clk),.y(v_y),.x(v_x),.Y0(got_Y0),.z(got_z));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/2014_q3c.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h\n",scan_clk,scan_y,scan_x,exp_Y0,mask_Y0,exp_z,mask_z);
if(rc!=7)$fatal(2,"vector parse failure");
v_y=scan_y;
v_x=scan_x;
v_clk=scan_clk;
#1;
if(((got_Y0 ^ exp_Y0) & mask_Y0) !== 1'd0) begin $display("MISMATCH 2014_q3c row=%0d port=Y0 got=%h expected=%h mask=%h",n,got_Y0,exp_Y0,mask_Y0);$fatal(1,"behavior mismatch");end
if(((got_z ^ exp_z) & mask_z) !== 1'd0) begin $display("MISMATCH 2014_q3c row=%0d port=z got=%h expected=%h mask=%h",n,got_z,exp_z,mask_z);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=32)$fatal(2,"wrong case count");
$display("PASS 2014_q3c checks=%0d",n);$fclose(file);$finish;end
endmodule
