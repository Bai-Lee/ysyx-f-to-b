module gate_system(input wire clock,reset,output reg done,output reg failed);
 wire ifu_req,lsu_req,lsu_wen;wire[31:0]ifu_addr,lsu_addr,lsu_wdata;wire[3:0]lsu_mask;wire[1:0]lsu_size;
 reg ifu_resp,lsu_resp;reg[31:0]ifu_rdata,lsu_rdata;
 reg[63:0]cycles;reg[5:0]break_wait;reg saw_fetch;
 wire unused_size=^lsu_size;
 ysyx_00000000 cpu(clock,reset,ifu_req,ifu_addr,ifu_resp,ifu_rdata,lsu_req,lsu_addr,lsu_size,lsu_wen,lsu_wdata,lsu_mask,lsu_resp,lsu_rdata);
`ifndef __ICARUS__
 import "DPI-C" function int unsigned gate_read(input int unsigned addr,input int kind);
 import "DPI-C" function void gate_write(input int unsigned addr,data,input byte unsigned mask);
 import "DPI-C" function void gate_tick(input longint unsigned count);
 import "DPI-C" function int gate_status();
`define E8_READ(A,K) gate_read(A,K)
`define E8_WRITE(A,D,M) gate_write(A,D,{4'b0,M})
`define E8_TICK(C) gate_tick(C)
`define E8_STATUS gate_status()
`else
`define E8_READ(A,K) $pmem_read(A,K)
`define E8_WRITE(A,D,M) $pmem_write(A,D,M)
`define E8_TICK(C) $pmem_tick(C)
`define E8_STATUS $pmem_status
`endif
 always @(posedge clock)begin : memory_service
  integer data,status,bad;
  if(reset)begin
   ifu_resp<=0;lsu_resp<=0;ifu_rdata<=0;lsu_rdata<=0;cycles<=0;break_wait<=0;saw_fetch<=0;done<=0;failed<=0;
  end else if(!done)begin
   bad=0;
   cycles<=cycles+1;`E8_TICK(cycles+1);
   ifu_resp<=0;lsu_resp<=0;
   // These case-equality checks reject X/Z control signals explicitly.
   if((ifu_req!==1'b0&&ifu_req!==1'b1)||(lsu_req!==1'b0&&lsu_req!==1'b1))begin
    $display("UNKNOWN_BUS_CONTROL cycle=%0d",cycles);bad=1;
   end
   if(ifu_req===1'b1)begin
    saw_fetch<=1;data=`E8_READ(ifu_addr,0);ifu_rdata<=data;ifu_resp<=1;
    if(data==32'h00100073)break_wait<=1;
    if(break_wait>2)begin $display("FETCH_AFTER_EBREAK");bad=1;end
   end
   if(lsu_req===1'b1)begin
    if(lsu_wen===1'b1)begin `E8_WRITE(lsu_addr,lsu_wdata,lsu_mask);lsu_rdata<=0;end
    else if(lsu_wen===1'b0)begin lsu_rdata<=`E8_READ(lsu_addr,1);end
    else begin $display("UNKNOWN_WRITE_ENABLE");bad=1;end
    lsu_resp<=1;
   end
   status=`E8_STATUS;
   if(status<0)begin $display("MEMORY_MODEL_ERROR");bad=1;end
   if(break_wait!=0)begin
    break_wait<=break_wait+1;
    if(break_wait==16)begin
     done<=1;failed<=(status!=1);
     if(status==1&&bad==0)$display("GOOD_TRAP gate memory/VPI, tohost success and ebreak fetch followed by quiet bus");
     else $display("BAD_TRAP or missing tohost value, status=%0d",status);
    end
   end
   if(cycles==32&&!saw_fetch)begin $display("NO_FETCH_AFTER_RESET");bad=1;end
   if(bad!=0)begin done<=1;failed<=1;end
  end
 end
`undef E8_READ
`undef E8_WRITE
`undef E8_TICK
`undef E8_STATUS
endmodule
