// Independently authored implementation of the F5/F6 sISA (not RISC-V).
// 8-bit PC and data; four writable GPRs including R0; synchronous high reset.
module instruction_rom_mux(input wire [7:0] addr,
                           input wire [2047:0] contents,
                           output wire [7:0] instruction);
  assign instruction = contents[8*addr +: 8];
endmodule

module gpr4x8(input wire clk, reset, wen,
             input wire [1:0] waddr, raddr_a, raddr_b,
             input wire [7:0] wdata,
             output wire [7:0] rdata_a, rdata_b,
             output wire [31:0] state);
  reg [7:0] regs [0:3];
  integer i;
  always @(posedge clk) begin
    if (reset) begin
      for (i=0;i<4;i=i+1) regs[i] <= 8'h00;
    end else if (wen) begin
`ifdef FAULT_R0_CONSTANT
      if (waddr != 0) regs[waddr] <= wdata;
`else
      regs[waddr] <= wdata;
`endif
    end
  end
  assign rdata_a=regs[raddr_a];
  assign rdata_b=regs[raddr_b];
  assign state={regs[3],regs[2],regs[1],regs[0]};
endmodule

module hex7(input wire [3:0] digit, output reg [6:0] segments);
  // bit order g f e d c b a; active high, no decimal point.
  always @* begin
    case(digit)
      4'h0:segments=7'h3f;4'h1:segments=7'h06;
      4'h2:segments=7'h5b;4'h3:segments=7'h4f;
      4'h4:segments=7'h66;4'h5:segments=7'h6d;
      4'h6:segments=7'h7d;4'h7:segments=7'h07;
      4'h8:segments=7'h7f;4'h9:segments=7'h6f;
      4'ha:segments=7'h77;4'hb:segments=7'h7c;
      4'hc:segments=7'h39;4'hd:segments=7'h5e;
      4'he:segments=7'h79;4'hf:segments=7'h71;
      default:segments=7'h00;
    endcase
  end
endmodule

module scpu_core #(parameter ENHANCED=0, parameter STAGE=2)
 (input wire clk, reset,
  input wire [7:0] instruction, switches, buttons,
  output reg [7:0] pc,
  output wire [31:0] gpr_state,
  output wire [7:0] led, hex_value,
  output wire [6:0] hex_high, hex_low,
  output wire io_write,
  output wire [2:0] io_device);
  wire [1:0] opcode=instruction[7:6];
  wire [1:0] rd=instruction[5:4];
  wire io_out=ENHANCED && opcode==2'b01 && instruction[3];
  wire io_in=ENHANCED && opcode==2'b01 && !instruction[3];
  wire [1:0] read_a=io_out ? rd : instruction[3:2];
  wire [7:0] a,b;
  reg write_enable;
  reg [7:0] write_data,next_pc;
  reg [7:0] led_storage,hex_storage;
  wire [2:0] immediate_shift={instruction[3:2],1'b0};
  wire [7:0] reference_r0=gpr_state[7:0];
  wire [7:0] displacement={{4{instruction[5]}},instruction[5:2]};
  gpr4x8 rf(clk,reset,write_enable,rd,read_a,instruction[1:0],write_data,a,b,gpr_state);
  always @* begin
    write_enable=1'b0;write_data=8'h00;next_pc=pc+8'd1;
    case(opcode)
      2'b10:begin
        write_enable=1'b1;
        if(ENHANCED) begin
`ifdef FAULT_LI_SHIFT
          write_data={6'b0,instruction[1:0]} << instruction[3:2];
`else
          write_data={6'b0,instruction[1:0]} << immediate_shift;
`endif
        end else write_data={4'b0,instruction[3:0]};
      end
      2'b00:if(STAGE>=1) begin write_enable=1'b1;write_data=a+b;end
      2'b11:if(STAGE>=2 && reference_r0!=b) begin
        if(ENHANCED) begin
`ifdef FAULT_BRANCH_SIGN
          next_pc=pc+{4'b0,instruction[5:2]};
`else
          next_pc=pc+displacement;
`endif
        end else next_pc={4'b0,instruction[5:2]};
      end
      2'b01:if(io_in) begin
        write_enable=1'b1;
        case(instruction[2:0])
          3'd0:write_data=switches;
          3'd1:write_data=buttons;
          default:write_data=8'h00; // unconnected input device
        endcase
      end
    endcase
  end
  always @(posedge clk) begin
    if(reset) begin pc<=0;led_storage<=0;hex_storage<=0;end
    else begin
      pc<=next_pc;
      if(io_out) begin
        case(instruction[2:0])
          3'd0:led_storage<=a;
          3'd1:hex_storage<=a;
          default:begin end // unconnected output device
        endcase
      end
    end
  end
`ifdef FAULT_LED_LIVE
  assign led=gpr_state[23:16];
`else
  assign led=led_storage;
`endif
  assign hex_value=hex_storage;
  assign io_write=io_out && !reset;
  assign io_device=instruction[2:0];
  hex7 high_digit(hex_storage[7:4],hex_high);
  hex7 low_digit(hex_storage[3:0],hex_low);
endmodule

module scpu_system #(parameter ENHANCED=0,parameter STAGE=2,
                     parameter [2047:0] IMAGE=2048'h0)
 (input wire clk,reset,input wire [7:0] switches,buttons,
  output wire [7:0] pc,instruction,
  output wire [31:0] gpr_state,
  output wire [7:0] led,hex_value,
  output wire [6:0] hex_high,hex_low);
  wire io_write;wire [2:0] io_device;
  instruction_rom_mux rom(pc,IMAGE,instruction);
  scpu_core #(.ENHANCED(ENHANCED),.STAGE(STAGE)) core(
    clk,reset,instruction,switches,buttons,pc,gpr_state,led,hex_value,
    hex_high,hex_low,io_write,io_device);
endmodule
