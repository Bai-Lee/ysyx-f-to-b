`timescale 1ns/1ps
module uart_clint_tb;
  parameter bit BAD_UART=0,BAD_CLINT=0;
  logic clock=0,reset=1;
  logic s_awvalid=0,s_wvalid=0,s_bready=0,s_arvalid=0,s_rready=0;
  logic [31:0] s_awaddr=0,s_wdata=0,s_araddr=0;
  logic [3:0] s_wstrb=0;logic [2:0] s_awprot=0,s_arprot=0;
  wire s_awready,s_wready,s_bvalid,s_arready,s_rvalid;wire [1:0] s_bresp,s_rresp;wire [31:0] s_rdata;
  wire tx_valid;wire [7:0] tx_data;
  axil_uart #(.FAULT_REPEAT_TX(BAD_UART)) uart(.*);
  logic c_awvalid=0,c_wvalid=0,c_bready=0,c_arvalid=0,c_rready=0;
  logic [31:0] c_awaddr=0,c_wdata=0,c_araddr=0;logic [3:0] c_wstrb=0;
  wire c_awready,c_wready,c_bvalid,c_arready,c_rvalid;wire [1:0] c_bresp,c_rresp;wire [31:0] c_rdata;wire [63:0] mtime;
  axil_clint #(.MTIME_RESET(64'h00000000fffffffc),.FAULT_UNLATCHED_HIGH(BAD_CLINT)) clint(
    .clock(clock),.reset(reset),.s_awvalid(c_awvalid),.s_awready(c_awready),.s_awaddr(c_awaddr),.s_awprot(3'b0),
    .s_wvalid(c_wvalid),.s_wready(c_wready),.s_wdata(c_wdata),.s_wstrb(c_wstrb),.s_bvalid(c_bvalid),.s_bready(c_bready),.s_bresp(c_bresp),
    .s_arvalid(c_arvalid),.s_arready(c_arready),.s_araddr(c_araddr),.s_arprot(3'b0),.s_rvalid(c_rvalid),.s_rready(c_rready),.s_rdata(c_rdata),.s_rresp(c_rresp),.mtime(mtime));
  integer ticks=0,tx_count=0,expected_tx=0;
  logic [7:0] expected_char;
  task automatic tick;
    begin #1;clock=1;#1;if(tx_valid)begin tx_count++;if(tx_data!==expected_char)$fatal(1,"TX_PAYLOAD");end clock=0;#1;ticks++;if(ticks>2000)$fatal(1,"TIME_BUDGET");end
  endtask
  task automatic reset_all;
    begin
      reset=1;#1;if(s_bvalid||s_rvalid||tx_valid||c_bvalid||c_rvalid)$fatal(1,"RESET_VALID_GATE");
      tick();reset=0;#1;
    end
  endtask
  task automatic write_uart(input [31:0] addr,input [31:0] value,input [3:0] mask,input integer order,input [1:0] response);
    integer start_count;logic [1:0] held_response;
    begin
      start_count=tx_count;expected_char=value[7:0];s_awaddr=addr;s_wdata=value;s_wstrb=mask;
      if(order==0)begin
        s_awvalid=1;#1;while(!s_awready)tick();tick();s_awvalid=0;
        repeat(3)begin if(s_bvalid)$fatal(1,"B_BEFORE_W");tick();end
        s_wvalid=1;#1;while(!s_wready)tick();tick();s_wvalid=0;
      end else if(order==1)begin
        s_wvalid=1;#1;while(!s_wready)tick();tick();s_wvalid=0;
        repeat(3)begin if(s_bvalid)$fatal(1,"B_BEFORE_AW");tick();end
        s_awvalid=1;#1;while(!s_awready)tick();tick();s_awvalid=0;
      end else begin
        s_awvalid=1;s_wvalid=1;#1;if(!s_awready||!s_wready)$fatal(1,"INITIAL_READY");tick();s_awvalid=0;s_wvalid=0;
      end
      while(!s_bvalid)tick();held_response=s_bresp;
      repeat(5)begin if(!s_bvalid||s_bresp!==held_response)$fatal(1,"B_STALL_STABILITY");tick();end
      if(s_bresp!==response)$fatal(1,"B_RESPONSE");
      if(addr==32'h10000000 && mask[0] && response==0)expected_tx++;
      if(tx_count!=expected_tx)$fatal(1,"TX_DUPLICATE_OR_LOST got=%0d expected=%0d",tx_count,expected_tx);
      if(tx_count-start_count>1)$fatal(1,"TX_SIDE_EFFECT_MULTIPLE");
      s_bready=1;tick();s_bready=0;#1;if(s_bvalid)$fatal(1,"B_NOT_CONSUMED");
    end
  endtask
  task automatic read_uart(input [31:0] addr,input [31:0] value,input [1:0] response);
    logic [31:0] held;logic [1:0] code;
    begin
      s_araddr=addr;s_arvalid=1;#1;while(!s_arready)tick();tick();s_arvalid=0;
      while(!s_rvalid)tick();held=s_rdata;code=s_rresp;
      repeat(4)begin if(!s_rvalid||s_rdata!==held||s_rresp!==code)$fatal(1,"R_STALL_STABILITY");tick();end
      if(held!==value||code!==response)$fatal(1,"R_RESPONSE");s_rready=1;tick();s_rready=0;
    end
  endtask
  task automatic read_clint(input [31:0] addr,output [31:0] value,input integer stall);
    logic [31:0] held;
    begin
      c_araddr=addr;c_arvalid=1;#1;while(!c_arready)tick();tick();c_arvalid=0;
      while(!c_rvalid)tick();held=c_rdata;value=held;
      repeat(stall)begin if(!c_rvalid||c_rdata!==held||c_rresp!==0)$fatal(1,"CLINT_STALL_STABILITY");tick();end
      c_rready=1;tick();c_rready=0;
    end
  endtask
  logic [31:0] low,high;logic [63:0] sampled;
  initial begin
    reset_all();
    /* Low is sampled before rollover; consume high only after rollover. */
    sampled=mtime;read_clint(32'h20000000,low,8);read_clint(32'h20000004,high,3);
    if({high,low}!==sampled)$fatal(1,"CLINT_TORN_READ got=%h expected=%h",{high,low},sampled);
    if(mtime[63:32]!==1)$fatal(1,"CLINT_DID_NOT_ROLLOVER");
    read_clint(32'h20000004,high,1);if(high!==mtime[63:32])$fatal(1,"HIGH_ONLY");
    c_awaddr=32'h20000000;c_wdata=0;c_wstrb=15;c_awvalid=1;c_wvalid=1;tick();c_awvalid=0;c_wvalid=0;
    if(!c_bvalid||c_bresp!==2'b10)$fatal(1,"READONLY_CLOCK_WRITE");c_bready=1;tick();c_bready=0;
    write_uart(32'h10000000,32'h00000041,1,0,0);
    write_uart(32'h10000000,32'h12345642,15,1,0);
    write_uart(32'h10000000,32'h00000043,1,2,0);
    for(integer mask=0;mask<16;mask++)write_uart(32'h10000000,32'h010203a5,4'(mask),mask%3,0);
    write_uart(32'h10000004,32'h55,1,2,2'b10);
    read_uart(32'h10000004,1,0);read_uart(32'h10000000,0,0);read_uart(32'h10000008,0,2'b10);
    /* Reset a partial write: it cannot reappear after reset. */
    s_awaddr=32'h10000000;s_awvalid=1;tick();s_awvalid=0;reset_all();
    s_wdata=32'h99;s_wstrb=1;s_wvalid=1;tick();s_wvalid=0;
    repeat(4)begin if(s_bvalid||tx_valid)$fatal(1,"RESET_PARTIAL_WRITE");tick();end
    reset_all();
    $display("UART_CLINT_PASS tx=%0d ticks=%0d AWfirst Wfirst simultaneous WSTRB stalled_responses reset rollover",tx_count,ticks);$finish;
  end
endmodule
