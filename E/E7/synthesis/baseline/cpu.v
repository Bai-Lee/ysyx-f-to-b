module minirv_decode(input wire [31:0] inst,pc,rs1_value,rs2_value,load_word,
 output wire [3:0] raddr1,raddr2,waddr,output wire wen,is_load,is_store,is_ebreak,
 output wire [31:0] result,next_pc,mem_addr,mem_wdata,output wire [3:0] mem_wmask,
 output wire [1:0] mem_size,output wire [2:0] fault_code);
  wire [6:0] opcode=inst[6:0];wire [2:0] f3=inst[14:12];
  wire add=(opcode==7'h33)&&(f3==0)&&(inst[31:25]==0);
  wire addi=(opcode==7'h13)&&(f3==0);
  wire lui=(opcode==7'h37);
  wire jalr=(opcode==7'h67)&&(f3==0);
  wire lw=(opcode==7'h03)&&(f3==2),lbu=(opcode==7'h03)&&(f3==4);
  wire sw=(opcode==7'h23)&&(f3==2),sb=(opcode==7'h23)&&(f3==0);
  assign is_ebreak=(inst==32'h00100073);
  assign raddr1=inst[18:15];assign raddr2=inst[23:20];assign waddr=inst[10:7];
`ifdef FAULT_SIGN_EXT
  wire [31:0] imm_i={20'b0,inst[31:20]};
`else
  wire [31:0] imm_i={{20{inst[31]}},inst[31:20]};
`endif
  wire [31:0] imm_s={{20{inst[31]}},inst[31:25],inst[11:7]};
  assign is_load=lw|lbu;assign is_store=sw|sb;assign wen=add|addi|lui|jalr|is_load;
  assign mem_addr=rs1_value+(is_store?imm_s:imm_i);
`ifdef FAULT_JALR_LOW_BIT
  assign next_pc=jalr?(rs1_value+imm_i):pc+32'd4;
`else
  assign next_pc=jalr?((rs1_value+imm_i)&32'hfffffffe):pc+32'd4;
`endif
  wire [4:0] shift={mem_addr[1:0],3'b0};
  wire [7:0] selected_byte=load_word[shift+:8];
`ifdef FAULT_LBU_SIGN
  wire [31:0] byte_value={{24{selected_byte[7]}},selected_byte};
`else
  wire [31:0] byte_value={24'b0,selected_byte};
`endif
  assign result=add?rs1_value+rs2_value:addi?rs1_value+imm_i:lui?{inst[31:12],12'b0}:
    jalr?pc+32'd4:lw?load_word:lbu?byte_value:32'b0;
  assign mem_wdata=sb?({24'b0,rs2_value[7:0]}<<shift):rs2_value;
`ifdef FAULT_SB_MASK
  assign mem_wmask=4'hf;
`else
  assign mem_wmask=sb?(4'b1<<mem_addr[1:0]):4'hf;
`endif
  assign mem_size=(sb|lbu)?2'd0:2'd2;
  wire bad_register=(wen&&inst[11])|((add|addi|jalr|is_load|is_store)&&inst[19])|((add|is_store)&&inst[24]);
  wire bad_encoding=!(add|addi|lui|jalr|is_load|is_store|is_ebreak)|bad_register;
  assign fault_code=bad_encoding?3'd1:((|pc[1:0])||(jalr&&(|next_pc[1:0])))?3'd2:
                    ((lw|sw)&&(|mem_addr[1:0]))?3'd3:3'd0;
endmodule

module minirv_regfile(input wire clock,reset,wen,input wire [3:0] raddr1,raddr2,waddr,
 input wire [31:0] wdata,output wire [31:0] rs1_value,rs2_value,output wire [511:0] debug_gpr);
  reg [31:0] regs[0:15];integer i;
  always @(posedge clock)begin
    if(reset)for(i=0;i<16;i=i+1)regs[i]<=0;
`ifdef FAULT_X0
    else if(wen)regs[waddr]<=wdata;
`else
    else if(wen&&(waddr!=0))regs[waddr]<=wdata;
`endif
  end
`ifdef FAULT_X0
  assign rs1_value=regs[raddr1];assign rs2_value=regs[raddr2];
  assign debug_gpr[31:0]=regs[0];
`else
  assign rs1_value=(raddr1==0)?32'b0:regs[raddr1];assign rs2_value=(raddr2==0)?32'b0:regs[raddr2];
  assign debug_gpr[31:0]=32'b0;
`endif
  for(genvar g=1;g<16;g=g+1)begin:observe
    assign debug_gpr[g*32+:32]=regs[g];
  end
endmodule

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

// Course interface exactly matches the provided 2607 SoC. The all-zero module
// label is an integration name, not a personal enrollment/official student ID.
module ysyx_00000000(
 input wire clock,reset,
 output wire io_ifu_reqValid,output wire[31:0]io_ifu_addr,
 input wire io_ifu_respValid,input wire[31:0]io_ifu_rdata,
 output wire io_lsu_reqValid,output wire[31:0]io_lsu_addr,
 output wire[1:0]io_lsu_size,output wire io_lsu_wen,
 output wire[31:0]io_lsu_wdata,output wire[3:0]io_lsu_wmask,
 input wire io_lsu_respValid,input wire[31:0]io_lsu_rdata);
 wire[31:0]unused_pc,unused_commit_pc,unused_commit_inst,unused_commit_next_pc;
 wire unused_halted,unused_commit_valid;wire[2:0]unused_fault,unused_state;
 wire[511:0]unused_gpr;wire[63:0]unused_cycles;
 minirv_bus #(.RESET_PC(32'h30000000),.MODE(3),.RANDOM_DELAY(0),.CSR_ENABLE(1),.PROJECT_ID(32'd26070001)) cpu(
  .clock(clock),.reset(reset),.io_ifu_reqValid(io_ifu_reqValid),.io_ifu_addr(io_ifu_addr),
  .io_ifu_respValid(io_ifu_respValid),.io_ifu_rdata(io_ifu_rdata),
  .io_lsu_reqValid(io_lsu_reqValid),.io_lsu_addr(io_lsu_addr),.io_lsu_size(io_lsu_size),
  .io_lsu_wen(io_lsu_wen),.io_lsu_wdata(io_lsu_wdata),.io_lsu_wmask(io_lsu_wmask),
  .io_lsu_respValid(io_lsu_respValid),.io_lsu_rdata(io_lsu_rdata),
  .pc(unused_pc),.halted(unused_halted),.fault(unused_fault),.commit_valid(unused_commit_valid),
  .commit_pc(unused_commit_pc),.commit_inst(unused_commit_inst),.commit_next_pc(unused_commit_next_pc),
  .debug_gpr(unused_gpr),.cycle_counter(unused_cycles),.debug_state(unused_state));
`ifndef SYNTHESIS
 import "DPI-C" function void soc_commit(input int unsigned pc,inst,next_pc,input bit[511:0]gpr,input longint unsigned mcycle);
 import "DPI-C" function void soc_request(input int unsigned addr,data,input byte unsigned mask,input bit wen);
 import "DPI-C" function void soc_response(input int unsigned data);
 import "DPI-C" function void soc_fault(input int unsigned pc,input int unsigned code);
 import "DPI-C" function void soc_tick(input bit reset,input longint unsigned count);
 import "DPI-C" function void soc_fetch_request(input int unsigned address);
 always @(posedge clock)begin
 if(!reset)begin
  if(io_ifu_reqValid)soc_fetch_request(io_ifu_addr);
  if(io_lsu_reqValid)soc_request(io_lsu_addr,io_lsu_wdata,{4'b0,io_lsu_wmask},io_lsu_wen);
  if(io_lsu_respValid)soc_response(io_lsu_rdata);
  if(unused_commit_valid)soc_commit(unused_commit_pc,unused_commit_inst,unused_commit_next_pc,unused_gpr,unused_cycles);
  if(unused_fault!=0)soc_fault(unused_pc,{29'b0,unused_fault});
 end
 soc_tick(reset,unused_cycles);
 end
`endif
endmodule
