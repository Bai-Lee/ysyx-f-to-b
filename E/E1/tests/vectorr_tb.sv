`timescale 1ns/1ps
module tb;
reg [7:0] v_in;
wire [7:0] got_out;reg [7:0] exp_out, mask_out;
reg [7:0] scan_in;
integer file,rc,n=0;top_module dut(.in(v_in),.out(got_out));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/vectorr.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h\n",scan_in,exp_out,mask_out);
if(rc!=3)$fatal(2,"vector parse failure");
v_in=scan_in;
#1;
if(((got_out ^ exp_out) & mask_out) !== 8'd0) begin $display("MISMATCH vectorr row=%0d port=out got=%h expected=%h mask=%h",n,got_out,exp_out,mask_out);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=256)$fatal(2,"wrong case count");
$display("PASS vectorr checks=%0d",n);$fclose(file);$finish;end
endmodule
