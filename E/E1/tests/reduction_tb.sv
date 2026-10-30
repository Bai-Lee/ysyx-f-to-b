`timescale 1ns/1ps
module tb;
reg [7:0] v_in;
wire  got_parity;reg  exp_parity, mask_parity;
reg [7:0] scan_in;
integer file,rc,n=0;top_module dut(.in(v_in),.parity(got_parity));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/reduction.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h\n",scan_in,exp_parity,mask_parity);
if(rc!=3)$fatal(2,"vector parse failure");
v_in=scan_in;
#1;
if(((got_parity ^ exp_parity) & mask_parity) !== 1'd0) begin $display("MISMATCH reduction row=%0d port=parity got=%h expected=%h mask=%h",n,got_parity,exp_parity,mask_parity);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=256)$fatal(2,"wrong case count");
$display("PASS reduction checks=%0d",n);$fclose(file);$finish;end
endmodule
