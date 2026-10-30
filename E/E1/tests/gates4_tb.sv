`timescale 1ns/1ps
module tb;
reg [3:0] v_in;
wire  got_out_and;reg  exp_out_and, mask_out_and;
wire  got_out_or;reg  exp_out_or, mask_out_or;
wire  got_out_xor;reg  exp_out_xor, mask_out_xor;
reg [3:0] scan_in;
integer file,rc,n=0;top_module dut(.in(v_in),.out_and(got_out_and),.out_or(got_out_or),.out_xor(got_out_xor));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/gates4.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h\n",scan_in,exp_out_and,mask_out_and,exp_out_or,mask_out_or,exp_out_xor,mask_out_xor);
if(rc!=7)$fatal(2,"vector parse failure");
v_in=scan_in;
#1;
if(((got_out_and ^ exp_out_and) & mask_out_and) !== 1'd0) begin $display("MISMATCH gates4 row=%0d port=out_and got=%h expected=%h mask=%h",n,got_out_and,exp_out_and,mask_out_and);$fatal(1,"behavior mismatch");end
if(((got_out_or ^ exp_out_or) & mask_out_or) !== 1'd0) begin $display("MISMATCH gates4 row=%0d port=out_or got=%h expected=%h mask=%h",n,got_out_or,exp_out_or,mask_out_or);$fatal(1,"behavior mismatch");end
if(((got_out_xor ^ exp_out_xor) & mask_out_xor) !== 1'd0) begin $display("MISMATCH gates4 row=%0d port=out_xor got=%h expected=%h mask=%h",n,got_out_xor,exp_out_xor,mask_out_xor);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=16)$fatal(2,"wrong case count");
$display("PASS gates4 checks=%0d",n);$fclose(file);$finish;end
endmodule
