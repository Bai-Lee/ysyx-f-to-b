module axil_arbiter2(
  input logic clock,reset,
  input logic s0_awvalid,
  output logic s0_awready,
  input logic [31:0] s0_awaddr,
  input logic [2:0] s0_awprot,
  input logic s0_wvalid,
  output logic s0_wready,
  input logic [31:0] s0_wdata,
  input logic [3:0] s0_wstrb,
  output logic s0_bvalid,
  input logic s0_bready,
  output logic [1:0] s0_bresp,
  input logic s0_arvalid,
  output logic s0_arready,
  input logic [31:0] s0_araddr,
  input logic [2:0] s0_arprot,
  output logic s0_rvalid,
  input logic s0_rready,
  output logic [31:0] s0_rdata,
  output logic [1:0] s0_rresp,
  input logic s1_awvalid,
  output logic s1_awready,
  input logic [31:0] s1_awaddr,
  input logic [2:0] s1_awprot,
  input logic s1_wvalid,
  output logic s1_wready,
  input logic [31:0] s1_wdata,
  input logic [3:0] s1_wstrb,
  output logic s1_bvalid,
  input logic s1_bready,
  output logic [1:0] s1_bresp,
  input logic s1_arvalid,
  output logic s1_arready,
  input logic [31:0] s1_araddr,
  input logic [2:0] s1_arprot,
  output logic s1_rvalid,
  input logic s1_rready,
  output logic [31:0] s1_rdata,
  output logic [1:0] s1_rresp,
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
  output wire debug_busy,debug_owner
);
  logic active,owner,write_mode,turn;
  wire want0=s0_arvalid||s0_awvalid||s0_wvalid;
  wire want1=s1_arvalid||s1_awvalid||s1_wvalid;
  wire choice=want0&&want1?turn:want1;
  assign debug_busy=!reset&&active;
  assign debug_owner=owner;
  always_comb begin
    m_awvalid=0;
    s0_awready=0;s1_awready=0;
    m_awaddr=0;
    m_awprot=0;
    m_wvalid=0;
    s0_wready=0;s1_wready=0;
    m_wdata=0;
    m_wstrb=0;
    s0_bvalid=0;s1_bvalid=0;
    m_bready=0;
    s0_bresp=0;s1_bresp=0;
    m_arvalid=0;
    s0_arready=0;s1_arready=0;
    m_araddr=0;
    m_arprot=0;
    s0_rvalid=0;s1_rvalid=0;
    m_rready=0;
    s0_rdata=0;s1_rdata=0;
    s0_rresp=0;s1_rresp=0;
    if(!reset&&active)begin
      if(write_mode)begin
        if(!owner) begin
          m_awvalid=s0_awvalid;
          s0_awready=m_awready;
          m_awaddr=s0_awaddr;
          m_awprot=s0_awprot;
          m_wvalid=s0_wvalid;
          s0_wready=m_wready;
          m_wdata=s0_wdata;
          m_wstrb=s0_wstrb;
          s0_bvalid=m_bvalid;
          m_bready=s0_bready;
          s0_bresp=m_bresp;
        end
        else begin
          m_awvalid=s1_awvalid;
          s1_awready=m_awready;
          m_awaddr=s1_awaddr;
          m_awprot=s1_awprot;
          m_wvalid=s1_wvalid;
          s1_wready=m_wready;
          m_wdata=s1_wdata;
          m_wstrb=s1_wstrb;
          s1_bvalid=m_bvalid;
          m_bready=s1_bready;
          s1_bresp=m_bresp;
        end
      end else begin
        if(!owner) begin
          m_arvalid=s0_arvalid;
          s0_arready=m_arready;
          m_araddr=s0_araddr;
          m_arprot=s0_arprot;
          s0_rvalid=m_rvalid;
          m_rready=s0_rready;
          s0_rdata=m_rdata;
          s0_rresp=m_rresp;
        end
        else begin
          m_arvalid=s1_arvalid;
          s1_arready=m_arready;
          m_araddr=s1_araddr;
          m_arprot=s1_arprot;
          s1_rvalid=m_rvalid;
          m_rready=s1_rready;
          s1_rdata=m_rdata;
          s1_rresp=m_rresp;
        end
      end
    end
  end
  always_ff @(posedge clock)begin
    if(reset)begin active<=0;owner<=0;write_mode<=0;turn<=0;end
    else if(!active)begin
      if(want0||want1)begin active<=1;owner<=choice;write_mode<=choice?!s1_arvalid:!s0_arvalid;end
    end else if((write_mode&&m_bvalid&&m_bready)||(!write_mode&&m_rvalid&&m_rready))begin
      active<=0;turn<=!owner;
    end
  end
endmodule
