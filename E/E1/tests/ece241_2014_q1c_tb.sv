`timescale 1ns/1ps
module tb;
reg [7:0] v_a;
reg [7:0] v_b;
wire [7:0] got_s;reg [7:0] exp_s, mask_s;
wire  got_overflow;reg  exp_overflow, mask_overflow;
reg [7:0] scan_a;
reg [7:0] scan_b;
integer file,rc,n=0;top_module dut(.a(v_a),.b(v_b),.s(got_s),.overflow(got_overflow));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/ece241_2014_q1c.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h\n",scan_a,scan_b,exp_s,mask_s,exp_overflow,mask_overflow);
if(rc!=6)$fatal(2,"vector parse failure");
v_a=scan_a;
v_b=scan_b;
#1;
if(((got_s ^ exp_s) & mask_s) !== 8'd0) begin $display("MISMATCH ece241_2014_q1c row=%0d port=s got=%h expected=%h mask=%h",n,got_s,exp_s,mask_s);$fatal(1,"behavior mismatch");end
if(((got_overflow ^ exp_overflow) & mask_overflow) !== 1'd0) begin $display("MISMATCH ece241_2014_q1c row=%0d port=overflow got=%h expected=%h mask=%h",n,got_overflow,exp_overflow,mask_overflow);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=65536)$fatal(2,"wrong case count");
$display("PASS ece241_2014_q1c checks=%0d",n);$fclose(file);$finish;end
endmodule
