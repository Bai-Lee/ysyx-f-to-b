#include "Vysyx_00000000.h"
#include "Vysyx_00000000__Dpi.h"
#include "verilated.h"
#include <array>
#include <chrono>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>
#include "../soc/sim/reference.hpp"
#include "../soc/sim/performance.hpp"
static std::unique_ptr<Reference> reference;
static BusMonitor bus;
static Performance performance;
static CpuState before;
static MemoryAccess pending;
static std::array<uint32_t,16> gpr{};
static uint64_t cycles=0,retired=0,ecalls=0,mrets=0;
static uint32_t pc=0,inst=0,fault=0;
static bool stopped=false,diff_failed=false;
static std::string uart;
void b_clock(svBit reset){if(reference)reference->clock_tick(reset);}
void b_perf_tick(unsigned state,unsigned events){performance.tick(state,events);}
void b_cache_tick(unsigned events){performance.cache_tick(events);}
void b_pipeline_tick(unsigned events){for(unsigned i=0;i<16;i++)if(events&(1u<<i))performance.pipeline_events[i]++;}
void c5_fault(unsigned at,unsigned why){pc=at;fault=why;stopped=true;}
void c5_memory(unsigned at,unsigned address,unsigned size,unsigned value,svBit write){
  performance.memory(address,write);
  if(pending.valid)throw std::runtime_error("DUPLICATE_MEMORY_COMMIT");
  uint32_t mask=size==4?0xffffffffu:(1u<<(8*size))-1;
  pending={true,write!=0,at,address,size,value&mask};
}
void c5_bus(unsigned channel,unsigned address,unsigned value,unsigned attributes){bus.accept(channel,address,value,attributes);}
void c5_retire(unsigned at,unsigned instruction,unsigned next,const svBitVecVal *registers){
  if(at!=before.pc)throw std::runtime_error("RETIRE_PC_SEQUENCE");
  validate_access(before,instruction,pending);bus.retire(at,instruction,pending);
  pc=at;inst=instruction;retired++;ecalls+=instruction==0x73;mrets+=instruction==0x30200073;
  std::memcpy(gpr.data(),registers,64);CpuState actual;actual.pc=next;std::memcpy(actual.r,registers,64);
  if(actual.r[0])throw std::runtime_error("X0_NONZERO");
  performance.retire(at,instruction,next,pending.address,pending.valid,pending.write);
  if(reference&&!reference->compare(before,actual,instruction,pending)){diff_failed=true;stopped=true;}
  before=actual;pending={};if(instruction==0x00100073)stopped=true;
}
struct Memory {
  std::vector<uint8_t> ram=std::vector<uint8_t>(128*1024*1024,0);
  std::array<uint8_t,8> uart_regs{};
  uint32_t mailbox_code=~0u;bool mailbox=false;
  uint32_t read(uint32_t address){
    address&=~3u;
    if(address>=0x80000000u&&uint64_t(address)+4<=0x88000000ull){uint32_t value;std::memcpy(&value,ram.data()+address-0x80000000u,4);return value;}
    if(address>=0x10000000u&&address<0x10000008u){uint32_t result=0;for(unsigned b=0;b<4;b++){unsigned index=address-0x10000000u+b;result|=uint32_t(index==5?0x60:uart_regs[index])<<(8*b);}return result;}
    if(address==0x30000000)return 0x800002b7u; // reset trampoline for fixed-reset gate-level profile
    if(address==0x30000004)return 0x00028067u;
    throw std::runtime_error("FAST_READ_RANGE");
  }
  void write(uint32_t address,uint32_t value,unsigned mask){
    address&=~3u;
    if(address>=0x80000000u&&uint64_t(address)+4<=0x88000000ull){for(unsigned b=0;b<4;b++)if(mask&(1u<<b))ram[address-0x80000000u+b]=uint8_t(value>>(8*b));return;}
    if(address>=0x10000000u&&address<0x10000008u){for(unsigned b=0;b<4;b++)if(mask&(1u<<b)){unsigned index=address-0x10000000u+b;uint8_t byte=value>>(8*b);if(index==0&&!(uart_regs[3]&128)){uart+=char(byte);std::putchar(byte);}else uart_regs[index]=byte;}return;}
    if(address==0x10001000&&mask==15){mailbox_code=value;return;}
    if(address==0x10001004&&mask==15&&value==0xb00d600d){mailbox=true;return;}
    throw std::runtime_error("FAST_WRITE_RANGE");
  }
};
static std::vector<uint8_t> load(const std::string&path){std::ifstream f(path,std::ios::binary|std::ios::ate);if(!f)throw std::runtime_error("IMAGE_OPEN");auto n=f.tellg();if(n<=0||n>128*1024*1024)throw std::runtime_error("IMAGE_SIZE");std::vector<uint8_t>b(n);f.seekg(0);f.read(reinterpret_cast<char*>(b.data()),n);if(!f)throw std::runtime_error("IMAGE_READ");return b;}
int main(int argc,char**argv){
  try{
    std::string image,ref,report,trace;uint64_t limit=2000000000;unsigned seed=0x2607b309,max_delay=2;bool no_diff=false;
    for(int i=1;i<argc;i++){std::string a=argv[i];auto value=[&](){if(++i>=argc)throw std::runtime_error("ARGUMENT");return std::string(argv[i]);};
      if(a=="--image")image=value();else if(a=="--ref")ref=value();else if(a=="--report")report=value();else if(a=="--trace")trace=value();
      else if(a=="--max-cycles")limit=std::stoull(value());else if(a=="--seed")seed=std::stoul(value(),nullptr,0);else if(a=="--delay")max_delay=std::stoul(value());else if(a=="--no-diff")no_diff=true;else throw std::runtime_error("UNKNOWN_ARGUMENT");}
    if(image.empty()||report.empty()||(ref.empty()&&!no_diff)||(!ref.empty()&&no_diff)||max_delay>100)throw std::runtime_error("CONFIGURATION");
    auto bytes=load(image);Memory memory;std::copy(bytes.begin(),bytes.end(),memory.ram.begin());
    before.pc=0x80000000;std::vector<uint8_t>rom(4096,0),flash(16*1024*1024,0xff);
    uint32_t trampoline[2]={0x800002b7,0x00028067};std::memcpy(flash.data(),trampoline,8);
    if(!no_diff){reference=std::make_unique<Reference>(ref,before.pc,rom,flash);reference->load(0x80000000,bytes);}
    if(!trace.empty()){performance.stream=std::fopen(trace.c_str(),"wb");if(!performance.stream)throw std::runtime_error("TRACE_OPEN");}
    VerilatedContext context;context.commandArgs(argc,argv);Vysyx_00000000 d{&context};
    d.clock=0;d.reset=1;d.io_interrupt=0;
    d.io_slave_awvalid=d.io_slave_wvalid=d.io_slave_bready=d.io_slave_arvalid=d.io_slave_rready=0;
    d.io_slave_awaddr=d.io_slave_awid=d.io_slave_awlen=d.io_slave_awsize=d.io_slave_awburst=0;
    d.io_slave_wdata=d.io_slave_wstrb=d.io_slave_wlast=d.io_slave_araddr=d.io_slave_arid=d.io_slave_arlen=d.io_slave_arsize=d.io_slave_arburst=0;
    d.io_master_arready=d.io_master_awready=d.io_master_wready=d.io_master_rvalid=d.io_master_bvalid=0;
    d.io_master_rid=d.io_master_rdata=d.io_master_rresp=d.io_master_rlast=d.io_master_bid=d.io_master_bresp=0;
    auto edge=[&](bool high){context.timeInc(1);d.clock=high;d.eval();};
    for(unsigned i=0;i<16;i++){edge(true);edge(false);}d.reset=0;d.eval();
    bool read=false,aw=false,w=false,b=false;uint32_t raddr=0,waddr=0,wdata=0;unsigned rid=0,wid=0,mask=0,rlen=0,rbeat=0,delay=0,rsize=2;
    auto rng=[&](){seed^=seed<<13;seed^=seed>>17;seed^=seed<<5;return seed;};
    auto start=std::chrono::steady_clock::now();
    while(!stopped&&cycles<limit){
      d.io_master_arready=!read&&!aw&&!w&&!b&&(rng()%4!=0);
      d.io_master_awready=!read&&!aw&&!b&&(rng()%4!=0);d.io_master_wready=!read&&!w&&!b&&(rng()%4!=0);
      d.io_master_rvalid=read&&delay==0;d.io_master_rdata=read?memory.read(raddr+(rbeat<<rsize)):0;
      d.io_master_rid=rid;d.io_master_rresp=0;d.io_master_rlast=rbeat==rlen;
      d.io_master_bvalid=b;d.io_master_bid=wid;d.io_master_bresp=0;d.eval();
      bool arfire=d.io_master_arvalid&&d.io_master_arready,rpop=d.io_master_rvalid&&d.io_master_rready;
      bool awfire=d.io_master_awvalid&&d.io_master_awready,wfire=d.io_master_wvalid&&d.io_master_wready,bpop=d.io_master_bvalid&&d.io_master_bready;
      uint32_t ra=d.io_master_araddr,wa=d.io_master_awaddr,wd=d.io_master_wdata;unsigned ri=d.io_master_arid,rl=d.io_master_arlen,rs=d.io_master_arsize,wi=d.io_master_awid,wm=d.io_master_wstrb;
      edge(true);edge(false);cycles++;
      if(arfire){read=true;raddr=ra;rid=ri;rlen=rl;rsize=rs;rbeat=0;delay=max_delay?rng()%(max_delay+1):0;}
      else if(rpop){if(rbeat==rlen)read=false;else{rbeat++;delay=max_delay?rng()%(max_delay+1):0;}}
      else if(read&&delay)delay--;
      if(awfire){aw=true;waddr=wa;wid=wi;}if(wfire){w=true;wdata=wd;mask=wm;}
      if(aw&&w&&!b){memory.write(waddr,wdata,mask);b=true;}
      if(bpop){b=false;aw=false;w=false;}
    }
    auto seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
    std::string result=fault?"NPC_FAULT":diff_failed?"DIFF_FAIL":!stopped?"CYCLE_LIMIT":gpr[10]?"BAD_TRAP":"GOOD_TRAP";
    int rc=fault?3:diff_failed?1:!stopped?124:gpr[10]?1:0;
    if(!rc&&(!memory.mailbox||memory.mailbox_code!=gpr[10]))throw std::runtime_error("EXIT_MAILBOX_MISSING");
    std::ofstream out(report);out<<"{\"result\":\""<<result<<"\",\"cycles\":"<<cycles<<",\"instructions\":"<<retired<<",\"a0\":"<<gpr[10]<<",\"fault\":"<<fault<<",\"pc\":"<<pc<<",\"instruction\":"<<inst<<",\"diff_enabled\":"<<(reference?"true":"false")<<",\"diff_checked\":"<<(reference?reference->checked:0)<<",\"device_sync_checked\":"<<(reference?reference->devices:0)<<",\"wall_seconds\":"<<seconds<<",\"ecalls\":"<<ecalls<<",\"mrets\":"<<mrets<<",\"uart_hex\":\"";
    static const char hex[]="0123456789abcdef";for(unsigned char c:uart)out<<hex[c>>4]<<hex[c&15];out<<"\",\"performance\":";performance.report(out);out<<"}\n";
    if(performance.stream)std::fclose(performance.stream);std::fprintf(stderr,"FAST_%s cycles=%llu instructions=%llu seconds=%.3f\n",result.c_str(),(unsigned long long)cycles,(unsigned long long)retired,seconds);return rc;
  }catch(const std::exception&e){std::fprintf(stderr,"FAST_ERROR %s\n",e.what());return 2;}
}
