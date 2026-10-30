module minirv_regfile(input wire clock,reset,wen,input wire [3:0] raddr1,raddr2,waddr,
 input wire [31:0] wdata,output wire [31:0] rs1_value,rs2_value,output wire [511:0] debug_gpr);
  reg [31:0] regs[0:15];integer i;
  always @(posedge clock)begin
    if(reset)for(i=0;i<16;i=i+1)regs[i]<=0;
`ifdef FAULT_X0
    else if(wen)regs[waddr]<=wdata;
`else
    else if(wen&&(waddr!=0))regs[waddr]<=wdata;
`endif
  end
`ifdef FAULT_X0
  assign rs1_value=regs[raddr1];assign rs2_value=regs[raddr2];
  assign debug_gpr[31:0]=regs[0];
`else
  assign rs1_value=(raddr1==0)?32'b0:regs[raddr1];assign rs2_value=(raddr2==0)?32'b0:regs[raddr2];
  assign debug_gpr[31:0]=32'b0;
`endif
  for(genvar g=1;g<16;g=g+1)begin:observe
    assign debug_gpr[g*32+:32]=regs[g];
  end
endmodule
