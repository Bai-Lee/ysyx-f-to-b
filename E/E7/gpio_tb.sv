module gpio_tb;
 reg clk=0,reset=1;always #5 clk=~clk;
 reg[31:0]addr=0,data=0;reg sel=0,enable=0,write=0;reg[3:0]strobe=0;
 reg[15:0]switches=0;wire ready,error;wire[31:0]rd;wire[15:0]led;wire[7:0]s[0:7];
 mygpio_top_apb dut(clk,reset,addr,sel,enable,3'b0,write,data,strobe,ready,rd,error,led,switches,s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7]);
 task cycle;begin @(posedge clk);#1;end endtask
 task put(input[31:0]a,v,input[3:0]mask,input bit bad=0);
  reg[15:0]before_led;
  begin
   @(negedge clk);before_led=led;addr=a;data=v;strobe=mask;sel=1;enable=0;write=1;
   cycle();if(led!==before_led)$fatal(1,"GPIO modified during APB setup");
   @(negedge clk);enable=1;#1;if(!ready||error!==bad)$fatal(1,"GPIO access completion/error mismatch");cycle();
   @(negedge clk);sel=0;enable=0;write=0;
  end
 endtask
 task get(input[31:0]a,expected,input bit bad);
  begin @(negedge clk);addr=a;sel=1;enable=0;write=0;strobe=0;cycle();@(negedge clk);enable=1;#1;
   if(!ready||error!==bad||rd!==expected)$fatal(1,"read mismatch addr=%h actual=%h expected=%h error=%b",a,rd,expected,error);
   cycle();@(negedge clk);sel=0;enable=0;
  end
 endtask
 integer m,i;reg[15:0]expected;reg[31:0]word;reg[7:0]table_seg[0:15];
 initial begin
  table_seg[0]=8'h03;table_seg[1]=8'h9f;table_seg[2]=8'h25;table_seg[3]=8'h0d;
  table_seg[4]=8'h99;table_seg[5]=8'h49;table_seg[6]=8'h41;table_seg[7]=8'h1f;
  table_seg[8]=8'h01;table_seg[9]=8'h09;table_seg[10]=8'h11;table_seg[11]=8'hc1;
  table_seg[12]=8'h63;table_seg[13]=8'h85;table_seg[14]=8'h61;table_seg[15]=8'h71;
  cycle();cycle();if(led!==0)$fatal(1,"reset failure");reset=0;
  for(m=0;m<16;m=m+1)begin
   put(0,0,15);put(0,32'hf6e5b2a1,m[3:0]);expected={m[1]?8'hb2:8'h00,m[0]?8'ha1:8'h00};
   get(0,{16'b0,expected},0);
  end
  switches=16'ha55a;get(4,32'ha55a,0);
  put(4,32'hffffffff,15,1);get(4,32'ha55a,0);put(12,32'hffffffff,15,1);
  get(12,0,1);
  for(m=0;m<16;m=m+1)begin
   word={8{m[3:0]}};put(8,word,15);get(8,word,0);
   for(i=0;i<8;i=i+1)if(s[i]!==table_seg[m])$fatal(1,"segment mismatch");
  end
  put(8,32'h01234567,15);put(8,32'h89abcdef,4'b0101);get(8,32'h01ab45ef,0);
  reset=1;cycle();if(led!==0||s[0]!==8'h03)$fatal(1,"second reset failure");
  $display("GPIO_APB_PASS all16_strobes all16_digits setup_access readonly reserved reset");$finish;
 end
 initial begin #20000;$fatal(1,"timeout");end
endmodule
