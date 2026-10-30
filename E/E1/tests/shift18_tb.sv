`timescale 1ns/1ps
module tb;
reg  v_clk;
reg  v_load;
reg  v_ena;
reg [1:0] v_amount;
reg [63:0] v_data;
wire [63:0] got_q;reg [63:0] exp_q, mask_q;
reg  scan_clk;
reg  scan_load;
reg  scan_ena;
reg [1:0] scan_amount;
reg [63:0] scan_data;
integer file,rc,n=0;top_module dut(.clk(v_clk),.load(v_load),.ena(v_ena),.amount(v_amount),.data(v_data),.q(got_q));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/shift18.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h\n",scan_clk,scan_load,scan_ena,scan_amount,scan_data,exp_q,mask_q);
if(rc!=7)$fatal(2,"vector parse failure");
v_load=scan_load;
v_ena=scan_ena;
v_amount=scan_amount;
v_data=scan_data;
v_clk=scan_clk;
#1;
if(((got_q ^ exp_q) & mask_q) !== 64'd0) begin $display("MISMATCH shift18 row=%0d port=q got=%h expected=%h mask=%h",n,got_q,exp_q,mask_q);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=4144)$fatal(2,"wrong case count");
$display("PASS shift18 checks=%0d",n);$fclose(file);$finish;end
endmodule
