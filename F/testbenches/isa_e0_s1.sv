module tb;
reg clk=0,reset=0;reg[7:0]ins=0,sw=0,btn=0;wire[7:0]pc,led,hx;wire[31:0]gpr;wire[6:0]hh,hl;wire iw;wire[2:0]idx;
integer f,rc,n=0,p,r0,r1,r2,r3,l,h,iv,sv,bv,ep,e0,e1,e2,e3,el,eh;
scpu_core #(.ENHANCED(0),.STAGE(1)) dut(clk,reset,ins,sw,btn,pc,gpr,led,hx,hh,hl,iw,idx);
initial begin
f=$fopen("/workspace/projects/ysyx_f_to_b/F/vectors/isa_e0_s1.txt","r");if(!f)$fatal(1,"vectors missing");
while(!$feof(f))begin
rc=$fscanf(f,"%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d\n",p,r0,r1,r2,r3,l,h,iv,sv,bv,ep,e0,e1,e2,e3,el,eh);
if(rc!=17)$fatal(1,"vector parse rc=%0d",rc);
clk=0;dut.pc=p;dut.rf.regs[0]=r0;dut.rf.regs[1]=r1;dut.rf.regs[2]=r2;dut.rf.regs[3]=r3;dut.led_storage=l;dut.hex_storage=h;ins=iv;sw=sv;btn=bv;
#2;clk=1;#2;
if(pc!==ep[7:0]||gpr!=={e3[7:0],e2[7:0],e1[7:0],e0[7:0]}||led!==el[7:0]||hx!==eh[7:0])begin
$display("MISMATCH unit=%0d prePC=%02x ins=%02x PC got=%02x expected=%02x GPR=%08x expected=%02x%02x%02x%02x",n,p,iv,pc,ep,gpr,e3,e2,e1,e0);$fatal(1,"ISA mismatch");end
n=n+1;
end
$fclose(f);$display("PASS ISA cases=%0d",n);$finish;end endmodule