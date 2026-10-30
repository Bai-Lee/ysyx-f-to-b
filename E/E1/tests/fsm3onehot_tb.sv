`timescale 1ns/1ps
module tb;
reg  v_in;
reg [3:0] v_state;
wire [3:0] got_next_state;reg [3:0] exp_next_state, mask_next_state;
wire  got_out;reg  exp_out, mask_out;
reg  scan_in;
reg [3:0] scan_state;
integer file,rc,n=0;top_module dut(.in(v_in),.state(v_state),.next_state(got_next_state),.out(got_out));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/fsm3onehot.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h\n",scan_in,scan_state,exp_next_state,mask_next_state,exp_out,mask_out);
if(rc!=6)$fatal(2,"vector parse failure");
v_in=scan_in;
v_state=scan_state;
#1;
if(((got_next_state ^ exp_next_state) & mask_next_state) !== 4'd0) begin $display("MISMATCH fsm3onehot row=%0d port=next_state got=%h expected=%h mask=%h",n,got_next_state,exp_next_state,mask_next_state);$fatal(1,"behavior mismatch");end
if(((got_out ^ exp_out) & mask_out) !== 1'd0) begin $display("MISMATCH fsm3onehot row=%0d port=out got=%h expected=%h mask=%h",n,got_out,exp_out,mask_out);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=32)$fatal(2,"wrong case count");
$display("PASS fsm3onehot checks=%0d",n);$fclose(file);$finish;end
endmodule
