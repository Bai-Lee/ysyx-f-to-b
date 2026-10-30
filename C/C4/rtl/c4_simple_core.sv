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
