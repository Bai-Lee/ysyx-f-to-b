module axil_xbar3 #(
  parameter logic [31:0] RAM_BASE=32'h80000000,
  parameter logic [31:0] RAM_BYTES=32'h08000000
)(
  input logic clock,reset,
  input logic s_awvalid,
  output logic s_awready,
  input logic [31:0] s_awaddr,
  input logic [2:0] s_awprot,
  input logic s_wvalid,
  output logic s_wready,
  input logic [31:0] s_wdata,
  input logic [3:0] s_wstrb,
  output logic s_bvalid,
  input logic s_bready,
  output logic [1:0] s_bresp,
  input logic s_arvalid,
  output logic s_arready,
  input logic [31:0] s_araddr,
  input logic [2:0] s_arprot,
  output logic s_rvalid,
  input logic s_rready,
  output logic [31:0] s_rdata,
  output logic [1:0] s_rresp,
  output logic [2:0] m_awvalid,
  input logic [2:0] m_awready,
  output logic [95:0] m_awaddr,
  output logic [8:0] m_awprot,
  output logic [2:0] m_wvalid,
  input logic [2:0] m_wready,
  output logic [95:0] m_wdata,
  output logic [11:0] m_wstrb,
  input logic [2:0] m_bvalid,
  output logic [2:0] m_bready,
  input logic [5:0] m_bresp,
  output logic [2:0] m_arvalid,
  input logic [2:0] m_arready,
  output logic [95:0] m_araddr,
  output logic [8:0] m_arprot,
  input logic [2:0] m_rvalid,
  output logic [2:0] m_rready,
  input logic [95:0] m_rdata,
  input logic [5:0] m_rresp
);
  localparam logic [2:0] IDLE=0,R_SEND=1,R_RESP=2,W_SEND=3,W_RESP=4,R_ERROR=5,W_ERROR=6;
  logic [2:0] state;logic [1:0] target;
  logic aw_have,w_have,aw_done,w_done;
  logic ar_have;
  logic [31:0] read_address;
  logic [2:0] read_protection;
  logic [31:0] address,data;logic [2:0] protection;logic [3:0] strobe;
  wire aw_fire=s_awvalid&&s_awready;
  wire w_fire=s_wvalid&&s_wready;
  wire [31:0] effective_addr=aw_have?address:s_awaddr;
  function automatic [1:0] decode(input logic [31:0] a);
    if({1'b0,a}>={1'b0,RAM_BASE} && {1'b0,a}<{1'b0,RAM_BASE}+{1'b0,RAM_BYTES})decode=0;
    else if(a[31:12]==20'h10000)decode=1;
    else if(a[31:12]==20'h20000)decode=2;
    else decode=3;
  endfunction
  always_comb begin
    m_awvalid=0;
    s_awready=0;
    m_awaddr=0;
    m_awprot=0;
    m_wvalid=0;
    s_wready=0;
    m_wdata=0;
    m_wstrb=0;
    s_bvalid=0;
    m_bready=0;
    s_bresp=0;
    m_arvalid=0;
    s_arready=0;
    m_araddr=0;
    m_arprot=0;
    s_rvalid=0;
    m_rready=0;
    s_rdata=0;
    s_rresp=0;
    if(!reset)case(state)
      IDLE:begin
        s_awready=!aw_have;s_wready=!w_have;
        s_arready=!ar_have;
      end
      R_SEND:begin
        m_arvalid[target]=1;m_araddr[target*32+:32]=read_address;m_arprot[target*3+:3]=read_protection;
      end
      R_RESP:begin
        s_rvalid=m_rvalid[target];s_rdata=m_rdata[target*32+:32];s_rresp=m_rresp[target*2+:2];m_rready[target]=s_rready;
      end
      W_SEND:begin
        m_awvalid[target]=!aw_done;m_awaddr[target*32+:32]=address;m_awprot[target*3+:3]=protection;
        m_wvalid[target]=!w_done;m_wdata[target*32+:32]=data;m_wstrb[target*4+:4]=strobe;
      end
      W_RESP:begin s_bvalid=m_bvalid[target];s_bresp=m_bresp[target*2+:2];m_bready[target]=s_bready;end
      R_ERROR:begin s_rvalid=1;s_rresp=2'b11;end
      W_ERROR:begin s_bvalid=1;s_bresp=2'b11;end
      default:begin end
    endcase
  end
  always_ff @(posedge clock)begin
    if(reset)begin state<=IDLE;target<=0;aw_have<=0;w_have<=0;aw_done<=0;w_done<=0;address<=0;data<=0;protection<=0;strobe<=0;ar_have<=0;read_address<=0;read_protection<=0;end
    else case(state)
      IDLE:begin
        if(aw_fire)begin address<=s_awaddr;protection<=s_awprot;aw_have<=1;end
        if(w_fire)begin data<=s_wdata;strobe<=s_wstrb;w_have<=1;end
        if(s_arvalid&&s_arready)begin ar_have<=1;read_address<=s_araddr;read_protection<=s_arprot;end
        if(ar_have)begin
          target<=decode(read_address);
          state<=((decode(read_address)==3)||(read_protection[2]&&decode(read_address)!=0))?R_ERROR:R_SEND;
        end else if((aw_have||aw_fire)&&(w_have||w_fire))begin
          target<=decode(effective_addr);aw_done<=0;w_done<=0;
          state<=(decode(effective_addr)==3)?W_ERROR:W_SEND;
        end
      end
      R_SEND:if(m_arvalid[target]&&m_arready[target])state<=R_RESP;
      R_RESP:if(s_rvalid&&s_rready)begin state<=IDLE;ar_have<=0;end
      W_SEND:begin
        if(m_awvalid[target]&&m_awready[target])aw_done<=1;
        if(m_wvalid[target]&&m_wready[target])w_done<=1;
        if((aw_done||(m_awvalid[target]&&m_awready[target]))&&(w_done||(m_wvalid[target]&&m_wready[target])))state<=W_RESP;
      end
      W_RESP:if(s_bvalid&&s_bready)begin state<=IDLE;aw_have<=0;w_have<=0;end
      R_ERROR:if(s_rvalid&&s_rready)begin state<=IDLE;ar_have<=0;end
      W_ERROR:if(s_bvalid&&s_bready)begin state<=IDLE;aw_have<=0;w_have<=0;end
      default:state<=IDLE;
    endcase
  end
endmodule
