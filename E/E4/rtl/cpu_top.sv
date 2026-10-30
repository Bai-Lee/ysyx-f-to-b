module cpu_top(input wire clk,reset,input wire [7:0] instruction,switches,buttons,
 output wire [7:0] pc,led,hex_value,output wire [31:0] gpr_state,
 output wire [6:0] hex_high,hex_low,output wire io_write,output wire [2:0] io_device);
  scpu_core #(.ENHANCED(1'b1),.STAGE(2)) cpu(clk,reset,instruction,switches,buttons,
    pc,gpr_state,led,hex_value,hex_high,hex_low,io_write,io_device);
endmodule
