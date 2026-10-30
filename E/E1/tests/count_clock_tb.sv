`timescale 1ns/1ps
module tb;
reg  v_clk;
reg  v_reset;
reg  v_ena;
wire  got_pm;reg  exp_pm, mask_pm;
wire [7:0] got_hh;reg [7:0] exp_hh, mask_hh;
wire [7:0] got_mm;reg [7:0] exp_mm, mask_mm;
wire [7:0] got_ss;reg [7:0] exp_ss, mask_ss;
reg  scan_clk;
reg  scan_reset;
reg  scan_ena;
integer file,rc,n=0;top_module dut(.clk(v_clk),.reset(v_reset),.ena(v_ena),.pm(got_pm),.hh(got_hh),.mm(got_mm),.ss(got_ss));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/count_clock.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h %h %h %h %h\n",scan_clk,scan_reset,scan_ena,exp_pm,mask_pm,exp_hh,mask_hh,exp_mm,mask_mm,exp_ss,mask_ss);
if(rc!=11)$fatal(2,"vector parse failure");
v_reset=scan_reset;
v_ena=scan_ena;
v_clk=scan_clk;
#1;
if(((got_pm ^ exp_pm) & mask_pm) !== 1'd0) begin $display("MISMATCH count_clock row=%0d port=pm got=%h expected=%h mask=%h",n,got_pm,exp_pm,mask_pm);$fatal(1,"behavior mismatch");end
if(((got_hh ^ exp_hh) & mask_hh) !== 8'd0) begin $display("MISMATCH count_clock row=%0d port=hh got=%h expected=%h mask=%h",n,got_hh,exp_hh,mask_hh);$fatal(1,"behavior mismatch");end
if(((got_mm ^ exp_mm) & mask_mm) !== 8'd0) begin $display("MISMATCH count_clock row=%0d port=mm got=%h expected=%h mask=%h",n,got_mm,exp_mm,mask_mm);$fatal(1,"behavior mismatch");end
if(((got_ss ^ exp_ss) & mask_ss) !== 8'd0) begin $display("MISMATCH count_clock row=%0d port=ss got=%h expected=%h mask=%h",n,got_ss,exp_ss,mask_ss);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=172822)$fatal(2,"wrong case count");
$display("PASS count_clock checks=%0d",n);$fclose(file);$finish;end
endmodule
