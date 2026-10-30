module tb;
reg clk=0,reset=1,wen=0;reg[1:0]wa=0,ra=0,rb=0;reg[7:0]wd=0;wire[7:0]a,b;wire[31:0]state;
reg[7:0]model[0:3];integer x,y,z,k,checks=0;
gpr4x8 dut(clk,reset,wen,wa,ra,rb,wd,a,b,state);
initial begin #1;clk=1;#1;clk=0;reset=0;for(k=0;k<4;k=k+1)model[k]=0;
for(x=0;x<4;x=x+1)for(y=0;y<256;y=y+1)begin
wa=x;wd=y;wen=1;#1;clk=1;#1;clk=0;model[x]=y;
for(z=0;z<16;z=z+1)begin ra=z/4;rb=z%4;#1;if(a!==model[ra]||b!==model[rb])$fatal(1,"GPR data");checks=checks+1;end
wen=0;wd=~y;#1;clk=1;#1;clk=0;
if(state!=={model[3],model[2],model[1],model[0]})$fatal(1,"GPR hold");
end
reset=1;#1;clk=1;#1;if(state!==0)$fatal(1,"GPR reset");
$display("PASS GPR read_checks=%0d writes=1024 hold_checks=1024",checks);$finish;end endmodule