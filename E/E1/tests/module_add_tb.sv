`timescale 1ns/1ps
module tb;
reg [31:0] v_a;
reg [31:0] v_b;
wire [31:0] got_sum;reg [31:0] exp_sum, mask_sum;
reg [31:0] scan_a;
reg [31:0] scan_b;
integer file,rc,n=0;top_module dut(.a(v_a),.b(v_b),.sum(got_sum));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/module_add.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h\n",scan_a,scan_b,exp_sum,mask_sum);
if(rc!=4)$fatal(2,"vector parse failure");
v_a=scan_a;
v_b=scan_b;
#1;
if(((got_sum ^ exp_sum) & mask_sum) !== 32'd0) begin $display("MISMATCH module_add row=%0d port=sum got=%h expected=%h mask=%h",n,got_sum,exp_sum,mask_sum);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=735)$fatal(2,"wrong case count");
$display("PASS module_add checks=%0d",n);$fclose(file);$finish;end
endmodule
