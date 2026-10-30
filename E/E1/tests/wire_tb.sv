`timescale 1ns/1ps
module tb;
reg  v_in;
wire  got_out;reg  exp_out, mask_out;
reg  scan_in;
integer file,rc,n=0;top_module dut(.in(v_in),.out(got_out));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/wire.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h\n",scan_in,exp_out,mask_out);
if(rc!=3)$fatal(2,"vector parse failure");
v_in=scan_in;
#1;
if(((got_out ^ exp_out) & mask_out) !== 1'd0) begin $display("MISMATCH wire row=%0d port=out got=%h expected=%h mask=%h",n,got_out,exp_out,mask_out);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=2)$fatal(2,"wrong case count");
$display("PASS wire checks=%0d",n);$fclose(file);$finish;end
endmodule
