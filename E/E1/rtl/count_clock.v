// HDL-106 12-hour clock
// Source: https://hdlbits.01xz.net/wiki/count_clock
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire clk,
  input wire reset,
  input wire ena,
  output wire pm,
  output wire [7:0] hh,
  output wire [7:0] mm,
  output wire [7:0] ss
);
reg pm_value;reg[7:0]hours,minutes,seconds;
assign pm=pm_value;assign hh=hours;assign mm=minutes;assign ss=seconds;
function[7:0] inc_bcd;input[7:0]v;begin inc_bcd=(v[3:0]==9)?v+8'd7:v+8'd1;end endfunction
always @(posedge clk)begin
if(reset)begin pm_value<=0;hours<=8'h12;minutes<=0;seconds<=0;end
else if(ena)begin
if(seconds==8'h59)begin seconds<=0;
if(minutes==8'h59)begin minutes<=0;
if(hours==8'h11)begin hours<=8'h12;pm_value<=~pm_value;end
else if(hours==8'h12)hours<=8'h01;else hours<=inc_bcd(hours);
end else minutes<=inc_bcd(minutes);
end else seconds<=inc_bcd(seconds);
end end
endmodule

`default_nettype wire
