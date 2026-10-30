// HDL-124 Simple one-hot state transitions 3
// Source: https://hdlbits.01xz.net/wiki/fsm3onehot
// Independently authored implementation; exact external names and ranges preserved.
`default_nettype none
module top_module(
  input wire in,
  input wire [3:0] state,
  output wire [3:0] next_state,
  output wire out
);
assign next_state[0]=~in&(state[0]|state[2]);assign next_state[1]=in&(state[0]|state[1]|state[3]);assign next_state[2]=~in&(state[1]|state[3]);assign next_state[3]=in&state[2];assign out=state[3];
endmodule

`default_nettype wire
