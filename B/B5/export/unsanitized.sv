












































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
  wire [2:0] delay_enable=0;wire [31:0] lfsr_seed=32'h2607c501;
  generate if(1)begin:pipelined
    ysyx_00000000_pipe #(.STAGE(4),.RESET_PC(32'h30000000),.FAULT_ADDI(0),.FORWARD(1),.PREDICT(2),.FAULT_FENCE_FLUSH(0),.FAULT_RAW(0),.FETCH_PIPELINED(1)) core(.*);
  end else begin:multicycle
    ysyx_00000000_core #(.STAGE(4),.RESET_PC(32'h30000000),.FAULT_ADDI(0)) core(.*);
  end endgenerate
  wire f_req_valid,f_req_ready,f_resp_valid,f_resp_ready,f_resp_last;
  wire [31:0] f_req_addr,f_resp_data;wire [7:0] f_req_len;wire [1:0] f_resp_error;
  wire cache_access,cache_hit,cache_miss,cache_bypass,cache_fill;
  wire cache_invalidate=!0&&exec_fire&&exec_inst[6:0]==7'h0f&&exec_inst[14:12]==1;
  generate if(1)begin:cached_fetch
    ysyx_00000000_icache #(.LINES(4),.WORDS(8),.WAYS(2),.USE_BURST(1),.PIPELINED(1)) icache(
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




























