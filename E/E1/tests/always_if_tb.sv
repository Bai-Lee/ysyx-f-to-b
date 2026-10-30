`timescale 1ns/1ps
module tb;
reg  v_a;
reg  v_b;
reg  v_sel_b1;
reg  v_sel_b2;
wire  got_out_assign;reg  exp_out_assign, mask_out_assign;
wire  got_out_always;reg  exp_out_always, mask_out_always;
reg  scan_a;
reg  scan_b;
reg  scan_sel_b1;
reg  scan_sel_b2;
integer file,rc,n=0;top_module dut(.a(v_a),.b(v_b),.sel_b1(v_sel_b1),.sel_b2(v_sel_b2),.out_assign(got_out_assign),.out_always(got_out_always));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/always_if.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h %h\n",scan_a,scan_b,scan_sel_b1,scan_sel_b2,exp_out_assign,mask_out_assign,exp_out_always,mask_out_always);
if(rc!=8)$fatal(2,"vector parse failure");
v_a=scan_a;
v_b=scan_b;
v_sel_b1=scan_sel_b1;
v_sel_b2=scan_sel_b2;
#1;
if(((got_out_assign ^ exp_out_assign) & mask_out_assign) !== 1'd0) begin $display("MISMATCH always_if row=%0d port=out_assign got=%h expected=%h mask=%h",n,got_out_assign,exp_out_assign,mask_out_assign);$fatal(1,"behavior mismatch");end
if(((got_out_always ^ exp_out_always) & mask_out_always) !== 1'd0) begin $display("MISMATCH always_if row=%0d port=out_always got=%h expected=%h mask=%h",n,got_out_always,exp_out_always,mask_out_always);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=16)$fatal(2,"wrong case count");
$display("PASS always_if checks=%0d",n);$fclose(file);$finish;end
endmodule
