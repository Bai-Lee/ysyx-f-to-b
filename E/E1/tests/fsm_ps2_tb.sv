`timescale 1ns/1ps
module tb;
reg  v_clk;
reg [7:0] v_in;
reg  v_reset;
wire  got_done;reg  exp_done, mask_done;
reg  scan_clk;
reg [7:0] scan_in;
reg  scan_reset;
integer file,rc,n=0;top_module dut(.clk(v_clk),.in(v_in),.reset(v_reset),.done(got_done));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/fsm_ps2.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h\n",scan_clk,scan_in,scan_reset,exp_done,mask_done);
if(rc!=5)$fatal(2,"vector parse failure");
v_in=scan_in;
v_reset=scan_reset;
v_clk=scan_clk;
#1;
if(((got_done ^ exp_done) & mask_done) !== 1'd0) begin $display("MISMATCH fsm_ps2 row=%0d port=done got=%h expected=%h mask=%h",n,got_done,exp_done,mask_done);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=9670)$fatal(2,"wrong case count");
$display("PASS fsm_ps2 checks=%0d",n);$fclose(file);$finish;end
endmodule
