`timescale 1ns/1ps
module tb;
reg [31:0] v_a;
reg [31:0] v_b;
reg  v_sub;
wire [31:0] got_sum;reg [31:0] exp_sum, mask_sum;
reg [31:0] scan_a;
reg [31:0] scan_b;
reg  scan_sub;
integer file,rc,n=0;top_module dut(.a(v_a),.b(v_b),.sub(v_sub),.sum(got_sum));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/module_addsub.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h\n",scan_a,scan_b,scan_sub,exp_sum,mask_sum);
if(rc!=5)$fatal(2,"vector parse failure");
v_a=scan_a;
v_b=scan_b;
v_sub=scan_sub;
#1;
if(((got_sum ^ exp_sum) & mask_sum) !== 32'd0) begin $display("MISMATCH module_addsub row=%0d port=sum got=%h expected=%h mask=%h",n,got_sum,exp_sum,mask_sum);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=532)$fatal(2,"wrong case count");
$display("PASS module_addsub checks=%0d",n);$fclose(file);$finish;end
endmodule
