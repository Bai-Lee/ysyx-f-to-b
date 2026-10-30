`timescale 1ns/1ps
module tb;
reg  v_p1a;
reg  v_p1b;
reg  v_p1c;
reg  v_p1d;
reg  v_p1e;
reg  v_p1f;
reg  v_p2a;
reg  v_p2b;
reg  v_p2c;
reg  v_p2d;
wire  got_p1y;reg  exp_p1y, mask_p1y;
wire  got_p2y;reg  exp_p2y, mask_p2y;
reg  scan_p1a;
reg  scan_p1b;
reg  scan_p1c;
reg  scan_p1d;
reg  scan_p1e;
reg  scan_p1f;
reg  scan_p2a;
reg  scan_p2b;
reg  scan_p2c;
reg  scan_p2d;
integer file,rc,n=0;top_module dut(.p1a(v_p1a),.p1b(v_p1b),.p1c(v_p1c),.p1d(v_p1d),.p1e(v_p1e),.p1f(v_p1f),.p1y(got_p1y),.p2a(v_p2a),.p2b(v_p2b),.p2c(v_p2c),.p2d(v_p2d),.p2y(got_p2y));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/7458.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h %h %h %h %h %h %h %h\n",scan_p1a,scan_p1b,scan_p1c,scan_p1d,scan_p1e,scan_p1f,scan_p2a,scan_p2b,scan_p2c,scan_p2d,exp_p1y,mask_p1y,exp_p2y,mask_p2y);
if(rc!=14)$fatal(2,"vector parse failure");
v_p1a=scan_p1a;
v_p1b=scan_p1b;
v_p1c=scan_p1c;
v_p1d=scan_p1d;
v_p1e=scan_p1e;
v_p1f=scan_p1f;
v_p2a=scan_p2a;
v_p2b=scan_p2b;
v_p2c=scan_p2c;
v_p2d=scan_p2d;
#1;
if(((got_p1y ^ exp_p1y) & mask_p1y) !== 1'd0) begin $display("MISMATCH 7458 row=%0d port=p1y got=%h expected=%h mask=%h",n,got_p1y,exp_p1y,mask_p1y);$fatal(1,"behavior mismatch");end
if(((got_p2y ^ exp_p2y) & mask_p2y) !== 1'd0) begin $display("MISMATCH 7458 row=%0d port=p2y got=%h expected=%h mask=%h",n,got_p2y,exp_p2y,mask_p2y);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=1024)$fatal(2,"wrong case count");
$display("PASS 7458 checks=%0d",n);$fclose(file);$finish;end
endmodule
