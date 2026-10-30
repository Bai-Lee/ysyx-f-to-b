`timescale 1ns/1ps
module tb;
reg [99:0] v_in;
wire [98:0] got_out_both;reg [98:0] exp_out_both, mask_out_both;
wire [99:1] got_out_any;reg [99:1] exp_out_any, mask_out_any;
wire [99:0] got_out_different;reg [99:0] exp_out_different, mask_out_different;
reg [99:0] scan_in;
integer file,rc,n=0;top_module dut(.in(v_in),.out_both(got_out_both),.out_any(got_out_any),.out_different(got_out_different));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/gatesv100.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h\n",scan_in,exp_out_both,mask_out_both,exp_out_any,mask_out_any,exp_out_different,mask_out_different);
if(rc!=7)$fatal(2,"vector parse failure");
v_in=scan_in;
#1;
if(((got_out_both ^ exp_out_both) & mask_out_both) !== 99'd0) begin $display("MISMATCH gatesv100 row=%0d port=out_both got=%h expected=%h mask=%h",n,got_out_both,exp_out_both,mask_out_both);$fatal(1,"behavior mismatch");end
if(((got_out_any ^ exp_out_any) & mask_out_any) !== 99'd0) begin $display("MISMATCH gatesv100 row=%0d port=out_any got=%h expected=%h mask=%h",n,got_out_any,exp_out_any,mask_out_any);$fatal(1,"behavior mismatch");end
if(((got_out_different ^ exp_out_different) & mask_out_different) !== 100'd0) begin $display("MISMATCH gatesv100 row=%0d port=out_different got=%h expected=%h mask=%h",n,got_out_different,exp_out_different,mask_out_different);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=602)$fatal(2,"wrong case count");
$display("PASS gatesv100 checks=%0d",n);$fclose(file);$finish;end
endmodule
