// MODE 1: one-cycle IFU + combinational LSU; MODE 2: one-cycle IFU/LSU;
// MODE 3: one outstanding request per port, explicit response for reads/writes.
module minirv_bus #(
 parameter [31:0] RESET_PC=32'h80000000,
 parameter integer MODE=3,
 parameter integer RANDOM_DELAY=0,
 parameter integer CSR_ENABLE=1,
 parameter [31:0] PROJECT_ID=32'd26070001
)(input wire clock,reset,
 output wire io_ifu_reqValid,output wire[31:0]io_ifu_addr,
 input wire io_ifu_respValid,input wire[31:0]io_ifu_rdata,
 output wire io_lsu_reqValid,output wire[31:0]io_lsu_addr,
 output wire[1:0]io_lsu_size,output wire io_lsu_wen,
 output wire[31:0]io_lsu_wdata,output wire[3:0]io_lsu_wmask,
 input wire io_lsu_respValid,input wire[31:0]io_lsu_rdata,
 output reg[31:0]pc,output reg halted,output reg[2:0]fault,
 output reg commit_valid,output reg[31:0]commit_pc,commit_inst,commit_next_pc,
 output wire[511:0]debug_gpr,output reg[63:0]cycle_counter,
 output wire[2:0]debug_state);
 localparam[2:0] FETCH=0,WAIT_IF=1,WAIT_LS=2,DELAY_LS=3;
 reg[2:0]state;reg[31:0]held_inst;
 reg[7:0]ifu_lfsr,lsu_lfsr;
 wire ifu_allowed=(RANDOM_DELAY==0)||(ifu_lfsr[2:0]==0);
 wire lsu_allowed=(RANDOM_DELAY==0)||(lsu_lfsr[2:0]==0);
 wire fetched=(state==WAIT_IF)&&((MODE!=3)||io_ifu_respValid);
 wire executing=fetched||(state==DELAY_LS);
 wire[31:0]instruction=(state==WAIT_IF)?io_ifu_rdata:held_inst;
 wire[3:0]ra,rb,rd;wire[31:0]a,b,alu_result,next_pc;
 wire dec_wen,is_load,is_store,is_break;wire[2:0]dec_fault;
 minirv_decode decode(instruction,pc,a,b,io_lsu_rdata,ra,rb,rd,dec_wen,is_load,is_store,is_break,
   alu_result,next_pc,io_lsu_addr,io_lsu_wdata,io_lsu_wmask,io_lsu_size,dec_fault);
 wire csr_encoding=(CSR_ENABLE!=0)&&(instruction[6:0]==7'h73)&&(instruction[14:12]==3'b010);
 wire[11:0]csr_address=instruction[31:20];
 wire csr_counter=(csr_address==12'hb00)||(csr_address==12'hb80);
 wire csr_known=csr_counter||(csr_address==12'hf11)||(csr_address==12'hf12);
 wire csr_write=(instruction[19:15]!=0);
 wire csr_valid=csr_encoding&&csr_known&&!instruction[19]&&!instruction[11]&&(!csr_write||csr_counter);
 wire[31:0]csr_value=(csr_address==12'hf11)?32'h79737978:(csr_address==12'hf12)?PROJECT_ID:
   (csr_address==12'hb00)?cycle_counter[31:0]:cycle_counter[63:32];
 wire[2:0]actual_fault=csr_valid?3'd0:dec_fault;
 wire memory_op=is_load||is_store;
 wire issue=executing&&memory_op&&(actual_fault==0)&&((MODE<3)||lsu_allowed)&&!reset&&!halted;
 wire completed=(!reset&&!halted)&&(actual_fault==0)&&(
   (executing&&(!memory_op||(MODE==1)||((MODE==2)&&is_store)))||
   ((state==WAIT_LS)&&((MODE!=3)||io_lsu_respValid)));
 wire[31:0]writeback=csr_valid?csr_value:alu_result;
 minirv_regfile registers(clock,reset,completed&&(dec_wen||csr_valid),ra,rb,rd,writeback,a,b,debug_gpr);
 assign io_ifu_reqValid=(state==FETCH)&&ifu_allowed&&!reset&&!halted;
 assign io_ifu_addr=pc;
 assign io_lsu_reqValid=issue;
 assign io_lsu_wen=is_store&&issue;
 assign debug_state=state;
 always @(posedge clock)begin
  if(reset)begin
   pc<=RESET_PC;halted<=0;fault<=0;commit_valid<=0;commit_pc<=0;commit_inst<=0;commit_next_pc<=0;
`ifndef FAULT_RESET_STATE
   state<=FETCH;
`endif
   held_inst<=0;cycle_counter<=0;ifu_lfsr<=8'hb5;lsu_lfsr<=8'h69;
  end else begin
   cycle_counter<=cycle_counter+64'd1;
   ifu_lfsr<={ifu_lfsr[6:0],ifu_lfsr[7]^ifu_lfsr[5]^ifu_lfsr[4]^ifu_lfsr[3]};
   lsu_lfsr<={lsu_lfsr[6:0],lsu_lfsr[7]^lsu_lfsr[5]^lsu_lfsr[4]^lsu_lfsr[3]};
   commit_valid<=0;
   if(!halted)begin
    if(io_ifu_reqValid)state<=WAIT_IF;
    if(fetched)held_inst<=instruction;
    if(executing)begin
     if(actual_fault!=0)begin halted<=1;fault<=actual_fault;end
     else if(memory_op)begin
      if(issue)state<=WAIT_LS;
      else state<=DELAY_LS;
     end
    end
    if(completed)begin
     commit_valid<=1;commit_pc<=pc;commit_inst<=instruction;commit_next_pc<=csr_valid?pc+32'd4:next_pc;
     pc<=csr_valid?pc+32'd4:next_pc;state<=FETCH;
     if(is_break)halted<=1;
     if(csr_valid&&csr_write)begin
      if(csr_address==12'hb00)cycle_counter<={cycle_counter[63:32],cycle_counter[31:0]|a};
      else cycle_counter<={cycle_counter[63:32]|a,cycle_counter[31:0]};
     end
    end
   end
  end
 end
endmodule
