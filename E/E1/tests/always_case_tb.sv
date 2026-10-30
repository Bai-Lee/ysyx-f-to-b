`timescale 1ns/1ps
module tb;
reg [2:0] v_sel;
reg [3:0] v_data0;
reg [3:0] v_data1;
reg [3:0] v_data2;
reg [3:0] v_data3;
reg [3:0] v_data4;
reg [3:0] v_data5;
wire [3:0] got_out;reg [3:0] exp_out, mask_out;
reg [2:0] scan_sel;
reg [3:0] scan_data0;
reg [3:0] scan_data1;
reg [3:0] scan_data2;
reg [3:0] scan_data3;
reg [3:0] scan_data4;
reg [3:0] scan_data5;
integer file,rc,n=0;top_module dut(.sel(v_sel),.data0(v_data0),.data1(v_data1),.data2(v_data2),.data3(v_data3),.data4(v_data4),.data5(v_data5),.out(got_out));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/always_case.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h %h %h\n",scan_sel,scan_data0,scan_data1,scan_data2,scan_data3,scan_data4,scan_data5,exp_out,mask_out);
if(rc!=9)$fatal(2,"vector parse failure");
v_sel=scan_sel;
v_data0=scan_data0;
v_data1=scan_data1;
v_data2=scan_data2;
v_data3=scan_data3;
v_data4=scan_data4;
v_data5=scan_data5;
#1;
if(((got_out ^ exp_out) & mask_out) !== 4'd0) begin $display("MISMATCH always_case row=%0d port=out got=%h expected=%h mask=%h",n,got_out,exp_out,mask_out);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=960)$fatal(2,"wrong case count");
$display("PASS always_case checks=%0d",n);$fclose(file);$finish;end
endmodule
