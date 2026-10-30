`timescale 1ns/1ps
module tb;
reg [1023:0] v_in;
reg [7:0] v_sel;
wire [3:0] got_out;reg [3:0] exp_out, mask_out;
reg [1023:0] scan_in;
reg [7:0] scan_sel;
integer file,rc,n=0;top_module dut(.in(v_in),.sel(v_sel),.out(got_out));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/mux256to1v.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h\n",scan_in,scan_sel,exp_out,mask_out);
if(rc!=4)$fatal(2,"vector parse failure");
v_in=scan_in;
v_sel=scan_sel;
#1;
if(((got_out ^ exp_out) & mask_out) !== 4'd0) begin $display("MISMATCH mux256to1v row=%0d port=out got=%h expected=%h mask=%h",n,got_out,exp_out,mask_out);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=1536)$fatal(2,"wrong case count");
$display("PASS mux256to1v checks=%0d",n);$fclose(file);$finish;end
endmodule
