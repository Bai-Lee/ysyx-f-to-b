`timescale 1ns/1ps
module tb;
reg [2:0] v_a;
reg [2:0] v_b;
wire [2:0] got_out_or_bitwise;reg [2:0] exp_out_or_bitwise, mask_out_or_bitwise;
wire  got_out_or_logical;reg  exp_out_or_logical, mask_out_or_logical;
wire [5:0] got_out_not;reg [5:0] exp_out_not, mask_out_not;
reg [2:0] scan_a;
reg [2:0] scan_b;
integer file,rc,n=0;top_module dut(.a(v_a),.b(v_b),.out_or_bitwise(got_out_or_bitwise),.out_or_logical(got_out_or_logical),.out_not(got_out_not));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/vectorgates.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h %h\n",scan_a,scan_b,exp_out_or_bitwise,mask_out_or_bitwise,exp_out_or_logical,mask_out_or_logical,exp_out_not,mask_out_not);
if(rc!=8)$fatal(2,"vector parse failure");
v_a=scan_a;
v_b=scan_b;
#1;
if(((got_out_or_bitwise ^ exp_out_or_bitwise) & mask_out_or_bitwise) !== 3'd0) begin $display("MISMATCH vectorgates row=%0d port=out_or_bitwise got=%h expected=%h mask=%h",n,got_out_or_bitwise,exp_out_or_bitwise,mask_out_or_bitwise);$fatal(1,"behavior mismatch");end
if(((got_out_or_logical ^ exp_out_or_logical) & mask_out_or_logical) !== 1'd0) begin $display("MISMATCH vectorgates row=%0d port=out_or_logical got=%h expected=%h mask=%h",n,got_out_or_logical,exp_out_or_logical,mask_out_or_logical);$fatal(1,"behavior mismatch");end
if(((got_out_not ^ exp_out_not) & mask_out_not) !== 6'd0) begin $display("MISMATCH vectorgates row=%0d port=out_not got=%h expected=%h mask=%h",n,got_out_not,exp_out_not,mask_out_not);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=64)$fatal(2,"wrong case count");
$display("PASS vectorgates checks=%0d",n);$fclose(file);$finish;end
endmodule
