`timescale 1ns/1ps
module tb;
reg [15:0] v_in;
wire [7:0] got_out_hi;reg [7:0] exp_out_hi, mask_out_hi;
wire [7:0] got_out_lo;reg [7:0] exp_out_lo, mask_out_lo;
reg [15:0] scan_in;
integer file,rc,n=0;top_module dut(.in(v_in),.out_hi(got_out_hi),.out_lo(got_out_lo));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/vector1.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h\n",scan_in,exp_out_hi,mask_out_hi,exp_out_lo,mask_out_lo);
if(rc!=5)$fatal(2,"vector parse failure");
v_in=scan_in;
#1;
if(((got_out_hi ^ exp_out_hi) & mask_out_hi) !== 8'd0) begin $display("MISMATCH vector1 row=%0d port=out_hi got=%h expected=%h mask=%h",n,got_out_hi,exp_out_hi,mask_out_hi);$fatal(1,"behavior mismatch");end
if(((got_out_lo ^ exp_out_lo) & mask_out_lo) !== 8'd0) begin $display("MISMATCH vector1 row=%0d port=out_lo got=%h expected=%h mask=%h",n,got_out_lo,exp_out_lo,mask_out_lo);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=65536)$fatal(2,"wrong case count");
$display("PASS vector1 checks=%0d",n);$fclose(file);$finish;end
endmodule
