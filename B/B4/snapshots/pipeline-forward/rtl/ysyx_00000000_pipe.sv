/* IF buffer -> decode/operand latch -> execute -> combined memory/retirement.
 * One in-order retirement per cycle. A stalled memory operation holds W;
 * ready/valid backpressure stops younger stages. System operations serialize.
 */
module ysyx_00000000_pipe #(
  parameter integer STAGE=4,
  parameter logic [31:0] RESET_PC=32'h80000000,
  parameter bit FAULT_ADDI=0,FORWARD=0,PREDICT=0,FAULT_FENCE_FLUSH=0,FAULT_RAW=0
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
  reg [31:0] d_pc,d_inst,d_prediction,e_pc,e_inst,e_prediction,e_a,e_b;
  reg [2:0] d_error,e_error;
  reg [31:0] w_pc,w_inst,w_next_pc,w_value,w_address,w_data;
  reg [3:0] w_rd;reg w_writes,w_load,w_store,w_sent;
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
  wire d_serial=serial(d_inst)||d_error!=0;
  wire e_serial=serial(e_inst)||e_error!=0;
  wire w_memory=w_load||w_store;
  wire [31:0] w_raw_data=d_resp_data>>{w_address[1:0],3'b0};
  reg [31:0] w_result;
  always @*begin
    w_result=w_value;
    if(w_load)case(w_inst[14:12])
      0:w_result={{24{w_raw_data[7]}},w_raw_data[7:0]};
      1:w_result={{16{w_raw_data[15]}},w_raw_data[15:0]};
      2:w_result=w_raw_data;
      4:w_result={24'b0,w_raw_data[7:0]};
      5:w_result={16'b0,w_raw_data[15:0]};
      default:w_result=0;
    endcase
  end
  wire w_done=w_valid&&(w_fault_code!=0||!w_memory||(w_sent&&d_resp_valid&&d_resp_ready));
  wire [2:0] w_fault=w_fault_code!=0?w_fault_code:((w_memory&&w_sent&&d_resp_valid&&d_resp_error!=0)?3'd5:3'd0);
  wire w_commit=!reset&&!halted&&w_done&&w_fault==0;
  wire w_failure=!reset&&!halted&&w_done&&w_fault!=0;
  wire system_fire=!reset&&!halted&&e_valid&&e_serial&&!w_valid;
  wire system_commit=system_fire&&e_fault==0;
  wire e_transfer=!reset&&!halted&&e_valid&&!e_serial&&(!w_valid||w_done)&&!w_failure;
  wire redirect=system_commit||(e_transfer&&e_fault==0&&control(e_inst)&&e_next_pc!=e_prediction);
  wire [31:0] redirect_pc=e_next_pc;
  wire e_space=!e_valid||e_transfer;
  wire system_busy=(d_valid&&d_serial)||(e_valid&&e_serial);
  wire control_stall=!PREDICT&&((d_valid&&control(d_inst))||(e_valid&&control(e_inst)));

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
  wire raw_stall=!FAULT_RAW&&d_valid&&(raw_a||raw_b);
  wire load_use=d_valid&&(((e_match_a||e_match_b)&&e_load)||(((w_match_a&&!e_match_a)||(w_match_b&&!e_match_b))&&w_load&&!w_done));
  wire [31:0] register_a=d_rs1[3:0]==0?32'b0:r[d_rs1[3:0]];
  wire [31:0] register_b=d_rs2[3:0]==0?32'b0:r[d_rs2[3:0]];
  wire [31:0] operand_a=FORWARD&&e_match_a?e_value:FORWARD&&w_match_a?w_result:register_a;
  wire [31:0] operand_b=FORWARD&&e_match_b?e_value:FORWARD&&w_match_b?w_result:register_b;
  wire d_transfer=!reset&&!halted&&d_valid&&e_space&&!raw_stall&&!redirect&&!w_failure&&
    !(e_valid&&e_serial)&&(!d_serial||(!e_valid&&!w_valid));

  wire [31:0] fetch_branch_imm={{19{i_resp_data[31]}},i_resp_data[31],i_resp_data[7],i_resp_data[30:25],i_resp_data[11:8],1'b0};
  wire [31:0] fetch_jump_imm={{11{i_resp_data[31]}},i_resp_data[31],i_resp_data[19:12],i_resp_data[20],i_resp_data[30:21],1'b0};
  wire [31:0] prediction=(PREDICT&&i_resp_data[6:0]==7'h6f)?pending_pc+fetch_jump_imm:
    (PREDICT&&i_resp_data[6:0]==7'h63&&i_resp_data[31])?pending_pc+fetch_branch_imm:pending_pc+4;
  wire i_req_fire=i_req_valid&&i_req_ready,i_resp_fire=i_resp_valid&&i_resp_ready;
  assign pc=halted&&fault!=0?fault_pc:arch_pc;
  assign d_req_size=w_size==1?3'd0:w_size==2?3'd1:3'd2;
  assign exec_pc=system_commit?e_pc:w_pc;
  assign exec_mem_addr=w_address;assign exec_mem_size=w_size;assign exec_mem_wdata=w_data;assign exec_mem_rdata=w_raw_data;
  assign debug_state=w_valid&&w_memory&&!w_done?3'd3:raw_stall?3'd4:control_stall?3'd5:system_busy?3'd6:e_valid||w_valid?3'd2:fetch_pending?3'd1:3'd0;
  for(genvar g=0;g<16;g++)begin:expose
    if(g==0)assign debug_gpr[g*32+:32]=0;else assign debug_gpr[g*32+:32]=r[g];
  end
  always @*begin
    i_req_valid=!reset&&!halted&&!fetch_pending&&!system_busy&&!control_stall;
    i_req_addr=fetch_pc;
    i_resp_ready=!reset&&!halted&&fetch_pending&&(!d_valid||d_transfer||discard_fetch||redirect);
    d_req_valid=!reset&&!halted&&w_valid&&w_memory&&!w_sent&&w_fault_code==0;
    d_req_addr=w_address;d_req_write=w_store;d_req_wdata=w_data<<{w_address[1:0],3'b0};
    case(w_size)
      1:d_req_wstrb=4'b0001<<w_address[1:0];
      2:d_req_wstrb=4'b0011<<w_address[1:0];
      default:d_req_wstrb=4'b1111;
    endcase
    if(!w_store)d_req_wstrb=0;
    d_resp_ready=!reset&&!halted&&w_valid&&w_memory&&w_sent;
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
      d_pc<=0;d_inst<=32'h13;d_prediction<=0;d_error<=0;e_pc<=0;e_inst<=32'h13;e_prediction<=0;e_a<=0;e_b<=0;e_error<=0;
      w_pc<=0;w_inst<=32'h13;w_next_pc<=0;w_value<=0;w_address<=0;w_data<=0;w_rd<=0;w_writes<=0;w_load<=0;w_store<=0;w_sent<=0;w_size<=4;w_fault_code<=0;
      csr_mstatus<=32'h1800;csr_mtvec<=0;csr_mscratch<=0;csr_mepc<=0;csr_mcause<=0;csr_mcycle<=0;
      halted<=0;fault<=0;commit_valid<=0;commit_pc<=0;commit_inst<=0;commit_next_pc<=0;
      for(integer j=1;j<16;j=j+1)r[j]<=0;
    end else begin
      csr_mcycle<=csr_mcycle+1;commit_valid<=0;
      if(!halted)begin
        if(d_req_valid&&d_req_ready)w_sent<=1;
        if(w_done)begin
          w_valid<=0;w_sent<=0;
          if(w_fault!=0)begin halted<=1;fault<=w_fault;fault_pc<=w_pc;d_valid<=0;e_valid<=0;end
          else begin
            if(w_writes&&w_rd!=0)r[w_rd]<=w_result;
            arch_pc<=w_next_pc;commit_valid<=1;commit_pc<=w_pc;commit_inst<=w_inst;commit_next_pc<=w_next_pc;
          end
        end
        if(e_transfer)begin
          w_valid<=1;w_pc<=e_pc;w_inst<=e_inst;w_next_pc<=e_next_pc;w_value<=e_value;w_rd<=e_inst[10:7];w_writes<=e_writes;
          w_address<=e_address;w_data<=e_data;w_size<=e_size;w_load<=e_load;w_store<=e_store;w_fault_code<=e_fault;w_sent<=0;e_valid<=0;
        end
        if(d_transfer)begin
          e_valid<=1;e_pc<=d_pc;e_inst<=d_inst;e_prediction<=d_prediction;e_error<=d_error;e_a<=operand_a;e_b<=operand_b;d_valid<=0;
        end
        if(i_req_fire)begin fetch_pending<=1;pending_pc<=fetch_pc;fetch_pc<=fetch_pc+4;discard_fetch<=redirect;end
        if(i_resp_fire)begin
          fetch_pending<=0;discard_fetch<=0;
          if(!discard_fetch&&!redirect)begin d_valid<=1;d_pc<=pending_pc;d_inst<=i_resp_data;d_prediction<=prediction;d_error<=i_resp_error!=0?3'd5:3'd0;fetch_pc<=prediction;end
        end
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
`ifndef SYNTHESIS
  import "DPI-C" function void b_pipeline_tick(input int unsigned events);
  always @(posedge clock)if(!reset&&!halted)begin
    b_pipeline_tick({20'b0,(!d_valid&&!e_valid),system_commit,w_commit,e_transfer,d_transfer,
      (d_transfer&&FORWARD&&(w_match_a||w_match_b)),(d_transfer&&FORWARD&&(e_match_a||e_match_b)),
      redirect,control_stall,(w_valid&&w_memory&&!w_done),load_use,raw_stall});
  end
`endif
endmodule
