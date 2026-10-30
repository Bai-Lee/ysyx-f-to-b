#include "Vaxi4_delayer.h"
#include "verilated.h"
#include "verilated_vcd_c.h"
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <memory>
#include <stdexcept>
#include <vector>
int main(int argc,char**argv) {
  Verilated::commandArgs(argc,argv);Verilated::traceEverOn(true);Vaxi4_delayer d;
  unsigned ratio=argc>1?std::strtoul(argv[1],nullptr,0):256;uint64_t time=0;
  std::unique_ptr<VerilatedVcdC> wave;
  if(argc>2){wave=std::make_unique<VerilatedVcdC>();d.trace(wave.get(),3);wave->open(argv[2]);}
  auto edge=[&](){d.clock=1;d.eval();if(wave)wave->dump(++time);else time++;d.clock=0;d.eval();if(wave)wave->dump(++time);else time++;};
  unsigned transactions=0,read_beats=0;
  try {
    for(unsigned test=0;test<48;test++) {
      d.reset=1;d.clock=0;d.in_arvalid=d.in_awvalid=d.in_wvalid=d.in_rready=d.in_bready=0;
      d.out_arready=d.out_awready=d.out_wready=d.out_rvalid=d.out_bvalid=0;
      d.out_rid=d.out_bid=d.out_rdata=d.out_rresp=d.out_bresp=d.out_rlast=0;
      d.in_arid=3;d.in_araddr=0xa0000000;d.in_arlen=0;d.in_arsize=2;d.in_arburst=1;
      d.in_awid=5;d.in_awaddr=0xa0001000;d.in_awlen=0;d.in_awsize=2;d.in_awburst=1;
      d.in_wdata=0x76543210;d.in_wstrb=15;d.in_wlast=1;d.eval();edge();edge();d.reset=0;
      unsigned count=(test%3==0?1:test%3==1?4:8);d.in_arlen=count-1;
      bool ar_sent=false,aw_sent=false,w_sent=false,b_sent=false,b_received=false;
      unsigned ar_at=0,aw_at=0,w_at=0,sent=0,received=0;
      unsigned r_start=1,w_start=1;
      unsigned r_stall_until=test%2?unsigned(35*ratio/256):0,b_stall_until=test%2?unsigned(25*ratio/256):0;
      std::vector<unsigned> due(count);unsigned b_due=0;
      bool stalled=false;uint32_t stalled_data=0;unsigned stalled_id=0,stalled_resp=0,stalled_last=0;
      for(unsigned t=1;t<2000;t++) {
        d.in_arvalid=!ar_sent;d.in_awvalid=!aw_sent&&(test%2?t>=3:true);d.in_wvalid=!w_sent;
        d.in_rready=t>=r_stall_until;d.in_bready=t>=b_stall_until;
        d.out_arready=t>=1+test%4;d.out_awready=t>=2+test%3;d.out_wready=t>=1+test%5;
        d.out_rvalid=ar_sent&&sent<count&&t>=ar_at+2+sent*2;
        d.out_rid=3;d.out_rdata=0xabc00000+sent;d.out_rresp=test%7==0?2:0;d.out_rlast=sent+1==count;
        d.out_bvalid=aw_sent&&w_sent&&!b_sent&&t>=std::max(aw_at,w_at)+3;d.out_bid=5;d.out_bresp=test%5==0?2:0;
        d.clock=0;d.eval();
        if(stalled&&(!d.in_rvalid||d.in_rdata!=stalled_data||d.in_rid!=stalled_id||d.in_rresp!=stalled_resp||d.in_rlast!=stalled_last))throw std::runtime_error("R_STABILITY");
        if(d.out_arvalid&&d.out_arready){if(ar_sent||d.out_arlen!=count-1||d.out_arid!=3)throw std::runtime_error("AR_FIELDS");ar_sent=true;ar_at=t;}
        if(d.out_awvalid&&d.out_awready){if(aw_sent||d.out_awaddr!=0xa0001000||d.out_awid!=5)throw std::runtime_error("AW_FIELDS");aw_sent=true;aw_at=t;}
        if(d.out_wvalid&&d.out_wready){if(w_sent||d.out_wdata!=0x76543210||d.out_wstrb!=15||!d.out_wlast)throw std::runtime_error("W_FIELDS");w_sent=true;w_at=t;}
        if(d.out_rvalid&&d.out_rready){due[sent]=r_start+((t-r_start)*ratio+255)/256;sent++;}
        if(d.out_bvalid&&d.out_bready){b_due=w_start+((t-w_start)*ratio+255)/256;b_sent=true;}
        if(d.in_rvalid&&d.in_rready){
          unsigned earliest=std::max(due[received],r_stall_until);
          // Consecutive overdue beats serialize at one beat per cycle.
          if(received&&earliest<=due[received-1])earliest=due[received-1]+1;
          if(t!=earliest||d.in_rdata!=0xabc00000+received||d.in_rid!=3||d.in_rresp!=(test%7==0?2:0)||d.in_rlast!=(received+1==count)){
            std::fprintf(stderr,"AXI_DELAY_MISMATCH test=%u ratio=%u beat=%u expected=%u actual=%u\n",test,ratio,received,earliest,t);throw std::runtime_error("R_CALIBRATION");
          }
          due[received]=t;received++;read_beats++;
        }
        if(d.in_bvalid&&d.in_bready){
          if(b_received||t!=std::max(b_due,b_stall_until)||d.in_bid!=5||d.in_bresp!=(test%5==0?2:0))throw std::runtime_error("B_CALIBRATION");b_received=true;
        }
        stalled=d.in_rvalid&&!d.in_rready;stalled_data=d.in_rdata;stalled_id=d.in_rid;stalled_resp=d.in_rresp;stalled_last=d.in_rlast;
        edge();
        if(received==count&&b_received){transactions++;break;}
        if(t==1999)throw std::runtime_error("TIMEOUT");
      }
    }
    if(wave)wave->close();std::printf("AXI_DELAY_PASS ratio_q=%u paired_transactions=%u read_beats=%u\n",ratio,transactions,read_beats);return 0;
  }catch(const std::exception&e){if(wave)wave->close();std::fprintf(stderr,"AXI_DELAY_TEST_FAIL %s\n",e.what());return 1;}
}
