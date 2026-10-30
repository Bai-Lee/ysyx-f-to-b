module dpi_example(input int a,b,output int result);
  import "DPI-C" function int add(input int a,input int b);
  initial $display("%x + %x = %x",1,2,add(1,2));
  always_comb result=add(a,b);
endmodule
