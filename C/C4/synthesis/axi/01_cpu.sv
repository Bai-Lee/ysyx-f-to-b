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
        s_arready=!aw_have&&!w_have&&!s_awvalid&&!s_wvalid;
      end
      R_SEND:begin
        m_arvalid[target]=1;m_araddr[target*32+:32]=address;m_arprot[target*3+:3]=protection;
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
    if(reset)begin state<=IDLE;target<=0;aw_have<=0;w_have<=0;aw_done<=0;w_done<=0;address<=0;data<=0;protection<=0;strobe<=0;end
    else case(state)
      IDLE:begin
        if(aw_fire)begin address<=s_awaddr;protection<=s_awprot;aw_have<=1;end
        if(w_fire)begin data<=s_wdata;strobe<=s_wstrb;w_have<=1;end
        if((aw_have||aw_fire)&&(w_have||w_fire))begin
          target<=decode(effective_addr);aw_done<=0;w_done<=0;
          state<=(decode(effective_addr)==3)?W_ERROR:W_SEND;
        end else if(s_arvalid&&s_arready)begin
          address<=s_araddr;protection<=s_arprot;target<=decode(s_araddr);
          state<=((decode(s_araddr)==3)||(s_arprot[2]&&decode(s_araddr)!=0))?R_ERROR:R_SEND;
        end
      end
      R_SEND:if(m_arvalid[target]&&m_arready[target])state<=R_RESP;
      R_RESP:if(s_rvalid&&s_rready)state<=IDLE;
      W_SEND:begin
        if(m_awvalid[target]&&m_awready[target])aw_done<=1;
        if(m_wvalid[target]&&m_wready[target])w_done<=1;
        if((aw_done||(m_awvalid[target]&&m_awready[target]))&&(w_done||(m_wvalid[target]&&m_wready[target])))state<=W_RESP;
      end
      W_RESP:if(s_bvalid&&s_bready)begin state<=IDLE;aw_have<=0;w_have<=0;end
      R_ERROR:if(s_rvalid&&s_rready)state<=IDLE;
      W_ERROR:if(s_bvalid&&s_bready)begin state<=IDLE;aw_have<=0;w_have<=0;end
      default:state<=IDLE;
    endcase
  end
endmodule

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

