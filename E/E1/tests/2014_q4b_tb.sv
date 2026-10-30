`timescale 1ns/1ps
module tb;
reg [3:0] v_SW;
reg [3:0] v_KEY;
wire [3:0] got_LEDR;reg [3:0] exp_LEDR, mask_LEDR;
reg [3:0] scan_SW;
reg [3:0] scan_KEY;
integer file,rc,n=0;top_module dut(.SW(v_SW),.KEY(v_KEY),.LEDR(got_LEDR));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/2014_q4b.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h\n",scan_SW,scan_KEY,exp_LEDR,mask_LEDR);
if(rc!=4)$fatal(2,"vector parse failure");
v_SW=scan_SW;
v_KEY=scan_KEY;
#1;
if(((got_LEDR ^ exp_LEDR) & mask_LEDR) !== 4'd0) begin $display("MISMATCH 2014_q4b row=%0d port=LEDR got=%h expected=%h mask=%h",n,got_LEDR,exp_LEDR,mask_LEDR);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=2002)$fatal(2,"wrong case count");
$display("PASS 2014_q4b checks=%0d",n);$fclose(file);$finish;end
endmodule
