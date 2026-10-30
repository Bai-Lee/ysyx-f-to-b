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
