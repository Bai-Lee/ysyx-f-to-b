`timescale 1ns/1ps
module tb;
reg  v_clk;
reg  v_reset;
reg [3:1] v_s;
wire  got_fr3;reg  exp_fr3, mask_fr3;
wire  got_fr2;reg  exp_fr2, mask_fr2;
wire  got_fr1;reg  exp_fr1, mask_fr1;
wire  got_dfr;reg  exp_dfr, mask_dfr;
reg  scan_clk;
reg  scan_reset;
reg [3:1] scan_s;
integer file,rc,n=0;top_module dut(.clk(v_clk),.reset(v_reset),.s(v_s),.fr3(got_fr3),.fr2(got_fr2),.fr1(got_fr1),.dfr(got_dfr));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/ece241_2013_q4.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h %h %h %h %h\n",scan_clk,scan_reset,scan_s,exp_fr3,mask_fr3,exp_fr2,mask_fr2,exp_fr1,mask_fr1,exp_dfr,mask_dfr);
if(rc!=11)$fatal(2,"vector parse failure");
v_reset=scan_reset;
v_s=scan_s;
v_clk=scan_clk;
#1;
if(((got_fr3 ^ exp_fr3) & mask_fr3) !== 1'd0) begin $display("MISMATCH ece241_2013_q4 row=%0d port=fr3 got=%h expected=%h mask=%h",n,got_fr3,exp_fr3,mask_fr3);$fatal(1,"behavior mismatch");end
if(((got_fr2 ^ exp_fr2) & mask_fr2) !== 1'd0) begin $display("MISMATCH ece241_2013_q4 row=%0d port=fr2 got=%h expected=%h mask=%h",n,got_fr2,exp_fr2,mask_fr2);$fatal(1,"behavior mismatch");end
if(((got_fr1 ^ exp_fr1) & mask_fr1) !== 1'd0) begin $display("MISMATCH ece241_2013_q4 row=%0d port=fr1 got=%h expected=%h mask=%h",n,got_fr1,exp_fr1,mask_fr1);$fatal(1,"behavior mismatch");end
if(((got_dfr ^ exp_dfr) & mask_dfr) !== 1'd0) begin $display("MISMATCH ece241_2013_q4 row=%0d port=dfr got=%h expected=%h mask=%h",n,got_dfr,exp_dfr,mask_dfr);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=2560)$fatal(2,"wrong case count");
$display("PASS ece241_2013_q4 checks=%0d",n);$fclose(file);$finish;end
endmodule
