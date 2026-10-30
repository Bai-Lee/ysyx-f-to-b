`timescale 1ns/1ps
module tb;
reg  v_a;
reg  v_b;
reg  v_c;
wire  got_w;reg  exp_w, mask_w;
wire  got_x;reg  exp_x, mask_x;
wire  got_y;reg  exp_y, mask_y;
wire  got_z;reg  exp_z, mask_z;
reg  scan_a;
reg  scan_b;
reg  scan_c;
integer file,rc,n=0;top_module dut(.a(v_a),.b(v_b),.c(v_c),.w(got_w),.x(got_x),.y(got_y),.z(got_z));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/wire4.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h %h %h %h %h\n",scan_a,scan_b,scan_c,exp_w,mask_w,exp_x,mask_x,exp_y,mask_y,exp_z,mask_z);
if(rc!=11)$fatal(2,"vector parse failure");
v_a=scan_a;
v_b=scan_b;
v_c=scan_c;
#1;
if(((got_w ^ exp_w) & mask_w) !== 1'd0) begin $display("MISMATCH wire4 row=%0d port=w got=%h expected=%h mask=%h",n,got_w,exp_w,mask_w);$fatal(1,"behavior mismatch");end
if(((got_x ^ exp_x) & mask_x) !== 1'd0) begin $display("MISMATCH wire4 row=%0d port=x got=%h expected=%h mask=%h",n,got_x,exp_x,mask_x);$fatal(1,"behavior mismatch");end
if(((got_y ^ exp_y) & mask_y) !== 1'd0) begin $display("MISMATCH wire4 row=%0d port=y got=%h expected=%h mask=%h",n,got_y,exp_y,mask_y);$fatal(1,"behavior mismatch");end
if(((got_z ^ exp_z) & mask_z) !== 1'd0) begin $display("MISMATCH wire4 row=%0d port=z got=%h expected=%h mask=%h",n,got_z,exp_z,mask_z);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=8)$fatal(2,"wrong case count");
$display("PASS wire4 checks=%0d",n);$fclose(file);$finish;end
endmodule
