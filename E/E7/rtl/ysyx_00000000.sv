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
