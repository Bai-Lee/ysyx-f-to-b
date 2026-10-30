`timescale 1ns/1ps
module tb;
reg [399:0] v_a;
reg [399:0] v_b;
reg  v_cin;
wire  got_cout;reg  exp_cout, mask_cout;
wire [399:0] got_sum;reg [399:0] exp_sum, mask_sum;
reg [399:0] scan_a;
reg [399:0] scan_b;
reg  scan_cin;
integer file,rc,n=0;top_module dut(.a(v_a),.b(v_b),.cin(v_cin),.cout(got_cout),.sum(got_sum));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/bcdadd100.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h\n",scan_a,scan_b,scan_cin,exp_cout,mask_cout,exp_sum,mask_sum);
if(rc!=7)$fatal(2,"vector parse failure");
v_a=scan_a;
v_b=scan_b;
v_cin=scan_cin;
#1;
if(((got_cout ^ exp_cout) & mask_cout) !== 1'd0) begin $display("MISMATCH bcdadd100 row=%0d port=cout got=%h expected=%h mask=%h",n,got_cout,exp_cout,mask_cout);$fatal(1,"behavior mismatch");end
if(((got_sum ^ exp_sum) & mask_sum) !== 400'd0) begin $display("MISMATCH bcdadd100 row=%0d port=sum got=%h expected=%h mask=%h",n,got_sum,exp_sum,mask_sum);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=502)$fatal(2,"wrong case count");
$display("PASS bcdadd100 checks=%0d",n);$fclose(file);$finish;end
endmodule
