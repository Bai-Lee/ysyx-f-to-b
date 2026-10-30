`timescale 1ns/1ps
module tb;
reg [15:0] v_a;
reg [15:0] v_b;
reg [15:0] v_c;
reg [15:0] v_d;
reg [15:0] v_e;
reg [15:0] v_f;
reg [15:0] v_g;
reg [15:0] v_h;
reg [15:0] v_i;
reg [3:0] v_sel;
wire [15:0] got_out;reg [15:0] exp_out, mask_out;
reg [15:0] scan_a;
reg [15:0] scan_b;
reg [15:0] scan_c;
reg [15:0] scan_d;
reg [15:0] scan_e;
reg [15:0] scan_f;
reg [15:0] scan_g;
reg [15:0] scan_h;
reg [15:0] scan_i;
reg [3:0] scan_sel;
integer file,rc,n=0;top_module dut(.a(v_a),.b(v_b),.c(v_c),.d(v_d),.e(v_e),.f(v_f),.g(v_g),.h(v_h),.i(v_i),.sel(v_sel),.out(got_out));
initial begin
file=$fopen("/workspace/projects/ysyx_f_to_b/E/E1/vectors/mux9to1v.txt","r");if(!file)$fatal(2,"vector file unavailable");
while(!$feof(file))begin
rc=$fscanf(file,"%h %h %h %h %h %h %h %h %h %h %h %h\n",scan_a,scan_b,scan_c,scan_d,scan_e,scan_f,scan_g,scan_h,scan_i,scan_sel,exp_out,mask_out);
if(rc!=12)$fatal(2,"vector parse failure");
v_a=scan_a;
v_b=scan_b;
v_c=scan_c;
v_d=scan_d;
v_e=scan_e;
v_f=scan_f;
v_g=scan_g;
v_h=scan_h;
v_i=scan_i;
v_sel=scan_sel;
#1;
if(((got_out ^ exp_out) & mask_out) !== 16'd0) begin $display("MISMATCH mux9to1v row=%0d port=out got=%h expected=%h mask=%h",n,got_out,exp_out,mask_out);$fatal(1,"behavior mismatch");end

n=n+1;end
if(n!=1600)$fatal(2,"wrong case count");
$display("PASS mux9to1v checks=%0d",n);$fclose(file);$finish;end
endmodule
