#pragma once
#include "memory.hpp"
#include <vector>
#include <cstdint>
#include <stdexcept>
#include <string>

struct BusTxn { bool instruction=false,write=false; uint32_t address=0,data=0; unsigned strobe=0,error=0; };
struct ChannelHold {
  bool held=false; uint64_t a=0,b=0;
  void check(bool valid,bool ready,uint64_t x,uint64_t y,const char *name) {
    if(held && (!valid || a!=x || b!=y))throw std::runtime_error(std::string("UNSTABLE_CHANNEL ")+name);
    held=valid&&!ready;a=x;b=y;
  }
};

class BusBackend {
  struct Pending { bool active=false; uint64_t due=0; BusTxn txn; } ip,dp,rp,bp;
  bool have_aw=false,have_w=false;uint32_t awaddr=0,wdata=0;unsigned awprot=0,wstrb=0;
  bool mon_ar=false,mon_aw=false,mon_w=false;uint32_t mon_addr=0,mon_awaddr=0,mon_wdata=0;unsigned mon_prot=0,mon_mask=0;
  uint32_t random_state;uint32_t gates=0;
  ChannelHold ih,dh,arh,awh,wh,rh,bh;
  uint64_t async_cycle=~uint64_t(0);BusTxn async_read;
  Memory &m;
  unsigned mode;
  uint32_t random() { random_state=Memory::advance(random_state);return random_state; }
  unsigned delay() { return randomized_latency?1u+(random()%20u):latency; }
  BusTxn read(uint32_t a,bool instruction) {
    BusTxn t;t.address=a;t.instruction=instruction;
    try {
      if((a&3)||(!allow_cpp_devices&&!m.contains(a,4)))throw std::runtime_error("unmapped bus read");
      t.data=m.peek(a,4,instruction?0:1);
    } catch(const std::exception&) {t.error=3;}
    return t;
  }
  BusTxn write(uint32_t a,uint32_t data,unsigned mask) {
    BusTxn t;t.address=a;t.data=data;t.strobe=mask;t.write=true;
    if((a&3)||(!allow_cpp_devices&&!m.contains(a,4))) {t.error=3;return t;}
    if(!mask)return t;
    if(m.contains(a,4)) {
      for(unsigned i=0;i<4;i++)if(mask&(1u<<i))m.bytes[a-Memory::base+i]=uint8_t(data>>(8*i));
      m.writes++;
    } else if(allow_cpp_devices&&a==0x10000000u&&(mask&1)) {
      try {m.write(a,1,data&255);}catch(const std::exception&){t.error=2;}
    } else t.error=3;
    return t;
  }
  void consumed(const BusTxn &t) {
    if(!t.instruction&&!t.write&&!t.error)m.consume(t.address,4,t.data);
  }
  void push(const BusTxn &t) {
    completed.push_back(t);
    if(completed.size()>3)throw std::runtime_error("TOO_MANY_TRANSACTIONS_BEFORE_COMMIT");
  }
public:
  unsigned latency=1;bool randomized_latency=false,backpressure=false,allow_cpp_devices=true;
  uint64_t request_count=0,response_count=0,wait_cycles=0;
  std::vector<BusTxn> completed;
  explicit BusBackend(Memory &memory,unsigned selected,uint32_t seed):random_state(seed?seed:0x2607c404),m(memory),mode(selected) {allow_cpp_devices=mode!=6;}
  void begin_cycle() {gates=random();}

  template<class T> void drive(T &d,uint64_t cycle) {
    if(mode<=4) {
      d.i_req_ready=mode<4?1:(!ip.active&&(!backpressure||(gates&1)));
      d.i_resp_valid=ip.active&&cycle>=ip.due;d.i_resp_data=ip.txn.data;d.i_resp_error=ip.txn.error;
      if(mode==1) {
        d.d_req_ready=1;d.d_resp_valid=d.d_req_valid;
        BusTxn t;
        if(d.d_req_valid&&d.d_req_write) {
          if((d.d_req_addr&3)||(!m.contains(d.d_req_addr,4)&&d.d_req_addr!=0x10000000u))t.error=3;
          else if(d.d_req_addr==0x10000000u&&d.d_req_wstrb&&!(d.d_req_wstrb&1))t.error=3;
          else if(d.d_req_addr==0x10000000u&&m.random_uart&&!m.armed)t.error=2;
        } else if(d.d_req_valid) {
          if(async_cycle!=cycle||async_read.address!=d.d_req_addr) {async_read=read(d.d_req_addr,false);async_cycle=cycle;}
          t=async_read;
        }
        d.d_resp_data=t.data;d.d_resp_error=t.error;
      } else {
        d.d_req_ready=mode<4?1:(!dp.active&&(!backpressure||(gates&2)));
        d.d_resp_valid=dp.active&&cycle>=dp.due;d.d_resp_data=dp.txn.data;d.d_resp_error=dp.txn.error;
      }
      d.mem_awready=0;d.mem_wready=0;d.mem_bvalid=0;d.mem_bresp=0;d.mem_arready=0;d.mem_rvalid=0;d.mem_rdata=0;d.mem_rresp=0;
    } else {
      d.i_req_ready=0;d.i_resp_valid=0;d.i_resp_data=0;d.i_resp_error=0;d.d_req_ready=0;d.d_resp_valid=0;d.d_resp_data=0;d.d_resp_error=0;
      d.mem_arready=!rp.active&&(!backpressure||(gates&1));
      d.mem_awready=!have_aw&&!bp.active&&(!backpressure||(gates&2));
      d.mem_wready=!have_w&&!bp.active&&(!backpressure||(gates&4));
      d.mem_rvalid=rp.active&&cycle>=rp.due;d.mem_rdata=rp.txn.data;d.mem_rresp=rp.txn.error;
      d.mem_bvalid=bp.active&&cycle>=bp.due;d.mem_bresp=bp.txn.error;
    }
  }

