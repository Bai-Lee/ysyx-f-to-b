#include "Vysyx_00000000_icache.h"
#include "verilated.h"
#include "verilated_vcd_c.h"
#include <memory>
#include <cstdint>
#include <cstdio>
#include <stdexcept>
#include <unordered_map>
#include <deque>

int main(int argc,char**argv) {
  Verilated::commandArgs(argc,argv);Verilated::traceEverOn(true);Vysyx_00000000_icache d;
  std::unique_ptr<VerilatedVcdC> wave;uint64_t timestamp=0;
  if(argc>1){wave=std::make_unique<VerilatedVcdC>();d.trace(wave.get(),3);wave->open(argv[1]);}
  uint32_t random=0x2607b301;auto rng=[&](){random^=random<<13;random^=random>>17;random^=random<<5;return random;};
  unsigned requests=0,responses=0,accesses=0,hits=0,misses=0,bypass=0;
  bool active=false;uint32_t base=0;unsigned length=0,beat=0,delay=0;
  std::unordered_map<uint32_t,uint32_t> changed;
  auto value=[&](uint32_t address){auto it=changed.find(address);return it==changed.end()?(address*0x9e3779b9u)^0x15aee123:it->second;};
  auto step=[&](){
    d.clock=0;d.m_ready=!active&&((rng()&3)!=0);
    d.r_valid=active&&delay==0;d.r_data=value(base+4*beat);d.r_last=beat==length;d.r_error=0;d.eval();
    bool req=d.m_valid&&d.m_ready,resp=d.r_valid&&d.r_ready;
    uint32_t req_addr=d.m_addr;unsigned req_len=d.m_len;
    if(d.event_access){accesses++;hits+=d.event_hit;misses+=d.event_miss;bypass+=d.event_bypass;}
    d.clock=1;d.eval();timestamp++;if(wave&&timestamp<4000)wave->dump(timestamp);
    if(req){if(active)throw std::runtime_error("DUPLICATE_MEMORY");active=true;base=req_addr;length=req_len;beat=0;delay=1+(rng()%7);requests++;}
    else if(resp){responses++;if(beat==length)active=false;else{beat++;delay=rng()%4;}}
    else if(active&&delay)delay--;
    d.clock=0;d.eval();timestamp++;if(wave&&timestamp<4000)wave->dump(timestamp);
  };
  d.reset=1;d.invalidate=0;d.q_valid=0;d.q_addr=0;d.p_ready=0;d.m_ready=0;d.r_valid=0;d.r_data=0;d.r_error=0;d.r_last=0;
  for(unsigned i=0;i<4;i++)step();d.reset=0;
  try {
    auto request=[&](uint32_t address){
      d.q_addr=address;d.q_valid=1;
      unsigned guard=0;
      while(true){d.eval();bool fire=d.q_ready;step();if(fire)break;if(++guard>10000)throw std::runtime_error("Q_TIMEOUT");}
      d.q_valid=0;d.p_ready=0;
      while(!d.p_valid){step();if(++guard>10000)throw std::runtime_error("P_TIMEOUT");}
      uint32_t data=d.p_data;
      for(unsigned i=0;i<(rng()&7);i++){step();if(!d.p_valid||d.p_data!=data)throw std::runtime_error("BACKPRESSURE_UNSTABLE");}
      if(d.p_error||data!=value(address)){std::fprintf(stderr,"CACHE_DATA_MISMATCH address=%08x expected=%08x actual=%08x\n",address,value(address),data);throw std::runtime_error("CACHE_DATA");}
      d.p_ready=1;step();d.p_ready=0;
    };
    uint32_t addresses[]={0xa0000000,0xa0000004,0xa0000100,0xa0000000,0x80000000,0x80000100,0x30000000,0x30000004,0x0f000000,0x10000000};
    for(unsigned round=0;round<50;round++){
      for(uint32_t address:addresses)request(address);
      request(0xa0000000+4*(rng()%128));
      if(round%5==0){
        // Store modifies backing instruction memory; FENCE.I must expose it.
        changed[0xa0000000]=rng();d.invalidate=1;step();d.invalidate=0;request(0xa0000000);
      }
    }
    for(unsigned i=0;i<8;i++)request(0xa0000400+4*i);
    uint64_t stream_start=timestamp;unsigned sent=0,received=0;std::deque<uint32_t> outstanding;
    while(received<256){
      d.q_valid=sent<256;d.q_addr=0xa0000400+4*(sent%8);d.p_ready=1;d.eval();
      bool push=d.q_valid&&d.q_ready,pop=d.p_valid&&d.p_ready;
      if(pop){if(outstanding.empty()||d.p_error||d.p_data!=value(outstanding.front()))throw std::runtime_error("STREAM_DATA");outstanding.pop_front();received++;}
      if(push){outstanding.push_back(d.q_addr);sent++;}
      step();if(timestamp-stream_start>4000)throw std::runtime_error("STREAM_TIMEOUT");
    }
    unsigned expected_stream=argc>2&&std::strtoul(argv[2],nullptr,0)?257:512;
    if((timestamp-stream_start)/2!=expected_stream)throw std::runtime_error("STREAM_THROUGHPUT");
    if(accesses!=hits+misses+bypass||bypass!=100)throw std::runtime_error("ACCOUNTING");
    if(wave)wave->close();std::printf("ICACHE_PASS accesses=%u hits=%u misses=%u bypass=%u memory_requests=%u beats=%u stream_requests=256 stream_cycles=%u\n",accesses,hits,misses,bypass,requests,responses,expected_stream);return 0;
  }catch(const std::exception&e){if(wave)wave->close();std::fprintf(stderr,"ICACHE_TEST_FAIL %s\n",e.what());return 1;}
}
