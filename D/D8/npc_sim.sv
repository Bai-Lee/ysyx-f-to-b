module npc_sim #(parameter bit FAULT_ADDI=0)
 (input wire clock,reset,input wire [63:0] sim_cycle,
 output wire [31:0] pc,output wire halted,output wire [2:0] fault,
 output wire commit_valid,output wire [31:0] commit_pc,commit_inst,commit_next_pc,
 output wire [511:0] debug_gpr);
  import "DPI-C" function int unsigned pmem_read(input int unsigned address,input int unsigned size,input int kind,input longint unsigned cycle);
  import "DPI-C" function void pmem_write(input int unsigned address,input int unsigned size,input int unsigned data,input longint unsigned cycle);
  import "DPI-C" function void pmem_load_commit(input int unsigned address,input int unsigned size,input int unsigned pc,input longint unsigned cycle);
  import "DPI-C" function void npc_finish(input int unsigned at_pc,input int unsigned code);
  import "DPI-C" function void npc_commit(input int unsigned at_pc,input int unsigned instruction);
  wire [31:0] inst,mem_addr,mem_wdata,mem_rdata;wire [2:0] mem_size;
  wire mem_ren,mem_wen,exec_valid,exec_ebreak;
  assign inst=(reset||halted)?32'h00000013:pmem_read(pc,4,0,sim_cycle);
  assign mem_rdata=mem_ren?pmem_read(mem_addr,{29'b0,mem_size},1,sim_cycle):32'b0;
  rv32e_core #(.FAULT_ADDI(FAULT_ADDI)) cpu(clock,reset,inst,mem_rdata,pc,mem_addr,mem_wdata,mem_size,
    mem_ren,mem_wen,exec_valid,exec_ebreak,halted,fault,commit_valid,commit_pc,commit_inst,commit_next_pc,debug_gpr);
  always @(posedge clock)begin
    if(mem_wen)pmem_write(mem_addr,{29'b0,mem_size},mem_wdata,sim_cycle);
    if(mem_ren)pmem_load_commit(mem_addr,{29'b0,mem_size},pc,sim_cycle);
    if(exec_valid)npc_commit(pc,inst);
    if(exec_valid&&exec_ebreak)npc_finish(pc,debug_gpr[351:320]);
  end
endmodule
