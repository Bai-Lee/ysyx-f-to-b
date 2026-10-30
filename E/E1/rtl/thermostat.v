// HDL-057 Thermostat
// Source: https://hdlbits.01xz.net/wiki/thermostat
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire too_cold,
  input wire too_hot,
  input wire mode,
  input wire fan_on,
  output wire heater,
  output wire aircon,
  output wire fan
);
assign heater=mode&too_cold;assign aircon=~mode&too_hot;assign fan=heater|aircon|fan_on;
endmodule

`default_nettype wire
