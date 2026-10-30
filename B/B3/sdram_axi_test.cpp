#include "Vb_sdram_axi_test.h"
#include "verilated.h"
#include "verilated_vcd_c.h"
#include <cstdint>
#include <cstdio>
#include <memory>
#include <stdexcept>
#include <unordered_map>
int main(int argc,char**argv) {
  Verilated::commandArgs(argc,argv);Verilated::traceEverOn(true);Vb_sdram_axi_test d;
  std::unique_ptr<VerilatedVcdC>wave;uint64_t ticks=0;
  if(argc>1){wave=std::make_unique<VerilatedVcdC>();d.trace(wave.get(),2);wave->open(argv[1]);}
  auto tick=[&](){d.clock=1;d.eval();if(wave&&ticks<3000)wave->dump(ticks*2+1);d.clock=0;d.eval();if(wave&&ticks<3000)wave->dump(ticks*2+2);ticks++;};
  uint32_t random=0x2607b318;auto rng=[&](){random^=random<<13;random^=random>>17;random^=random<<5;return random;};
  std::unordered_map<uint32_t,uint32_t> memory;unsigned writes=0,reads=0,beats=0;
  d.reset=1;d.clock=0;d.in_arvalid=d.in_awvalid=d.in_wvalid=0;d.in_rready=d.in_bready=0;
  d.in_araddr=d.in_awaddr=d.in_wdata=0;d.in_arid=3;d.in_awid=5;d.in_arlen=d.in_awlen=0;
  d.in_arsize=d.in_awsize=2;d.in_arburst=d.in_awburst=1;d.in_wstrb=15;d.in_wlast=1;
  d.eval();tick();tick();d.reset=0;for(unsigned i=0;i<60;i++)tick();
  try {
    auto write=[&](uint32_t address,uint32_t data,unsigned mask){
      bool aw=false,w=false,done=false;unsigned awdelay=rng()%4,wdelay=rng()%4;
      d.in_awaddr=address;d.in_wdata=data;d.in_wstrb=mask;d.in_bready=0;
      for(unsigned t=0;t<1000&&!done;t++){
        d.in_awvalid=!aw&&t>=awdelay;d.in_wvalid=!w&&t>=wdelay;d.in_bready=(rng()%4)!=0;d.eval();
        if(d.in_awvalid&&d.in_awready)aw=true;if(d.in_wvalid&&d.in_wready)w=true;
        if(d.in_bvalid&&d.in_bready){if(!aw||!w||d.in_bid!=5||d.in_bresp)throw std::runtime_error("WRITE_RESPONSE");done=true;}
        tick();
      }
      d.in_awvalid=d.in_wvalid=d.in_bready=0;if(!done)throw std::runtime_error("WRITE_TIMEOUT");
      uint32_t&old=memory[address&~3u];for(unsigned b=0;b<4;b++)if(mask&(1u<<b))old=(old&~(255u<<(8*b)))|(data&(255u<<(8*b)));writes++;
    };
    auto read=[&](uint32_t address,unsigned length){
      bool ar=false;unsigned got=0;bool held=false;uint32_t last=0;
      d.in_araddr=address;d.in_arlen=length-1;
      for(unsigned t=0;t<1000&&got<length;t++){
        d.in_arvalid=!ar;d.in_rready=rng()%3!=0;d.eval();
        if(held&&(!d.in_rvalid||d.in_rdata!=last))throw std::runtime_error("READ_BACKPRESSURE");
        if(d.in_arvalid&&d.in_arready)ar=true;
        if(d.in_rvalid&&d.in_rready){
          uint32_t expected=memory.at(address+got*4);
          if(d.in_rresp||d.in_rid!=3||d.in_rlast!=(got+1==length)||d.in_rdata!=expected){std::fprintf(stderr,"SDRAM_DATA_MISMATCH address=%08x beat=%u expected=%08x actual=%08x resp=%u\n",address,got,expected,d.in_rdata,unsigned(d.in_rresp));throw std::runtime_error("READ_DATA");}
          got++;beats++;
        }
        held=d.in_rvalid&&!d.in_rready;last=d.in_rdata;tick();
      }
      d.in_arvalid=d.in_rready=0;if(got!=length)throw std::runtime_error("READ_TIMEOUT");reads++;
    };
    for(unsigned rank=0;rank<2;rank++)for(unsigned bank=0;bank<4;bank++)for(unsigned row:{0u,8191u})for(unsigned col:{0u,504u}) {
      uint32_t base=0xa0000000u|(rank<<26)|(row<<13)|(bank<<11)|(col<<2);
      for(unsigned word=0;word<8;word++)write(base+word*4,(base+word*4)^0x76543210u,15);
      read(base,1);read(base,4);read(base,8);
      for(unsigned word=0;word<8;word++){write(base+word*4,0xaabbccdd^word,1u<<(word&3));write(base+word*4,0x11223344^word,word&1?12:3);}
      read(base,8);
    }
    if(memory.at(0xa7fffffc)==0)throw std::runtime_error("HIGHEST_ADDRESS");
    if(wave)wave->close();std::printf("SDRAM_AXI_PASS writes=%u reads=%u beats=%u distinct_words=%zu max_address=a7fffffc cycles=%llu\n",writes,reads,beats,memory.size(),(unsigned long long)ticks);return 0;
  }catch(const std::exception&e){if(wave)wave->close();std::fprintf(stderr,"SDRAM_AXI_FAIL %s\n",e.what());return 1;}
}
