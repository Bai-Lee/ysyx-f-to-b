`timescale 1ns/1ps
module tb;
reg  v_clk;
reg  v_load;
reg [511:0] v_data;
wire [511:0] got_q;reg [511:0] exp_q, mask_q;
reg  scan_clk;
reg  scan_load;
reg [511:0] scan_data;
integer file,rc,n=0;top_module dut(.clk(v_clk),.load(v_load),.data(v_data),.q(got_q));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/rule110.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h\n",scan_clk,scan_load,scan_data,exp_q,mask_q);
if(rc!=5)$fatal(2,"vector parse failure");
v_load=scan_load;
v_data=scan_data;
v_clk=scan_clk;
#1;
if(((got_q ^ exp_q) & mask_q) !== 512'd0) begin $display("MISMATCH rule110 row=%0d port=q got=%h expected=%h mask=%h",n,got_q,exp_q,mask_q);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=1008)$fatal(2,"wrong case count");
$display("PASS rule110 checks=%0d",n);$fclose(file);$finish;end
endmodule
