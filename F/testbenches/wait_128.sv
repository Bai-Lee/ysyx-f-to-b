module tb;
reg clk=0,reset=1;reg[7:0]sw=0,btn=0;wire[7:0]pc,ins,led,hx;wire[31:0]gpr;wire[6:0]hh,hl;reg[7:0]old_pc,committed_instruction;
integer f,log,rc,n=0,rv,sv,bv,ep,e0,e1,e2,e3,el,eh,ehh,ehl;
scpu_system #(.ENHANCED(1),.STAGE(2),.IMAGE(2048'h0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c369fbc95180f5582917b1a09040)) dut(clk,reset,sw,btn,pc,ins,gpr,led,hx,hh,hl);
initial begin
$dumpfile("/workspace/projects/ysyx_f_to_b/artifacts/F/rtl_wait_128/trace.vcd");$dumpvars(0,dut);
f=$fopen("/workspace/projects/ysyx_f_to_b/F/vectors/wait_128.txt","r");log=$fopen("/workspace/projects/ysyx_f_to_b/artifacts/F/rtl_wait_128/commits.csv","w");if(!f||!log)$fatal(1,"file open");
$fwrite(log,"cycle,reset,old_pc,instruction,new_pc,r0,r1,r2,r3,led,hex\n");
while(!$feof(f))begin
rc=$fscanf(f,"%d %d %d %d %d %d %d %d %d %d %d %d\n",rv,sv,bv,ep,e0,e1,e2,e3,el,eh,ehh,ehl);if(rc!=12)$fatal(1,"bad vector %0d",rc);
clk=0;reset=rv;sw=sv;btn=bv;#5;old_pc=pc;committed_instruction=ins;clk=1;#1;
if(pc!==ep[7:0]||gpr!=={e3[7:0],e2[7:0],e1[7:0],e0[7:0]}||led!==el[7:0]||hx!==eh[7:0]||hh!==ehh[6:0]||hl!==ehl[6:0])begin
$display("MISMATCH cycle=%0d PC=%02x expected=%02x GPR=%08x expected=%02x%02x%02x%02x LED=%02x/%02x HEX=%02x/%02x",n,pc,ep,gpr,e3,e2,e1,e0,led,el,hx,eh);$fatal(1,"firmware mismatch");end
$fwrite(log,"%0d,%0d,%02x,%02x,%02x,%02x,%02x,%02x,%02x,%02x,%02x\n",n,rv,old_pc,committed_instruction,pc,gpr[7:0],gpr[15:8],gpr[23:16],gpr[31:24],led,hx);
#4;n=n+1;end
$fclose(f);$fclose(log);$display("PASS FIRMWARE wait_128 cycles=%0d pc=%02x r0=%02x r1=%02x r2=%02x r3=%02x led=%02x hex=%02x",n,pc,gpr[7:0],gpr[15:8],gpr[23:16],gpr[31:24],led,hx);$finish;end endmodule