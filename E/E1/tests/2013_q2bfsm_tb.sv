`timescale 1ns/1ps
module tb;
reg  v_clk;
reg  v_resetn;
reg  v_x;
reg  v_y;
wire  got_f;reg  exp_f, mask_f;
wire  got_g;reg  exp_g, mask_g;
reg  scan_clk;
reg  scan_resetn;
reg  scan_x;
reg  scan_y;
integer file,rc,n=0;top_module dut(.clk(v_clk),.resetn(v_resetn),.x(v_x),.y(v_y),.f(got_f),.g(got_g));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/2013_q2bfsm.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h %h\n",scan_clk,scan_resetn,scan_x,scan_y,exp_f,mask_f,exp_g,mask_g);
if(rc!=8)$fatal(2,"vector parse failure");
v_resetn=scan_resetn;
v_x=scan_x;
v_y=scan_y;
v_clk=scan_clk;
#1;
if(((got_f ^ exp_f) & mask_f) !== 1'd0) begin $display("MISMATCH 2013_q2bfsm row=%0d port=f got=%h expected=%h mask=%h",n,got_f,exp_f,mask_f);$fatal(1,"behavior mismatch");end
if(((got_g ^ exp_g) & mask_g) !== 1'd0) begin $display("MISMATCH 2013_q2bfsm row=%0d port=g got=%h expected=%h mask=%h",n,got_g,exp_g,mask_g);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=76672)$fatal(2,"wrong case count");
$display("PASS 2013_q2bfsm checks=%0d",n);$fclose(file);$finish;end
endmodule
