module alu_naive(input [3:0] a,b,input [2:0] op,output reg[3:0] y);
always @*case(op)
0:y=a+b;
1:y=a-b;
2:y={3'b0,a<b};
3:y={3'b0,$signed(a)<$signed(b)};
4:y=a<<b[1:0];
5:y=a>>b[1:0];
6:y=$signed(a)>>>b[1:0];
7:y=a^b;
endcase
endmodule
module alu_shared(input [3:0] a,b,input [2:0] op,output reg[3:0] y);
wire subtract=(op!=0);
wire [4:0] sum={1'b0,a}+{1'b0,(b^{4{subtract}})}+{4'b0,subtract};
wire signed_less=(a[3]!=b[3])?a[3]:sum[3];
always @*case(op)
0,1:y=sum[3:0];
2:y={3'b0,!sum[4]};
3:y={3'b0,signed_less};
4:y=a<<b[1:0];
5:y=a>>b[1:0];
6:y=$signed(a)>>>b[1:0];
7:y=a^b;
endcase
endmodule
