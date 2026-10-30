module b_adder32(input wire clock,input wire [31:0] a,b,output reg [31:0] sum);
  reg [31:0] a_q,b_q;
  always @(posedge clock)begin a_q<=a;b_q<=b;sum<=a_q+b_q;end
endmodule
module b_regfile16(input wire clock,input wire we,input wire [3:0] wa,ra,rb,input wire [31:0] wd,
                  output reg [31:0] a,b);
  reg we_q;reg [3:0] wa_q,ra_q,rb_q;reg [31:0] wd_q;
  reg [31:0] regs[1:15];
  always @(posedge clock)begin
    we_q<=we;wa_q<=wa;ra_q<=ra;rb_q<=rb;wd_q<=wd;
    if(we_q&&wa_q!=0)regs[wa_q]<=wd_q;
    a<=ra_q==0?32'b0:regs[ra_q];b<=rb_q==0?32'b0:regs[rb_q];
  end
endmodule
