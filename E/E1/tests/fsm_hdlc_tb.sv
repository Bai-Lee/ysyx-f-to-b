`timescale 1ns/1ps
module tb;
reg  v_clk;
reg  v_reset;
reg  v_in;
wire  got_disc;reg  exp_disc, mask_disc;
wire  got_flag;reg  exp_flag, mask_flag;
wire  got_err;reg  exp_err, mask_err;
reg  scan_clk;
reg  scan_reset;
reg  scan_in;
integer file,rc,n=0;top_module dut(.clk(v_clk),.reset(v_reset),.in(v_in),.disc(got_disc),.flag(got_flag),.err(got_err));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/fsm_hdlc.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h %h %h\n",scan_clk,scan_reset,scan_in,exp_disc,mask_disc,exp_flag,mask_flag,exp_err,mask_err);
if(rc!=9)$fatal(2,"vector parse failure");
v_reset=scan_reset;
v_in=scan_in;
v_clk=scan_clk;
#1;
if(((got_disc ^ exp_disc) & mask_disc) !== 1'd0) begin $display("MISMATCH fsm_hdlc row=%0d port=disc got=%h expected=%h mask=%h",n,got_disc,exp_disc,mask_disc);$fatal(1,"behavior mismatch");end
if(((got_flag ^ exp_flag) & mask_flag) !== 1'd0) begin $display("MISMATCH fsm_hdlc row=%0d port=flag got=%h expected=%h mask=%h",n,got_flag,exp_flag,mask_flag);$fatal(1,"behavior mismatch");end
if(((got_err ^ exp_err) & mask_err) !== 1'd0) begin $display("MISMATCH fsm_hdlc row=%0d port=err got=%h expected=%h mask=%h",n,got_err,exp_err,mask_err);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=11836)$fatal(2,"wrong case count");
$display("PASS fsm_hdlc checks=%0d",n);$fclose(file);$finish;end
endmodule
