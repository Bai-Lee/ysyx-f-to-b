module c4_sim #(parameter integer MODE=4,parameter bit FAULT_ADDI=0,parameter logic[63:0] MTIME_RESET=0)(
 input wire clock,reset,
 input wire [63:0] sim_cycle,
 input wire [2:0] delay_enable,
 input wire [31:0] lfsr_seed,
 output wire [31:0] pc,
 output wire halted,
 output wire [2:0] fault,
 output wire commit_valid,
 output wire [31:0] commit_pc,
 output wire [31:0] commit_inst,
 output wire [31:0] commit_next_pc,
 output wire [511:0] debug_gpr,
 output wire exec_fire,
 output wire [31:0] exec_pc,
 output wire [31:0] exec_inst,
 output wire exec_ebreak,
 output wire exec_mem_valid,
 output wire exec_mem_write,
 output wire [31:0] exec_mem_addr,
 output wire [2:0] exec_mem_size,
 output wire [31:0] exec_mem_wdata,
 output wire [31:0] exec_mem_rdata,
 output wire [2:0] debug_state,
 output wire i_req_valid,
 output wire [31:0] i_req_addr,
 input wire i_req_ready,
 input wire i_resp_valid,
 input wire [31:0] i_resp_data,
 input wire [1:0] i_resp_error,
 output wire i_resp_ready,
 output wire d_req_valid,
 output wire [31:0] d_req_addr,
 output wire d_req_write,
 output wire [31:0] d_req_wdata,
 output wire [3:0] d_req_wstrb,
 input wire d_req_ready,
 input wire d_resp_valid,
 input wire [31:0] d_resp_data,
 input wire [1:0] d_resp_error,
 output wire d_resp_ready,
 output logic mem_awvalid,
 input logic mem_awready,
 output logic [31:0] mem_awaddr,
 output logic [2:0] mem_awprot,
 output logic mem_wvalid,
 input logic mem_wready,
 output logic [31:0] mem_wdata,
 output logic [3:0] mem_wstrb,
 input logic mem_bvalid,
 output logic mem_bready,
 input logic [1:0] mem_bresp,
 output logic mem_arvalid,
 input logic mem_arready,
 output logic [31:0] mem_araddr,
 output logic [2:0] mem_arprot,
 input logic mem_rvalid,
 output logic mem_rready,
 input logic [31:0] mem_rdata,
 input logic [1:0] mem_rresp,
 output logic mon_awvalid,
 output logic mon_awready,
 output logic [31:0] mon_awaddr,
 output logic [2:0] mon_awprot,
 output logic mon_wvalid,
 output logic mon_wready,
 output logic [31:0] mon_wdata,
 output logic [3:0] mon_wstrb,
 output logic mon_bvalid,
 output logic mon_bready,
 output logic [1:0] mon_bresp,
 output logic mon_arvalid,
 output logic mon_arready,
 output logic [31:0] mon_araddr,
 output logic [2:0] mon_arprot,
 output logic mon_rvalid,
 output logic mon_rready,
 output logic [31:0] mon_rdata,
 output logic [1:0] mon_rresp,
 output wire uart_tx_valid,
 output wire [7:0] uart_tx_data,
 output wire [63:0] mtime,
 output wire debug_arb_busy,debug_arb_owner
);
generate if(MODE<=4)begin: simple
 c4_simple_core #(.STAGE(MODE),.FAULT_ADDI(FAULT_ADDI)) core(
