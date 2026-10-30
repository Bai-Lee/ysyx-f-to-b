`timescale 1ns/1ps
module tb;
reg [7:0] v_a;
reg [7:0] v_b;
reg [7:0] v_c;
reg [7:0] v_d;
wire [7:0] got_min;reg [7:0] exp_min, mask_min;
reg [7:0] scan_a;
reg [7:0] scan_b;
reg [7:0] scan_c;
reg [7:0] scan_d;
integer file,rc,n=0;top_module dut(.a(v_a),.b(v_b),.c(v_c),.d(v_d),.min(got_min));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/conditional.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h\n",scan_a,scan_b,scan_c,scan_d,exp_min,mask_min);
if(rc!=6)$fatal(2,"vector parse failure");
v_a=scan_a;
v_b=scan_b;
v_c=scan_c;
v_d=scan_d;
#1;
if(((got_min ^ exp_min) & mask_min) !== 8'd0) begin $display("MISMATCH conditional row=%0d port=min got=%h expected=%h mask=%h",n,got_min,exp_min,mask_min);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=466)$fatal(2,"wrong case count");
$display("PASS conditional checks=%0d",n);$fclose(file);$finish;end
endmodule