module c4_simple_core #(
  parameter integer STAGE=4,
  parameter logic [31:0] RESET_PC=32'h80000000,
  parameter bit FAULT_ADDI=0
)(
  input logic clock,reset,
  input logic [2:0] delay_enable,input logic [31:0] lfsr_seed,
  output logic i_req_valid,output logic [31:0] i_req_addr,input logic i_req_ready,
  input logic i_resp_valid,input logic [31:0] i_resp_data,input logic [1:0] i_resp_error,output logic i_resp_ready,
  output logic d_req_valid,output logic [31:0] d_req_addr,output logic d_req_write,
  output logic [31:0] d_req_wdata,output logic [3:0] d_req_wstrb,input logic d_req_ready,
  input logic d_resp_valid,input logic [31:0] d_resp_data,input logic [1:0] d_resp_error,output logic d_resp_ready,
  output wire [31:0] pc,output wire halted,output wire [2:0] fault,
  output wire commit_valid,output wire [31:0] commit_pc,commit_inst,commit_next_pc,output wire [511:0] debug_gpr,
  output logic exec_fire,output wire [31:0] exec_pc,output logic [31:0] exec_inst,output logic exec_ebreak,
  output logic exec_mem_valid,exec_mem_write,output wire [31:0] exec_mem_addr,
  output wire [2:0] exec_mem_size,output wire [31:0] exec_mem_wdata,exec_mem_rdata,
  output wire [2:0] debug_state
);
  localparam logic [2:0] F_REQ=0,F_WAIT=1,D_REQ=2,D_WAIT=3;
  logic [2:0] state;
  logic [31:0] held_inst,lfsr;
  logic i_pending,d_pending;
  logic advance;logic [2:0] bus_fault;
  wire [31:0] logical_addr,logical_wdata;
  wire [2:0] logical_size;
  wire mem_ren,mem_wen,execute_valid,execute_ebreak;
  wire [31:0] load_data=d_resp_data >> {logical_addr[1:0],3'b000};
  wire mem_op=mem_ren||mem_wen;
  wire i_gap=(STAGE>=3)&&delay_enable[0];
  wire d_gap=(STAGE>=3)&&delay_enable[1];
  wire r_gap=(STAGE>=4)&&delay_enable[2];
  wire i_issue=i_pending||!i_gap||lfsr[0];
  wire d_issue=d_pending||!d_gap||lfsr[9];
  wire r_accept=!r_gap||lfsr[17];
  wire i_req_fire=i_req_valid&&i_req_ready;
  wire i_resp_fire=i_resp_valid&&i_resp_ready;
  wire d_req_fire=d_req_valid&&d_req_ready;
  wire d_resp_fire=d_resp_valid&&d_resp_ready;
  assign exec_pc=pc;
  assign exec_mem_addr=logical_addr;
  assign exec_mem_size=logical_size;
  assign exec_mem_wdata=logical_wdata;
  assign exec_mem_rdata=load_data;
  assign debug_state=state;

  always_comb begin
    exec_inst=(state==F_WAIT)?i_resp_data:held_inst;
    i_req_addr=pc;i_req_valid=0;i_resp_ready=0;
    d_req_valid=0;d_req_addr={logical_addr[31:2],2'b00};
    d_req_write=mem_wen;d_req_wdata=logical_wdata << {logical_addr[1:0],3'b000};
    case(logical_size)
      3'd1:d_req_wstrb=4'b0001 << logical_addr[1:0];
      3'd2:d_req_wstrb=4'b0011 << logical_addr[1:0];
      default:d_req_wstrb=4'b1111;
    endcase
    if(!mem_wen)d_req_wstrb=0;
    d_resp_ready=0;advance=0;bus_fault=0;
    if(!reset&&!halted)begin
      case(state)
        F_REQ:i_req_valid=i_issue;
        F_WAIT:begin
          i_resp_ready=r_accept;
          if(i_resp_fire)begin
            if(i_resp_error!=0)begin advance=1;bus_fault=5;end
            else if(!mem_op)advance=1;
            else begin
              d_req_valid=(STAGE==1)||d_issue;
              if(STAGE==1)begin
                d_resp_ready=d_req_valid&&d_req_ready;
                if(d_resp_fire)begin advance=1;if(d_resp_error!=0)bus_fault=5;end
              end
            end
          end
        end
        D_REQ:d_req_valid=d_issue;
        D_WAIT:begin
          d_resp_ready=r_accept;
          if(d_resp_fire)begin advance=1;if(d_resp_error!=0)bus_fault=5;end
        end
        default:begin advance=1;bus_fault=5;end
      endcase
    end
    exec_fire=advance&&execute_valid&&bus_fault==0;
    exec_ebreak=exec_fire&&execute_ebreak;
    exec_mem_valid=exec_fire&&mem_op;
    exec_mem_write=exec_mem_valid&&mem_wen;
  end

  rv32e_execute #(.RESET_PC(RESET_PC),.FAULT_ADDI(FAULT_ADDI)) cpu(
    .clock(clock),.reset(reset),.advance(advance),.bus_fault(bus_fault),.inst(exec_inst),.mem_rdata(load_data),
    .pc(pc),.mem_addr(logical_addr),.mem_wdata(logical_wdata),.mem_size(logical_size),
    .mem_ren(mem_ren),.mem_wen(mem_wen),.exec_valid(execute_valid),.exec_ebreak(execute_ebreak),
    .halted(halted),.fault(fault),.commit_valid(commit_valid),.commit_pc(commit_pc),
    .commit_inst(commit_inst),.commit_next_pc(commit_next_pc),.debug_gpr(debug_gpr));

  always_ff @(posedge clock)begin
    if(reset)begin
      state<=F_REQ;held_inst<=32'h00000013;i_pending<=0;d_pending<=0;
      lfsr<=(lfsr_seed==0)?32'h26070401:lfsr_seed;
    end else begin
      lfsr<={lfsr[30:0],lfsr[31]^lfsr[21]^lfsr[1]^lfsr[0]};
      if(!halted)begin
        case(state)
          F_REQ:begin
            if(i_req_valid)i_pending<=1;
            if(i_req_fire)begin state<=F_WAIT;i_pending<=0;end
          end
          F_WAIT:if(i_resp_fire)begin
            held_inst<=i_resp_data;
            if(advance)begin state<=F_REQ;d_pending<=0;end
            else if(d_req_fire)begin state<=D_WAIT;d_pending<=0;end
            else begin state<=D_REQ;d_pending<=d_req_valid;end
          end
          D_REQ:begin
            if(d_req_valid)d_pending<=1;
            if(d_req_fire)begin state<=D_WAIT;d_pending<=0;end
          end
          D_WAIT:if(d_resp_fire)state<=F_REQ;
          default:state<=F_REQ;
        endcase
      end
    end
  end
endmodule

module rv32e_execute #(
  parameter logic [31:0] RESET_PC=32'h80000000,
  parameter bit FAULT_ADDI=0
)(input logic clock,reset,advance,input logic [2:0] bus_fault,input logic [31:0] inst,mem_rdata,
  output logic [31:0] pc,mem_addr,mem_wdata,
  output logic [2:0] mem_size,
  output logic mem_ren,mem_wen,exec_valid,exec_ebreak,
  output logic halted,output logic [2:0] fault,
  output logic commit_valid,output logic [31:0] commit_pc,commit_inst,commit_next_pc,
  output wire [511:0] debug_gpr);
  logic [31:0] r[0:15];
  wire [4:0] rd=inst[11:7],rs1=inst[19:15],rs2=inst[24:20];
  wire [2:0] f3=inst[14:12];wire [6:0] f7=inst[31:25];
  wire [31:0] a=rs1[3:0]==0?32'b0:r[rs1[3:0]];
  wire [31:0] b=rs2[3:0]==0?32'b0:r[rs2[3:0]];
  wire [31:0] imm_i={{20{inst[31]}},inst[31:20]};
  wire [31:0] imm_s={{20{inst[31]}},inst[31:25],inst[11:7]};
  wire [31:0] imm_b={{19{inst[31]}},inst[31],inst[7],inst[30:25],inst[11:8],1'b0};
  wire [31:0] imm_j={{11{inst[31]}},inst[31],inst[19:12],inst[20],inst[30:21],1'b0};
  logic [31:0] value,next_pc;
  logic writes,loads,stores,uses_a,uses_b,legal,take;
  logic [2:0] decode_fault;
  for(genvar g=0;g<16;g++)begin: expose
    assign debug_gpr[g*32+:32]=(g==0)?32'b0:r[g];
  end
  always_comb begin
    value=0;next_pc=pc+32'd4;mem_addr=0;mem_wdata=b;mem_size=3'd4;
    writes=0;loads=0;stores=0;uses_a=0;uses_b=0;legal=1;take=0;exec_ebreak=0;
    case(inst[6:0])
      7'h37:begin writes=1;value={inst[31:12],12'b0};end
      7'h17:begin writes=1;value=pc+{inst[31:12],12'b0};end
      7'h6f:begin writes=1;value=pc+32'd4;next_pc=pc+imm_j;end
      7'h67:begin writes=1;uses_a=1;legal=f3==0;value=pc+32'd4;next_pc=(a+imm_i)&32'hfffffffe;end
      7'h63:begin
        uses_a=1;uses_b=1;
        case(f3)
          0:take=a==b;1:take=a!=b;
          4:take=$signed(a)<$signed(b);5:take=$signed(a)>=$signed(b);
          6:take=a<b;7:take=a>=b;default:legal=0;
        endcase
        if(take)next_pc=pc+imm_b;
      end
      7'h03:begin
        uses_a=1;writes=1;loads=1;mem_addr=a+imm_i;
        case(f3)
          0:begin mem_size=1;value={{24{mem_rdata[7]}},mem_rdata[7:0]};end
          1:begin mem_size=2;value={{16{mem_rdata[15]}},mem_rdata[15:0]};end
          2:begin mem_size=4;value=mem_rdata;end
          4:begin mem_size=1;value={24'b0,mem_rdata[7:0]};end
          5:begin mem_size=2;value={16'b0,mem_rdata[15:0]};end
          default:legal=0;
        endcase
      end
      7'h23:begin
        uses_a=1;uses_b=1;stores=1;mem_addr=a+imm_s;
        case(f3)
          0:mem_size=1;1:mem_size=2;2:mem_size=4;default:legal=0;
        endcase
      end
      7'h13:begin
        uses_a=1;writes=1;
        case(f3)
          0:value=a+imm_i+(FAULT_ADDI?32'd1:32'd0);
          1:begin value=a<<rs2;legal=f7==0;end
          2:value={31'b0,$signed(a)<$signed(imm_i)};
          3:value={31'b0,a<imm_i};4:value=a^imm_i;
          5:begin value=(f7==7'h20) ? 32'($signed(a)>>>rs2) : a>>rs2;legal=f7==0||f7==7'h20;end
          6:value=a|imm_i;7:value=a&imm_i;
          default:legal=0;
        endcase
      end
      7'h33:begin
        uses_a=1;uses_b=1;writes=1;
        case(f3)
          0:begin value=(f7==7'h20) ? a-b : a+b;legal=f7==0||f7==7'h20;end
          1:begin value=a<<b[4:0];legal=f7==0;end
          2:begin value={31'b0,$signed(a)<$signed(b)};legal=f7==0;end
          3:begin value={31'b0,a<b};legal=f7==0;end
          4:begin value=a^b;legal=f7==0;end
          5:begin value=(f7==7'h20) ? 32'($signed(a)>>>b[4:0]) : a>>b[4:0];legal=f7==0||f7==7'h20;end
          6:begin value=a|b;legal=f7==0;end
          7:begin value=a&b;legal=f7==0;end
          default:legal=0;
        endcase
      end
      7'h0f:legal=f3==0||f3==1; // sequential, no-cache EEI
      7'h73:begin legal=inst==32'h00100073;exec_ebreak=legal;end
      default:legal=0;
    endcase
    decode_fault=0;
    if(!legal)decode_fault=1;
    else if((writes&&rd[4])||(uses_a&&rs1[4])||(uses_b&&rs2[4]))decode_fault=2;
    else if(pc[1:0]!=0||next_pc[1:0]!=0)decode_fault=3;
    else if((loads||stores)&&((mem_size==2&&mem_addr[0])||(mem_size==4&&mem_addr[1:0]!=0)))decode_fault=4;
    exec_valid=!reset&&!halted&&decode_fault==0;
    mem_ren=exec_valid&&loads;mem_wen=exec_valid&&stores;
  end
  always_ff @(posedge clock)begin
    if(reset)begin
      pc<=RESET_PC;halted<=0;fault<=0;commit_valid<=0;commit_pc<=0;commit_inst<=0;commit_next_pc<=0;
      for(integer j=0;j<16;j=j+1)r[j]<=0;
    end else begin
      commit_valid<=0;
      if(!halted&&advance)begin
        if(bus_fault!=0)begin halted<=1;fault<=bus_fault;end
        else if(decode_fault!=0)begin halted<=1;fault<=decode_fault;end
        else begin
          if(writes&&rd!=0)r[rd[3:0]]<=value;
          pc<=next_pc;commit_valid<=1;commit_pc<=pc;commit_inst<=inst;commit_next_pc<=next_pc;
          if(exec_ebreak)halted<=1;
        end
      end
    end
  end
endmodule

module simple_to_axil #(parameter bit READ_ONLY=0,parameter logic [2:0] PROT=0)(
  input logic clock,reset,
  input logic req_valid,output logic req_ready,input logic [31:0] req_addr,input logic req_write,
  input logic [31:0] req_wdata,input logic [3:0] req_wstrb,
  output logic resp_valid,input logic resp_ready,output logic [31:0] resp_data,output logic [1:0] resp_error,
  output logic m_awvalid,input logic m_awready,output logic [31:0] m_awaddr,output logic [2:0] m_awprot,
  output logic m_wvalid,input logic m_wready,output logic [31:0] m_wdata,output logic [3:0] m_wstrb,
  input logic m_bvalid,output logic m_bready,input logic [1:0] m_bresp,
  output logic m_arvalid,input logic m_arready,output logic [31:0] m_araddr,output logic [2:0] m_arprot,
  input logic m_rvalid,output logic m_rready,input logic [31:0] m_rdata,input logic [1:0] m_rresp
);
  localparam logic [2:0] IDLE=0,R_ADDR=1,R_RESP=2,W_SEND=3,W_RESP=4,ERROR=5;
  logic [2:0] state;logic [31:0] address,data;logic [3:0] strobe;logic aw_done,w_done;
  always_comb begin
    req_ready=!reset&&state==IDLE;resp_valid=0;resp_data=0;resp_error=0;
    m_awvalid=0;m_awaddr=READ_ONLY?32'b0:address;m_awprot=READ_ONLY?3'b0:PROT;
    m_wvalid=0;m_wdata=READ_ONLY?32'b0:data;m_wstrb=READ_ONLY?4'b0:strobe;m_bready=0;
    m_arvalid=0;m_araddr=address;m_arprot=PROT;m_rready=0;
    if(!reset)case(state)
      R_ADDR:m_arvalid=1;
      R_RESP:begin resp_valid=m_rvalid;resp_data=m_rdata;resp_error=m_rresp;m_rready=resp_ready;end
      W_SEND:if(!READ_ONLY)begin m_awvalid=!aw_done;m_wvalid=!w_done;end
      W_RESP:if(!READ_ONLY)begin resp_valid=m_bvalid;resp_error=m_bresp;m_bready=resp_ready;end
      ERROR:begin resp_valid=1;resp_error=2'b10;end
      default:begin end
    endcase
  end
  always_ff @(posedge clock)begin
    if(reset)begin state<=IDLE;address<=0;data<=0;strobe<=0;aw_done<=0;w_done<=0;end
    else case(state)
      IDLE:if(req_valid&&req_ready)begin
        address<=req_addr;data<=req_wdata;strobe<=req_wstrb;aw_done<=0;w_done<=0;
        state<=req_write?(READ_ONLY?ERROR:W_SEND):R_ADDR;
      end
      R_ADDR:if(m_arvalid&&m_arready)state<=R_RESP;
      R_RESP:if(m_rvalid&&m_rready)state<=IDLE;
      W_SEND:begin
        if(m_awvalid&&m_awready)aw_done<=1;
        if(m_wvalid&&m_wready)w_done<=1;
        if((aw_done||(m_awvalid&&m_awready))&&(w_done||(m_wvalid&&m_wready)))state<=W_RESP;
      end
      W_RESP:if(m_bvalid&&m_bready)state<=IDLE;
      ERROR:if(resp_valid&&resp_ready)state<=IDLE;
      default:state<=IDLE;
    endcase
  end
endmodule
