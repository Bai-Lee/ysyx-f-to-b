`timescale 1ns/1ps
module tb;
reg  v_too_cold;
reg  v_too_hot;
reg  v_mode;
reg  v_fan_on;
wire  got_heater;reg  exp_heater, mask_heater;
wire  got_aircon;reg  exp_aircon, mask_aircon;
wire  got_fan;reg  exp_fan, mask_fan;
reg  scan_too_cold;
reg  scan_too_hot;
reg  scan_mode;
reg  scan_fan_on;
integer file,rc,n=0;top_module dut(.too_cold(v_too_cold),.too_hot(v_too_hot),.mode(v_mode),.fan_on(v_fan_on),.heater(got_heater),.aircon(got_aircon),.fan(got_fan));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/thermostat.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h %h %h %h\n",scan_too_cold,scan_too_hot,scan_mode,scan_fan_on,exp_heater,mask_heater,exp_aircon,mask_aircon,exp_fan,mask_fan);
if(rc!=10)$fatal(2,"vector parse failure");
v_too_cold=scan_too_cold;
v_too_hot=scan_too_hot;
v_mode=scan_mode;
v_fan_on=scan_fan_on;
#1;
if(((got_heater ^ exp_heater) & mask_heater) !== 1'd0) begin $display("MISMATCH thermostat row=%0d port=heater got=%h expected=%h mask=%h",n,got_heater,exp_heater,mask_heater);$fatal(1,"behavior mismatch");end
if(((got_aircon ^ exp_aircon) & mask_aircon) !== 1'd0) begin $display("MISMATCH thermostat row=%0d port=aircon got=%h expected=%h mask=%h",n,got_aircon,exp_aircon,mask_aircon);$fatal(1,"behavior mismatch");end
if(((got_fan ^ exp_fan) & mask_fan) !== 1'd0) begin $display("MISMATCH thermostat row=%0d port=fan got=%h expected=%h mask=%h",n,got_fan,exp_fan,mask_fan);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=16)$fatal(2,"wrong case count");
$display("PASS thermostat checks=%0d",n);$fclose(file);$finish;end
endmodule
