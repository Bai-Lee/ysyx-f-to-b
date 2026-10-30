`timescale 1ns/1ps
module tb;
reg  v_clk;
reg [7:0] v_in;
wire [7:0] got_pedge;reg [7:0] exp_pedge, mask_pedge;
reg  scan_clk;
reg [7:0] scan_in;
integer file,rc,n=0;top_module dut(.clk(v_clk),.in(v_in),.pedge(got_pedge));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/edgedetect.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h\n",scan_clk,scan_in,exp_pedge,mask_pedge);
if(rc!=4)$fatal(2,"vector parse failure");
v_in=scan_in;
v_clk=scan_clk;
#1;
if(((got_pedge ^ exp_pedge) & mask_pedge) !== 8'd0) begin $display("MISMATCH edgedetect row=%0d port=pedge got=%h expected=%h mask=%h",n,got_pedge,exp_pedge,mask_pedge);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=2018)$fatal(2,"wrong case count");
$display("PASS edgedetect checks=%0d",n);$fclose(file);$finish;end
endmodule