.clock(clock),
.reset(reset),
.delay_enable(delay_enable),
.lfsr_seed(lfsr_seed),
.pc(pc),
.halted(halted),
.fault(fault),
.commit_valid(commit_valid),
.commit_pc(commit_pc),
.commit_inst(commit_inst),
.commit_next_pc(commit_next_pc),
.debug_gpr(debug_gpr),
.exec_fire(exec_fire),
.exec_pc(exec_pc),
.exec_inst(exec_inst),
.exec_ebreak(exec_ebreak),
.exec_mem_valid(exec_mem_valid),
.exec_mem_write(exec_mem_write),
.exec_mem_addr(exec_mem_addr),
.exec_mem_size(exec_mem_size),
.exec_mem_wdata(exec_mem_wdata),
.exec_mem_rdata(exec_mem_rdata),
.debug_state(debug_state),
.i_req_valid(i_req_valid),
.i_req_addr(i_req_addr),
.i_req_ready(i_req_ready),
.i_resp_valid(i_resp_valid),
.i_resp_data(i_resp_data),
.i_resp_error(i_resp_error),
.i_resp_ready(i_resp_ready),
.d_req_valid(d_req_valid),
.d_req_addr(d_req_addr),
.d_req_write(d_req_write),
.d_req_wdata(d_req_wdata),
.d_req_wstrb(d_req_wstrb),
.d_req_ready(d_req_ready),
.d_resp_valid(d_resp_valid),
.d_resp_data(d_resp_data),
.d_resp_error(d_resp_error),
.d_resp_ready(d_resp_ready));
 assign mem_awvalid=1'd0;
 assign mon_awvalid=1'd0;
 assign mon_awready=1'd0;
 assign mem_awaddr=32'd0;
 assign mon_awaddr=32'd0;
 assign mem_awprot=3'd0;
 assign mon_awprot=3'd0;
 assign mem_wvalid=1'd0;
 assign mon_wvalid=1'd0;
 assign mon_wready=1'd0;
 assign mem_wdata=32'd0;
 assign mon_wdata=32'd0;
 assign mem_wstrb=4'd0;
 assign mon_wstrb=4'd0;
 assign mon_bvalid=1'd0;
 assign mem_bready=1'd0;
 assign mon_bready=1'd0;
 assign mon_bresp=2'd0;
 assign mem_arvalid=1'd0;
 assign mon_arvalid=1'd0;
 assign mon_arready=1'd0;
 assign mem_araddr=32'd0;
 assign mon_araddr=32'd0;
 assign mem_arprot=3'd0;
 assign mon_arprot=3'd0;
 assign mon_rvalid=1'd0;
 assign mem_rready=1'd0;
 assign mon_rready=1'd0;
 assign mon_rdata=32'd0;
 assign mon_rresp=2'd0;
 assign uart_tx_valid=0;assign uart_tx_data=0;assign mtime=0;assign debug_arb_busy=0;assign debug_arb_owner=0;
end else begin: axi
 assign i_req_valid=1'd0;
 assign i_req_addr=32'd0;
 assign i_resp_ready=1'd0;
 assign d_req_valid=1'd0;
 assign d_req_addr=32'd0;
 assign d_req_write=1'd0;
 assign d_req_wdata=32'd0;
 assign d_req_wstrb=4'd0;
 assign d_resp_ready=1'd0;
 if(MODE==5)begin: external_devices
 c4_axi_core #(.FAULT_ADDI(FAULT_ADDI)) core(
.clock(clock),
.reset(reset),
.delay_enable(delay_enable),
.lfsr_seed(lfsr_seed),
.pc(pc),
.halted(halted),
.fault(fault),
.commit_valid(commit_valid),
.commit_pc(commit_pc),
.commit_inst(commit_inst),
.commit_next_pc(commit_next_pc),
.debug_gpr(debug_gpr),
.exec_fire(exec_fire),
.exec_pc(exec_pc),
.exec_inst(exec_inst),
.exec_ebreak(exec_ebreak),
.exec_mem_valid(exec_mem_valid),
.exec_mem_write(exec_mem_write),
.exec_mem_addr(exec_mem_addr),
.exec_mem_size(exec_mem_size),
.exec_mem_wdata(exec_mem_wdata),
.exec_mem_rdata(exec_mem_rdata),
.debug_state(debug_state),
.m_awvalid(mem_awvalid),
.m_awready(mem_awready),
.m_awaddr(mem_awaddr),
.m_awprot(mem_awprot),
.m_wvalid(mem_wvalid),
.m_wready(mem_wready),
.m_wdata(mem_wdata),
.m_wstrb(mem_wstrb),
.m_bvalid(mem_bvalid),
.m_bready(mem_bready),
.m_bresp(mem_bresp),
.m_arvalid(mem_arvalid),
.m_arready(mem_arready),
.m_araddr(mem_araddr),
.m_arprot(mem_arprot),
.m_rvalid(mem_rvalid),
.m_rready(mem_rready),
.m_rdata(mem_rdata),
.m_rresp(mem_rresp),
.debug_arb_busy(debug_arb_busy),
.debug_arb_owner(debug_arb_owner));
 assign mon_awvalid=mem_awvalid;
 assign mon_awready=mem_awready;
 assign mon_awaddr=mem_awaddr;
 assign mon_awprot=mem_awprot;
 assign mon_wvalid=mem_wvalid;
 assign mon_wready=mem_wready;
 assign mon_wdata=mem_wdata;
 assign mon_wstrb=mem_wstrb;
 assign mon_bvalid=mem_bvalid;
 assign mon_bready=mem_bready;
 assign mon_bresp=mem_bresp;
 assign mon_arvalid=mem_arvalid;
 assign mon_arready=mem_arready;
 assign mon_araddr=mem_araddr;
 assign mon_arprot=mem_arprot;
 assign mon_rvalid=mem_rvalid;
 assign mon_rready=mem_rready;
 assign mon_rdata=mem_rdata;
 assign mon_rresp=mem_rresp;
 assign uart_tx_valid=0;assign uart_tx_data=0;assign mtime=0;
 end else begin: rtl_devices
 c4_axi_soc #(.FAULT_ADDI(FAULT_ADDI),.MTIME_RESET(MTIME_RESET)) core(