  template<class T> void sample(T &d,uint64_t cycle) {
    if(mode<=4) {
      ih.check(d.i_req_valid,d.i_req_ready,d.i_req_addr,0,"simple-I");
      dh.check(d.d_req_valid,d.d_req_ready,(uint64_t(d.d_req_addr)<<32)|d.d_req_wdata,(unsigned(d.d_req_write)<<4)|d.d_req_wstrb,"simple-D");
      if(d.i_resp_valid&&d.i_resp_ready){push(ip.txn);ip.active=false;response_count++;}
      if(mode>1&&d.d_resp_valid&&d.d_resp_ready){consumed(dp.txn);push(dp.txn);dp.active=false;response_count++;}
      if(d.i_req_valid&&d.i_req_ready) {
        if(ip.active)throw std::runtime_error("DUPLICATE_IFETCH_REQUEST");
        ip={true,cycle+delay(),read(d.i_req_addr,true)};request_count++;
      }
      if(d.d_req_valid&&d.d_req_ready) {
        if(dp.active)throw std::runtime_error("DUPLICATE_DATA_REQUEST");
        if(mode==1&&!d.d_req_write&&(async_cycle!=cycle||async_read.address!=d.d_req_addr))throw std::runtime_error("ASYNC_READ_NOT_SETTLED");
        auto t=d.d_req_write?write(d.d_req_addr,d.d_req_wdata,d.d_req_wstrb):(mode==1?async_read:read(d.d_req_addr,false));
        request_count++;
        if(mode==1) {
          if(!d.d_resp_valid||!d.d_resp_ready)throw std::runtime_error("STAGE1_ASYNC_CONTRACT");
          if(!d.d_req_write)t.data=d.d_resp_data;
          consumed(t);push(t);response_count++;
        } else dp={true,cycle+delay(),t};
      }
    } else {
      // Observe the complete CPU master, including RTL device transactions.
      arh.check(d.mon_arvalid,d.mon_arready,d.mon_araddr,d.mon_arprot,"AR");
      awh.check(d.mon_awvalid,d.mon_awready,d.mon_awaddr,d.mon_awprot,"AW");
      wh.check(d.mon_wvalid,d.mon_wready,d.mon_wdata,d.mon_wstrb,"W");
      rh.check(d.mon_rvalid,d.mon_rready,d.mon_rdata,d.mon_rresp,"R");
      bh.check(d.mon_bvalid,d.mon_bready,d.mon_bresp,0,"B");
      if(d.mon_arvalid&&d.mon_arready) {
        if(mon_ar)throw std::runtime_error("MULTIPLE_OUTSTANDING_READS");
        mon_ar=true;mon_addr=d.mon_araddr;mon_prot=d.mon_arprot;
      }
      if(d.mon_awvalid&&d.mon_awready) {
        if(mon_aw)throw std::runtime_error("DUPLICATE_AW");
        mon_aw=true;mon_awaddr=d.mon_awaddr;
      }
      if(d.mon_wvalid&&d.mon_wready) {
        if(mon_w)throw std::runtime_error("DUPLICATE_W");
        mon_w=true;mon_wdata=d.mon_wdata;mon_mask=d.mon_wstrb;
      }
      if(d.mon_rvalid&&d.mon_rready) {
        if(!mon_ar)throw std::runtime_error("UNSOLICITED_R");
        push({bool(mon_prot&4),false,mon_addr,d.mon_rdata,0,d.mon_rresp});mon_ar=false;
      }
      if(d.mon_bvalid&&d.mon_bready) {
        if(!mon_aw||!mon_w)throw std::runtime_error("B_BEFORE_AW_AND_W");
        push({false,true,mon_awaddr,mon_wdata,mon_mask,d.mon_bresp});mon_aw=mon_w=false;
      }
      // The RAM slave is separate from the monitor. In MODE6 it cannot bypass
      // the RTL UART/CLINT with a C++ MMIO implementation.
      if(d.mem_rvalid&&d.mem_rready){consumed(rp.txn);rp.active=false;response_count++;}
      if(d.mem_bvalid&&d.mem_bready){bp.active=false;have_aw=have_w=false;response_count++;}
      if(d.mem_arvalid&&d.mem_arready){rp={true,cycle+delay(),read(d.mem_araddr,bool(d.mem_arprot&4))};request_count++;}
      if(d.mem_awvalid&&d.mem_awready){have_aw=true;awaddr=d.mem_awaddr;awprot=d.mem_awprot;}
      if(d.mem_wvalid&&d.mem_wready){have_w=true;wdata=d.mem_wdata;wstrb=d.mem_wstrb;}
      if(have_aw&&have_w&&!bp.active){bp={true,cycle+delay(),write(awaddr,wdata,wstrb)};request_count++;}
    }
  }
};
