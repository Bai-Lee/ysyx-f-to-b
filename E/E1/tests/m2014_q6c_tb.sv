`timescale 1ns/1ps
module tb;
reg [6:1] v_y;
reg  v_w;
wire  got_Y2;reg  exp_Y2, mask_Y2;
wire  got_Y4;reg  exp_Y4, mask_Y4;
reg [6:1] scan_y;
reg  scan_w;
integer file,rc,n=0;top_module dut(.y(v_y),.w(v_w),.Y2(got_Y2),.Y4(got_Y4));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/m2014_q6c.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h\n",scan_y,scan_w,exp_Y2,mask_Y2,exp_Y4,mask_Y4);
if(rc!=6)$fatal(2,"vector parse failure");
v_y=scan_y;
v_w=scan_w;
#1;
if(((got_Y2 ^ exp_Y2) & mask_Y2) !== 1'd0) begin $display("MISMATCH m2014_q6c row=%0d port=Y2 got=%h expected=%h mask=%h",n,got_Y2,exp_Y2,mask_Y2);$fatal(1,"behavior mismatch");end
if(((got_Y4 ^ exp_Y4) & mask_Y4) !== 1'd0) begin $display("MISMATCH m2014_q6c row=%0d port=Y4 got=%h expected=%h mask=%h",n,got_Y4,exp_Y4,mask_Y4);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=128)$fatal(2,"wrong case count");
$display("PASS m2014_q6c checks=%0d",n);$fclose(file);$finish;end
endmodule
