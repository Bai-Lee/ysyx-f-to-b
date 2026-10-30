`timescale 1ns/1ps
module tb;
reg [2:0] v_vec;
wire [2:0] got_outv;reg [2:0] exp_outv, mask_outv;
wire  got_o2;reg  exp_o2, mask_o2;
wire  got_o1;reg  exp_o1, mask_o1;
wire  got_o0;reg  exp_o0, mask_o0;
reg [2:0] scan_vec;
integer file,rc,n=0;top_module dut(.vec(v_vec),.outv(got_outv),.o2(got_o2),.o1(got_o1),.o0(got_o0));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/vector0.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h %h %h\n",scan_vec,exp_outv,mask_outv,exp_o2,mask_o2,exp_o1,mask_o1,exp_o0,mask_o0);
if(rc!=9)$fatal(2,"vector parse failure");
v_vec=scan_vec;
#1;
if(((got_outv ^ exp_outv) & mask_outv) !== 3'd0) begin $display("MISMATCH vector0 row=%0d port=outv got=%h expected=%h mask=%h",n,got_outv,exp_outv,mask_outv);$fatal(1,"behavior mismatch");end
if(((got_o2 ^ exp_o2) & mask_o2) !== 1'd0) begin $display("MISMATCH vector0 row=%0d port=o2 got=%h expected=%h mask=%h",n,got_o2,exp_o2,mask_o2);$fatal(1,"behavior mismatch");end
if(((got_o1 ^ exp_o1) & mask_o1) !== 1'd0) begin $display("MISMATCH vector0 row=%0d port=o1 got=%h expected=%h mask=%h",n,got_o1,exp_o1,mask_o1);$fatal(1,"behavior mismatch");end
if(((got_o0 ^ exp_o0) & mask_o0) !== 1'd0) begin $display("MISMATCH vector0 row=%0d port=o0 got=%h expected=%h mask=%h",n,got_o0,exp_o0,mask_o0);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=8)$fatal(2,"wrong case count");
$display("PASS vector0 checks=%0d",n);$fclose(file);$finish;end
endmodule
