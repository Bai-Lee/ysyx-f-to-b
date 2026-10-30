// HDL-036 Avoiding latches
// Source: https://hdlbits.01xz.net/wiki/always_nolatches
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire [15:0] scancode,
  output reg left,
  output reg down,
  output reg right,
  output reg up
);
always @* begin {left,down,right,up}=4'b0;case(scancode)16'he06b:left=1;16'he072:down=1;16'he074:right=1;16'he075:up=1;default:begin end endcase end
endmodule

`default_nettype wire
