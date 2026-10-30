`timescale 1ns/1ps
module tb;
wire  got_one;reg  exp_one, mask_one;
integer file,rc,n=0;top_module dut(.one(got_one));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/step_one.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h\n",exp_one,mask_one);
if(rc!=2)$fatal(2,"vector parse failure");

#1;
if(((got_one ^ exp_one) & mask_one) !== 1'd0) begin $display("MISMATCH step_one row=%0d port=one got=%h expected=%h mask=%h",n,got_one,exp_one,mask_one);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=2)$fatal(2,"wrong case count");
$display("PASS step_one checks=%0d",n);$fclose(file);$finish;end
endmodule
