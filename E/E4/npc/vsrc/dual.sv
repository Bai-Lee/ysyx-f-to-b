`timescale 1ns/1ns
module dual(input wire a,b,output wire f);
`ifdef FAULT_XOR
  assign f=a|b;
`else
  assign f=a^b;
`endif
endmodule
