module c4_axi_core #(
  parameter logic [31:0] RESET_PC=32'h80000000,parameter bit FAULT_ADDI=0
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
  output logic m_awvalid,
  input logic m_awready,
  output logic [31:0] m_awaddr,
  output logic [2:0] m_awprot,
  output logic m_wvalid,
  input logic m_wready,
  output logic [31:0] m_wdata,
  output logic [3:0] m_wstrb,
  input logic m_bvalid,
  output logic m_bready,
  input logic [1:0] m_bresp,
  output logic m_arvalid,
  input logic m_arready,
  output logic [31:0] m_araddr,
  output logic [2:0] m_arprot,
  input logic m_rvalid,
  output logic m_rready,
  input logic [31:0] m_rdata,
  input logic [1:0] m_rresp,
  output wire debug_arb_busy,debug_arb_owner
);
  wire i_req_valid,i_req_ready,i_resp_valid,i_resp_ready;
  wire [31:0] i_req_addr,i_resp_data;wire [1:0] i_resp_error;
  wire d_req_valid,d_req_ready,d_req_write,d_resp_valid,d_resp_ready;
  wire [31:0] d_req_addr,d_req_wdata,d_resp_data;wire [3:0] d_req_wstrb;wire [1:0] d_resp_error;
  wire if_awvalid;
  wire if_awready;
  wire [31:0] if_awaddr;
  wire [2:0] if_awprot;
  wire if_wvalid;
  wire if_wready;
  wire [31:0] if_wdata;
  wire [3:0] if_wstrb;
  wire if_bvalid;
  wire if_bready;
  wire [1:0] if_bresp;
  wire if_arvalid;
  wire if_arready;
  wire [31:0] if_araddr;
  wire [2:0] if_arprot;
  wire if_rvalid;
  wire if_rready;
  wire [31:0] if_rdata;
  wire [1:0] if_rresp;
  wire ls_awvalid;
  wire ls_awready;
  wire [31:0] ls_awaddr;
  wire [2:0] ls_awprot;
  wire ls_wvalid;
  wire ls_wready;
  wire [31:0] ls_wdata;
  wire [3:0] ls_wstrb;
  wire ls_bvalid;
  wire ls_bready;
  wire [1:0] ls_bresp;
  wire ls_arvalid;
  wire ls_arready;
  wire [31:0] ls_araddr;
  wire [2:0] ls_arprot;
  wire ls_rvalid;
  wire ls_rready;
  wire [31:0] ls_rdata;
  wire [1:0] ls_rresp;
  c4_simple_core #(.STAGE(4),.RESET_PC(RESET_PC),.FAULT_ADDI(FAULT_ADDI)) core(.*);
  simple_to_axil #(.READ_ONLY(1),.PROT(3'd4)) i_adapter(
    .clock(clock),.reset(reset),
    .req_valid(i_req_valid),
    .req_ready(i_req_ready),
    .req_addr(i_req_addr),
    .req_write(1'b0),
    .req_wdata(32'b0),
    .req_wstrb(4'b0),
    .resp_valid(i_resp_valid),
    .resp_ready(i_resp_ready),
    .resp_data(i_resp_data),
    .resp_error(i_resp_error),
    .m_awvalid(if_awvalid),
    .m_awready(if_awready),
    .m_awaddr(if_awaddr),
    .m_awprot(if_awprot),
    .m_wvalid(if_wvalid),
    .m_wready(if_wready),
    .m_wdata(if_wdata),
    .m_wstrb(if_wstrb),
    .m_bvalid(if_bvalid),
    .m_bready(if_bready),
    .m_bresp(if_bresp),
    .m_arvalid(if_arvalid),
    .m_arready(if_arready),
    .m_araddr(if_araddr),
    .m_arprot(if_arprot),
    .m_rvalid(if_rvalid),
    .m_rready(if_rready),
    .m_rdata(if_rdata),
    .m_rresp(if_rresp));
  simple_to_axil #(.READ_ONLY(0),.PROT(3'd0)) d_adapter(
    .clock(clock),.reset(reset),
    .req_valid(d_req_valid),
    .req_ready(d_req_ready),
    .req_addr(d_req_addr),
    .req_write(d_req_write),
    .req_wdata(d_req_wdata),
    .req_wstrb(d_req_wstrb),
    .resp_valid(d_resp_valid),
    .resp_ready(d_resp_ready),
    .resp_data(d_resp_data),
    .resp_error(d_resp_error),
    .m_awvalid(ls_awvalid),
    .m_awready(ls_awready),
    .m_awaddr(ls_awaddr),
    .m_awprot(ls_awprot),
    .m_wvalid(ls_wvalid),
    .m_wready(ls_wready),
    .m_wdata(ls_wdata),
    .m_wstrb(ls_wstrb),
    .m_bvalid(ls_bvalid),
    .m_bready(ls_bready),
    .m_bresp(ls_bresp),
    .m_arvalid(ls_arvalid),
    .m_arready(ls_arready),
    .m_araddr(ls_araddr),
    .m_arprot(ls_arprot),
    .m_rvalid(ls_rvalid),
    .m_rready(ls_rready),
    .m_rdata(ls_rdata),
    .m_rresp(ls_rresp));
  axil_arbiter2 arbiter(.clock(clock),.reset(reset),
    .s0_awvalid(if_awvalid),
    .s0_awready(if_awready),
    .s0_awaddr(if_awaddr),
    .s0_awprot(if_awprot),
    .s0_wvalid(if_wvalid),
    .s0_wready(if_wready),
    .s0_wdata(if_wdata),
    .s0_wstrb(if_wstrb),
    .s0_bvalid(if_bvalid),
    .s0_bready(if_bready),
    .s0_bresp(if_bresp),
    .s0_arvalid(if_arvalid),
    .s0_arready(if_arready),
    .s0_araddr(if_araddr),
    .s0_arprot(if_arprot),
    .s0_rvalid(if_rvalid),
    .s0_rready(if_rready),
    .s0_rdata(if_rdata),
    .s0_rresp(if_rresp),
    .s1_awvalid(ls_awvalid),
    .s1_awready(ls_awready),
    .s1_awaddr(ls_awaddr),
    .s1_awprot(ls_awprot),
    .s1_wvalid(ls_wvalid),
    .s1_wready(ls_wready),
    .s1_wdata(ls_wdata),
    .s1_wstrb(ls_wstrb),
    .s1_bvalid(ls_bvalid),
    .s1_bready(ls_bready),
    .s1_bresp(ls_bresp),
    .s1_arvalid(ls_arvalid),
    .s1_arready(ls_arready),
    .s1_araddr(ls_araddr),
    .s1_arprot(ls_arprot),
    .s1_rvalid(ls_rvalid),
    .s1_rready(ls_rready),
    .s1_rdata(ls_rdata),
    .s1_rresp(ls_rresp),
    .m_awvalid(m_awvalid),
    .m_awready(m_awready),
    .m_awaddr(m_awaddr),
    .m_awprot(m_awprot),
    .m_wvalid(m_wvalid),
    .m_wready(m_wready),
    .m_wdata(m_wdata),
    .m_wstrb(m_wstrb),
    .m_bvalid(m_bvalid),
    .m_bready(m_bready),
    .m_bresp(m_bresp),
    .m_arvalid(m_arvalid),
    .m_arready(m_arready),
    .m_araddr(m_araddr),
    .m_arprot(m_arprot),
    .m_rvalid(m_rvalid),
    .m_rready(m_rready),
    .m_rdata(m_rdata),
    .m_rresp(m_rresp),
    .debug_busy(debug_arb_busy),.debug_owner(debug_arb_owner));
endmodule