.clock(clock),
.reset(reset),
.delay_enable(delay_enable),
.lfsr_seed(lfsr_seed),
.pc(pc),
.halted(halted),
.fault(fault),
.commit_valid(commit_valid),
.commit_pc(commit_pc),
.commit_inst(commit_inst),
.commit_next_pc(commit_next_pc),
.debug_gpr(debug_gpr),
.exec_fire(exec_fire),
.exec_pc(exec_pc),
.exec_inst(exec_inst),
.exec_ebreak(exec_ebreak),
.exec_mem_valid(exec_mem_valid),
.exec_mem_write(exec_mem_write),
.exec_mem_addr(exec_mem_addr),
.exec_mem_size(exec_mem_size),
.exec_mem_wdata(exec_mem_wdata),
.exec_mem_rdata(exec_mem_rdata),
.debug_state(debug_state),
.mem_awvalid(mem_awvalid),
.mem_awready(mem_awready),
.mem_awaddr(mem_awaddr),
.mem_awprot(mem_awprot),
.mem_wvalid(mem_wvalid),
.mem_wready(mem_wready),
.mem_wdata(mem_wdata),
.mem_wstrb(mem_wstrb),
.mem_bvalid(mem_bvalid),
.mem_bready(mem_bready),
.mem_bresp(mem_bresp),
.mem_arvalid(mem_arvalid),
.mem_arready(mem_arready),
.mem_araddr(mem_araddr),
.mem_arprot(mem_arprot),
.mem_rvalid(mem_rvalid),
.mem_rready(mem_rready),
.mem_rdata(mem_rdata),
.mem_rresp(mem_rresp),
.mon_awvalid(mon_awvalid),
.mon_awready(mon_awready),
.mon_awaddr(mon_awaddr),
.mon_awprot(mon_awprot),
.mon_wvalid(mon_wvalid),
.mon_wready(mon_wready),
.mon_wdata(mon_wdata),
.mon_wstrb(mon_wstrb),
.mon_bvalid(mon_bvalid),
.mon_bready(mon_bready),
.mon_bresp(mon_bresp),
.mon_arvalid(mon_arvalid),
.mon_arready(mon_arready),
.mon_araddr(mon_araddr),
.mon_arprot(mon_arprot),
.mon_rvalid(mon_rvalid),
.mon_rready(mon_rready),
.mon_rdata(mon_rdata),
.mon_rresp(mon_rresp),
.uart_tx_valid(uart_tx_valid),
.uart_tx_data(uart_tx_data),
.mtime(mtime),
.debug_arb_busy(debug_arb_busy),
.debug_arb_owner(debug_arb_owner));
 end
end endgenerate
import "DPI-C" function void npc_commit(input int unsigned pc,input int unsigned instruction);
import "DPI-C" function void npc_finish(input int unsigned pc,input int unsigned code);
import "DPI-C" function void c4_data_commit(input int unsigned address,input int unsigned size,input int unsigned value,input bit is_write);
always @(posedge clock) if(!reset && exec_fire) begin
  npc_commit(exec_pc,exec_inst);
  if(exec_mem_valid)c4_data_commit(exec_mem_addr,{29'b0,exec_mem_size},exec_mem_write?exec_mem_wdata:exec_mem_rdata,exec_mem_write);
  if(exec_ebreak)npc_finish(exec_pc,debug_gpr[351:320]);
end
wire unused_cycle = ^sim_cycle;
endmodule
