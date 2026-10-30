module b_sdram_axi_test #(parameter integer RANKS=2,POWERUP_CYCLES=10)(
  input wire clock,reset,
  output wire in_awready,input wire in_awvalid,input wire [31:0] in_awaddr,
  input wire [3:0] in_awid,input wire [7:0] in_awlen,input wire [2:0] in_awsize,input wire [1:0] in_awburst,
  output wire in_wready,input wire in_wvalid,input wire [31:0] in_wdata,input wire [3:0] in_wstrb,input wire in_wlast,
  input wire in_bready,output wire in_bvalid,output wire [1:0] in_bresp,output wire [3:0] in_bid,
  output wire in_arready,input wire in_arvalid,input wire [31:0] in_araddr,
  input wire [3:0] in_arid,input wire [7:0] in_arlen,input wire [2:0] in_arsize,input wire [1:0] in_arburst,
  input wire in_rready,output wire in_rvalid,output wire [1:0] in_rresp,output wire [31:0] in_rdata,
  output wire in_rlast,output wire [3:0] in_rid
);
wire sdram_clk,sdram_cke,sdram_ras,sdram_cas,sdram_we;wire [RANKS-1:0] sdram_cs;wire [12:0] sdram_a;wire [1:0] sdram_ba;wire [3:0] sdram_dqm;wire [31:0] sdram_dq;
b_sdram32_axi #(.RANKS(RANKS),.POWERUP_CYCLES(POWERUP_CYCLES)) controller(.*);
sdram memory(.clk(sdram_clk),.cke(sdram_cke),.cs(sdram_cs),.ras(sdram_ras),.cas(sdram_cas),.we(sdram_we),.a(sdram_a),.ba(sdram_ba),.dqm(sdram_dqm),.dq(sdram_dq));
endmodule
