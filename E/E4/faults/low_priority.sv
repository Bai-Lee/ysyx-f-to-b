module full_adder(input wire a,b,ci, output wire s,co);
  assign s=a^b^ci;
  assign co=(a&b)|(a&ci)|(b&ci);
endmodule
module ripple #(parameter integer N=4)(input wire [N-1:0] a,b,input wire ci,
 output wire [N-1:0] s,output wire co,overflow);
  wire [N:0] c; assign c[0]=ci;
  for(genvar i=0;i<N;i=i+1) begin:fa
    full_adder u(a[i],b[i],c[i],s[i],c[i+1]);
  end
  assign co=c[N]; assign overflow=c[N]^c[N-1];
endmodule
module hex_segment(input wire [3:0] value,output reg [6:0] seg);
  // Active low, bits g..a, matching NJU HEX[6:0].
  always @* case(value)
    0:seg=7'h40;1:seg=7'h79;2:seg=7'h24;3:seg=7'h30;
    4:seg=7'h19;5:seg=7'h12;6:seg=7'h02;7:seg=7'h78;
    8:seg=7'h00;9:seg=7'h10;10:seg=7'h08;11:seg=7'h03;
    12:seg=7'h46;13:seg=7'h21;14:seg=7'h06;15:seg=7'h0e;
    default:seg=7'h7f;
  endcase
endmodule
module priority83(input wire [7:0] x,input wire en,output wire [2:0] code,output wire valid);
`ifdef FAULT_PRIORITY
  assign code=x[0]?3'd0:x[1]?3'd1:x[2]?3'd2:x[3]?3'd3:x[4]?3'd4:x[5]?3'd5:x[6]?3'd6:3'd7;
`else
  assign code=!en?3'd0:x[0]?3'd0:x[1]?3'd1:x[2]?3'd2:x[3]?3'd3:x[4]?3'd4:x[5]?3'd5:x[6]?3'd6:x[7]?3'd7:3'd0;
`endif
  assign valid=en & (|x);
endmodule
module barrel #(parameter integer N=8, parameter integer LOGN=3)
 (input wire [N-1:0] data,input wire [LOGN-1:0] amount,input wire left,arithmetic,
 output wire [N-1:0] value);
  wire [N-1:0] stage[0:LOGN];assign stage[0]=data;
  for(genvar i=0;i<LOGN;i=i+1)begin:muxstage
    // Isolate the signed shift before the unsigned mux context can coerce it.
    wire [N-1:0] arithmetic_right=$signed(stage[i]) >>> (1<<i);
    wire [N-1:0] shifted_right=arithmetic ? arithmetic_right : (stage[i] >> (1<<i));
    assign stage[i+1]=!amount[i]?stage[i]:left?(stage[i]<<(1<<i)):shifted_right;
  end
  assign value=stage[LOGN];
endmodule
module alu4(input wire [3:0] a,b,input wire [2:0] op,output wire [3:0] value,
 output wire carry,overflow,zero,less_s,less_u);
  wire sub=(op==1)||(op==6)||(op==7);
  wire [3:0] adjusted=b^{4{sub}};
  wire [3:0] sum;wire c,ov;
  ripple #(4) adder(a,adjusted,sub,sum,c,ov);
  assign less_s=sum[3]^ov;assign less_u=~c;
  assign value=(op==0||op==1)?sum:(op==2)?~a:(op==3)?a&b:(op==4)?a|b:
               (op==5)?a^b:(op==6)?{3'b0,less_s}:{3'b0,a==b};
  assign carry=(op<=1)?c:1'b0;
`ifdef FAULT_OVERFLOW
  assign overflow=1'b0;
`else
  assign overflow=(op<=1)?ov:1'b0;
`endif
  assign zero=~(|value);
endmodule
module comb(input wire [7:0] a,b,x,input wire en,cin,input wire [2:0] op,shamt,
 input wire left,arithmetic,input wire [31:0] data32,input wire [4:0] shamt32,
 output wire [3:0] dec24,output wire [7:0] dec38,
 output wire [1:0] enc42,output wire enc42_valid,output wire [2:0] prio,
 output wire prio_valid,output wire [6:0] seg,
 output wire [3:0] sum4,alu,output wire carry4,ov4,carry8,ov8,
 output wire [7:0] sum8,shift8,output wire [31:0] shift32,
 output wire alu_c,alu_o,alu_z,less_s,less_u,fa_s,fa_c);
  assign dec24=en?(4'b1<<x[1:0]):4'b0;
  assign dec38=en?(8'b1<<x[2:0]):8'b0;
  wire [3:0] e=x[3:0];
  assign enc42_valid=en && ((e==1)||(e==2)||(e==4)||(e==8));
  assign enc42=!enc42_valid?2'b0:e[3]?2'd3:e[2]?2'd2:e[1]?2'd1:2'd0;
  priority83 p(x,en,prio,prio_valid);hex_segment h({1'b0,prio},seg);
  full_adder f(a[0],b[0],cin,fa_s,fa_c);
  ripple #(4) r4(a[3:0],b[3:0],cin,sum4,carry4,ov4);
  ripple #(8) r8(a,b,cin,sum8,carry8,ov8);
  alu4 u(a[3:0],b[3:0],op,alu,alu_c,alu_o,alu_z,less_s,less_u);
  barrel b8(a,shamt,left,arithmetic,shift8);
  barrel #(32,5) b32(data32,shamt32,left,arithmetic,shift32);
endmodule
