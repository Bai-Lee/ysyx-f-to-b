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
