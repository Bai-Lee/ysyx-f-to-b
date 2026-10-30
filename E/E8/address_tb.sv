`timescale 1ns/1ns
module address_tb;
 reg clock=0,reset=1;always #1 clock=~clock;
 wire iq,lq,lw;wire[31:0]ia,la,wd;wire[3:0]mask;wire[1:0]size;
 reg ir=0,lr=0;reg[31:0]idata=0,ldata=0;
 wire[31:0]pc,cp,ci,cn;wire halt,commit;wire[2:0]fault,state;wire[511:0]gprs;wire[63:0]count;
 minirv_bus dut(clock,reset,iq,ia,ir,idata,lq,la,size,lw,wd,mask,lr,ldata,pc,halt,fault,commit,cp,ci,cn,gprs,count,state);
 reg[31:0]rom[0:64];reg[31:0]addresses[0:15];integer request=0,run_number=0;string romfile,addrfile;
`ifdef TEST_ADDRESS_CLIPPING
 wire[31:0]observed_addr={4'b0,la[27:0]};
`else
 wire[31:0]observed_addr=la;
`endif
 initial begin
  if(!$value$plusargs("rom=%s",romfile)||!$value$plusargs("addresses=%s",addrfile))$fatal(1,"fixture path missing");
  $readmemh(romfile,rom,0,64);$readmemh(addrfile,addresses,0,15);
  repeat(3)@(negedge clock);if(gprs!==512'b0)$fatal(1,"cold reset did not clear registers");reset=0;
  wait(halt);@(negedge clock);if(fault!==0||request!=32)$fatal(1,"first execution incomplete");
  reset=1;run_number=1;repeat(3)@(negedge clock);if(gprs!==512'b0||pc!==32'h80000000)$fatal(1,"warm reset failed");reset=0;
  wait(halt);@(negedge clock);if(fault!==0||request!=32)$fatal(1,"second execution incomplete");
  $display("FULL_ADDRESS_AND_WARM_RESET_PASS 16 addresses x read/write x 2 runs");$finish;
 end
 always @(posedge clock)begin
  if(reset)begin ir<=0;lr<=0;idata<=0;ldata<=0;request=0;end
  else begin
   ir<=iq;lr<=lq;
   if(iq)begin
    if(ia<32'h80000000||ia>32'h80000100||ia[1:0]!=0)$fatal(1,"unexpected fetch address");
    idata<=rom[(ia-32'h80000000)>>2];
   end
   if(lq)begin
    if(request>=32||observed_addr!==addresses[request/2]||size!==0)$fatal(1,"ADDRESS_FORWARDING_ERROR index=%0d addr=%h expected=%h",request,observed_addr,addresses[request/2]);
    if((request%2)==0)begin
     if(lw!==0)$fatal(1,"expected byte load");
     ldata<=32'ha5<<(8*la[1:0]);
    end else begin
     if(lw!==1||mask!==(4'b1<<la[1:0])||wd!==(32'ha5<<(8*la[1:0])))$fatal(1,"byte store lane/data mismatch");
    end
    request=request+1;
   end
  end
 end
 initial begin #10000;$fatal(1,"deadline exceeded");end
endmodule
