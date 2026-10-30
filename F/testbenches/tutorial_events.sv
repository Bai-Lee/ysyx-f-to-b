`timescale 1ns/1ps
module tb;reg e=0,reset=1;wire inv,pulse;reg q;integer log;
not #(1) inverter(inv,e);and #(1) both(pulse,e,inv);
always @(posedge pulse or posedge reset)if(reset)q<=0;else q<=1;
initial begin $dumpfile("/workspace/projects/ysyx_f_to_b/artifacts/F/rtl_tutorial_events/trace.vcd");$dumpvars(0,tb);log=$fopen("/workspace/projects/ysyx_f_to_b/artifacts/F/rtl_tutorial_events/events.csv","w");$fwrite(log,"time,e,not_e,pulse,q\n");
#4;reset=0;#6;e=1;#5;
if(pulse!==0||q!==1)$fatal(1,"Propagation pulse was not captured");
$display("PASS EVENT_TRACE final_pulse=0 captured_q=1");$fclose(log);$finish;end
always @(e or inv or pulse or q)if(log)$fwrite(log,"%0t,%b,%b,%b,%b\n",$time,e,inv,pulse,q);
endmodule