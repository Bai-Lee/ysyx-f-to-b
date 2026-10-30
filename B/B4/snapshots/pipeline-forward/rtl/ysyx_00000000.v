`ifndef C5_RESET_PC
`define C5_RESET_PC 32'h20000000
`endif
`ifndef C5_FAULT_ADDI
`define C5_FAULT_ADDI 0
`endif
`ifndef C5_CORE_DELAYS
`define C5_CORE_DELAYS 0
`endif
`ifndef B_ICACHE_ENABLE
`define B_ICACHE_ENABLE 0
`endif
`ifndef B_ICACHE_LINES
`define B_ICACHE_LINES 16
`endif
`ifndef B_ICACHE_WORDS
`define B_ICACHE_WORDS 1
`endif
`ifndef B_ICACHE_WAYS
`define B_ICACHE_WAYS 1
`endif
`ifndef B_ICACHE_BURST
`define B_ICACHE_BURST 0
`endif
`ifndef B_FAULT_FENCE
`define B_FAULT_FENCE 0
`endif
`ifndef B_PIPELINE
`define B_PIPELINE 0
`endif
`ifndef B_FORWARD
`define B_FORWARD 0
`endif
`ifndef B_PREDICT
`define B_PREDICT 0
`endif
`ifndef B_FAULT_FENCE_FLUSH
`define B_FAULT_FENCE_FLUSH 0
`endif
`ifndef B_FAULT_RAW
`define B_FAULT_RAW 0
`endif
module ysyx_00000000(
input wire clock,reset,io_interrupt,
input wire io_master_awready,
output logic io_master_awvalid,
output logic [31:0] io_master_awaddr,
output logic [3:0] io_master_awid,
output logic [7:0] io_master_awlen,
output logic [2:0] io_master_awsize,
output logic [1:0] io_master_awburst,
input wire io_master_wready,
output logic io_master_wvalid,
output logic [31:0] io_master_wdata,
output logic [3:0] io_master_wstrb,
output logic io_master_wlast,
output logic io_master_bready,
input wire io_master_bvalid,
input wire [1:0] io_master_bresp,
input wire [3:0] io_master_bid,
input wire io_master_arready,
output logic io_master_arvalid,
output logic [31:0] io_master_araddr,
output logic [3:0] io_master_arid,
output logic [7:0] io_master_arlen,
output logic [2:0] io_master_arsize,
output logic [1:0] io_master_arburst,
output logic io_master_rready,
input wire io_master_rvalid,
input wire [1:0] io_master_rresp,
input wire [31:0] io_master_rdata,
input wire io_master_rlast,
input wire [3:0] io_master_rid,
output logic io_slave_awready,
input wire io_slave_awvalid,
input wire [31:0] io_slave_awaddr,
input wire [3:0] io_slave_awid,
input wire [7:0] io_slave_awlen,
input wire [2:0] io_slave_awsize,
input wire [1:0] io_slave_awburst,
output logic io_slave_wready,
input wire io_slave_wvalid,
input wire [31:0] io_slave_wdata,
input wire [3:0] io_slave_wstrb,
input wire io_slave_wlast,
input wire io_slave_bready,
output logic io_slave_bvalid,
output logic [1:0] io_slave_bresp,
output logic [3:0] io_slave_bid,
output logic io_slave_arready,
input wire io_slave_arvalid,
input wire [31:0] io_slave_araddr,
input wire [3:0] io_slave_arid,
input wire [7:0] io_slave_arlen,
input wire [2:0] io_slave_arsize,
input wire [1:0] io_slave_arburst,
input wire io_slave_rready,
output logic io_slave_rvalid,
output logic [1:0] io_slave_rresp,
output logic [31:0] io_slave_rdata,
output logic io_slave_rlast,
output logic [3:0] io_slave_rid
);
  wire unused_inputs=^{io_interrupt,io_slave_awvalid,io_slave_awaddr,io_slave_awid,io_slave_awlen,io_slave_awsize,io_slave_awburst,io_slave_wvalid,io_slave_wdata,io_slave_wstrb,io_slave_wlast,io_slave_bready,io_slave_arvalid,io_slave_araddr,io_slave_arid,io_slave_arlen,io_slave_arsize,io_slave_arburst,io_slave_rready};
  assign io_slave_awready='0;
  assign io_slave_wready='0;
  assign io_slave_bvalid='0;
  assign io_slave_bresp='0;
  assign io_slave_bid='0;
  assign io_slave_arready='0;
  assign io_slave_rvalid='0;
  assign io_slave_rresp='0;
  assign io_slave_rdata='0;
  assign io_slave_rlast='0;
  assign io_slave_rid='0;

  wire i_req_valid,i_req_ready,i_resp_valid,i_resp_ready;
  wire [31:0] i_req_addr,i_resp_data;wire [1:0] i_resp_error;
  wire d_req_valid,d_req_ready,d_req_write,d_resp_valid,d_resp_ready;
  wire [31:0] d_req_addr,d_req_wdata,d_resp_data;wire [3:0] d_req_wstrb;
  wire [2:0] d_req_size;wire [1:0] d_resp_error;
  wire [31:0] pc;wire halted;wire [2:0] fault,debug_state;
  wire commit_valid;wire [31:0] commit_pc,commit_inst,commit_next_pc;wire [511:0] debug_gpr;
  wire exec_fire,exec_ebreak,exec_mem_valid,exec_mem_write;
  wire [31:0] exec_pc,exec_inst,exec_mem_addr,exec_mem_wdata,exec_mem_rdata;wire [2:0] exec_mem_size;
  wire [2:0] delay_enable=`C5_CORE_DELAYS;wire [31:0] lfsr_seed=32'h2607c501;
  generate if(`B_PIPELINE)begin:pipelined
    ysyx_00000000_pipe #(.STAGE(4),.RESET_PC(`C5_RESET_PC),.FAULT_ADDI(`C5_FAULT_ADDI),.FORWARD(`B_FORWARD),.PREDICT(`B_PREDICT),.FAULT_FENCE_FLUSH(`B_FAULT_FENCE_FLUSH),.FAULT_RAW(`B_FAULT_RAW)) core(.*);
  end else begin:multicycle
    ysyx_00000000_core #(.STAGE(4),.RESET_PC(`C5_RESET_PC),.FAULT_ADDI(`C5_FAULT_ADDI)) core(.*);
  end endgenerate
  wire f_req_valid,f_req_ready,f_resp_valid,f_resp_ready,f_resp_last;
  wire [31:0] f_req_addr,f_resp_data;wire [7:0] f_req_len;wire [1:0] f_resp_error;
  wire cache_access,cache_hit,cache_miss,cache_bypass,cache_fill;
  wire cache_invalidate=!`B_FAULT_FENCE&&exec_fire&&exec_inst[6:0]==7'h0f&&exec_inst[14:12]==1;
  generate if(`B_ICACHE_ENABLE)begin:cached_fetch
    ysyx_00000000_icache #(.LINES(`B_ICACHE_LINES),.WORDS(`B_ICACHE_WORDS),.WAYS(`B_ICACHE_WAYS),.USE_BURST(`B_ICACHE_BURST)) icache(
      .clock(clock),.reset(reset),.invalidate(cache_invalidate),
      .q_valid(i_req_valid),.q_addr(i_req_addr),.q_ready(i_req_ready),
      .p_valid(i_resp_valid),.p_data(i_resp_data),.p_error(i_resp_error),.p_ready(i_resp_ready),
      .m_valid(f_req_valid),.m_addr(f_req_addr),.m_len(f_req_len),.m_ready(f_req_ready),
      .r_valid(f_resp_valid),.r_data(f_resp_data),.r_error(f_resp_error),.r_last(f_resp_last),.r_ready(f_resp_ready),
      .event_access(cache_access),.event_hit(cache_hit),.event_miss(cache_miss),.event_bypass(cache_bypass),.event_fill(cache_fill));
  end else begin:uncached_fetch
    assign f_req_valid=i_req_valid;assign f_req_addr=i_req_addr;assign f_req_len=0;
    assign i_req_ready=f_req_ready;assign i_resp_valid=f_resp_valid;assign i_resp_data=f_resp_data;assign i_resp_error=f_resp_error;assign f_resp_ready=i_resp_ready;
    assign cache_access=0;assign cache_hit=0;assign cache_miss=0;assign cache_bypass=0;assign cache_fill=0;
  end endgenerate
  localparam logic [2:0] IDLE=0,READ_ADDRESS=1,READ_RESPONSE=2,WRITE_CHANNELS=3,WRITE_RESPONSE=4,LOCAL_RESPONSE=5;
  logic [2:0] state;
  logic owner_data,turn,aw_done,w_done;
  logic [31:0] address,data,local_data;
  logic [3:0] strobe;
  logic [2:0] size;
  logic [7:0] read_length,read_beat;
  logic [1:0] local_error;
  logic [63:0] mtime;
  logic [31:0] latched_high;
  logic high_valid;
  wire choose_data=d_req_valid&&(!f_req_valid||turn);
  wire request=(f_req_valid||d_req_valid)&&state==IDLE&&!reset;
  wire [31:0] chosen_address=choose_data?d_req_addr:f_req_addr;
  wire [2:0] chosen_size=choose_data?d_req_size:3'd2;
  wire chosen_write=choose_data&&d_req_write;
  wire internal_clint=chosen_address[31:16]==16'h0200;
  wire executable=(chosen_address>=32'h0f000000&&chosen_address<32'h0f002000)||
                  (chosen_address>=32'h20000000&&chosen_address<32'h20001000)||
                  chosen_address[31:28]==4'h3||chosen_address[31:29]==3'b100||
                  chosen_address[31:29]==3'b101||chosen_address[31:30]==2'b11;
  wire response_ready=owner_data?d_resp_ready:f_resp_ready;
  logic response_valid;logic [31:0] response_data;logic [1:0] response_error;
  assign f_req_ready=!reset&&state==IDLE&&!choose_data;
  assign d_req_ready=!reset&&state==IDLE&&choose_data;
  assign f_resp_valid=!owner_data&&response_valid;
  assign d_resp_valid=owner_data&&response_valid;
  assign f_resp_data=response_data;assign d_resp_data=response_data;
  assign f_resp_error=response_error;assign d_resp_error=response_error;
  assign f_resp_last=state==READ_RESPONSE?io_master_rlast:1'b1;
  always_comb begin
    io_master_awvalid=0;io_master_awaddr=address;io_master_awid=1;io_master_awlen=0;io_master_awsize=size;io_master_awburst=1;
    io_master_wvalid=0;io_master_wdata=data;io_master_wstrb=strobe;io_master_wlast=0;io_master_bready=0;
    io_master_arvalid=0;io_master_araddr=address;io_master_arid={3'b0,owner_data};io_master_arlen=read_length;io_master_arsize=size;io_master_arburst=1;
    io_master_rready=0;response_valid=0;response_data=0;response_error=0;
    if(!reset)case(state)
      READ_ADDRESS:io_master_arvalid=1;
      READ_RESPONSE:begin
        response_valid=io_master_rvalid;response_data=io_master_rdata;
        response_error=(io_master_rid!={3'b0,owner_data}||io_master_rlast!=(read_beat==read_length))?2'b10:io_master_rresp;
        io_master_rready=response_ready;
      end
      WRITE_CHANNELS:begin io_master_awvalid=!aw_done;io_master_wvalid=!w_done;io_master_wlast=!w_done;end
      WRITE_RESPONSE:begin
        response_valid=io_master_bvalid;response_error=io_master_bid!=1?2'b10:io_master_bresp;io_master_bready=response_ready;
      end
      LOCAL_RESPONSE:begin response_valid=1;response_data=local_data;response_error=local_error;end
      default:begin end
    endcase
  end
  always_ff @(posedge clock)begin
    if(reset)begin
      state<=IDLE;owner_data<=0;turn<=0;aw_done<=0;w_done<=0;address<=0;data<=0;strobe<=0;size<=0;
      read_length<=0;read_beat<=0;
      local_data<=0;local_error<=0;mtime<=0;latched_high<=0;high_valid<=0;
    end else begin
      mtime<=mtime+1;
      case(state)
        IDLE:if(request)begin
          owner_data<=choose_data;address<=chosen_address;data<=d_req_wdata;strobe<=d_req_wstrb;size<=chosen_size;
          read_length<=choose_data?8'b0:f_req_len;read_beat<=0;
          aw_done<=0;w_done<=0;local_data<=0;local_error<=0;
          if((!choose_data&&!executable)||internal_clint)begin
            state<=LOCAL_RESPONSE;
            if(!choose_data) local_error<=2'b11;
            else if(chosen_write||chosen_size!=2) local_error<=2'b10;
            else if(chosen_address[15:0]==0)begin local_data<=mtime[31:0];latched_high<=mtime[63:32];high_valid<=1;end
            else if(chosen_address[15:0]==4)begin local_data<=high_valid?latched_high:mtime[63:32];high_valid<=0;end
            else local_error<=2'b10;
          end else state<=chosen_write?WRITE_CHANNELS:READ_ADDRESS;
        end
        READ_ADDRESS:if(io_master_arvalid&&io_master_arready)state<=READ_RESPONSE;
        READ_RESPONSE:if(response_valid&&response_ready)begin
          if(io_master_rlast)begin state<=IDLE;turn<=!owner_data;end
          else read_beat<=read_beat+1;
        end
        WRITE_CHANNELS:begin
          if(io_master_awvalid&&io_master_awready)aw_done<=1;
          if(io_master_wvalid&&io_master_wready)w_done<=1;
          if((aw_done||(io_master_awvalid&&io_master_awready))&&(w_done||(io_master_wvalid&&io_master_wready)))state<=WRITE_RESPONSE;
        end
        WRITE_RESPONSE:if(response_valid&&response_ready)begin state<=IDLE;turn<=!owner_data;end
        LOCAL_RESPONSE:if(response_ready)begin state<=IDLE;turn<=!owner_data;end
        default:state<=IDLE;
      endcase
    end
  end
`ifndef SYNTHESIS
  import "DPI-C" function void b_clock(input bit reset_active);
  import "DPI-C" function void b_perf_tick(input int unsigned state,input int unsigned events);
  import "DPI-C" function void b_cache_tick(input int unsigned events);
  reg observed_reset;
  always @(posedge clock)observed_reset<=reset;
  import "DPI-C" function void c5_retire(input int unsigned at_pc,input int unsigned inst,input int unsigned next_pc,input bit [511:0] registers);
  import "DPI-C" function void c5_fault(input int unsigned at_pc,input int unsigned code);
  import "DPI-C" function void c5_memory(input int unsigned at_pc,input int unsigned addr,input int unsigned bytes,input int unsigned value,input bit write_op);
  import "DPI-C" function void c5_bus(input int unsigned channel,input int unsigned addr,input int unsigned value,input int unsigned attr);
  always @(negedge clock)begin
    if(!reset)begin
      if(commit_valid)c5_retire(commit_pc,commit_inst,commit_next_pc,debug_gpr);
      if(fault!=0)c5_fault(pc,{29'b0,fault});
    end
    b_clock(observed_reset);
  end
  always @(posedge clock)if(!reset)begin
    b_cache_tick({26'b0,cache_invalidate,cache_fill,cache_bypass,cache_miss,cache_hit,cache_access});
    if(!halted)b_perf_tick({29'b0,debug_state},{22'b0,d_req_valid,i_resp_valid,i_req_valid,d_req_write,exec_mem_valid,exec_fire,d_resp_valid&&d_resp_ready,d_req_valid&&d_req_ready,i_resp_valid&&i_resp_ready,i_req_valid&&i_req_ready});
    if(exec_fire&&exec_mem_valid)c5_memory(exec_pc,exec_mem_addr,{29'b0,exec_mem_size},exec_mem_write?exec_mem_wdata:exec_mem_rdata,exec_mem_write);
    if(io_master_arvalid&&io_master_arready)c5_bus(0,io_master_araddr,0,{13'b0,io_master_arid,io_master_arlen,io_master_arsize,io_master_arburst,2'b0});
    if(io_master_rvalid&&io_master_rready)c5_bus(1,0,io_master_rdata,{25'b0,io_master_rid,io_master_rlast,io_master_rresp});
    if(io_master_awvalid&&io_master_awready)c5_bus(2,io_master_awaddr,0,{13'b0,io_master_awid,io_master_awlen,io_master_awsize,io_master_awburst,2'b0});
    if(io_master_wvalid&&io_master_wready)c5_bus(3,0,io_master_wdata,{27'b0,io_master_wlast,io_master_wstrb});
    if(io_master_bvalid&&io_master_bready)c5_bus(4,0,0,{26'b0,io_master_bid,io_master_bresp});
  end
`endif
endmodule
