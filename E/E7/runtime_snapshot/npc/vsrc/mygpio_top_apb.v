module mygpio_top_apb(
 input clock,reset,input [31:0]in_paddr,input in_psel,in_penable,
 input [2:0]in_pprot,input in_pwrite,input [31:0]in_pwdata,input [3:0]in_pstrb,
 output in_pready,output reg[31:0]in_prdata,output in_pslverr,
 output reg[15:0]gpio_out,input [15:0]gpio_in,
 output [7:0]gpio_seg_0,gpio_seg_1,gpio_seg_2,gpio_seg_3,
 output [7:0]gpio_seg_4,gpio_seg_5,gpio_seg_6,gpio_seg_7);
 reg[31:0]digits;
`ifdef FAULT_GPIO_SETUP_WRITE
 wire access=in_psel;
`else
 wire access=in_psel&&in_penable;
`endif
 wire led_selected=(in_paddr[3:2]==0);
 wire input_selected=(in_paddr[3:2]==1);
 wire seg_selected=(in_paddr[3:2]==2);
 // The upstream APB crossbar decodes the page. Byte access is selected by pstrb.
 wire unused_fields=^{in_paddr[31:4],in_paddr[1:0],in_pprot};
 assign in_pready=1'b1;
 assign in_pslverr=access&&(!(led_selected||input_selected||seg_selected)||(in_pwrite&&input_selected));
 always @* begin
  in_prdata=0;
  if(led_selected)in_prdata={16'b0,gpio_out};
  else if(input_selected)in_prdata={16'b0,gpio_in};
  else if(seg_selected)in_prdata=digits;
 end
 always @(posedge clock)begin
  if(reset)begin gpio_out<=0;digits<=0;end
  else if(access&&in_pwrite&&!in_pslverr)begin
   if(led_selected)begin
    if(in_pstrb[0])gpio_out[7:0]<=in_pwdata[7:0];
    if(in_pstrb[1])gpio_out[15:8]<=in_pwdata[15:8];
   end
   if(seg_selected)begin
    if(in_pstrb[0])digits[7:0]<=in_pwdata[7:0];
    if(in_pstrb[1])digits[15:8]<=in_pwdata[15:8];
    if(in_pstrb[2])digits[23:16]<=in_pwdata[23:16];
    if(in_pstrb[3])digits[31:24]<=in_pwdata[31:24];
   end
  end
 end
 function [7:0]segment(input[3:0]x);
  case(x)
   0:segment=8'h03;1:segment=8'h9f;2:segment=8'h25;3:segment=8'h0d;
   4:segment=8'h99;5:segment=8'h49;6:segment=8'h41;7:segment=8'h1f;
   8:segment=8'h01;9:segment=8'h09;10:segment=8'h11;11:segment=8'hc1;
   12:segment=8'h63;13:segment=8'h85;14:segment=8'h61;15:segment=8'h71;
  endcase
 endfunction
 assign gpio_seg_0=segment(digits[3:0]);assign gpio_seg_1=segment(digits[7:4]);
 assign gpio_seg_2=segment(digits[11:8]);assign gpio_seg_3=segment(digits[15:12]);
 assign gpio_seg_4=segment(digits[19:16]);assign gpio_seg_5=segment(digits[23:20]);
 assign gpio_seg_6=segment(digits[27:24]);assign gpio_seg_7=segment(digits[31:28]);
endmodule
