/* Bounded arithmetic-sequence proof. One abstract rising edge per SAT step.
 * Three arbitrary legal RV32E ADDI/ADD/SUB/LUI instructions, then EBREAK.
 * A one-cycle ROM can accept a new request while its response is consumed.
 * No data-memory operations, interrupts or asynchronous resets in this proof.
 */
module pipeline_miter #(parameter bit FORWARD=0,FAULT_RAW=0)(input wire clock);
  reg initialized=0;
  always @(posedge clock)initialized<=1;
  wire reset=!initialized;
  (* anyconst *) reg [95:0] program_words;
  function automatic [31:0] rom(input [31:0] address);
    begin case(address)
      0:rom=program_words[31:0];4:rom=program_words[63:32];8:rom=program_words[95:64];
      default:rom=32'h00100073;
    endcase end
  endfunction
  for(genvar k=0;k<3;k++)begin:legal_program
    wire [31:0] instruction=program_words[k*32+:32];
    wire immediate=(instruction[6:0]==7'h13&&instruction[14:12]==0);
    wire arithmetic=(instruction[6:0]==7'h33&&instruction[14:12]==0&&(instruction[31:25]==0||instruction[31:25]==7'h20));
    wire upper=instruction[6:0]==7'h37;
    always @*begin
      assume(immediate||arithmetic||upper);
      assume(instruction[11]==0);
      if(immediate||arithmetic)assume(instruction[19]==0);
      if(arithmetic)assume(instruction[24]==0);
    end
  end
  wire req,ready,response_ready;wire [31:0] address;
  reg pending=0;reg [31:0] held_address=0;
  assign ready=!reset&&(!pending||response_ready);
  always @(posedge clock)begin
    if(reset)begin pending<=0;held_address<=0;end
    else begin
      if(pending&&response_ready)pending<=0;
      if(req&&ready)begin pending<=1;held_address<=address;end
    end
  end
  wire cv,halted,data_request;wire [31:0] cpc,ci,cnpc,pipe_pc;wire [2:0] fault;wire [511:0] pipe_gpr;
  ysyx_00000000_pipe #(.RESET_PC(0),.FORWARD(FORWARD),.FAULT_RAW(FAULT_RAW),.FETCH_PIPELINED(1)) pipe(
    .clock(clock),.reset(reset),.delay_enable(3'b0),.lfsr_seed(32'b0),
    .i_req_valid(req),.i_req_addr(address),.i_req_ready(ready),.i_resp_valid(pending&&!reset),.i_resp_data(rom(held_address)),.i_resp_error(2'b0),.i_resp_ready(response_ready),
    .d_req_valid(data_request),.d_req_ready(1'b1),.d_resp_valid(1'b0),.d_resp_data(32'b0),.d_resp_error(2'b0),
    .pc(pipe_pc),.halted(halted),.fault(fault),.commit_valid(cv),.commit_pc(cpc),.commit_inst(ci),.commit_next_pc(cnpc),.debug_gpr(pipe_gpr));
  wire [31:0] gold_pc;wire [511:0] gold_gpr;
  ysyx_00000000_execute #(.RESET_PC(0)) gold(
    .clock(clock),.reset(reset),.advance(cv&&!reset),.bus_fault(3'b0),.inst(rom(gold_pc)),.mem_rdata(32'b0),.pc(gold_pc),.debug_gpr(gold_gpr));
  reg compare_valid=0;reg [511:0] saved_gpr;reg [31:0] saved_pc;
  reg [5:0] cycle=0,retirements=0;
  always @(posedge clock)begin
    if(reset)begin compare_valid<=0;cycle<=0;retirements<=0;end
    else begin
      cycle<=cycle+1;
      assert(fault==0);assert(!data_request);
      if(req)assert(address<=12&&address[1:0]==0);
      if(compare_valid)begin assert(saved_gpr==gold_gpr);assert(saved_pc==gold_pc);end
      if(cv)begin assert(cpc==gold_pc);assert(ci==rom(gold_pc));saved_gpr<=pipe_gpr;saved_pc<=cnpc;retirements<=retirements+1;end
      compare_valid<=cv;
      // This prevents a vacuous safety pass by a deadlocked implementation.
      if(cycle==22)begin assert(halted);assert(retirements==4);end
    end
  end
endmodule
