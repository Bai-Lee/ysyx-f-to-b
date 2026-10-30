`timescale 1ns/1ps
module tb;
reg  v_a;
reg  v_b;
wire  got_out;reg  exp_out, mask_out;
reg  scan_a;
reg  scan_b;
integer file,rc,n=0;top_module dut(.a(v_a),.b(v_b),.out(got_out));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/andgate.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h\n",scan_a,scan_b,exp_out,mask_out);
if(rc!=4)$fatal(2,"vector parse failure");
v_a=scan_a;
v_b=scan_b;
#1;
if(((got_out ^ exp_out) & mask_out) !== 1'd0) begin $display("MISMATCH andgate row=%0d port=out got=%h expected=%h mask=%h",n,got_out,exp_out,mask_out);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=4)$fatal(2,"wrong case count");
$display("PASS andgate checks=%0d",n);$fclose(file);$finish;end
endmodule
