`timescale 1ns/1ps
module cpu_four_state_tb;
reg clock=0; always #5 clock=~clock;
reg reset=1;
wire m_awready;
wire m_awvalid;
wire [31:0] m_awaddr;
wire [3:0] m_awid;
wire [7:0] m_awlen;
wire [2:0] m_awsize;
wire [1:0] m_awburst;
wire m_wready;
wire m_wvalid;
wire [31:0] m_wdata;
wire [3:0] m_wstrb;
wire m_wlast;
wire m_bready;
reg m_bvalid;
reg [1:0] m_bresp;
reg [3:0] m_bid;
wire m_arready;
wire m_arvalid;
wire [31:0] m_araddr;
wire [3:0] m_arid;
wire [7:0] m_arlen;
wire [2:0] m_arsize;
wire [1:0] m_arburst;
wire m_rready;
reg m_rvalid;
reg [1:0] m_rresp;
reg [31:0] m_rdata;
reg m_rlast;
reg [3:0] m_rid;
ysyx_00000000 dut(.clock(clock),.reset(reset),.io_interrupt(1'b0),.io_master_awready(m_awready),.io_master_awvalid(m_awvalid),.io_master_awaddr(m_awaddr),.io_master_awid(m_awid),.io_master_awlen(m_awlen),.io_master_awsize(m_awsize),.io_master_awburst(m_awburst),.io_master_wready(m_wready),.io_master_wvalid(m_wvalid),.io_master_wdata(m_wdata),.io_master_wstrb(m_wstrb),.io_master_wlast(m_wlast),.io_master_bready(m_bready),.io_master_bvalid(m_bvalid),.io_master_bresp(m_bresp),.io_master_bid(m_bid),.io_master_arready(m_arready),.io_master_arvalid(m_arvalid),.io_master_araddr(m_araddr),.io_master_arid(m_arid),.io_master_arlen(m_arlen),.io_master_arsize(m_arsize),.io_master_arburst(m_arburst),.io_master_rready(m_rready),.io_master_rvalid(m_rvalid),.io_master_rresp(m_rresp),.io_master_rdata(m_rdata),.io_master_rlast(m_rlast),.io_master_rid(m_rid),.io_slave_awready(),.io_slave_awvalid(1'b0),.io_slave_awaddr(32'b0),.io_slave_awid(4'b0),.io_slave_awlen(8'b0),.io_slave_awsize(3'b0),.io_slave_awburst(2'b0),.io_slave_wready(),.io_slave_wvalid(1'b0),.io_slave_wdata(32'b0),.io_slave_wstrb(4'b0),.io_slave_wlast(1'b0),.io_slave_bready(1'b0),.io_slave_bvalid(),.io_slave_bresp(),.io_slave_bid(),.io_slave_arready(),.io_slave_arvalid(1'b0),.io_slave_araddr(32'b0),.io_slave_arid(4'b0),.io_slave_arlen(8'b0),.io_slave_arsize(3'b0),.io_slave_arburst(2'b0),.io_slave_rready(1'b0),.io_slave_rvalid(),.io_slave_rresp(),.io_slave_rdata(),.io_slave_rlast(),.io_slave_rid());
  // Full128MiB virtual RAM, allocated in4KiB pages. Unwritten data stays X.
  //8MiB resident-page budget is sufficient for these test-scale programs.
  localparam integer MAX_PAGES=2048,MAX_IMAGE_WORDS=1048576;
  integer page_slot[0:32767];reg [31:0] ram[0:MAX_PAGES*1024-1];
  reg [31:0] image_words[0:MAX_IMAGE_WORDS-1];
  reg [31:0] sram[0:2047];
  reg [7:0] uart_reg[0:7];
  integer allocated=0,image_count,max_cycles=60000000,soc_mode=0,fast_mode=0;
  integer cycles=0,read_transactions=0,read_beats=0,write_transactions=0;
  reg [31:0] random_state=32'h2607b501;
  reg read_pending=0,aw_saved=0,w_saved=0;
  reg [31:0] read_address,write_address,write_data;
  reg [3:0] read_id,write_id,write_mask;
  integer read_length=0,read_size=0,read_beat=0,read_delay=0;
  reg [31:0] exit_code=32'hffffffff;
  string image_file,wave_file;
  integer i,j;
  assign m_arready=!reset&&!read_pending&&!aw_saved&&!w_saved&&!m_bvalid&&(fast_mode||random_state[0]);
  assign m_awready=!reset&&!read_pending&&!aw_saved&&!m_bvalid&&(fast_mode||random_state[3]);
  assign m_wready=!reset&&!read_pending&&!w_saved&&!m_bvalid&&(fast_mode||random_state[7]);
  wire ar_fire=m_arvalid&&m_arready,aw_fire=m_awvalid&&m_awready,w_fire=m_wvalid&&m_wready;

  function automatic [31:0] memory_read(input [31:0] address);
    integer page,slot,index,b;reg [31:0] aligned,value;
    begin
      aligned=address&32'hfffffffc;value=32'bx;
      if((!soc_mode&&aligned>=32'h80000000&&aligned<32'h88000000)||(soc_mode&&aligned>=32'ha0000000&&aligned<32'ha8000000))begin
        page=(aligned-(soc_mode?32'ha0000000:32'h80000000))>>12;slot=page_slot[page];index=(aligned>>2)&1023;
        if(slot>=0)value=ram[slot*1024+index];
      end else if(soc_mode&&aligned>=32'h30000000&&aligned<32'h31000000)begin
        index=(aligned-32'h30000000)>>2;if(index<image_count)value=image_words[index];
      end else if(soc_mode&&aligned>=32'h0f000000&&aligned<32'h0f002000)value=sram[(aligned-32'h0f000000)>>2];
      else if(!soc_mode&&aligned>=32'h30000000&&aligned<32'h30000020)begin
        case(aligned)
          32'h30000000:value=32'h800002b7;
          32'h30000004:value=32'h00028067;
          default:value=32'h00000013;
        endcase
      end else if(aligned>=32'h10000000&&aligned<32'h10000008)begin
        value=0;
        for(b=0;b<4;b=b+1)begin index=aligned-32'h10000000+b;value[b*8+:8]=index==5?8'h60:uart_reg[index];end
      end else begin $display("UNMAPPED_READ address=%08x",address);$fatal(1,"B5_MEMORY_MAP");end
      memory_read=value;
    end
  endfunction

  task automatic memory_write(input [31:0] address,value,input [3:0] mask);
    integer page,slot,index,b;reg [31:0] aligned;reg [7:0] byte_value;
    begin
      aligned=address&32'hfffffffc;
      if((!soc_mode&&aligned>=32'h80000000&&aligned<32'h88000000)||(soc_mode&&aligned>=32'ha0000000&&aligned<32'ha8000000))begin
        page=(aligned-(soc_mode?32'ha0000000:32'h80000000))>>12;slot=page_slot[page];index=(aligned>>2)&1023;
        if(slot<0)begin
          if(allocated>=MAX_PAGES)begin $display("RESOURCE_LIMIT sparse RAM pages exhausted");$fatal(1,"B5_MODEL_CAPACITY");end
          slot=allocated;allocated=allocated+1;page_slot[page]=slot;
        end
        for(b=0;b<4;b=b+1)if(mask[b])ram[slot*1024+index][b*8+:8]=value[b*8+:8];
      end else if(soc_mode&&aligned>=32'h0f000000&&aligned<32'h0f002000)begin
        index=(aligned-32'h0f000000)>>2;for(b=0;b<4;b=b+1)if(mask[b])sram[index][b*8+:8]=value[b*8+:8];
      end else if(aligned>=32'h10000000&&aligned<32'h10000008)begin
        for(b=0;b<4;b=b+1)if(mask[b])begin
          index=aligned-32'h10000000+b;byte_value=value[b*8+:8];
          if(index==0&&!uart_reg[3][7])$write("%c",byte_value);else uart_reg[index]=byte_value;
        end
      end else if(aligned==32'h10001000&&mask==15)exit_code=value;
      else if(aligned==32'h10001004&&mask==15&&value==32'hb00d600d)begin
        if(exit_code!==0)begin $display("B5_BAD_TRAP code=%08x",exit_code);$fatal(1,"B5_PROGRAM_FAILED");end
        $display("\nB5_PROGRAM_PASS cycles=%0d reads=%0d beats=%0d writes=%0d pages=%0d",cycles,read_transactions,read_beats,write_transactions,allocated);
        $finish;
      end else begin $display("UNMAPPED_WRITE address=%08x",address);$fatal(1,"B5_MEMORY_MAP");end
    end
  endtask

  initial begin
    if(!$value$plusargs("IMAGE=%s",image_file))$fatal(1,"IMAGE_REQUIRED");
    if(!$value$plusargs("WORDS=%d",image_count))$fatal(1,"WORDS_REQUIRED");
    if(image_count<=0||image_count>MAX_IMAGE_WORDS)$fatal(1,"IMAGE_SIZE");
    if($value$plusargs("MAX_CYCLES=%d",max_cycles))begin end
    if($value$plusargs("SOC=%d",soc_mode))begin end
    if($value$plusargs("FAST=%d",fast_mode))begin end
    for(i=0;i<32768;i=i+1)page_slot[i]=-1;
    for(i=0;i<8;i=i+1)uart_reg[i]=0;
    $readmemh(image_file,image_words,0,image_count-1);
    if(!soc_mode)for(i=0;i<image_count;i=i+1)memory_write(32'h80000000+i*4,image_words[i],4'hf);
    if($value$plusargs("WAVE=%s",wave_file))begin $dumpfile(wave_file);$dumpvars(1,cpu_four_state_tb);end
    repeat(20)@(negedge clock);reset=0;
  end
  always @(posedge clock)begin
    if(reset)begin
      cycles<=0;random_state<=32'h2607b501;read_pending<=0;aw_saved<=0;w_saved<=0;
      m_rvalid<=0;m_rdata<=32'bx;m_rid<=0;m_rresp<=0;m_rlast<=0;
      m_bvalid<=0;m_bid<=0;m_bresp<=0;
      read_address<=0;read_id<=0;read_length<=0;read_size<=0;read_beat<=0;read_delay<=0;
      write_address<=0;write_data<=0;write_id<=0;write_mask<=0;
      read_transactions<=0;read_beats<=0;write_transactions<=0;
    end else begin
      cycles<=cycles+1;random_state<={random_state[30:0],random_state[31]^random_state[21]^random_state[1]^random_state[0]};
      if(cycles>=max_cycles)begin $display("B5_CYCLE_LIMIT cycles=%0d",cycles);$fatal(1,"B5_NO_SUCCESS_MAILBOX");end
      if(cycles==10000&&read_transactions==0)$fatal(1,"B5_NO_EXTERNAL_FETCH_AFTER_RESET");
      if((^{m_arvalid,m_awvalid,m_wvalid,m_rready,m_bready})===1'bx)$fatal(1,"AXI_CONTROL_UNKNOWN");
      if(m_arvalid&&(^{m_araddr,m_arid,m_arlen,m_arsize,m_arburst})===1'bx)$fatal(1,"AXI_AR_UNKNOWN");
      if(m_awvalid&&(^{m_awaddr,m_awid,m_awlen,m_awsize,m_awburst})===1'bx)$fatal(1,"AXI_AW_UNKNOWN");
      if(m_wvalid)begin
        if((^{m_wstrb,m_wlast})===1'bx)$fatal(1,"AXI_W_CONTROL_UNKNOWN");
        for(j=0;j<4;j=j+1)if(m_wstrb[j]&&(^m_wdata[j*8+:8])===1'bx)$fatal(1,"AXI_WRITE_ACTIVE_BYTE_UNKNOWN");
      end
      if(ar_fire)begin
        if(m_arburst!=1||m_arlen>7||m_arsize>2||(m_araddr&((32'd1<<m_arsize)-1))!=0)$fatal(1,"AXI_AR_FIELDS");
        read_pending<=1;read_address<=m_araddr;read_id<=m_arid;read_length<=m_arlen;read_size<=m_arsize;read_beat<=0;read_delay<=random_state[9:8];read_transactions<=read_transactions+1;
        if(fast_mode)begin m_rvalid<=1;m_rdata<=memory_read(m_araddr);m_rid<=m_arid;m_rlast<=m_arlen==0;m_rresp<=0;read_delay<=0;end
      end
      if(read_pending&&!m_rvalid)begin
        if(read_delay>0)read_delay<=read_delay-1;
        else begin m_rvalid<=1;m_rdata<=memory_read(read_address+(read_beat<<read_size));m_rid<=read_id;m_rlast<=read_beat==read_length;m_rresp<=0;end
      end
      if(m_rvalid&&m_rready)begin
        m_rvalid<=0;read_beats<=read_beats+1;
        if(m_rlast)read_pending<=0;else begin
          read_beat<=read_beat+1;read_delay<=random_state[11:10];
          if(fast_mode)begin m_rvalid<=1;m_rdata<=memory_read(read_address+((read_beat+1)<<read_size));m_rlast<=read_beat+1==read_length;read_delay<=0;end
        end
      end
      if(aw_fire)begin
        if(m_awburst!=1||m_awlen!=0||m_awsize>2||(m_awaddr&((32'd1<<m_awsize)-1))!=0)$fatal(1,"AXI_AW_FIELDS");
        aw_saved<=1;write_address<=m_awaddr;write_id<=m_awid;
      end
      if(w_fire)begin if(!m_wlast)$fatal(1,"AXI_W_LAST");w_saved<=1;write_data<=m_wdata;write_mask<=m_wstrb;end
      if((aw_saved||aw_fire)&&(w_saved||w_fire)&&!m_bvalid)begin
        memory_write(aw_fire?m_awaddr:write_address,w_fire?m_wdata:write_data,w_fire?m_wstrb:write_mask);
        write_transactions<=write_transactions+1;m_bvalid<=1;m_bid<=aw_fire?m_awid:write_id;m_bresp<=0;
      end
      if(m_bvalid&&m_bready)begin m_bvalid<=0;aw_saved<=0;w_saved<=0;end
      if(cycles!=0&&cycles%1000000==0)$display("B5_PROGRESS cycles=%0d reads=%0d writes=%0d pages=%0d",cycles,read_transactions,write_transactions,allocated);
    end
  end

endmodule
