`timescale 1ns/1ps
module tb;
reg clock=0;
reg [7:0] a=1,b=2,c=3,d=4,e=5;
reg nb_a=0,nb_b=1, bl_a=0,bl_b=1;
reg display_a=0,zero_q=0;
reg [7:0] ordered=0;
always @(posedge clock) begin b=a; c<=b; d=c; e<=d; a=e; end
always @(posedge clock) nb_a<=nb_b;
always @(posedge clock) nb_b<=nb_a;
always @(posedge clock) bl_a=bl_b;
always @(posedge clock) bl_b=bl_a;
always @(posedge clock) display_a=1;
always @(posedge clock) begin
  $display("ACTIVE display_a=%0d",display_a);
  $strobe("MONITOR display_a=%0d",display_a);
end
initial begin
  zero_q<=1;
  ordered<=8'd1; ordered<=8'd2; ordered<=8'd3;
  #0;
  if(zero_q!==0 || ordered!==0) $fatal(1,"inactive must precede NBA");
  $display("INACTIVE zero_q=%0d ordered=%0d",zero_q,ordered);
  #1;
  if(zero_q!==1 || ordered!==3) $fatal(1,"ordered NBA result");
  clock=1;
  #1;
  if({a,b,c,d,e}!=={8'd5,8'd1,8'd1,8'd3,8'd3}) $fatal(1,"mixed result");
  if({nb_a,nb_b}!==2'b10) $fatal(1,"NBA swap");
  if({bl_a,bl_b}!==2'b00 && {bl_a,bl_b}!==2'b11) $fatal(1,"blocking race set");
  if(display_a!==1) $fatal(1,"settled display");
  $display("EVENT_PASS mixed=%0d,%0d,%0d,%0d,%0d NBA=%b%b blocking_observation=%b%b",a,b,c,d,e,nb_a,nb_b,bl_a,bl_b);
  $finish;
end
endmodule
