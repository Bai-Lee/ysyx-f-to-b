`timescale 1ns/1ns
module iverilog_top;
 reg clock=0,reset=1;wire done,failed;reg[63:0]cycles=0,max_cycles=500000000;string waveform;
 gate_system system(clock,reset,done,failed);
 initial begin
  if($value$plusargs("max_cycles=%d",max_cycles))begin end
  if($value$plusargs("wave=%s",waveform))begin $dumpfile(waveform);$dumpvars(0,iverilog_top);end
  $pmem_init;
  repeat(5)@(negedge clock);reset=0;
 end
 always #1 clock=~clock;
 always @(negedge clock)if(!reset)begin
  cycles=cycles+1;
  if(done)begin
   $pmem_report(failed);
   if(failed)$fatal(1,"FOUR_STATE_VALIDATION_FAILED");
   else $finish;
  end
  if(cycles>=max_cycles)begin $pmem_report(1);$fatal(1,"CYCLE_LIMIT");end
 end
endmodule
