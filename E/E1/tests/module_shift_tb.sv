`timescale 1ns/1ps
module tb;
reg  v_clk;
reg  v_d;
wire  got_q;reg  exp_q, mask_q;
reg  scan_clk;
reg  scan_d;
integer file,rc,n=0;top_module dut(.clk(v_clk),.d(v_d),.q(got_q));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/module_shift.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h\n",scan_clk,scan_d,exp_q,mask_q);
if(rc!=4)$fatal(2,"vector parse failure");
v_d=scan_d;
v_clk=scan_clk;
#1;
if(((got_q ^ exp_q) & mask_q) !== 1'd0) begin $display("MISMATCH module_shift row=%0d port=q got=%h expected=%h mask=%h",n,got_q,exp_q,mask_q);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=500)$fatal(2,"wrong case count");
$display("PASS module_shift checks=%0d",n);$fclose(file);$finish;end
endmodule
