`timescale 1ns/1ps
module tb;
reg [4:0] v_a;
reg [4:0] v_b;
reg [4:0] v_c;
reg [4:0] v_d;
reg [4:0] v_e;
reg [4:0] v_f;
wire [7:0] got_w;reg [7:0] exp_w, mask_w;
wire [7:0] got_x;reg [7:0] exp_x, mask_x;
wire [7:0] got_y;reg [7:0] exp_y, mask_y;
wire [7:0] got_z;reg [7:0] exp_z, mask_z;
reg [4:0] scan_a;
reg [4:0] scan_b;
reg [4:0] scan_c;
reg [4:0] scan_d;
reg [4:0] scan_e;
reg [4:0] scan_f;
integer file,rc,n=0;top_module dut(.a(v_a),.b(v_b),.c(v_c),.d(v_d),.e(v_e),.f(v_f),.w(got_w),.x(got_x),.y(got_y),.z(got_z));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/vector3.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h %h %h %h %h %h %h %h\n",scan_a,scan_b,scan_c,scan_d,scan_e,scan_f,exp_w,mask_w,exp_x,mask_x,exp_y,mask_y,exp_z,mask_z);
if(rc!=14)$fatal(2,"vector parse failure");
v_a=scan_a;
v_b=scan_b;
v_c=scan_c;
v_d=scan_d;
v_e=scan_e;
v_f=scan_f;
#1;
if(((got_w ^ exp_w) & mask_w) !== 8'd0) begin $display("MISMATCH vector3 row=%0d port=w got=%h expected=%h mask=%h",n,got_w,exp_w,mask_w);$fatal(1,"behavior mismatch");end
if(((got_x ^ exp_x) & mask_x) !== 8'd0) begin $display("MISMATCH vector3 row=%0d port=x got=%h expected=%h mask=%h",n,got_x,exp_x,mask_x);$fatal(1,"behavior mismatch");end
if(((got_y ^ exp_y) & mask_y) !== 8'd0) begin $display("MISMATCH vector3 row=%0d port=y got=%h expected=%h mask=%h",n,got_y,exp_y,mask_y);$fatal(1,"behavior mismatch");end
if(((got_z ^ exp_z) & mask_z) !== 8'd0) begin $display("MISMATCH vector3 row=%0d port=z got=%h expected=%h mask=%h",n,got_z,exp_z,mask_z);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=462)$fatal(2,"wrong case count");
$display("PASS vector3 checks=%0d",n);$fclose(file);$finish;end
endmodule
