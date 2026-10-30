`timescale 1ns/1ps
module simple_cpu_tb;
  parameter integer STAGE=1;
  parameter bit BAD=0;
  reg clock=0,reset=1;
  always #5 clock=~clock;
  wire iv,ir,drdy,dv,dw,drr;
  wire [31:0] ia,da,wd;wire [3:0] ws;
  reg rv=0;reg [31:0] rd=0;
  wire dvresp;wire [31:0] ddata;
  reg dvreg=0;reg [31:0] ddreg=0;
  reg [31:0] word=0;
  wire [31:0] pc,cp,ci,cn;wire halted,cv;wire [2:0] fault;
  wire [511:0] regs;
  c4_simple_core #(.STAGE(STAGE),.FAULT_ADDI(BAD)) dut(
    .clock(clock),.reset(reset),.delay_enable(3'b000),.lfsr_seed(32'd1),
    .i_req_valid(iv),.i_req_addr(ia),.i_req_ready(1'b1),.i_resp_valid(rv),.i_resp_data(rd),.i_resp_error(2'b00),.i_resp_ready(ir),
    .d_req_valid(dv),.d_req_addr(da),.d_req_write(dw),.d_req_wdata(wd),.d_req_wstrb(ws),.d_req_ready(1'b1),
    .d_resp_valid(dvresp),.d_resp_data(ddata),.d_resp_error(2'b00),.d_resp_ready(drr),
    .pc(pc),.halted(halted),.fault(fault),.commit_valid(cv),.commit_pc(cp),.commit_inst(ci),.commit_next_pc(cn),.debug_gpr(regs));
  assign dvresp=STAGE==1?dv:dvreg;
  assign ddata=STAGE==1?word:ddreg;
  function automatic [31:0] rom(input [31:0] address);
    case(address)
      32'h80000000:rom=32'h800102b7;
      32'h80000004:rom=32'h00100093;
      32'h80000008:rom=32'h0012a023;
      32'h8000000c:rom=32'h00028103;
      32'h80000010:rom=32'h00000513;
      32'h80000014:rom=32'h00100073;
      default:rom=32'hffffffff;
    endcase
  endfunction
  integer k;
  always @(posedge clock) begin
    if(reset)begin rv<=0;rd<=0;dvreg<=0;ddreg<=0;end
    else begin
      rv<=iv;if(iv)rd<=rom(ia);
      dvreg<=dv;if(dv)ddreg<=word;
      if(dv&&dw)begin
        if(da!==32'h80010000)$fatal(1,"STORE_ADDRESS");
        for(k=0;k<4;k=k+1)if(ws[k])word[k*8+:8]<=wd[k*8+:8];
      end
    end
  end
  integer cycle=0,commits=0,prior_cycle=0,wanted;
  reg [511:0] prior_regs=0;reg [31:0] prior_pc=32'h80000000;
  always @(posedge clock) begin
    if(reset)begin cycle=0;commits=0;prior_cycle=0;prior_regs=0;prior_pc=32'h80000000;end
    else begin
      cycle=cycle+1;#1;
      if(fault)$fatal(1,"UNEXPECTED_FAULT");
      if(cv)begin
        commits=commits+1;wanted=(STAGE==2&&(commits==3||commits==4))?3:2;
        if(cycle-prior_cycle!=wanted)$fatal(1,"CYCLE_CONTRACT stage=%0d insn=%0d delta=%0d wanted=%0d",STAGE,commits,cycle-prior_cycle,wanted);
        if(cp!==32'h80000000+4*(commits-1)||cn!==cp+4)$fatal(1,"PC_CONTRACT");
        if(commits>=2&&regs[63:32]!==32'd1)$fatal(1,"REGISTER_MISMATCH x1");
        if(commits>=4&&regs[95:64]!==32'd1)$fatal(1,"REGISTER_MISMATCH x2");
        if(regs[31:0]!==0)$fatal(1,"ZERO_REGISTER");
        $display("RETIRE stage=%0d ordinal=%0d cycle=%0d pc=%h inst=%h",STAGE,commits,cycle,cp,ci);
        prior_cycle=cycle;prior_regs=regs;prior_pc=pc;
      end else if(regs!==prior_regs||pc!==prior_pc)$fatal(1,"STATE_MOVED_WHILE_WAITING");
      if(halted)begin
        if(commits!=6||word!==32'd1)$fatal(1,"FINAL_STATE");
        $display("SIMPLE_CPU_PASS stage=%0d cycles=%0d",STAGE,cycle);$finish;
      end
      if(cycle>100)$fatal(1,"TIMEOUT_NOT_PASS");
    end
  end
  reg [4095:0] path;
  initial begin
    if($value$plusargs("vcd=%s",path))begin $dumpfile(path);$dumpvars(0,simple_cpu_tb);end
    repeat(2)@(posedge clock);@(negedge clock)reset=0;
  end
endmodule
