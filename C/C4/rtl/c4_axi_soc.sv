module c4_axi_soc #(
  parameter logic [31:0] RESET_PC=32'h80000000,parameter bit FAULT_ADDI=0,
  parameter logic [31:0] RAM_BASE=32'h80000000,RAM_BYTES=32'h08000000,
  parameter logic [63:0] MTIME_RESET=0
)(
  input logic clock,reset,
  input logic [2:0] delay_enable,
  input logic [31:0] lfsr_seed,
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
  wire bus_awvalid;
  wire bus_awready;
  wire [31:0] bus_awaddr;
  wire [2:0] bus_awprot;
  wire bus_wvalid;
  wire bus_wready;
  wire [31:0] bus_wdata;
  wire [3:0] bus_wstrb;
  wire bus_bvalid;
  wire bus_bready;
  wire [1:0] bus_bresp;
  wire bus_arvalid;
  wire bus_arready;
  wire [31:0] bus_araddr;
  wire [2:0] bus_arprot;
  wire bus_rvalid;
  wire bus_rready;
  wire [31:0] bus_rdata;
  wire [1:0] bus_rresp;
  wire [2:0] x_awvalid;
  wire [2:0] x_awready;
  wire [95:0] x_awaddr;
  wire [8:0] x_awprot;
  wire [2:0] x_wvalid;
  wire [2:0] x_wready;
  wire [95:0] x_wdata;
  wire [11:0] x_wstrb;
  wire [2:0] x_bvalid;
  wire [2:0] x_bready;
  wire [5:0] x_bresp;
  wire [2:0] x_arvalid;
  wire [2:0] x_arready;
  wire [95:0] x_araddr;
  wire [8:0] x_arprot;
  wire [2:0] x_rvalid;
  wire [2:0] x_rready;
  wire [95:0] x_rdata;
  wire [5:0] x_rresp;
  assign mon_awvalid=bus_awvalid;
  assign mem_awvalid=x_awvalid[0:0];
  assign mon_awready=bus_awready;
  assign x_awready[0:0]=mem_awready;
  assign mon_awaddr=bus_awaddr;
  assign mem_awaddr=x_awaddr[31:0];
  assign mon_awprot=bus_awprot;
  assign mem_awprot=x_awprot[2:0];
  assign mon_wvalid=bus_wvalid;
  assign mem_wvalid=x_wvalid[0:0];
  assign mon_wready=bus_wready;
  assign x_wready[0:0]=mem_wready;
  assign mon_wdata=bus_wdata;
  assign mem_wdata=x_wdata[31:0];
  assign mon_wstrb=bus_wstrb;
  assign mem_wstrb=x_wstrb[3:0];
  assign mon_bvalid=bus_bvalid;
  assign x_bvalid[0:0]=mem_bvalid;
  assign mon_bready=bus_bready;
  assign mem_bready=x_bready[0:0];
  assign mon_bresp=bus_bresp;
  assign x_bresp[1:0]=mem_bresp;
  assign mon_arvalid=bus_arvalid;
  assign mem_arvalid=x_arvalid[0:0];
  assign mon_arready=bus_arready;
  assign x_arready[0:0]=mem_arready;
  assign mon_araddr=bus_araddr;
  assign mem_araddr=x_araddr[31:0];
  assign mon_arprot=bus_arprot;
  assign mem_arprot=x_arprot[2:0];
  assign mon_rvalid=bus_rvalid;
  assign x_rvalid[0:0]=mem_rvalid;
  assign mon_rready=bus_rready;
  assign mem_rready=x_rready[0:0];
  assign mon_rdata=bus_rdata;
  assign x_rdata[31:0]=mem_rdata;
  assign mon_rresp=bus_rresp;
  assign x_rresp[1:0]=mem_rresp;
  c4_axi_core #(.RESET_PC(RESET_PC),.FAULT_ADDI(FAULT_ADDI)) cpu(
    .clock(clock),.reset(reset),.delay_enable(delay_enable),.lfsr_seed(lfsr_seed),
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
    .m_awvalid(bus_awvalid),
    .m_awready(bus_awready),
    .m_awaddr(bus_awaddr),
    .m_awprot(bus_awprot),
    .m_wvalid(bus_wvalid),
    .m_wready(bus_wready),
    .m_wdata(bus_wdata),
    .m_wstrb(bus_wstrb),
    .m_bvalid(bus_bvalid),
    .m_bready(bus_bready),
    .m_bresp(bus_bresp),
    .m_arvalid(bus_arvalid),
    .m_arready(bus_arready),
    .m_araddr(bus_araddr),
    .m_arprot(bus_arprot),
    .m_rvalid(bus_rvalid),
    .m_rready(bus_rready),
    .m_rdata(bus_rdata),
    .m_rresp(bus_rresp),
    .debug_arb_busy(debug_arb_busy),.debug_arb_owner(debug_arb_owner));
  axil_xbar3 #(.RAM_BASE(RAM_BASE),.RAM_BYTES(RAM_BYTES)) xbar(
    .clock(clock),.reset(reset),
    .s_awvalid(bus_awvalid),
    .s_awready(bus_awready),
    .s_awaddr(bus_awaddr),
    .s_awprot(bus_awprot),
    .s_wvalid(bus_wvalid),
    .s_wready(bus_wready),
    .s_wdata(bus_wdata),
    .s_wstrb(bus_wstrb),
    .s_bvalid(bus_bvalid),
    .s_bready(bus_bready),
    .s_bresp(bus_bresp),
    .s_arvalid(bus_arvalid),
    .s_arready(bus_arready),
    .s_araddr(bus_araddr),
    .s_arprot(bus_arprot),
    .s_rvalid(bus_rvalid),
    .s_rready(bus_rready),
    .s_rdata(bus_rdata),
    .s_rresp(bus_rresp),
    .m_awvalid(x_awvalid),
    .m_awready(x_awready),
    .m_awaddr(x_awaddr),
    .m_awprot(x_awprot),
    .m_wvalid(x_wvalid),
    .m_wready(x_wready),
    .m_wdata(x_wdata),
    .m_wstrb(x_wstrb),
    .m_bvalid(x_bvalid),
    .m_bready(x_bready),
    .m_bresp(x_bresp),
    .m_arvalid(x_arvalid),
    .m_arready(x_arready),
    .m_araddr(x_araddr),
    .m_arprot(x_arprot),
    .m_rvalid(x_rvalid),
    .m_rready(x_rready),
    .m_rdata(x_rdata),
    .m_rresp(x_rresp));
  axil_uart uart(.clock(clock),.reset(reset),
    .s_awvalid(x_awvalid[1+:1]),
    .s_awready(x_awready[1+:1]),
    .s_awaddr(x_awaddr[32+:32]),
    .s_awprot(x_awprot[3+:3]),
    .s_wvalid(x_wvalid[1+:1]),
    .s_wready(x_wready[1+:1]),
    .s_wdata(x_wdata[32+:32]),
    .s_wstrb(x_wstrb[4+:4]),
    .s_bvalid(x_bvalid[1+:1]),
    .s_bready(x_bready[1+:1]),
    .s_bresp(x_bresp[2+:2]),
    .s_arvalid(x_arvalid[1+:1]),
    .s_arready(x_arready[1+:1]),
    .s_araddr(x_araddr[32+:32]),
    .s_arprot(x_arprot[3+:3]),
    .s_rvalid(x_rvalid[1+:1]),
    .s_rready(x_rready[1+:1]),
    .s_rdata(x_rdata[32+:32]),
    .s_rresp(x_rresp[2+:2]),
    .tx_valid(uart_tx_valid),.tx_data(uart_tx_data));
  axil_clint #(.MTIME_RESET(MTIME_RESET)) clint(.clock(clock),.reset(reset),
    .s_awvalid(x_awvalid[2+:1]),
    .s_awready(x_awready[2+:1]),
    .s_awaddr(x_awaddr[64+:32]),
    .s_awprot(x_awprot[6+:3]),
    .s_wvalid(x_wvalid[2+:1]),
    .s_wready(x_wready[2+:1]),
    .s_wdata(x_wdata[64+:32]),
    .s_wstrb(x_wstrb[8+:4]),
    .s_bvalid(x_bvalid[2+:1]),
    .s_bready(x_bready[2+:1]),
    .s_bresp(x_bresp[4+:2]),
    .s_arvalid(x_arvalid[2+:1]),
    .s_arready(x_arready[2+:1]),
    .s_araddr(x_araddr[64+:32]),
    .s_arprot(x_arprot[6+:3]),
    .s_rvalid(x_rvalid[2+:1]),
    .s_rready(x_rready[2+:1]),
    .s_rdata(x_rdata[64+:32]),
    .s_rresp(x_rresp[4+:2]),
    .mtime(mtime));
endmodule
