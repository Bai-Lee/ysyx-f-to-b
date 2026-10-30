from pathlib import Path
import re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(ROOT/'make_cpu_wrapper.py')],check=True)
header=(ROOT/'rtl/ysyx_00000000.v').read_text().split(');',1)[0]
ports=re.findall(r'(input wire|output logic)\s*(\[[^\]]+\])?\s*(io_\w+)',header)
declarations=['`timescale 1ns/1ps','module axi4_cpu_tb;','logic clock=0,reset=1,io_interrupt=0;always #5 clock=~clock;']
declarations += [('logic ' if kind=='input wire' else 'wire ')+(width+' ' if width else '')+name+';' for kind,width,name in ports]
declarations += ['ysyx_00000000 dut(.*);']
unused=[name for kind,width,name in ports if name.startswith('io_slave_') and kind=='output logic']
initial=''.join(name+"='1;" for kind,width,name in ports if name.startswith('io_slave_') and kind=='input wire')
body=r'''
integer scenario=0,cycles=0,instructions=0,reads=0,writes=0,rstalls=0;
logic ar_have=0,aw_have=0,w_have=0;
logic [31:0] raddr=0,waddr=0,wdata=0,ram=0;
logic [3:0] wstrb=0;
integer read_delay=0;
function automatic [31:0] instruction(input [31:0] addr);
 case(addr)
  32'h20000000:instruction=32'h0f0002b7;
  32'h20000004:instruction=32'h05a00313;
  32'h20000008:instruction=32'h006281a3;
  32'h2000000c:instruction=32'h0032c383;
  32'h20000010:instruction=32'hfa638513;
  32'h20000014:instruction=32'h00100073;
  default:instruction=32'hffffffff;
 endcase
endfunction
assign io_master_rid=scenario==4?4'd1:4'd0;
assign io_master_rlast=scenario!=3;
assign io_master_rresp=0;
assign io_master_bid=scenario==5?4'd1:4'd0;
assign io_master_bresp=0;
always_comb begin
 io_master_arready=!reset&&!ar_have&&!io_master_rvalid&&(cycles%5==3);
 io_master_awready=!reset&&!aw_have&&!io_master_bvalid&&((scenario==1||scenario==2)||w_have);
 io_master_wready=!reset&&!w_have&&!io_master_bvalid&&(scenario==1?aw_have:1'b1);
end
always @(posedge clock)begin
 cycles<=cycles+1;
 if(cycles>2000)$fatal(1,"AXI4_TEST_TIMEOUT");
 if(reset)begin ar_have<=0;aw_have<=0;w_have<=0;io_master_rvalid<=0;io_master_bvalid<=0;io_master_rdata<=0;read_delay<=0;ram<=0;reads<=0;writes<=0;rstalls<=0;end
 else begin
  if({UNUSED_OUTPUTS}!==0)$fatal(1,"UNUSED_SLAVE_OUTPUT_NOT_ZERO");
  if(io_master_arvalid&&io_master_arready)begin
   if(io_master_arid!=0||io_master_arlen!=0||io_master_arburst!=1)$fatal(1,"AR_FIELDS");
   if(io_master_araddr==32'h0f000003)begin if(io_master_arsize!=0)$fatal(1,"NARROW_AR_SIZE");end
   else if(io_master_arsize!=2)$fatal(1,"FETCH_AR_SIZE");
   ar_have<=1;raddr<=io_master_araddr;read_delay<=3;reads<=reads+1;
  end
  if(ar_have&&read_delay>0)read_delay<=read_delay-1;
  if(ar_have&&read_delay==0&&!io_master_rvalid)begin io_master_rvalid<=1;io_master_rdata<=raddr == 32'h0f000003 ? ram : instruction(raddr);end
  if(io_master_rvalid&&!io_master_rready)rstalls<=rstalls+1;
  if(io_master_rvalid&&io_master_rready)begin io_master_rvalid<=0;ar_have<=0;end
  if(io_master_awvalid&&io_master_awready)begin
   if(io_master_awaddr!=32'h0f000003||io_master_awid!=0||io_master_awlen!=0||io_master_awsize!=0||io_master_awburst!=1)$fatal(1,"AW_FIELDS");
   waddr<=io_master_awaddr;aw_have<=1;
  end
  if(io_master_wvalid&&io_master_wready)begin
   if(io_master_wlast!=1||io_master_wstrb!=8||io_master_wdata!=32'h5a000000)$fatal(1,"W_FIELDS");
   wdata<=io_master_wdata;wstrb<=io_master_wstrb;w_have<=1;
  end
  if(aw_have&&w_have&&!io_master_bvalid)begin
   if(waddr!=32'h0f000003)$fatal(1,"WRITE_ADDRESS_CAPTURE");
   for(integer i=0;i<4;i++)if(wstrb[i])ram[i*8+:8]<=wdata[i*8+:8];
   writes<=writes+1;io_master_bvalid<=1;
  end
  if(io_master_bvalid&&io_master_bready)begin io_master_bvalid<=0;aw_have<=0;w_have<=0;end
 end
end
logic ar_stall=0,aw_stall=0,w_stall=0;
logic [31:0] held_ar=0,held_aw=0,held_w=0;logic [3:0] held_strb=0;
always @(posedge clock)begin
 if(reset)begin ar_stall<=0;aw_stall<=0;w_stall<=0;end
 else begin
  if(ar_stall&&(!io_master_arvalid||io_master_araddr!==held_ar))$fatal(1,"AR_UNSTABLE");
  if(aw_stall&&(!io_master_awvalid||io_master_awaddr!==held_aw))$fatal(1,"AW_UNSTABLE");
  if(w_stall&&(!io_master_wvalid||io_master_wdata!==held_w||io_master_wstrb!==held_strb))$fatal(1,"W_UNSTABLE");
  ar_stall<=io_master_arvalid&&!io_master_arready;held_ar<=io_master_araddr;
  aw_stall<=io_master_awvalid&&!io_master_awready;held_aw<=io_master_awaddr;
  w_stall<=io_master_wvalid&&!io_master_wready;held_w<=io_master_wdata;held_strb<=io_master_wstrb;
 end
end
always @(negedge clock)begin
 if(reset)begin
  instructions=0;
  if(io_master_arvalid||io_master_awvalid||io_master_wvalid)$fatal(1,"RESET_VALID_GATE");
 end else begin
  if(dut.commit_valid)instructions++;
  if(dut.fault!=0)begin
   if(!(scenario>=3&&scenario<=5)||dut.fault!=5||instructions!=(scenario==5?2:0))$fatal(1,"WRONG_PROTOCOL_REJECTION");
   $display("AXI4_CPU_PROTOCOL_REJECT_PASS scenario=%0d fault=%0d instructions=%0d",scenario,dut.fault,instructions);$finish;
  end else if(dut.halted)begin
   if(scenario>=3&&scenario<=5)$fatal(1,"BAD_RESPONSE_NOT_REJECTED");
   if(instructions!=6||reads!=7||writes!=1||ram!=32'h5a000000||dut.debug_gpr[224+:32]!=32'h5a||dut.debug_gpr[320+:32]!=0||rstalls==0)$fatal(1,"RESULT_OR_COVERAGE instructions=%0d reads=%0d writes=%0d rstalls=%0d",instructions,reads,writes,rstalls);
   $display("AXI4_CPU_PROTOCOL_PASS scenario=%0d cycles=%0d reads=%0d writes=%0d rstalls=%0d",scenario,cycles,reads,writes,rstalls);$finish;
  end
 end
end
initial begin
 UNUSED_INITIAL
 if(!$value$plusargs("SCENARIO=%d",scenario))scenario=0;
 repeat(4)@(negedge clock);reset=0;
 if(scenario==6)begin
  wait(ar_have);@(negedge clock);reset=1;repeat(2)@(negedge clock);reset=0;
 end
end
endmodule
'''
text='\n'.join(declarations)+'\n'+body.replace('UNUSED_OUTPUTS',','.join(unused)).replace('UNUSED_INITIAL',initial)
(ROOT/'rtl_tests/axi4_cpu_tb.sv').write_text(text)
print('C5_AXI4_CPU_TEST_GENERATED',flush=True)
