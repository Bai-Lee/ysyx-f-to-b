`timescale 1ns/1ps
module tb;
reg  v_a;
reg  v_b;
reg  v_c;
reg  v_d;
reg  v_e;
wire [24:0] got_out;reg [24:0] exp_out, mask_out;
reg  scan_a;
reg  scan_b;
reg  scan_c;
reg  scan_d;
reg  scan_e;
integer file,rc,n=0;top_module dut(.a(v_a),.b(v_b),.c(v_c),.d(v_d),.e(v_e),.out(got_out));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/vector5.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h\n",scan_a,scan_b,scan_c,scan_d,scan_e,exp_out,mask_out);
if(rc!=7)$fatal(2,"vector parse failure");
v_a=scan_a;
v_b=scan_b;
v_c=scan_c;
v_d=scan_d;
v_e=scan_e;
#1;
if(((got_out ^ exp_out) & mask_out) !== 25'd0) begin $display("MISMATCH vector5 row=%0d port=out got=%h expected=%h mask=%h",n,got_out,exp_out,mask_out);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=32)$fatal(2,"wrong case count");
$display("PASS vector5 checks=%0d",n);$fclose(file);$finish;end
endmodule
