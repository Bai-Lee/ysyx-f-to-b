module lint_bad(input wire [7:0] a,input wire en,output reg [3:0] q);always @* if(en)q=a;endmodule
