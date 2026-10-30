`timescale 1ns/1ps
module tb;
reg  v_in;
reg [9:0] v_state;
wire [9:0] got_next_state;reg [9:0] exp_next_state, mask_next_state;
wire  got_out1;reg  exp_out1, mask_out1;
wire  got_out2;reg  exp_out2, mask_out2;
reg  scan_in;
reg [9:0] scan_state;
integer file,rc,n=0;top_module dut(.in(v_in),.state(v_state),.next_state(got_next_state),.out1(got_out1),.out2(got_out2));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/fsm_onehot.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h %h\n",scan_in,scan_state,exp_next_state,mask_next_state,exp_out1,mask_out1,exp_out2,mask_out2);
if(rc!=8)$fatal(2,"vector parse failure");
v_in=scan_in;
v_state=scan_state;
#1;
if(((got_next_state ^ exp_next_state) & mask_next_state) !== 10'd0) begin $display("MISMATCH fsm_onehot row=%0d port=next_state got=%h expected=%h mask=%h",n,got_next_state,exp_next_state,mask_next_state);$fatal(1,"behavior mismatch");end
if(((got_out1 ^ exp_out1) & mask_out1) !== 1'd0) begin $display("MISMATCH fsm_onehot row=%0d port=out1 got=%h expected=%h mask=%h",n,got_out1,exp_out1,mask_out1);$fatal(1,"behavior mismatch");end
if(((got_out2 ^ exp_out2) & mask_out2) !== 1'd0) begin $display("MISMATCH fsm_onehot row=%0d port=out2 got=%h expected=%h mask=%h",n,got_out2,exp_out2,mask_out2);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=2048)$fatal(2,"wrong case count");
$display("PASS fsm_onehot checks=%0d",n);$fclose(file);$finish;end
endmodule
