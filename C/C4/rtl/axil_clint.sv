module axil_clint #(parameter logic [31:0] BASE=32'h20000000,
  parameter logic [63:0] MTIME_RESET=0,parameter bit FAULT_UNLATCHED_HIGH=0)(
  input logic clock,reset,
  input logic s_awvalid,output wire s_awready,input logic [31:0] s_awaddr,input logic [2:0] s_awprot,
  input logic s_wvalid,output wire s_wready,input logic [31:0] s_wdata,input logic [3:0] s_wstrb,
  output wire s_bvalid,input logic s_bready,output wire [1:0] s_bresp,
  input logic s_arvalid,output wire s_arready,input logic [31:0] s_araddr,input logic [2:0] s_arprot,
  output wire s_rvalid,input logic s_rready,output wire [31:0] s_rdata,output wire [1:0] s_rresp,
  output logic [63:0] mtime
);
  wire wr_fire,rd_fire;wire [31:0] wr_addr,wr_data,rd_addr;wire [3:0] wr_strb;
  wire [1:0] wr_resp=2'b10;
  logic [31:0] high_latch;logic latch_valid;
  wire is_low=(rd_addr&32'hfffffffc)==BASE;
  wire is_high=(rd_addr&32'hfffffffc)==BASE+4;
  wire [1:0] rd_resp=(is_low||is_high)?2'b00:2'b10;
  wire [31:0] rd_data=is_low?mtime[31:0]:(is_high?((latch_valid&&!FAULT_UNLATCHED_HIGH)?high_latch:mtime[63:32]):32'b0);
  wire unused_write=^{wr_fire,wr_addr,wr_data,wr_strb};
  axil_reg_frontend front(.*);
  always_ff @(posedge clock)begin
    if(reset)begin mtime<=MTIME_RESET;high_latch<=0;latch_valid<=0;end
    else begin
      mtime<=mtime+64'd1;
      if(rd_fire&&is_low)begin high_latch<=mtime[63:32];latch_valid<=1;end
      else if(rd_fire&&is_high)latch_valid<=0;
    end
  end
endmodule
