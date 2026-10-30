`timescale 1ns/1ps
module tb;
wire  got_zero;reg  exp_zero, mask_zero;
integer file,rc,n=0;top_module dut(.zero(got_zero));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/zero.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h\n",exp_zero,mask_zero);
if(rc!=2)$fatal(2,"vector parse failure");

#1;
if(((got_zero ^ exp_zero) & mask_zero) !== 1'd0) begin $display("MISMATCH zero row=%0d port=zero got=%h expected=%h mask=%h",n,got_zero,exp_zero,mask_zero);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=2)$fatal(2,"wrong case count");
$display("PASS zero checks=%0d",n);$fclose(file);$finish;end
endmodule
