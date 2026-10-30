module npc_sim #(parameter [31:0] RESET_PC=32'b0)
 (input wire clock,reset,input wire [63:0] sim_cycle,
 output wire [31:0] pc,output wire halted,output wire [2:0] fault,
 output wire commit_valid,output wire [31:0] commit_pc,commit_inst,commit_next_pc,
 output wire [511:0] debug_gpr);
  import "DPI-C" function int unsigned pmem_read(input int unsigned address,input int kind,input longint unsigned cycle);
  import "DPI-C" function void pmem_write(input int unsigned address,input int unsigned data,input byte unsigned mask,input longint unsigned cycle);
  import "DPI-C" function void npc_finish(input int unsigned at_pc,input int unsigned code);
  import "DPI-C" function void pmem_load_commit(input int unsigned address,input int unsigned at_pc,input longint unsigned cycle);
  wire [31:0] inst,mem_addr,mem_wdata,mem_rdata;wire [3:0] mem_wmask;wire [1:0] unused_size;
  wire mem_ren,mem_wen,exec_valid,exec_ebreak;
  assign inst=(reset||halted)?32'h00000013:pmem_read(pc,0,sim_cycle);
  assign mem_rdata=mem_ren?pmem_read(mem_addr,1,sim_cycle):32'b0;
  minirv_single #(.RESET_PC(RESET_PC)) cpu(clock,reset,inst,mem_rdata,pc,mem_addr,mem_wdata,
    mem_wmask,unused_size,mem_ren,mem_wen,exec_valid,exec_ebreak,halted,fault,commit_valid,
    commit_pc,commit_inst,commit_next_pc,debug_gpr);
  // Side effects occur once at the architectural write edge, never in a combinational evaluator.
  always @(posedge clock)begin
    if(mem_wen)pmem_write(mem_addr,mem_wdata,{4'b0,mem_wmask},sim_cycle);
    if(mem_ren)pmem_load_commit(mem_addr,pc,sim_cycle);
    if(exec_valid&&exec_ebreak)begin
      npc_finish(pc,debug_gpr[351:320]);
`ifdef FAULT_BREAK_REPEAT
      npc_finish(pc,debug_gpr[351:320]);
`endif
    end
  end
endmodule
