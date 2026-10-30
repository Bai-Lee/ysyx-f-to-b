`timescale 1ns/1ps
module tb;
reg clock=0,reset=1;reg [31:0] inst=32'h00000013;wire[31:0] pc,ma,mw,cp,ci,cn;
wire[2:0] ms,fault;wire mr,mwe,valid,ebreak,halted,commit;wire[511:0] regs;
rv32e_core dut(clock,reset,inst,32'b0,pc,ma,mw,ms,mr,mwe,valid,ebreak,halted,fault,commit,cp,ci,cn,regs);
task tick;begin clock=0;#1;clock=1;#1;end endtask
task check_reset;integer i;begin
 if(pc!==32'h80000000||halted!==0||fault!==0||commit!==0||mr!==0||mwe!==0)$fatal(1,"RESET_CONTROL");
 for(i=0;i<16;i=i+1)if(regs[32*i+:32]!==0)$fatal(1,"RESET_REGISTER %0d",i);
end endtask
initial begin
 tick;check_reset;
 reset=0;inst=32'hfff00793;tick;if(regs[15*32+:32]!==32'hffffffff)$fatal(1,"seed x15");
 inst=32'h00500093;tick;if(regs[32+:32]!==5)$fatal(1,"seed ra");
 reset=1;tick;check_reset;
 reset=0;inst=32'h00100073;tick;if(!halted||!commit)$fatal(1,"halt");
 inst=32'h00100793;tick;if(commit||regs[15*32+:32]!==0||pc!==32'h80000004)$fatal(1,"post halt");
 reset=1;tick;check_reset;
 reset=0;inst=32'h00100813;tick;if(!halted||fault!==2||commit)$fatal(1,"x16 fault");
 reset=1;tick;check_reset;
 $display("RESET_PASS initial dirty halt fault and quiet outputs");$finish;
end
endmodule
