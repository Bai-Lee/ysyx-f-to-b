module single_with_memories(
  input wire clock,reset,
  input wire program_write,input wire [7:0] program_address,input wire [31:0] program_data,
  output wire [31:0] pc,output wire halted,output wire [2:0] fault
);
  reg [31:0] imem[0:255];
  reg [31:0] dmem[0:255];
  wire [31:0] inst=imem[pc[9:2]];
  wire [31:0] address,wdata;
  wire [2:0] size;
  wire ren,wen;
  wire [31:0] rdata=dmem[address[9:2]] >> {address[1:0],3'b000};
  wire [3:0] strobe=(size==1?4'b0001:size==2?4'b0011:4'b1111)<<address[1:0];
  wire [31:0] shifted=wdata << {address[1:0],3'b000};
  rv32e_execute cpu(.clock(clock),.reset(reset),.advance(1'b1),.bus_fault(3'b0),.inst(inst),.mem_rdata(rdata),
    .pc(pc),.mem_addr(address),.mem_wdata(wdata),.mem_size(size),.mem_ren(ren),.mem_wen(wen),
    .halted(halted),.fault(fault),.exec_valid(),.exec_ebreak(),.commit_valid(),.commit_pc(),.commit_inst(),.commit_next_pc(),.debug_gpr());
  always @(posedge clock) begin
    if(program_write)imem[program_address]<=program_data;
    if(wen)begin
      if(strobe[0])dmem[address[9:2]][7:0]<=shifted[7:0];
      if(strobe[1])dmem[address[9:2]][15:8]<=shifted[15:8];
      if(strobe[2])dmem[address[9:2]][23:16]<=shifted[23:16];
      if(strobe[3])dmem[address[9:2]][31:24]<=shifted[31:24];
    end
  end
endmodule
