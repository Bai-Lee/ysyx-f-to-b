`timescale 1ns/1ps
module tb;
reg  v_cpu_overheated;
reg  v_arrived;
reg  v_gas_tank_empty;
wire  got_shut_off_computer;reg  exp_shut_off_computer, mask_shut_off_computer;
wire  got_keep_driving;reg  exp_keep_driving, mask_keep_driving;
reg  scan_cpu_overheated;
reg  scan_arrived;
reg  scan_gas_tank_empty;
integer file,rc,n=0;top_module dut(.cpu_overheated(v_cpu_overheated),.shut_off_computer(got_shut_off_computer),.arrived(v_arrived),.gas_tank_empty(v_gas_tank_empty),.keep_driving(got_keep_driving));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/always_if2.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h\n",scan_cpu_overheated,scan_arrived,scan_gas_tank_empty,exp_shut_off_computer,mask_shut_off_computer,exp_keep_driving,mask_keep_driving);
if(rc!=7)$fatal(2,"vector parse failure");
v_cpu_overheated=scan_cpu_overheated;
v_arrived=scan_arrived;
v_gas_tank_empty=scan_gas_tank_empty;
#1;
if(((got_shut_off_computer ^ exp_shut_off_computer) & mask_shut_off_computer) !== 1'd0) begin $display("MISMATCH always_if2 row=%0d port=shut_off_computer got=%h expected=%h mask=%h",n,got_shut_off_computer,exp_shut_off_computer,mask_shut_off_computer);$fatal(1,"behavior mismatch");end
if(((got_keep_driving ^ exp_keep_driving) & mask_keep_driving) !== 1'd0) begin $display("MISMATCH always_if2 row=%0d port=keep_driving got=%h expected=%h mask=%h",n,got_keep_driving,exp_keep_driving,mask_keep_driving);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=8)$fatal(2,"wrong case count");
$display("PASS always_if2 checks=%0d",n);$fclose(file);$finish;end
endmodule
