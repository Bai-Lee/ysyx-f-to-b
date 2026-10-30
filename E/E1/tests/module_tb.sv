`timescale 1ns/1ps
module tb;
reg  v_a;
reg  v_b;
reg  v_stub0;
wire  got_out;reg  exp_out, mask_out;
reg  scan_a;
reg  scan_b;
reg  scan_stub0;
integer file,rc,n=0;top_module dut(.a(v_a),.b(v_b),.out(got_out));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/module.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h\n",scan_a,scan_b,scan_stub0,exp_out,mask_out);
if(rc!=5)$fatal(2,"vector parse failure");
v_a=scan_a;
v_b=scan_b;
v_stub0=scan_stub0;
#1;
if(((got_out ^ exp_out) & mask_out) !== 1'd0) begin $display("MISMATCH module row=%0d port=out got=%h expected=%h mask=%h",n,got_out,exp_out,mask_out);$fatal(1,"behavior mismatch");end
if(dut.u.in1!==v_a||dut.u.in2!==v_b)$fatal(1,"MISMATCH module input mapping");
n=n+1;end
if(n!=8)$fatal(2,"wrong case count");
$display("PASS module checks=%0d",n);$fclose(file);$finish;end
endmodule
