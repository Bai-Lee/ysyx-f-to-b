module axil_reg_frontend(
  input logic clock,reset,
  input logic s_awvalid,output logic s_awready,input logic [31:0] s_awaddr,input logic [2:0] s_awprot,
  input logic s_wvalid,output logic s_wready,input logic [31:0] s_wdata,input logic [3:0] s_wstrb,
  output logic s_bvalid,input logic s_bready,output logic [1:0] s_bresp,
  input logic s_arvalid,output logic s_arready,input logic [31:0] s_araddr,input logic [2:0] s_arprot,
  output logic s_rvalid,input logic s_rready,output logic [31:0] s_rdata,output logic [1:0] s_rresp,
  output logic wr_fire,output logic [31:0] wr_addr,wr_data,output logic [3:0] wr_strb,input logic [1:0] wr_resp,
  output logic rd_fire,output logic [31:0] rd_addr,input logic [31:0] rd_data,input logic [1:0] rd_resp
);
  logic aw_hold,w_hold,b_valid,r_valid;logic [31:0] address,data;logic [3:0] strobe;
  wire unused_prot=^{s_awprot,s_arprot};
  always_comb begin
    s_bvalid=!reset&&b_valid;s_rvalid=!reset&&r_valid;
    s_awready=!reset&&!aw_hold&&!s_bvalid;s_wready=!reset&&!w_hold&&!s_bvalid;
    wr_addr=aw_hold?address:s_awaddr;wr_data=w_hold?data:s_wdata;wr_strb=w_hold?strobe:s_wstrb;
    wr_fire=!reset&&!s_bvalid&&(aw_hold||(s_awvalid&&s_awready))&&(w_hold||(s_wvalid&&s_wready));
    s_arready=!reset&&!s_rvalid;rd_fire=s_arvalid&&s_arready;rd_addr=s_araddr;
  end
  always_ff @(posedge clock)begin
    if(reset)begin aw_hold<=0;w_hold<=0;address<=0;data<=0;strobe<=0;b_valid<=0;s_bresp<=0;r_valid<=0;s_rdata<=0;s_rresp<=0;end
    else begin
      if(s_bvalid&&s_bready)b_valid<=0;
      if(s_rvalid&&s_rready)r_valid<=0;
      if(s_awvalid&&s_awready)begin address<=s_awaddr;aw_hold<=1;end
      if(s_wvalid&&s_wready)begin data<=s_wdata;strobe<=s_wstrb;w_hold<=1;end
      if(wr_fire)begin aw_hold<=0;w_hold<=0;b_valid<=1;s_bresp<=wr_resp;end
      if(rd_fire)begin r_valid<=1;s_rdata<=rd_data;s_rresp<=rd_resp;end
    end
  end
endmodule
