module shift_register(input wire clk,reset,enable,input wire [2:0] mode,
 input wire [7:0] data,input wire serial_in,output reg [7:0] q);
  wire [7:0] next_value=(mode==0)?8'b0:(mode==1)?data:(mode==2)?{1'b0,q[7:1]}:
    (mode==3)?{q[6:0],1'b0}:(mode==4)?{q[7],q[7:1]}:(mode==5)?{serial_in,q[7:1]}:
    (mode==6)?{q[0],q[7:1]}:{q[6:0],q[7]};
  always @(posedge clk) if(reset)q<=0;else if(enable)q<=next_value;
endmodule
module lfsr8(input wire clk,reset,enable,load,input wire [7:0] seed,output reg [7:0] q);
`ifdef FAULT_LFSR
  wire feedback=q[4]^q[3]^q[1]^q[0];
`else
  wire feedback=q[4]^q[3]^q[2]^q[0];
`endif
  always @(posedge clk)
    if(reset)q<=8'd1;
    else if(load)q<=seed;
    else if(enable)q<=(q==0)?8'd1:{feedback,q[7:1]};
endmodule
module run_detector(input wire clk,reset_n,enable,w,output wire z,output reg [3:0] state,
 output reg [8:0] onehot,output wire z_onehot,output wire z_mealy);
  wire [3:0] next_state=w?((state>=5&&state<8)?state+4'd1:state==8?4'd8:4'd5):
                             ((state>=1&&state<4)?state+4'd1:state==4?4'd4:4'd1);
  wire [8:0] oh_next=w?{onehot[7]|onehot[8],onehot[6],onehot[5],|onehot[4:0],5'b0}:
                          {4'b0,onehot[3]|onehot[4],onehot[2],onehot[1],onehot[0]|(|onehot[8:5]),1'b0};
  reg last;reg [1:0] count3;
  assign z=(state==4)||(state==8);assign z_onehot=onehot[4]|onehot[8];
  assign z_mealy=(count3==3)&&(last==w)&&reset_n;
  always @(posedge clk) begin
    if(!reset_n)begin state<=0;onehot<=9'd1;last<=0;count3<=0;end
    else if(enable)begin
      state<=next_state;onehot<=oh_next;last<=w;
      count3<=(count3!=0&&last==w)?((count3==3)?2'd3:count3+2'd1):2'd1;
    end
  end
endmodule
module running_light #(parameter integer PERIOD=5000001)(input wire clk,reset,output reg [15:0] led);
  reg [31:0] count;
  always @(posedge clk)begin
    if(reset)begin led<=16'd1;count<=0;end
    else begin
      if(count==0)led<={led[14:0],led[15]};
      count<=(count==32'(PERIOD-1))?32'd0:count+32'd1;
    end
  end
endmodule
module sequential(input wire clk,reset,reset_n,enable,load,serial_in,w,
 input wire [2:0] mode,input wire [7:0] data,
 output wire [7:0] q,lfsr,output wire z,z_onehot,z_mealy,
 output wire [3:0] state,output wire [8:0] onehot,output wire [15:0] light);
  shift_register s(clk,reset,enable,mode,data,serial_in,q);
  lfsr8 l(clk,reset,enable,load,data,lfsr);
  run_detector d(clk,reset_n,enable,w,z,state,onehot,z_onehot,z_mealy);
  running_light r(clk,reset,light);
endmodule
