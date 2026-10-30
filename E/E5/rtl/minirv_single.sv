module minirv_single #(parameter [31:0] RESET_PC=32'b0)
 (input wire clock,reset,input wire [31:0] inst,mem_rdata,
 output reg [31:0] pc,output wire [31:0] mem_addr,mem_wdata,
 output wire [3:0] mem_wmask,output wire [1:0] mem_size,
 output wire mem_ren,mem_wen,exec_valid,exec_ebreak,
 output reg halted,output reg [2:0] fault,
 output reg commit_valid,output reg [31:0] commit_pc,commit_inst,commit_next_pc,
 output wire [511:0] debug_gpr);
  wire [3:0] rs1,rs2,rd;wire [31:0] a,b,result,next_pc;
  wire write_reg,load,store;wire [2:0] decode_fault;
  minirv_decode idu(inst,pc,a,b,mem_rdata,rs1,rs2,rd,write_reg,load,store,exec_ebreak,
    result,next_pc,mem_addr,mem_wdata,mem_wmask,mem_size,decode_fault);
  assign exec_valid=!reset&&!halted&&(decode_fault==0);
  minirv_regfile rf(clock,reset,exec_valid&&write_reg,rs1,rs2,rd,result,a,b,debug_gpr);
  assign mem_ren=exec_valid&&load;assign mem_wen=exec_valid&&store;
  always @(posedge clock)begin
    if(reset)begin pc<=RESET_PC;halted<=0;fault<=0;commit_valid<=0;commit_pc<=0;commit_inst<=0;commit_next_pc<=0;end
    else begin
      commit_valid<=0;
      if(!halted)begin
        if(decode_fault!=0)begin fault<=decode_fault;halted<=1;end
        else begin
          commit_valid<=1;commit_pc<=pc;commit_inst<=inst;commit_next_pc<=next_pc;pc<=next_pc;
          if(exec_ebreak)halted<=1;
        end
      end
    end
  end
endmodule
