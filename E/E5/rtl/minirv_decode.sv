module minirv_decode(input wire [31:0] inst,pc,rs1_value,rs2_value,load_word,
 output wire [3:0] raddr1,raddr2,waddr,output wire wen,is_load,is_store,is_ebreak,
 output wire [31:0] result,next_pc,mem_addr,mem_wdata,output wire [3:0] mem_wmask,
 output wire [1:0] mem_size,output wire [2:0] fault_code);
  wire [6:0] opcode=inst[6:0];wire [2:0] f3=inst[14:12];
  wire add=(opcode==7'h33)&&(f3==0)&&(inst[31:25]==0);
  wire addi=(opcode==7'h13)&&(f3==0);
  wire lui=(opcode==7'h37);
  wire jalr=(opcode==7'h67)&&(f3==0);
  wire lw=(opcode==7'h03)&&(f3==2),lbu=(opcode==7'h03)&&(f3==4);
  wire sw=(opcode==7'h23)&&(f3==2),sb=(opcode==7'h23)&&(f3==0);
  assign is_ebreak=(inst==32'h00100073);
  assign raddr1=inst[18:15];assign raddr2=inst[23:20];assign waddr=inst[10:7];
`ifdef FAULT_SIGN_EXT
  wire [31:0] imm_i={20'b0,inst[31:20]};
`else
  wire [31:0] imm_i={{20{inst[31]}},inst[31:20]};
`endif
  wire [31:0] imm_s={{20{inst[31]}},inst[31:25],inst[11:7]};
  assign is_load=lw|lbu;assign is_store=sw|sb;assign wen=add|addi|lui|jalr|is_load;
  assign mem_addr=rs1_value+(is_store?imm_s:imm_i);
`ifdef FAULT_JALR_LOW_BIT
  assign next_pc=jalr?(rs1_value+imm_i):pc+32'd4;
`else
  assign next_pc=jalr?((rs1_value+imm_i)&32'hfffffffe):pc+32'd4;
`endif
  wire [4:0] shift={mem_addr[1:0],3'b0};
  wire [7:0] selected_byte=load_word[shift+:8];
`ifdef FAULT_LBU_SIGN
  wire [31:0] byte_value={{24{selected_byte[7]}},selected_byte};
`else
  wire [31:0] byte_value={24'b0,selected_byte};
`endif
  assign result=add?rs1_value+rs2_value:addi?rs1_value+imm_i:lui?{inst[31:12],12'b0}:
    jalr?pc+32'd4:lw?load_word:lbu?byte_value:32'b0;
  assign mem_wdata=sb?({24'b0,rs2_value[7:0]}<<shift):rs2_value;
`ifdef FAULT_SB_MASK
  assign mem_wmask=4'hf;
`else
  assign mem_wmask=sb?(4'b1<<mem_addr[1:0]):4'hf;
`endif
  assign mem_size=(sb|lbu)?2'd0:2'd2;
  wire bad_register=(wen&&inst[11])|((add|addi|jalr|is_load|is_store)&&inst[19])|((add|is_store)&&inst[24]);
  wire bad_encoding=!(add|addi|lui|jalr|is_load|is_store|is_ebreak)|bad_register;
  assign fault_code=bad_encoding?3'd1:((|pc[1:0])||(jalr&&(|next_pc[1:0])))?3'd2:
                    ((lw|sw)&&(|mem_addr[1:0]))?3'd3:3'd0;
endmodule
