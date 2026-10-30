module priority4(input wire[3:0] in,output wire valid,output reg[1:0] code);
assign valid=|in;
always @* begin
  if(in[3])code=3;else if(in[2])code=2;else if(in[1])code=1;else code=0;
end
endmodule
module priority16(input wire[15:0] in,output wire valid,output wire[3:0] code);
wire[3:0] group_valid;wire[1:0] c0,c1,c2,c3,group_code;wire[1:0] local_code;
priority4 p0(in[3:0],group_valid[0],c0),p1(in[7:4],group_valid[1],c1),
          p2(in[11:8],group_valid[2],c2),p3(in[15:12],group_valid[3],c3);
priority4 groups(group_valid,valid,group_code);
assign local_code=group_code==3?c3:group_code==2?c2:group_code==1?c1:c0;
assign code={group_code,local_code};
endmodule
module count_ends16(input wire[15:0] in,output wire[4:0] clz,ctz,clo,cto);
wire[15:0] reverse,inv_reverse;wire v0,v1,v2,v3;wire[3:0] i0,i1,i2,i3;
genvar n;generate for(n=0;n<16;n=n+1)begin assign reverse[n]=in[15-n];end endgenerate
assign inv_reverse=~reverse;
priority16 a(in,v0,i0),b(reverse,v1,i1),c(~in,v2,i2),d(inv_reverse,v3,i3);
assign clz=v0?5'd15-{1'b0,i0}:5'd16;
assign ctz=v1?5'd15-{1'b0,i1}:5'd16;
assign clo=v2?5'd15-{1'b0,i2}:5'd16;
assign cto=v3?5'd15-{1'b0,i3}:5'd16;
endmodule
module half_adder(input wire a,b,output wire sum,carry);
assign sum=a^b;assign carry=a&b;
endmodule
module fa_two_halves(input wire a,b,cin,output wire sum,carry);
wire p,g,c;half_adder first(a,b,p,g);half_adder second(p,cin,sum,c);assign carry=g|c;
endmodule
