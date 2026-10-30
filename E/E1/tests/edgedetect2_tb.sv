`timescale 1ns/1ps
module tb;
reg  v_clk;
reg [7:0] v_in;
wire [7:0] got_anyedge;reg [7:0] exp_anyedge, mask_anyedge;
reg  scan_clk;
reg [7:0] scan_in;
integer file,rc,n=0;top_module dut(.clk(v_clk),.in(v_in),.anyedge(got_anyedge));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/edgedetect2.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h\n",scan_clk,scan_in,exp_anyedge,mask_anyedge);
if(rc!=4)$fatal(2,"vector parse failure");
v_in=scan_in;
v_clk=scan_clk;
#1;
if(((got_anyedge ^ exp_anyedge) & mask_anyedge) !== 8'd0) begin $display("MISMATCH edgedetect2 row=%0d port=anyedge got=%h expected=%h mask=%h",n,got_anyedge,exp_anyedge,mask_anyedge);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=2018)$fatal(2,"wrong case count");
$display("PASS edgedetect2 checks=%0d",n);$fclose(file);$finish;end
endmodule
