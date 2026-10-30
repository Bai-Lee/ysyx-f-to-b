module tb;
  reg[3:0] value;wire[6:0] seg;reg[6:0] expected[0:15];integer i;
  hex_segment d(value,seg);
  initial begin
    expected[0]=7'h3f;expected[1]=7'h06;expected[2]=7'h5b;expected[3]=7'h4f;
    expected[4]=7'h66;expected[5]=7'h6d;expected[6]=7'h7d;expected[7]=7'h07;
    expected[8]=7'h7f;expected[9]=7'h6f;expected[10]=7'h77;expected[11]=7'h7c;
    expected[12]=7'h39;expected[13]=7'h5e;expected[14]=7'h79;expected[15]=7'h71;
    for(i=0;i<16;i=i+1)begin value=i;#1;if((~seg)!==expected[i])$fatal(1,"hex digit %d",i);end
    $display("PASS hex decoder all16 values, active-low g..a");$finish;
  end
endmodule
