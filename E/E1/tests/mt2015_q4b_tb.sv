`timescale 1ns/1ps
module tb;
reg  v_x;
reg  v_y;
wire  got_z;reg  exp_z, mask_z;
reg  scan_x;
reg  scan_y;
integer file,rc,n=0;top_module dut(.x(v_x),.y(v_y),.z(got_z));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/mt2015_q4b.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h\n",scan_x,scan_y,exp_z,mask_z);
if(rc!=4)$fatal(2,"vector parse failure");
v_x=scan_x;
v_y=scan_y;
#1;
if(((got_z ^ exp_z) & mask_z) !== 1'd0) begin $display("MISMATCH mt2015_q4b row=%0d port=z got=%h expected=%h mask=%h",n,got_z,exp_z,mask_z);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=4)$fatal(2,"wrong case count");
$display("PASS mt2015_q4b checks=%0d",n);$fclose(file);$finish;end
endmodule
