`timescale 1ns/1ps
module tb;
reg  v_clk;
reg  v_resetn;
reg [1:0] v_byteena;
reg [15:0] v_d;
wire [15:0] got_q;reg [15:0] exp_q, mask_q;
reg  scan_clk;
reg  scan_resetn;
reg [1:0] scan_byteena;
reg [15:0] scan_d;
integer file,rc,n=0;top_module dut(.clk(v_clk),.resetn(v_resetn),.byteena(v_byteena),.d(v_d),.q(got_q));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/dff16e.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h\n",scan_clk,scan_resetn,scan_byteena,scan_d,exp_q,mask_q);
if(rc!=6)$fatal(2,"vector parse failure");
v_resetn=scan_resetn;
v_byteena=scan_byteena;
v_d=scan_d;
v_clk=scan_clk;
#1;
if(((got_q ^ exp_q) & mask_q) !== 16'd0) begin $display("MISMATCH dff16e row=%0d port=q got=%h expected=%h mask=%h",n,got_q,exp_q,mask_q);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=2000)$fatal(2,"wrong case count");
$display("PASS dff16e checks=%0d",n);$fclose(file);$finish;end
endmodule
