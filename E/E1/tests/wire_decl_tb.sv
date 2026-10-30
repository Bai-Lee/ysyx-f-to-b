`timescale 1ns/1ps
module tb;
reg  v_a;
reg  v_b;
reg  v_c;
reg  v_d;
wire  got_out;reg  exp_out, mask_out;
wire  got_out_n;reg  exp_out_n, mask_out_n;
reg  scan_a;
reg  scan_b;
reg  scan_c;
reg  scan_d;
integer file,rc,n=0;top_module dut(.a(v_a),.b(v_b),.c(v_c),.d(v_d),.out(got_out),.out_n(got_out_n));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/wire_decl.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h %h\n",scan_a,scan_b,scan_c,scan_d,exp_out,mask_out,exp_out_n,mask_out_n);
if(rc!=8)$fatal(2,"vector parse failure");
v_a=scan_a;
v_b=scan_b;
v_c=scan_c;
v_d=scan_d;
#1;
if(((got_out ^ exp_out) & mask_out) !== 1'd0) begin $display("MISMATCH wire_decl row=%0d port=out got=%h expected=%h mask=%h",n,got_out,exp_out,mask_out);$fatal(1,"behavior mismatch");end
if(((got_out_n ^ exp_out_n) & mask_out_n) !== 1'd0) begin $display("MISMATCH wire_decl row=%0d port=out_n got=%h expected=%h mask=%h",n,got_out_n,exp_out_n,mask_out_n);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=16)$fatal(2,"wrong case count");
$display("PASS wire_decl checks=%0d",n);$fclose(file);$finish;end
endmodule
