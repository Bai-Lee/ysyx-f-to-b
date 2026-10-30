module tb;
reg[7:0] address;wire[7:0] instruction;reg[7:0] expected[0:255];integer i;
program_rom d(address,instruction);
initial begin
$readmemh("/workspace/projects/ysyx_f_to_b/E/E4/data/f6_output.hex",expected);
for(i=0;i<256;i=i+1)begin address=i;#1;if(instruction!==expected[i])$fatal(1,"ROM byte %d",i);end
$display("PASS RTL ROM256 bytes match frozen program");$finish;
end endmodule
