`timescale 1ns/1ps
module tb;
reg  v_a;
reg  v_b;
reg  v_c;
reg  v_d;
reg  v_stub0;
reg  v_stub1;
wire  got_out1;reg  exp_out1, mask_out1;
wire  got_out2;reg  exp_out2, mask_out2;
reg  scan_a;
reg  scan_b;
reg  scan_c;
reg  scan_d;
reg  scan_stub0;
reg  scan_stub1;
integer file,rc,n=0;top_module dut(.a(v_a),.b(v_b),.c(v_c),.d(v_d),.out1(got_out1),.out2(got_out2));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/module_name.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h %h %h %h\n",scan_a,scan_b,scan_c,scan_d,scan_stub0,scan_stub1,exp_out1,mask_out1,exp_out2,mask_out2);
if(rc!=10)$fatal(2,"vector parse failure");
v_a=scan_a;
v_b=scan_b;
v_c=scan_c;
v_d=scan_d;
v_stub0=scan_stub0;
v_stub1=scan_stub1;
#1;
if(((got_out1 ^ exp_out1) & mask_out1) !== 1'd0) begin $display("MISMATCH module_name row=%0d port=out1 got=%h expected=%h mask=%h",n,got_out1,exp_out1,mask_out1);$fatal(1,"behavior mismatch");end
if(((got_out2 ^ exp_out2) & mask_out2) !== 1'd0) begin $display("MISMATCH module_name row=%0d port=out2 got=%h expected=%h mask=%h",n,got_out2,exp_out2,mask_out2);$fatal(1,"behavior mismatch");end
if(dut.u.in1!==v_a||dut.u.in2!==v_b||dut.u.in3!==v_c||dut.u.in4!==v_d)$fatal(1,"MISMATCH module input mapping");
n=n+1;end
if(n!=64)$fatal(2,"wrong case count");
$display("PASS module_name checks=%0d",n);$fclose(file);$finish;end
endmodule