endmodule
/* Pure RV32E decoder/ALU; load completion and architectural state live in the pipeline. */
module ysyx_00000000_alu #(parameter bit FAULT_ADDI=0)(
  input wire [31:0] pc,inst,a,b,mem_rdata,csr_old,csr_mtvec,csr_mepc,
  input wire csr_known,csr_readonly,
  output logic [31:0] value,next_pc,mem_addr,mem_wdata,csr_new,
  output logic [2:0] mem_size,decode_fault,
  output logic writes,loads,stores,uses_a,uses_b,exec_ebreak,csr_write,do_ecall,do_mret
);
  logic legal,take;logic [31:0] csr_operand;
  wire [4:0] rd=inst[11:7],rs1=inst[19:15],rs2=inst[24:20];
  wire [2:0] f3=inst[14:12];wire [6:0] f7=inst[31:25];
  wire [31:0] imm_i={{20{inst[31]}},inst[31:20]};
  wire [31:0] imm_s={{20{inst[31]}},inst[31:25],inst[11:7]};
  wire [31:0] imm_b={{19{inst[31]}},inst[31],inst[7],inst[30:25],inst[11:8],1'b0};
  wire [31:0] imm_j={{11{inst[31]}},inst[31],inst[19:12],inst[20],inst[30:21],1'b0};
  always_comb begin
    value=0;next_pc=pc+32'd4;mem_addr=0;mem_wdata=b;mem_size=3'd4;
    writes=0;loads=0;stores=0;uses_a=0;uses_b=0;legal=1;take=0;exec_ebreak=0;
    csr_write=0;csr_new=csr_old;csr_operand=f3[2]?{27'b0,rs1}:a;do_ecall=0;do_mret=0;
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
      7'h73:begin
        if(inst==32'h00100073)exec_ebreak=1;
        else if(inst==32'h00000073)begin do_ecall=1;next_pc={csr_mtvec[31:2],2'b0};end
        else if(inst==32'h30200073)begin do_mret=1;next_pc=csr_mepc;end
        else if(f3==1||f3==2||f3==3||f3==5||f3==6||f3==7)begin
          writes=1;uses_a=!f3[2];value=csr_old;legal=csr_known;
          case(f3[1:0])
            1:begin csr_write=1;csr_new=csr_operand;end
            2:begin csr_write=rs1!=0;csr_new=csr_old|csr_operand;end
            3:begin csr_write=rs1!=0;csr_new=csr_old&~csr_operand;end
            default:legal=0;
          endcase
          if(csr_write&&csr_readonly)legal=0;
        end else legal=0;
      end
      default:legal=0;
    endcase
    decode_fault=0;
    if(!legal)decode_fault=1;
    else if((writes&&rd[4])||(uses_a&&rs1[4])||(uses_b&&rs2[4]))decode_fault=2;
    else if(pc[1:0]!=0||next_pc[1:0]!=0)decode_fault=3;
    else if((loads||stores)&&((mem_size==2&&mem_addr[0])||(mem_size==4&&mem_addr[1:0]!=0)))decode_fault=4;
  end
endmodule
module ysyx_00000000_core #(
  parameter integer STAGE=4,
  parameter logic [31:0] RESET_PC=32'h80000000,
  parameter bit FAULT_ADDI=0
)(
  input logic clock,reset,
  input logic [2:0] delay_enable,input logic [31:0] lfsr_seed,
  output logic i_req_valid,output logic [31:0] i_req_addr,input logic i_req_ready,
  input logic i_resp_valid,input logic [31:0] i_resp_data,input logic [1:0] i_resp_error,output logic i_resp_ready,
  output wire [2:0] d_req_size,output logic d_req_valid,output logic [31:0] d_req_addr,output logic d_req_write,
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
  assign d_req_size=logical_size==1?3'd0:logical_size==2?3'd1:3'd2;

  always_comb begin
    exec_inst=(state==F_WAIT)?i_resp_data:held_inst;
    i_req_addr=pc;i_req_valid=0;i_resp_ready=0;
    d_req_valid=0;d_req_addr=logical_addr;
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

  ysyx_00000000_execute #(.RESET_PC(RESET_PC),.FAULT_ADDI(FAULT_ADDI)) cpu(
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
module ysyx_00000000_execute #(
  parameter logic [31:0] RESET_PC=32'h80000000,
  parameter bit FAULT_ADDI=0,
  parameter logic [31:0] PROJECT_ID=32'h26070001
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
  logic [31:0] csr_mstatus,csr_mtvec,csr_mscratch,csr_mepc,csr_mcause;
  logic [63:0] csr_mcycle;
  logic [31:0] csr_old,csr_new,csr_operand;
  logic csr_known,csr_readonly,csr_write,do_ecall,do_mret;
  wire [11:0] csr_address=inst[31:20];
  always_comb begin
    csr_old=0;csr_known=1;csr_readonly=0;
    case(csr_address)
      12'h300:csr_old=csr_mstatus;
      12'h305:csr_old=csr_mtvec;
      12'h340:csr_old=csr_mscratch;
      12'h341:csr_old=csr_mepc;
      12'h342:csr_old=csr_mcause;
      12'hb00:csr_old=csr_mcycle[31:0];
      12'hb80:csr_old=csr_mcycle[63:32];
      12'hf11:begin csr_old=32'h79737978;csr_readonly=1;end
      12'hf12:begin csr_old=PROJECT_ID;csr_readonly=1;end
      12'hf13:begin csr_old=1;csr_readonly=1;end
      12'hf14:begin csr_old=0;csr_readonly=1;end
      default:csr_known=0;
    endcase
  end
  for(genvar g=0;g<16;g++)begin: expose
    assign debug_gpr[g*32+:32]=(g==0)?32'b0:r[g];
  end
  always_comb begin
    value=0;next_pc=pc+32'd4;mem_addr=0;mem_wdata=b;mem_size=3'd4;
    writes=0;loads=0;stores=0;uses_a=0;uses_b=0;legal=1;take=0;exec_ebreak=0;
    csr_write=0;csr_new=csr_old;csr_operand=f3[2]?{27'b0,rs1}:a;do_ecall=0;do_mret=0;
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
      7'h73:begin
        if(inst==32'h00100073)exec_ebreak=1;
        else if(inst==32'h00000073)begin do_ecall=1;next_pc={csr_mtvec[31:2],2'b0};end
        else if(inst==32'h30200073)begin do_mret=1;next_pc=csr_mepc;end
        else if(f3==1||f3==2||f3==3||f3==5||f3==6||f3==7)begin
          writes=1;uses_a=!f3[2];value=csr_old;legal=csr_known;
          case(f3[1:0])
            1:begin csr_write=1;csr_new=csr_operand;end
            2:begin csr_write=rs1!=0;csr_new=csr_old|csr_operand;end
            3:begin csr_write=rs1!=0;csr_new=csr_old&~csr_operand;end
            default:legal=0;
          endcase
          if(csr_write&&csr_readonly)legal=0;
        end else legal=0;
      end
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
      csr_mstatus<=32'h1800;csr_mtvec<=0;csr_mscratch<=0;csr_mepc<=0;csr_mcause<=0;
      csr_mcycle<=0;
      for(integer j=0;j<16;j=j+1)r[j]<=0;
    end else begin
      csr_mcycle<=csr_mcycle+64'd1;
      commit_valid<=0;
      if(!halted&&advance)begin
        if(bus_fault!=0)begin halted<=1;fault<=bus_fault;end
        else if(decode_fault!=0)begin halted<=1;fault<=decode_fault;end
        else begin
          if(writes&&rd!=0)r[rd[3:0]]<=value;
          if(csr_write)case(csr_address)
            12'h300:csr_mstatus<=32'h1800|(csr_new&32'h88);
            12'h305:csr_mtvec<={csr_new[31:2],1'b0,(csr_new[1:0]==1)};
            12'h340:csr_mscratch<=csr_new;
            12'h341:csr_mepc<={csr_new[31:2],2'b0};
            12'h342:csr_mcause<=csr_new;
            12'hb00:csr_mcycle<={csr_mcycle[63:32],csr_new};
            12'hb80:csr_mcycle<={csr_new,csr_mcycle[31:0]};
            default:begin end
          endcase
          if(do_ecall)begin
            csr_mepc<=pc;csr_mcause<=11;csr_mstatus<=32'h1800|({31'b0,csr_mstatus[3]}<<7);
          end
          if(do_mret)csr_mstatus<=32'h1880|({31'b0,csr_mstatus[7]}<<3);
          pc<=next_pc;commit_valid<=1;commit_pc<=pc;commit_inst<=inst;commit_next_pc<=next_pc;
          if(exec_ebreak)halted<=1;
        end
      end
    end
  end
endmodule
/* Blocking parameterized instruction cache; refill metadata commits atomically. */
module ysyx_00000000_icache #(
  parameter integer LINES=16,WORDS=1,WAYS=1,
  parameter bit USE_BURST=0,FAULT_TAG=0,PIPELINED=0
)(
  input wire clock,reset,invalidate,
  input wire q_valid,input wire [31:0] q_addr,output wire q_ready,
  output wire p_valid,output wire [31:0] p_data,output wire [1:0] p_error,input wire p_ready,
  output wire m_valid,output wire [31:0] m_addr,output wire [7:0] m_len,input wire m_ready,
  input wire r_valid,input wire [31:0] r_data,input wire [1:0] r_error,input wire r_last,output wire r_ready,
  output wire event_access,event_hit,event_miss,event_bypass,event_fill
);
  localparam integer SETS=LINES/WAYS,WORD_BITS=$clog2(WORDS),SET_BITS=$clog2(SETS);
  localparam integer BEAT_BITS=WORD_BITS>0?WORD_BITS:1;
  localparam integer TAG_BITS=32-2-WORD_BITS-SET_BITS;
  localparam logic [31:0] LINE_ADDRESS_MASK=32'hffffffff << (2+WORD_BITS);
  localparam integer INDEX_WIDTH=$clog2(LINES)>0?$clog2(LINES):1;
  localparam [2:0] IDLE=0,REQUEST=1,FILL=2,RESPONSE=3;
  reg [2:0] state;
  reg [LINES-1:0] valid;
  reg [TAG_BITS-1:0] tags[0:LINES-1];
  reg [31:0] data[0:LINES*WORDS-1];
  reg [SETS-1:0] replace_way;
  reg [31:0] address,response_data;
  reg [1:0] response_error,fill_error;
  reg [INDEX_WIDTH-1:0] selected_line;
  reg [BEAT_BITS-1:0] beat;
  reg cached,burst,poison;
  wire [31:0] query_set=(q_addr>>(2+WORD_BITS))&32'(SETS-1);
  wire [31:0] query_word=(q_addr>>2)&32'(WORDS-1);
  wire [TAG_BITS-1:0] query_tag=TAG_BITS'(q_addr>>(2+WORD_BITS+SET_BITS));
  wire query_cacheable=(q_addr>=32'h30000000&&q_addr<32'h31000000)||
    (q_addr>=32'h80000000&&q_addr<32'h80400000)||(q_addr>=32'ha0000000&&q_addr<32'ha8000000);
  reg hit;reg [INDEX_WIDTH-1:0] hit_line,victim_line;
  integer w;
  always @*begin
    hit=0;hit_line=0;victim_line=INDEX_WIDTH'(query_set*WAYS+(WAYS==2?32'(replace_way[query_set]):0));
    for(w=0;w<WAYS;w=w+1)begin
      if(valid[query_set*WAYS+w]&&(FAULT_TAG||tags[query_set*WAYS+w]==query_tag))begin
        hit=1;hit_line=INDEX_WIDTH'(query_set*WAYS+w);
      end
      if(!valid[query_set*WAYS+w])victim_line=INDEX_WIDTH'(query_set*WAYS+w);
    end
  end
  assign q_ready=!reset&&(state==IDLE||(PIPELINED&&state==RESPONSE&&p_ready))&&!invalidate;
  assign p_valid=!reset&&state==RESPONSE;
  assign p_data=response_data;assign p_error=response_error;
  assign m_valid=!reset&&state==REQUEST;
  wire [31:0] beat_word={{(32-BEAT_BITS){1'b0}},beat};
  wire [31:0] byte_offset=WORDS==1?32'b0:{{(30-BEAT_BITS){1'b0}},beat,2'b0};
  // Aligned line base and the bounded word offset occupy disjoint bits.
  assign m_addr=cached?((address&LINE_ADDRESS_MASK)|(burst?32'b0:byte_offset)):address;
  assign m_len=burst?8'(WORDS-1):8'b0;
  assign r_ready=!reset&&state==FILL;
  assign event_access=q_valid&&q_ready;
  assign event_hit=event_access&&query_cacheable&&hit;
  assign event_miss=event_access&&query_cacheable&&!hit;
  assign event_bypass=event_access&&!query_cacheable;
  assign event_fill=r_valid&&r_ready&&cached&&(beat==WORDS-1)&&fill_error==0&&r_error==0;
  wire [31:0] held_word=(address>>2)&32'(WORDS-1);
  wire finish=!cached||(beat==WORDS-1)||(burst&&r_last);
  wire [1:0] current_error=fill_error|r_error|((r_last!=(burst?(beat==WORDS-1):1'b1))?2'b10:2'b00);
  always @(posedge clock)begin
    if(reset)begin
      state<=IDLE;valid<=0;replace_way<=0;address<=0;response_data<=0;response_error<=0;
      fill_error<=0;selected_line<=0;beat<=0;cached<=0;burst<=0;poison<=0;
    end else begin
      case(state)
        IDLE,RESPONSE:begin
          if(state==RESPONSE&&p_ready)state<=IDLE;
          if(event_access)begin
          address<=q_addr;response_error<=0;fill_error<=0;beat<=0;poison<=0;
          cached<=query_cacheable;burst<=USE_BURST&&WORDS>1&&q_addr>=32'ha0000000&&q_addr<32'ha8000000;
          if(query_cacheable&&hit)begin
            response_data<=data[32'(hit_line)*WORDS+query_word];state<=RESPONSE;
            if(WAYS==2)replace_way[query_set]<=!hit_line[0];
          end else begin
            selected_line<=victim_line;state<=REQUEST;
            if(query_cacheable)valid[victim_line]<=0;
          end
          end
        end
        REQUEST:if(m_valid&&m_ready)state<=FILL;
        FILL:if(r_valid&&r_ready)begin
          fill_error<=current_error;
          if(cached)data[32'(selected_line)*WORDS+beat_word]<=r_data;
          if(!cached||held_word==beat_word)response_data<=r_data;
          if(finish)begin
            response_error<=current_error;state<=RESPONSE;
            if(cached&&!poison&&!invalidate&&current_error==0)begin
              tags[selected_line]<=TAG_BITS'(address>>(2+WORD_BITS+SET_BITS));valid[selected_line]<=1;
              if(WAYS==2)replace_way[(address>>(2+WORD_BITS))&32'(SETS-1)]<=!selected_line[0];
            end
          end else begin beat<=beat+1;if(!burst)state<=REQUEST;end
        end
        default:state<=IDLE;
      endcase
      if(invalidate)begin valid<=0;if(state!=IDLE)poison<=1;end
    end
  end





endmodule
/* IF buffer -> decode/operand latch -> execute -> combined memory/retirement.
 * One in-order retirement per cycle. A stalled memory operation holds W;
 * ready/valid backpressure stops younger stages. System operations serialize.
 */
module ysyx_00000000_pipe #(
  parameter integer STAGE=4,
  parameter logic [31:0] RESET_PC=32'h80000000,
  parameter bit FAULT_ADDI=0,FORWARD=0,FAULT_FENCE_FLUSH=0,FAULT_RAW=0,FETCH_PIPELINED=0,
  parameter integer PREDICT=0
)(
  input logic clock,reset,
  input logic [2:0] delay_enable,input logic [31:0] lfsr_seed,
  output logic i_req_valid,output logic [31:0] i_req_addr,input logic i_req_ready,
  input logic i_resp_valid,input logic [31:0] i_resp_data,input logic [1:0] i_resp_error,output logic i_resp_ready,
  output wire [2:0] d_req_size,output logic d_req_valid,output logic [31:0] d_req_addr,output logic d_req_write,
  output logic [31:0] d_req_wdata,output logic [3:0] d_req_wstrb,input logic d_req_ready,
  input logic d_resp_valid,input logic [31:0] d_resp_data,input logic [1:0] d_resp_error,output logic d_resp_ready,
  output wire [31:0] pc,output logic halted,output logic [2:0] fault,
  output logic commit_valid,output logic [31:0] commit_pc,commit_inst,commit_next_pc,output wire [511:0] debug_gpr,
  output logic exec_fire,output wire [31:0] exec_pc,output logic [31:0] exec_inst,output logic exec_ebreak,
  output logic exec_mem_valid,exec_mem_write,output wire [31:0] exec_mem_addr,
  output wire [2:0] exec_mem_size,output wire [31:0] exec_mem_wdata,exec_mem_rdata,
  output wire [2:0] debug_state
);
  reg [31:0] r[1:15];
  reg [31:0] arch_pc,fault_pc,fetch_pc,pending_pc;
  reg fetch_pending,discard_fetch;
  reg d_valid,e_valid,w_valid;
  reg [31:0] d_pc,d_inst,e_pc,e_inst;
  reg [2:0] d_error,e_error;
  reg [31:0] w_pc,w_inst,w_next_pc,w_value,w_address;
  reg [3:0] w_rd;reg w_writes,w_load,w_store,w_sent,w_loaded;
  reg [2:0] w_size,w_fault_code;
  reg [31:0] csr_mstatus,csr_mtvec,csr_mscratch,csr_mepc,csr_mcause;
  reg [63:0] csr_mcycle;
  reg [31:0] csr_old;reg csr_known,csr_readonly;
  wire [11:0] csr_address=e_inst[31:20];
  wire [31:0] e_value,e_next_pc,e_address,e_data,e_csr_new;
  wire [2:0] e_size,e_decode_fault;
  wire e_writes,e_load,e_store,e_uses_a,e_uses_b,e_ebreak,e_csr_write,e_ecall,e_mret;
  wire [2:0] e_fault=e_error!=0?e_error:e_decode_fault;
  function automatic serial(input [31:0] instruction);
    begin serial=instruction[6:0]==7'h73||(instruction[6:0]==7'h0f&&!(FAULT_FENCE_FLUSH&&instruction[14:12]==1));end
  endfunction
  function automatic control(input [31:0] instruction);
    begin control=instruction[6:0]==7'h63||instruction[6:0]==7'h6f||instruction[6:0]==7'h67;end
  endfunction
  function automatic control_wait(input [31:0] instruction);
    begin control_wait=control(instruction)&&(PREDICT==0||(PREDICT==2&&instruction[6:0]!=7'h6f));end
  endfunction
  wire d_serial=serial(d_inst)||d_error!=0;
  wire e_serial=serial(e_inst)||e_error!=0;
  wire w_memory=w_load||w_store;
  wire [31:0] w_raw_data=d_resp_data>>{w_address[1:0],3'b0};
  reg [31:0] load_result;
  wire [31:0] w_result=w_value;
  always @*begin
    load_result=0;
    case(w_inst[14:12])
      0:load_result={{24{w_raw_data[7]}},w_raw_data[7:0]};
      1:load_result={{16{w_raw_data[15]}},w_raw_data[15:0]};
      2:load_result=w_raw_data;
      4:load_result={24'b0,w_raw_data[7:0]};
      5:load_result={16'b0,w_raw_data[15:0]};
      default:load_result=0;
    endcase
  end
  wire w_done=w_valid&&(w_fault_code!=0||!w_memory||(w_load?w_loaded:(w_sent&&d_resp_valid&&d_resp_ready)));
  wire [2:0] w_fault=w_fault_code!=0?w_fault_code:((w_memory&&w_sent&&d_resp_valid&&d_resp_error!=0)?3'd5:3'd0);
  wire w_commit=!reset&&!halted&&w_done&&w_fault==0;
  wire w_failure=!reset&&!halted&&w_done&&w_fault!=0;
  wire system_fire=!reset&&!halted&&e_valid&&e_serial&&!w_valid;
  wire system_commit=system_fire&&e_fault==0;
  wire e_transfer=!reset&&!halted&&e_valid&&!e_serial&&(!w_valid||w_done)&&!w_failure;
  wire [31:0] e_branch_imm={{19{e_inst[31]}},e_inst[31],e_inst[7],e_inst[30:25],e_inst[11:8],1'b0};
  wire [31:0] e_jump_imm={{11{e_inst[31]}},e_inst[31],e_inst[19:12],e_inst[20],e_inst[30:21],1'b0};
  // This predictor has no dynamic state: its prior prediction is exactly
  // reconstructed from the retained PC/instruction, saving two32-bit registers.
  wire [31:0] e_prediction=(PREDICT&&e_inst[6:0]==7'h6f)?e_pc+e_jump_imm:
    (PREDICT==1&&e_inst[6:0]==7'h63)?e_pc+e_branch_imm:e_pc+4;
  wire branch_redirect=e_transfer&&e_fault==0&&control(e_inst)&&e_next_pc!=e_prediction;
  wire redirect=system_commit||branch_redirect;
  wire [31:0] redirect_pc=e_next_pc;
  wire e_space=!e_valid||e_transfer;
  wire system_busy=(d_valid&&d_serial)||(e_valid&&e_serial);
  wire control_stall=(d_valid&&control_wait(d_inst))||(e_valid&&control_wait(e_inst));

  wire [4:0] d_rs1=d_inst[19:15],d_rs2=d_inst[24:20];
  reg d_uses_a,d_uses_b;
  always @*begin
    d_uses_a=0;d_uses_b=0;
    case(d_inst[6:0])
      7'h67,7'h03,7'h13:d_uses_a=1;
      7'h63,7'h23,7'h33:begin d_uses_a=1;d_uses_b=1;end
      7'h73:d_uses_a=d_inst[14:12]!=0&&!d_inst[14];
      default:begin end
    endcase
  end
  wire e_match_a=d_uses_a&&d_rs1!=0&&e_valid&&e_writes&&e_inst[11:7]!=0&&d_rs1==e_inst[11:7];
  wire e_match_b=d_uses_b&&d_rs2!=0&&e_valid&&e_writes&&e_inst[11:7]!=0&&d_rs2==e_inst[11:7];
  wire w_match_a=d_uses_a&&d_rs1!=0&&w_valid&&w_writes&&w_rd!=0&&d_rs1=={1'b0,w_rd};
  wire w_match_b=d_uses_b&&d_rs2!=0&&w_valid&&w_writes&&w_rd!=0&&d_rs2=={1'b0,w_rd};
  wire e_ready_data=!e_load&&e_fault==0&&!e_serial;
  wire w_ready_data=(!w_load||w_done)&&w_fault==0;
  wire raw_a=e_match_a?(!FORWARD||!e_ready_data):(w_match_a&&(!FORWARD||!w_ready_data));
  wire raw_b=e_match_b?(!FORWARD||!e_ready_data):(w_match_b&&(!FORWARD||!w_ready_data));
  wire raw_stall=!FAULT_RAW&&!FORWARD&&d_valid&&(raw_a||raw_b);
  // Read the register file in E. Only W is older than the current E stage,
  // so one forwarding source replaces two full operand pipeline registers.
  wire e_from_w_a=e_valid&&e_uses_a&&e_inst[19:15]!=0&&w_valid&&w_writes&&w_rd!=0&&e_inst[19:15]=={1'b0,w_rd};
  wire e_from_w_b=e_valid&&e_uses_b&&e_inst[24:20]!=0&&w_valid&&w_writes&&w_rd!=0&&e_inst[24:20]=={1'b0,w_rd};
  wire [31:0] register_a=e_inst[18:15]==0?32'b0:r[e_inst[18:15]];
  wire [31:0] register_b=e_inst[23:20]==0?32'b0:r[e_inst[23:20]];
  wire [31:0] e_a=FORWARD&&e_from_w_a?w_result:register_a;
  wire [31:0] e_b=FORWARD&&e_from_w_b?w_result:register_b;
  wire load_use=FORWARD?(e_valid&&w_valid&&w_load&&!w_done&&(e_from_w_a||e_from_w_b)):
    d_valid&&(((e_match_a||e_match_b)&&e_load)||(((w_match_a&&!e_match_a)||(w_match_b&&!e_match_b))&&w_load&&!w_done));
  wire d_transfer=!reset&&!halted&&d_valid&&e_space&&!raw_stall&&!redirect&&!w_failure&&
    !(e_valid&&e_serial)&&(!d_serial||(!e_valid&&!w_valid));

  wire [31:0] fetch_branch_imm={{19{i_resp_data[31]}},i_resp_data[31],i_resp_data[7],i_resp_data[30:25],i_resp_data[11:8],1'b0};
  wire [31:0] fetch_jump_imm={{11{i_resp_data[31]}},i_resp_data[31],i_resp_data[19:12],i_resp_data[20],i_resp_data[30:21],1'b0};
  wire [31:0] prediction=(PREDICT&&i_resp_data[6:0]==7'h6f)?pending_pc+fetch_jump_imm:
    (PREDICT==1&&i_resp_data[6:0]==7'h63)?pending_pc+fetch_branch_imm:pending_pc+4;
  wire stream_fetch=FETCH_PIPELINED&&fetch_pending&&i_resp_valid&&i_resp_ready&&!discard_fetch&&!redirect&&
    !serial(i_resp_data)&&!control_wait(i_resp_data)&&i_resp_error==0;
  wire i_req_fire=i_req_valid&&i_req_ready,i_resp_fire=i_resp_valid&&i_resp_ready;
  assign pc=halted&&fault!=0?fault_pc:arch_pc;
  assign d_req_size=w_size==1?3'd0:w_size==2?3'd1:3'd2;
  assign exec_pc=system_commit?e_pc:w_pc;
  assign exec_mem_addr=w_address;assign exec_mem_size=w_size;assign exec_mem_wdata=w_value;assign exec_mem_rdata=w_value;
  assign debug_state=w_valid&&w_memory&&!w_done?3'd3:raw_stall?3'd4:control_stall?3'd5:system_busy?3'd6:e_valid||w_valid?3'd2:fetch_pending?3'd1:3'd0;
  for(genvar g=0;g<16;g++)begin:expose
    if(g==0)assign debug_gpr[g*32+:32]=0;else assign debug_gpr[g*32+:32]=r[g];
  end
  always @*begin
    i_req_valid=!reset&&!halted&&(!fetch_pending||stream_fetch)&&!system_busy&&!control_stall;
    i_req_addr=stream_fetch?prediction:fetch_pc;
    i_resp_ready=!reset&&!halted&&fetch_pending&&(!d_valid||d_transfer||discard_fetch||redirect);
    d_req_valid=!reset&&!halted&&w_valid&&w_memory&&!w_sent&&w_fault_code==0;
    d_req_addr=w_address;d_req_write=w_store;d_req_wdata=w_value<<{w_address[1:0],3'b0};
    case(w_size)
      1:d_req_wstrb=4'b0001<<w_address[1:0];
      2:d_req_wstrb=4'b0011<<w_address[1:0];
      default:d_req_wstrb=4'b1111;
    endcase
    if(!w_store)d_req_wstrb=0;
    d_resp_ready=!reset&&!halted&&w_valid&&w_memory&&w_sent&&(!w_load||!w_loaded);
    exec_fire=w_commit||system_commit;exec_inst=system_commit?e_inst:w_inst;
    exec_ebreak=system_commit&&e_ebreak;
    exec_mem_valid=w_commit&&w_memory;exec_mem_write=exec_mem_valid&&w_store;
  end
  always @*begin
    csr_old=0;csr_known=1;csr_readonly=0;
    case(csr_address)
      12'h300:csr_old=csr_mstatus;12'h305:csr_old=csr_mtvec;12'h340:csr_old=csr_mscratch;
      12'h341:csr_old=csr_mepc;12'h342:csr_old=csr_mcause;
      12'hb00:csr_old=csr_mcycle[31:0];12'hb80:csr_old=csr_mcycle[63:32];
      12'hf11:begin csr_old=32'h79737978;csr_readonly=1;end
      12'hf12:begin csr_old=32'h26070001;csr_readonly=1;end
      12'hf13:begin csr_old=1;csr_readonly=1;end
      12'hf14:begin csr_old=0;csr_readonly=1;end
      default:csr_known=0;
    endcase
  end
  ysyx_00000000_alu #(.FAULT_ADDI(FAULT_ADDI)) alu(
    .pc(e_pc),.inst(e_inst),.a(e_a),.b(e_b),.mem_rdata(32'b0),.csr_old(csr_old),.csr_mtvec(csr_mtvec),.csr_mepc(csr_mepc),
    .csr_known(csr_known),.csr_readonly(csr_readonly),.value(e_value),.next_pc(e_next_pc),.mem_addr(e_address),.mem_wdata(e_data),.csr_new(e_csr_new),
    .mem_size(e_size),.decode_fault(e_decode_fault),.writes(e_writes),.loads(e_load),.stores(e_store),.uses_a(e_uses_a),.uses_b(e_uses_b),
    .exec_ebreak(e_ebreak),.csr_write(e_csr_write),.do_ecall(e_ecall),.do_mret(e_mret));
  always @(posedge clock)begin
    if(reset)begin
      arch_pc<=RESET_PC;fault_pc<=RESET_PC;fetch_pc<=RESET_PC;pending_pc<=RESET_PC;
      fetch_pending<=0;discard_fetch<=0;d_valid<=0;e_valid<=0;w_valid<=0;
      d_pc<=0;d_inst<=32'h13;d_error<=0;e_pc<=0;e_inst<=32'h13;e_error<=0;
      w_pc<=0;w_inst<=32'h13;w_next_pc<=0;w_value<=0;w_address<=0;w_rd<=0;w_writes<=0;w_load<=0;w_store<=0;w_sent<=0;w_loaded<=0;w_size<=4;w_fault_code<=0;
      csr_mstatus<=32'h1800;csr_mtvec<=0;csr_mscratch<=0;csr_mepc<=0;csr_mcause<=0;csr_mcycle<=0;
      halted<=0;fault<=0;commit_valid<=0;commit_pc<=0;commit_inst<=0;commit_next_pc<=0;
      for(integer j=1;j<16;j=j+1)r[j]<=0;
    end else begin
      csr_mcycle<=csr_mcycle+1;commit_valid<=0;
      if(!halted)begin
        if(d_req_valid&&d_req_ready)w_sent<=1;
        if(w_valid&&w_load&&d_resp_valid&&d_resp_ready)begin
          w_value<=load_result;w_loaded<=1;
          if(d_resp_error!=0)w_fault_code<=5;
        end
        if(w_done)begin
          w_valid<=0;w_sent<=0;w_loaded<=0;
          if(w_fault!=0)begin halted<=1;fault<=w_fault;fault_pc<=w_pc;d_valid<=0;e_valid<=0;end
          else begin
            if(w_writes&&w_rd!=0)r[w_rd]<=w_result;
            arch_pc<=w_next_pc;commit_valid<=1;commit_pc<=w_pc;commit_inst<=w_inst;commit_next_pc<=w_next_pc;
          end
        end
        if(e_transfer)begin
          w_valid<=1;w_pc<=e_pc;w_inst<=e_inst;w_next_pc<=e_next_pc;w_value<=e_store?e_data:e_value;w_rd<=e_inst[10:7];w_writes<=e_writes;
          if(e_load||e_store)w_address<=e_address;
          w_size<=e_size;w_load<=e_load;w_store<=e_store;w_fault_code<=e_fault;w_sent<=0;w_loaded<=0;e_valid<=0;
        end
        if(d_transfer)begin
          e_valid<=1;e_pc<=d_pc;e_inst<=d_inst;e_error<=d_error;d_valid<=0;
        end
        if(i_resp_fire)begin
          fetch_pending<=0;discard_fetch<=0;
          if(!discard_fetch&&!redirect)begin d_valid<=1;d_pc<=pending_pc;d_inst<=i_resp_data;d_error<=i_resp_error!=0?3'd5:3'd0;fetch_pc<=prediction;end
        end
        if(i_req_fire)begin fetch_pending<=1;pending_pc<=i_req_addr;fetch_pc<=i_req_addr+4;discard_fetch<=redirect;end
        if(system_fire)begin
          e_valid<=0;
          if(e_fault!=0)begin halted<=1;fault<=e_fault;fault_pc<=e_pc;d_valid<=0;end
          else begin
            if(e_writes&&e_inst[11:7]!=0)r[e_inst[10:7]]<=e_value;
            if(e_csr_write)case(csr_address)
              12'h300:csr_mstatus<=32'h1800|(e_csr_new&32'h88);
              12'h305:csr_mtvec<={e_csr_new[31:2],1'b0,(e_csr_new[1:0]==1)};
              12'h340:csr_mscratch<=e_csr_new;12'h341:csr_mepc<={e_csr_new[31:2],2'b0};12'h342:csr_mcause<=e_csr_new;
              12'hb00:csr_mcycle<={csr_mcycle[63:32],e_csr_new};12'hb80:csr_mcycle<={e_csr_new,csr_mcycle[31:0]};
              default:begin end
            endcase
            if(e_ecall)begin csr_mepc<=e_pc;csr_mcause<=11;csr_mstatus<=32'h1800|({31'b0,csr_mstatus[3]}<<7);end
            if(e_mret)csr_mstatus<=32'h1880|({31'b0,csr_mstatus[7]}<<3);
            arch_pc<=e_next_pc;commit_valid<=1;commit_pc<=e_pc;commit_inst<=e_inst;commit_next_pc<=e_next_pc;
            if(e_ebreak)halted<=1;
          end
        end
        if(redirect)begin
          fetch_pc<=redirect_pc;d_valid<=0;e_valid<=0;
          if(fetch_pending&&!i_resp_fire)discard_fetch<=1;
        end
      end
    end
  end








endmodule
