`timescale 1ns/1ps
module tb;
reg [3:0] v_in;
wire [1:0] got_pos;reg [1:0] exp_pos, mask_pos;
reg [3:0] scan_in;
integer file,rc,n=0;top_module dut(.in(v_in),.pos(got_pos));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/always_case2.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h\n",scan_in,exp_pos,mask_pos);
if(rc!=3)$fatal(2,"vector parse failure");
v_in=scan_in;
#1;
if(((got_pos ^ exp_pos) & mask_pos) !== 2'd0) begin $display("MISMATCH always_case2 row=%0d port=pos got=%h expected=%h mask=%h",n,got_pos,exp_pos,mask_pos);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=16)$fatal(2,"wrong case count");
$display("PASS always_case2 checks=%0d",n);$fclose(file);$finish;end
endmodule
