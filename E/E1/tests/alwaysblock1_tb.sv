`timescale 1ns/1ps
module tb;
reg  v_a;
reg  v_b;
wire  got_out_assign;reg  exp_out_assign, mask_out_assign;
wire  got_out_alwaysblock;reg  exp_out_alwaysblock, mask_out_alwaysblock;
reg  scan_a;
reg  scan_b;
integer file,rc,n=0;top_module dut(.a(v_a),.b(v_b),.out_assign(got_out_assign),.out_alwaysblock(got_out_alwaysblock));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/alwaysblock1.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h\n",scan_a,scan_b,exp_out_assign,mask_out_assign,exp_out_alwaysblock,mask_out_alwaysblock);
if(rc!=6)$fatal(2,"vector parse failure");
v_a=scan_a;
v_b=scan_b;
#1;
if(((got_out_assign ^ exp_out_assign) & mask_out_assign) !== 1'd0) begin $display("MISMATCH alwaysblock1 row=%0d port=out_assign got=%h expected=%h mask=%h",n,got_out_assign,exp_out_assign,mask_out_assign);$fatal(1,"behavior mismatch");end
if(((got_out_alwaysblock ^ exp_out_alwaysblock) & mask_out_alwaysblock) !== 1'd0) begin $display("MISMATCH alwaysblock1 row=%0d port=out_alwaysblock got=%h expected=%h mask=%h",n,got_out_alwaysblock,exp_out_alwaysblock,mask_out_alwaysblock);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=4)$fatal(2,"wrong case count");
$display("PASS alwaysblock1 checks=%0d",n);$fclose(file);$finish;end
endmodule
