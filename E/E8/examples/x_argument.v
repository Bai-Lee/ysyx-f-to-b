module x_argument;
 integer word;
 initial begin
  $pmem_init;
  word=$pmem_read(32'hxxxx0000,0);
  if($pmem_status!==-1)$fatal(2,"VPI accepted X input as an integer");
  $display("EXPECTED_X_ARGUMENT_REJECTION");
  $finish;
 end
endmodule
