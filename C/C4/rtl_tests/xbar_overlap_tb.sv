`timescale 1ns/1ps
module xbar_overlap_tb;
logic clock=0,reset=1; always #5 clock=~clock;
logic [1:0] s_awvalid;
logic [1:0] s_awready;
logic [1:0] [31:0] s_awaddr;
logic [1:0] [2:0] s_awprot;
logic [1:0] s_wvalid;
logic [1:0] s_wready;
logic [1:0] [31:0] s_wdata;
logic [1:0] [3:0] s_wstrb;
logic [1:0] s_bvalid;
logic [1:0] s_bready;
logic [1:0] [1:0] s_bresp;
logic [1:0] s_arvalid;
logic [1:0] s_arready;
logic [1:0] [31:0] s_araddr;
logic [1:0] [2:0] s_arprot;
logic [1:0] s_rvalid;
logic [1:0] s_rready;
logic [1:0] [31:0] s_rdata;
logic [1:0] [1:0] s_rresp;
logic [0:0] a_awvalid;
logic [0:0] a_awready;
logic [0:0] [31:0] a_awaddr;
logic [0:0] [2:0] a_awprot;
logic [0:0] a_wvalid;
logic [0:0] a_wready;
logic [0:0] [31:0] a_wdata;
logic [0:0] [3:0] a_wstrb;
logic [0:0] a_bvalid;
logic [0:0] a_bready;
logic [0:0] [1:0] a_bresp;
logic [0:0] a_arvalid;
logic [0:0] a_arready;
logic [0:0] [31:0] a_araddr;
logic [0:0] [2:0] a_arprot;
logic [0:0] a_rvalid;
logic [0:0] a_rready;
logic [0:0] [31:0] a_rdata;
logic [0:0] [1:0] a_rresp;
logic [2:0] m_awvalid;
logic [2:0] m_awready;
logic [2:0] [31:0] m_awaddr;
logic [2:0] [2:0] m_awprot;
logic [2:0] m_wvalid;
logic [2:0] m_wready;
logic [2:0] [31:0] m_wdata;
logic [2:0] [3:0] m_wstrb;
logic [2:0] m_bvalid;
logic [2:0] m_bready;
logic [2:0] [1:0] m_bresp;
logic [2:0] m_arvalid;
logic [2:0] m_arready;
logic [2:0] [31:0] m_araddr;
logic [2:0] [2:0] m_arprot;
logic [2:0] m_rvalid;
logic [2:0] m_rready;
logic [2:0] [31:0] m_rdata;
logic [2:0] [1:0] m_rresp;
wire debug_busy,debug_owner;
assign debug_busy=0;assign debug_owner=0;
assign a_awvalid[0]=s_awvalid[0];
assign s_awready[0]=a_awready[0];
assign s_awready[1]=0;
assign a_awaddr[0]=s_awaddr[0];
assign a_awprot[0]=s_awprot[0];
assign a_wvalid[0]=s_wvalid[0];
assign s_wready[0]=a_wready[0];
assign s_wready[1]=0;
assign a_wdata[0]=s_wdata[0];
assign a_wstrb[0]=s_wstrb[0];
assign s_bvalid[0]=a_bvalid[0];
assign s_bvalid[1]=0;
assign a_bready[0]=s_bready[0];
assign s_bresp[0]=a_bresp[0];
assign s_bresp[1]=0;
assign a_arvalid[0]=s_arvalid[0];
assign s_arready[0]=a_arready[0];
assign s_arready[1]=0;
assign a_araddr[0]=s_araddr[0];
assign a_arprot[0]=s_arprot[0];
assign s_rvalid[0]=a_rvalid[0];
assign s_rvalid[1]=0;
assign a_rready[0]=s_rready[0];
assign s_rdata[0]=a_rdata[0];
assign s_rdata[1]=0;
assign s_rresp[0]=a_rresp[0];
assign s_rresp[1]=0;
axil_xbar3 xbar(.clock(clock),.reset(reset),.s_awvalid(a_awvalid[0]),
.s_awready(a_awready[0]),
.s_awaddr(a_awaddr[0]),
.s_awprot(a_awprot[0]),
.s_wvalid(a_wvalid[0]),
.s_wready(a_wready[0]),
.s_wdata(a_wdata[0]),
.s_wstrb(a_wstrb[0]),
.s_bvalid(a_bvalid[0]),
.s_bready(a_bready[0]),
.s_bresp(a_bresp[0]),
.s_arvalid(a_arvalid[0]),
.s_arready(a_arready[0]),
.s_araddr(a_araddr[0]),
.s_arprot(a_arprot[0]),
.s_rvalid(a_rvalid[0]),
.s_rready(a_rready[0]),
.s_rdata(a_rdata[0]),
.s_rresp(a_rresp[0]),.m_awvalid(m_awvalid),
.m_awready(m_awready),
.m_awaddr(m_awaddr),
.m_awprot(m_awprot),
.m_wvalid(m_wvalid),
.m_wready(m_wready),
.m_wdata(m_wdata),
.m_wstrb(m_wstrb),
.m_bvalid(m_bvalid),
.m_bready(m_bready),
.m_bresp(m_bresp),
.m_arvalid(m_arvalid),
.m_arready(m_arready),
.m_araddr(m_araddr),
.m_arprot(m_arprot),
.m_rvalid(m_rvalid),
.m_rready(m_rready),
.m_rdata(m_rdata),
.m_rresp(m_rresp));

integer cycle=0,write_count=0,read_count=0,contended=0,completed0=0,completed1=0;
logic [2:0] aw_have=0,w_have=0;
logic [2:0][31:0] held_aw=0,held_w=0;
logic [2:0][3:0] held_strb=0;
logic previous_busy=0,previous_both=0,last_owner=1;
integer grant0=0,grant1=0;
function automatic [1:0] decode(input [31:0] addr);
  if(addr>=32'h80000000 && addr<32'h88000000)decode=0;
  else if(addr>=32'h10000000 && addr<32'h10001000)decode=1;
  else if(addr>=32'h20000000 && addr<32'h20001000)decode=2;
  else decode=3;
endfunction
function automatic [31:0] read_value(input [31:0] addr,input [2:0] prot,input integer target);
  read_value=addr ^ (32'h11000011*(target+1)) ^ {29'b0,prot};
endfunction
function automatic [31:0] write_value(input [31:0] addr);
  write_value=addr^32'h53a96c78;
endfunction
function automatic [3:0] write_mask(input [31:0] addr);
  write_mask=addr[5:2];
endfunction
always_comb begin
  m_awready=0;m_wready=0;m_arready=0;
  for(integer j=0;j<3;j++)begin
    m_awready[j]=!reset&&!aw_have[j]&&!m_bvalid[j]&&((cycle%7)==2);
    m_wready[j]=!reset&&!w_have[j]&&!m_bvalid[j]&&((cycle%5)==1);
    m_arready[j]=!reset&&!m_rvalid[j]&&((cycle%5)==3);
  end
end
always @(posedge clock)begin
  cycle<=cycle+1;
  if(cycle>30000)$fatal(1,"FABRIC_TIMEOUT");
  if(reset)begin
    m_bvalid<=0;m_bresp<=0;m_rvalid<=0;m_rresp<=0;m_rdata<=0;
    aw_have<=0;w_have<=0;held_aw<=0;held_w<=0;held_strb<=0;
    previous_busy<=0;previous_both<=0;last_owner<=1;
  end else begin
    if(debug_busy&&!previous_busy)begin
      if(debug_owner)grant1<=grant1+1;else grant0<=grant0+1;
      if(previous_both)begin
        contended<=contended+1;
        if(debug_owner===last_owner)$fatal(1,"ROUND_ROBIN_STARVATION");
      end
    end
    if(debug_busy&&((a_rvalid[0]&&a_rready[0])||(a_bvalid[0]&&a_bready[0])))last_owner<=debug_owner;
    previous_busy<=debug_busy;
    previous_both<=(s_arvalid[0]||s_awvalid[0]||s_wvalid[0])&&(s_arvalid[1]||s_awvalid[1]||s_wvalid[1]);
    if(s_bvalid[0]&&s_bvalid[1])$fatal(1,"B_TO_BOTH_MASTERS");
    if(s_rvalid[0]&&s_rvalid[1])$fatal(1,"R_TO_BOTH_MASTERS");
    if(!debug_owner&&(s_bvalid[1]||s_rvalid[1]))$fatal(1,"RESPONSE_WRONG_OWNER");
    if(debug_owner&&(s_bvalid[0]||s_rvalid[0]))$fatal(1,"RESPONSE_WRONG_OWNER");
    for(integer j=0;j<3;j++)begin
      if(m_arvalid[j]&&m_arready[j])begin
        if(decode(m_araddr[j])!=j)$fatal(1,"XBAR_READ_TARGET");
        m_rvalid[j]<=1;m_rdata[j]<=read_value(m_araddr[j],m_arprot[j],j);
        m_rresp[j]<=((m_araddr[j]&32'h80)!=0)?2:0;read_count<=read_count+1;
      end
      if(m_rvalid[j]&&m_rready[j])m_rvalid[j]<=0;
      if(m_awvalid[j]&&m_awready[j])begin held_aw[j]<=m_awaddr[j];aw_have[j]<=1;end
      if(m_wvalid[j]&&m_wready[j])begin held_w[j]<=m_wdata[j];held_strb[j]<=m_wstrb[j];w_have[j]<=1;end
      if(aw_have[j]&&w_have[j]&&!m_bvalid[j])begin
        if(decode(held_aw[j])!=j)$fatal(1,"XBAR_WRITE_TARGET");
        if(held_w[j]!==write_value(held_aw[j])||held_strb[j]!==write_mask(held_aw[j]))$fatal(1,"WRITE_PAIR_MIXED");
        m_bvalid[j]<=1;m_bresp[j]<=((held_aw[j]&32'h80)!=0)?2:0;
        aw_have[j]<=0;w_have[j]<=0;write_count<=write_count+1;
      end
      if(m_bvalid[j]&&m_bready[j])m_bvalid[j]<=0;
    end
  end
end
// All valid payloads must survive arbitrary receiver stalls, including errors.
logic [1:0] held_rvalid=0,held_bvalid=0;
logic [1:0][31:0] held_rdata=0;logic [1:0][1:0] held_rresp=0,held_bresp=0;
logic [2:0] stalled_ar=0,stalled_aw=0,stalled_w=0;
logic [2:0][31:0] stalled_araddr=0,stalled_awaddr=0,stalled_wdata=0;
logic [2:0][2:0] stalled_arprot=0,stalled_awprot=0;logic [2:0][3:0] stalled_wstrb=0;
always @(posedge clock)begin
  if(reset)begin held_rvalid<=0;held_bvalid<=0;stalled_ar<=0;stalled_aw<=0;stalled_w<=0;end
  else begin
    for(integer j=0;j<2;j++)begin
      if(held_rvalid[j]&&(!s_rvalid[j]||s_rdata[j]!==held_rdata[j]||s_rresp[j]!==held_rresp[j]))$fatal(1,"R_STALL_STABILITY");
      if(held_bvalid[j]&&(!s_bvalid[j]||s_bresp[j]!==held_bresp[j]))$fatal(1,"B_STALL_STABILITY");
    end
    for(integer j=0;j<3;j++)begin
      if(stalled_ar[j]&&(!m_arvalid[j]||m_araddr[j]!==stalled_araddr[j]||m_arprot[j]!==stalled_arprot[j]))$fatal(1,"AR_STALL_STABILITY");
      if(stalled_aw[j]&&(!m_awvalid[j]||m_awaddr[j]!==stalled_awaddr[j]||m_awprot[j]!==stalled_awprot[j]))$fatal(1,"AW_STALL_STABILITY");
      if(stalled_w[j]&&(!m_wvalid[j]||m_wdata[j]!==stalled_wdata[j]||m_wstrb[j]!==stalled_wstrb[j]))$fatal(1,"W_STALL_STABILITY");
    end
    held_rvalid<=s_rvalid&~s_rready;held_rdata<=s_rdata;held_rresp<=s_rresp;
    held_bvalid<=s_bvalid&~s_bready;held_bresp<=s_bresp;
    stalled_ar<=m_arvalid&~m_arready;stalled_araddr<=m_araddr;stalled_arprot<=m_arprot;
    stalled_aw<=m_awvalid&~m_awready;stalled_awaddr<=m_awaddr;stalled_awprot<=m_awprot;
    stalled_w<=m_wvalid&~m_wready;stalled_wdata<=m_wdata;stalled_wstrb<=m_wstrb;
  end
end
task automatic send_aw(input integer who,input [31:0] addr,input integer delay_cycles);
  begin
    repeat(delay_cycles)@(negedge clock);
    s_awaddr[who]=addr;s_awprot[who]=who;s_awvalid[who]=1;
    do @(posedge clock);while(!s_awready[who]);
    @(negedge clock);s_awvalid[who]=0;
  end
endtask
task automatic send_w(input integer who,input [31:0] addr,input integer delay_cycles);
  begin
    repeat(delay_cycles)@(negedge clock);
    s_wdata[who]=write_value(addr);s_wstrb[who]=write_mask(addr);s_wvalid[who]=1;
    do @(posedge clock);while(!s_wready[who]);
    @(negedge clock);s_wvalid[who]=0;
  end
endtask
task automatic transaction(input integer who,input [31:0] addr,input bit write_op,input [2:0] prot,input integer order);
  logic [1:0] target,expected_response;logic [31:0] expected_data;integer start;
  begin
    start=cycle;target=decode(addr);
    expected_response=(target==3||(!write_op&&prot[2]&&target!=0))?3:(addr[7]?2:0);
    expected_data=expected_response==3?0:read_value(addr,prot,target);
    @(negedge clock);
    if(write_op)begin
      fork
        send_aw(who,addr,order==0?0:order==1?6:0);
        send_w(who,addr,order==0?6:0);
      join
      wait(s_bvalid[who]);repeat(5)@(negedge clock);
      if(s_bresp[who]!==expected_response)$fatal(1,"WRITE_RESPONSE");
      s_bready[who]=1;@(posedge clock);@(negedge clock);s_bready[who]=0;
    end else begin
      s_araddr[who]=addr;s_arprot[who]=prot;s_arvalid[who]=1;
      do @(posedge clock);while(!s_arready[who]);
      @(negedge clock);s_arvalid[who]=0;
      wait(s_rvalid[who]);repeat(4)@(negedge clock);
      if(s_rresp[who]!==expected_response||s_rdata[who]!==expected_data)$fatal(1,"READ_RESPONSE who=%0d addr=%h got=%h expected=%h",who,addr,s_rdata[who],expected_data);
      s_rready[who]=1;@(posedge clock);@(negedge clock);s_rready[who]=0;
    end
    if(cycle-start>200)$fatal(1,"BOUNDED_SERVICE");
    if(who==0)completed0++;else completed1++;
  end
endtask
task automatic master(input integer who);
  logic [31:0] address;logic [2:0] prot;
  begin
    for(integer n=0;n<48;n++)begin
      case(n%4)
        0:address=32'h80000000;
        1:address=32'h10000000;
        2:address=32'h20000000;
        3:address=32'h30000000;
      endcase
      address=address+who*256+n*4;
      prot=n%5==0?4:0;
      transaction(who,address,who==1&&n%3!=0,prot,n%3);
    end
  end
endtask

// Keep the next ARVALID asserted while the current R waits: sustained demand.
task automatic stream_reader(input integer who);
  logic [31:0] address;integer start;
  begin
    address=32'h80000400+who*256;
    @(negedge clock);s_araddr[who]=address;s_arprot[who]=0;s_arvalid[who]=1;
    for(integer n=0;n<32;n++)begin
      start=cycle;
      do @(posedge clock);while(!s_arready[who]);
      @(negedge clock);if(n==31)s_arvalid[who]=0;
      wait(s_rvalid[who]);repeat(3)@(negedge clock);
      if(s_rdata[who]!==read_value(address,0,0)||s_rresp[who]!==0)$fatal(1,"READ_RESPONSE_STREAM");
      s_rready[who]=1;@(posedge clock);@(negedge clock);s_rready[who]=0;
      if(cycle-start>200)$fatal(1,"STREAM_SERVICE_BOUND");
      if(who==0)completed0++;else completed1++;
    end
  end
endtask
task automatic reset_all;
  begin
    @(negedge clock);reset=1;#1;
    if(debug_busy||s_bvalid||s_rvalid||a_awvalid||a_wvalid||a_arvalid||m_awvalid||m_wvalid||m_arvalid)$fatal(1,"RESET_VALID_GATING");
    repeat(2)@(negedge clock);reset=0;
  end
endtask

initial begin
 s_awvalid=0;s_awaddr=0;s_awprot=0;s_wvalid=0;s_wdata=0;s_wstrb=0;s_bready=0;s_arvalid=0;s_araddr=0;s_arprot=0;s_rready=0;
 reset_all();
 // Request inputs must not combinationally change this interface's READY outputs.
 @(negedge clock);
 if(!s_arready[0]||!s_awready[0]||!s_wready[0])$fatal(1,"INITIAL_READY");
 s_awvalid[0]=1;s_wvalid[0]=1;#1;
 if(!s_arready[0])$fatal(1,"COMBINATIONAL_VALID_TO_READY");
 s_awvalid[0]=0;s_wvalid[0]=0;
 for(integer n=0;n<9;n++)begin
   fork
     transaction(0,32'h80000a00+n*4,0,0,0);
     transaction(0,32'h10000b00+n*4,1,0,n%3);
   join
 end
 if(read_count!=9||write_count!=9||completed0!=18)$fatal(1,"OVERLAP_TRANSACTION_LOST");
 $display("XBAR_OVERLAP_PASS reads=%0d writes=%0d cycles=%0d",read_count,write_count,cycle);$finish;
end
endmodule
