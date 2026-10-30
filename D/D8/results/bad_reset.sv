module rv32e_core #(
  parameter logic [31:0] RESET_PC=32'h80000000,
  parameter bit FAULT_ADDI=0
)(input logic clock,reset,input logic [31:0] inst,mem_rdata,
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
  for(genvar g=0;g<16;g++)begin: expose
    assign debug_gpr[g*32+:32]=(g==0)?32'b0:r[g];
  end
  always_comb begin
    value=0;next_pc=pc+32'd4;mem_addr=0;mem_wdata=b;mem_size=3'd4;
    writes=0;loads=0;stores=0;uses_a=0;uses_b=0;legal=1;take=0;exec_ebreak=0;
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
      7'h73:begin legal=inst==32'h00100073;exec_ebreak=legal;end
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
      for(integer j=0;j<16;j=j+1)r[j]<=1;
    end else begin
      commit_valid<=0;
      if(!halted)begin
        if(decode_fault!=0)begin halted<=1;fault<=decode_fault;end
        else begin
          if(writes&&rd!=0)r[rd[3:0]]<=value;
          pc<=next_pc;commit_valid<=1;commit_pc<=pc;commit_inst<=inst;commit_next_pc<=next_pc;
          if(exec_ebreak)halted<=1;
        end
      end
    end
  end
endmodule
