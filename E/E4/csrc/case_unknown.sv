module cases(input wire [3:0] x,output reg [2:0] exact_value,z_value,x_value);
  always @* case(x)
    4'b0001:exact_value=0;4'b0010:exact_value=1;4'b0100:exact_value=2;4'b1000:exact_value=3;default:exact_value=7;
  endcase
  always @* casez(x)
    4'b1???:z_value=3;4'b01??:z_value=2;4'b001?:z_value=1;4'b0001:z_value=0;default:z_value=7;
  endcase
  always @* casex(x)
    4'b1???:x_value=3;4'b01??:x_value=2;4'b001?:x_value=1;4'b0001:x_value=0;default:x_value=7;
  endcase
endmodule
module tb;
  reg[3:0] value;wire[2:0] exact_value,z_value,x_value;cases d(value,exact_value,z_value,x_value);
  initial begin
    value=4'b0011;#1;if(exact_value!==7||z_value!==1||x_value!==1)$fatal(1,"multi-hot priority");
    value=4'bx001;#1;if(exact_value!==7||z_value!==7||x_value!==3)$fatal(1,"X masking");
    $display("X001 exact=%d casez=%d casex=%d",exact_value,z_value,x_value);
    value=4'bz001;#1;if(exact_value!==7||z_value!==3||x_value!==3)$fatal(1,"Z masking");
    $display("Z001 exact=%d casez=%d casex=%d",exact_value,z_value,x_value);
    $display("PASS 4-state case/casez/casex distinction");$finish;
  end
endmodule
