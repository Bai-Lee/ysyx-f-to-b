module axil_uart #(parameter logic [31:0] BASE=32'h10000000,parameter bit FAULT_REPEAT_TX=0)(
  input logic clock,reset,
  input logic s_awvalid,output wire s_awready,input logic [31:0] s_awaddr,input logic [2:0] s_awprot,
  input logic s_wvalid,output wire s_wready,input logic [31:0] s_wdata,input logic [3:0] s_wstrb,
  output wire s_bvalid,input logic s_bready,output wire [1:0] s_bresp,
  input logic s_arvalid,output wire s_arready,input logic [31:0] s_araddr,input logic [2:0] s_arprot,
  output wire s_rvalid,input logic s_rready,output wire [31:0] s_rdata,output wire [1:0] s_rresp,
  output wire tx_valid,output logic [7:0] tx_data
);
  wire wr_fire,rd_fire;wire [31:0] wr_addr,wr_data,rd_addr;wire [3:0] wr_strb;
  wire [1:0] wr_resp=((wr_addr&32'hfffffffc)==BASE)?2'b00:2'b10;
  wire [1:0] rd_resp=(((rd_addr&32'hfffffffc)==BASE)||((rd_addr&32'hfffffffc)==BASE+4))?2'b00:2'b10;
  wire [31:0] rd_data=((rd_addr&32'hfffffffc)==BASE+4)?32'd1:32'b0;
  wire unused_read=rd_fire;
  logic tx_pulse,pending_tx;
  assign tx_valid=!reset&&tx_pulse;
  axil_reg_frontend front(.*);
  always_ff @(posedge clock)begin
    if(reset)begin tx_pulse<=0;tx_data<=0;pending_tx<=0;end
    else begin
      tx_pulse<=0;
      if(s_bvalid&&s_bready)pending_tx<=0;
      if(FAULT_REPEAT_TX&&s_bvalid&&pending_tx)tx_pulse<=1;
      if(wr_fire)begin
        pending_tx<=wr_resp==0&&wr_strb[0];
        if(wr_resp==0&&wr_strb[0])begin tx_pulse<=1;tx_data<=wr_data[7:0];end
      end
    end
  end
endmodule
