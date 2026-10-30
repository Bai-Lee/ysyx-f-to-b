`timescale 1ns/1ns
module lab_board(input wire clk,reset,input wire [3:0] mode,input wire [11:0] sw,
 input wire [4:0] btn,input wire ps2_clk,ps2_data,
 output wire [15:0] led,output wire [7:0] seg0,seg1,seg2,seg3,seg4,seg5,seg6,seg7,
 output wire VGA_HSYNC,VGA_VSYNC,VGA_BLANK_N,output wire [7:0] VGA_R,VGA_G,VGA_B,
 output wire uart_tx,output wire [7:0] cpu_pc,cpu_instruction,output wire [31:0] cpu_gpr,
 output wire [7:0] dbg_key,dbg_ascii,dbg_count,dbg_code,output wire dbg_active,dbg_valid,dbg_error,dbg_shift,dbg_ctrl,
 output wire [9:0] dbg_x,dbg_y,dbg_h,dbg_v,output wire dbg_dx,dbg_dy,
 output wire [3:0] dbg_state,output wire [8:0] dbg_onehot);
  reg [2:0] button_sync;
  always @(posedge clk)if(reset)button_sync<=0;else button_sync<={button_sync[1:0],btn[0]};
  wire step=button_sync[1]&~button_sync[2];
  wire [2:0] prio;wire prio_valid;priority83 p(sw[7:0],sw[8],prio,prio_valid);
  wire [3:0] alu;wire carry,overflow,zero,less_s,less_u;
  alu4 u_alu(sw[3:0],sw[7:4],sw[10:8],alu,carry,overflow,zero,less_s,less_u);
  wire [7:0] lfsr_value,shift_value;
  lfsr8 l(clk,reset,step,btn[1],sw[7:0],lfsr_value);
  shift_register sh(clk,reset,step,sw[10:8],sw[7:0],sw[11],shift_value);
  wire z,unused_z_oh,unused_z_mealy;
  run_detector fsm(clk,sw[0]&&!reset,step,sw[1],z,dbg_state,dbg_onehot,unused_z_oh,unused_z_mealy);
  keyboard kb(clk,reset||(mode!=6),ps2_clk,ps2_data,dbg_code,dbg_valid,dbg_error,
    dbg_key,dbg_ascii,dbg_count,dbg_active,dbg_shift,dbg_ctrl);
  wire [15:0] light;running_light r(clk,reset,light);
  wire hs,vs,blank;wire [7:0] vr,vg,vb;
  vga v(clk,reset,mode==8,4'd3,4'd2,hs,vs,blank,vr,vg,vb,dbg_h,dbg_v,dbg_x,dbg_y,dbg_dx,dbg_dy);
  assign VGA_HSYNC=hs;assign VGA_VSYNC=vs;
  assign VGA_BLANK_N=((mode==7)||(mode==8))&&blank;
  assign VGA_R=vr;assign VGA_G=vg;assign VGA_B=vb;
  wire [7:0] cpu_led,cpu_hex;wire [6:0] unused_high,unused_low;
  wire unused_write;wire [2:0] unused_device;
  program_rom rom(cpu_pc,cpu_instruction);
  cpu_top cpu(clk,reset,cpu_instruction,sw[7:0],{3'b0,btn},cpu_pc,cpu_led,cpu_hex,cpu_gpr,
    unused_high,unused_low,unused_write,unused_device);
  assign led=mode==0?{15'b0,sw[0]^sw[1]}:
    mode==1?{11'b0,prio_valid,1'b0,prio}:
    mode==2?{7'b0,(sw[10:8]>=3'd6)&&less_u,(sw[10:8]>=3'd6)&&less_s,zero,overflow,carry,alu}:
    mode==3?{8'b0,lfsr_value}:mode==4?{8'b0,shift_value}:
    mode==5?{8'b0,dbg_state,3'b0,z}:mode==6?{14'b0,dbg_ctrl,dbg_shift}:
    mode==9?{8'b0,cpu_led}:mode==10?light:16'b0;
  wire [23:0] digits=mode==1?{21'b0,prio}:mode==2?{20'b0,alu}:
    mode==3?{16'b0,lfsr_value}:mode==4?{16'b0,shift_value}:
    mode==6?{dbg_count,dbg_ascii,dbg_key}:mode==9?{8'b0,cpu_hex,cpu_led}:24'b0;
  wire [6:0] h[0:5];wire [7:0] s[0:5];
  for(genvar i=0;i<6;i=i+1)begin:hexes
    hex_segment hex(digits[i*4+:4],h[i]);
    wire show=(mode==6)?(i>=4||dbg_active):
      (mode==1||mode==2)?(i==0):(mode==3||mode==4)?(i<2):(mode==9)?(i<4):1'b0;
    assign s[i]=show?{h[i][0],h[i][1],h[i][2],h[i][3],h[i][4],h[i][5],h[i][6],1'b1}:8'hff;
  end
  assign seg0=s[0];assign seg1=s[1];assign seg2=s[2];assign seg3=s[3];assign seg4=s[4];assign seg5=s[5];
  assign seg6=8'hff;assign seg7=8'hff;assign uart_tx=1'b1;
endmodule
