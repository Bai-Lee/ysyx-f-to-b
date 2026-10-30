`timescale 1ns/1ps
module tb;
reg  v_clk;
reg  v_a;
reg  v_b;
wire  got_out_assign;reg  exp_out_assign, mask_out_assign;
wire  got_out_always_comb;reg  exp_out_always_comb, mask_out_always_comb;
wire  got_out_always_ff;reg  exp_out_always_ff, mask_out_always_ff;
reg  scan_clk;
reg  scan_a;
reg  scan_b;
integer file,rc,n=0;top_module dut(.clk(v_clk),.a(v_a),.b(v_b),.out_assign(got_out_assign),.out_always_comb(got_out_always_comb),.out_always_ff(got_out_always_ff));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/alwaysblock2.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h %h %h\n",scan_clk,scan_a,scan_b,exp_out_assign,mask_out_assign,exp_out_always_comb,mask_out_always_comb,exp_out_always_ff,mask_out_always_ff);
if(rc!=9)$fatal(2,"vector parse failure");
v_a=scan_a;
v_b=scan_b;
v_clk=scan_clk;
#1;
if(((got_out_assign ^ exp_out_assign) & mask_out_assign) !== 1'd0) begin $display("MISMATCH alwaysblock2 row=%0d port=out_assign got=%h expected=%h mask=%h",n,got_out_assign,exp_out_assign,mask_out_assign);$fatal(1,"behavior mismatch");end
if(((got_out_always_comb ^ exp_out_always_comb) & mask_out_always_comb) !== 1'd0) begin $display("MISMATCH alwaysblock2 row=%0d port=out_always_comb got=%h expected=%h mask=%h",n,got_out_always_comb,exp_out_always_comb,mask_out_always_comb);$fatal(1,"behavior mismatch");end
if(((got_out_always_ff ^ exp_out_always_ff) & mask_out_always_ff) !== 1'd0) begin $display("MISMATCH alwaysblock2 row=%0d port=out_always_ff got=%h expected=%h mask=%h",n,got_out_always_ff,exp_out_always_ff,mask_out_always_ff);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=240)$fatal(2,"wrong case count");
$display("PASS alwaysblock2 checks=%0d",n);$fclose(file);$finish;end
endmodule
