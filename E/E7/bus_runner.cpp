#include "Vminirv_bus.h"
#include "verilated.h"
#include "verilated_vcd_c.h"
#include "ref.h"
#include "memory.hpp"
#include <iostream>
#include <iomanip>
#include <memory>
struct Pending {bool active=false,read=false;uint64_t due=0;uint32_t addr=0,data=0;};
static Memory *dm;static size_t io_cursor=0;
static int ref_read(void*o,uint32_t a,unsigned n,int kind,uint32_t*v){
 try{auto*m=static_cast<Memory*>(o);if(m->contains(a,n)){*v=m->read_ram(a,n);return 0;}
  if(kind!=1||io_cursor>=dm->io_reads.size())return -1;auto ev=dm->io_reads[io_cursor++];if(ev.address!=a)return -1;*v=n==1?(ev.word>>((a&3)*8))&255:ev.word;return 0;
 }catch(...){return -1;}
}
static int ref_write(void*o,uint32_t a,unsigned n,uint32_t v){try{static_cast<Memory*>(o)->write(a,n,v);return 0;}catch(...){return -1;}}
static uint64_t number(const char*s){size_t n;auto v=std::stoull(s,&n,0);if(s[n])throw std::runtime_error("bad number");return v;}
static uint32_t lfsr(uint32_t x){return (x>>1)^((0u-(x&1u))&0xd0000001u);}
int main(int argc,char**argv){try{
 std::string image,report,trace,events,until;uint64_t max=10000000000ull,freq=100000000;uint32_t base=0x80000000,delay=1,seed=260707;unsigned mode=3,mem_mb=128,until_count=1;bool random=false,uart_random=false,inject_read=false,inject_store=false,injected=false;
 for(int i=1;i<argc;i++){std::string a=argv[i];auto value=[&](){if(i+1>=argc)throw std::runtime_error("missing value");return argv[++i];};
  if(a=="--image")image=value();else if(a=="--report")report=value();else if(a=="--trace")trace=value();else if(a=="--events")events=value();else if(a=="--base")base=number(value());
  else if(a=="--mode")mode=number(value());else if(a=="--delay")delay=number(value());else if(a=="--frequency")freq=number(value());else if(a=="--seed")seed=number(value());else if(a=="--max-cycles")max=number(value());else if(a=="--mem-mb")mem_mb=number(value());
  else if(a=="--random")random=true;else if(a=="--devices"){}else if(a=="--uart-random")uart_random=true;else if(a=="--until-output")until=value();else if(a=="--until-count")until_count=number(value());else if(a=="--inject-read-bit")inject_read=true;else if(a=="--inject-double-store")inject_store=true;else throw std::runtime_error("unknown option "+a);
 }
 if(image.empty()||mode<1||mode>3||!delay||!seed||!freq)throw std::runtime_error("invalid configuration");
 Memory dut(base,mem_mb*1024*1024),refmem(base,mem_mb*1024*1024);dut.load(image);refmem.bytes=dut.bytes;dut.devices=refmem.devices=true;dut.frequency=freq;dut.random_uart=uart_random;refmem.quiet=true;dm=&dut;
 MiniState ref;minirv_reset(&ref,base);MiniBus bus{&refmem,ref_read,ref_write};
 VerilatedContext ctx;ctx.commandArgs(argc,argv);if(!trace.empty())ctx.traceEverOn(true);Vminirv_bus d{&ctx};std::unique_ptr<VerilatedVcdC>vcd;
 if(!trace.empty()){vcd.reset(new VerilatedVcdC);d.trace(vcd.get(),8);vcd->open(trace.c_str());}
 std::ofstream eventfile;if(!events.empty()){eventfile.open(events);eventfile<<"cycle,pc,state,ifu_req,ifu_resp,lsu_req,lsu_resp,lsu_wen,lsu_addr,commit,commit_inst\n";}
 d.reset=1;d.clock=0;d.io_ifu_respValid=0;d.io_lsu_respValid=0;d.io_ifu_rdata=0;d.io_lsu_rdata=0;d.eval();d.clock=1;d.eval();d.reset=0;
 Pending ip,lp;uint64_t cycles=0,commits=0,irequests=0,lrequests=0,responses=0,refcycle=0;std::string result="CYCLE_LIMIT";int rc=124;size_t cursor=0,matches=0;
 auto begin=std::chrono::steady_clock::now();
 auto latency=[&](){seed=lfsr(seed);return random?1+(seed%31):delay;};
 for(;cycles<max;){
  cycles++;dut.cycles=cycles;d.clock=0;d.io_ifu_respValid=0;d.io_lsu_respValid=0;
  if(ip.active&&ip.due==cycles){d.io_ifu_respValid=1;d.io_ifu_rdata=ip.data;ip.active=false;responses++;}
  if(lp.active&&lp.due==cycles){d.io_lsu_respValid=1;d.io_lsu_rdata=lp.data;if(lp.read)dut.consume_read(lp.addr,lp.data);lp.active=false;responses++;}
  d.eval();
  bool irq=d.io_ifu_reqValid,lrq=d.io_lsu_reqValid,lwrite=d.io_lsu_wen;uint32_t before_state=d.debug_state,before_pc=d.pc,laddr=d.io_lsu_addr;
  if(irq){if(ip.active)throw std::runtime_error("duplicate IFU request");ip={true,true,cycles+latency(),d.io_ifu_addr,dut.peek_word(d.io_ifu_addr,0)};irequests++;}
  if(lrq){
   if(lp.active)throw std::runtime_error("duplicate LSU request");lrequests++;
   if(d.io_lsu_wen){dut.write_mask(d.io_lsu_addr,d.io_lsu_wdata,d.io_lsu_wmask);if(inject_store&&!injected){dut.write_mask(d.io_lsu_addr,d.io_lsu_wdata,d.io_lsu_wmask);injected=true;}}
   uint32_t data=d.io_lsu_wen?0:dut.peek_word(d.io_lsu_addr,1);
   if(inject_read&&!injected&&!d.io_lsu_wen&&dut.contains(d.io_lsu_addr,4)){data^=1u<<(8*(d.io_lsu_addr&3));injected=true;}
   if(mode==1){d.io_lsu_rdata=data;if(!d.io_lsu_wen)dut.consume_read(d.io_lsu_addr,data);d.eval();}
   else if(mode==3||!d.io_lsu_wen)lp={true,!bool(d.io_lsu_wen),cycles+latency(),d.io_lsu_addr,data};
  }
  ctx.timeInc(5);if(vcd)vcd->dump(ctx.time());d.clock=1;d.eval();ctx.timeInc(5);if(vcd)vcd->dump(ctx.time());
  if(d.fault){rc=3;result="NPC_FAULT";break;}
  uint64_t next_refcycle=refcycle+1;
  if(d.commit_valid){
   uint32_t ins=refmem.read_ram(ref.pc,4);bool csr=(ins&0x707f)==0x2073;MiniEvent ev{};int err=0;
   if(csr){
    unsigned rd=(ins>>7)&31,rs=(ins>>15)&31,cs=ins>>20;uint32_t value=0;
    if(rd>=16||rs>=16)err=1;
    else if(cs==0xf11)value=0x79737978u;else if(cs==0xf12)value=26070001u;
    else if(cs==0xb00)value=uint32_t(refcycle);else if(cs==0xb80)value=uint32_t(refcycle>>32);else err=1;
    if(rs){if(cs==0xb00)next_refcycle=(refcycle&0xffffffff00000000ull)|(value|ref.r[rs]);else if(cs==0xb80)next_refcycle=(uint64_t(value|ref.r[rs])<<32)|uint32_t(refcycle);else err=1;}
    if(rd)ref.r[rd]=value;ref.pc+=4;
   }else err=minirv_step(&ref,&bus,&ev);
   bool good=!err&&d.pc==ref.pc&&io_cursor==dut.io_reads.size()&&dut.stores.size()==refmem.stores.size();
   for(unsigned j=0;j<16;j++)if(d.debug_gpr[j]!=ref.r[j]){good=false;std::cerr<<"REG_DIFF x"<<j<<" dut="<<std::hex<<d.debug_gpr[j]<<" ref="<<ref.r[j]<<std::dec<<"\n";}
   for(size_t j=0;good&&j<dut.stores.size();j++){auto a=dut.stores[j],b=refmem.stores[j];if(a.address!=b.address||a.data!=b.data||a.size!=b.size)good=false;}
   if(!good){rc=1;result="DIFF_FAIL";std::cerr<<"DIFF pc="<<std::hex<<d.commit_pc<<" inst="<<d.commit_inst<<std::dec<<" step="<<commits<<" ref_fault="<<ref.fault<<" store_events="<<dut.stores.size()<<"/"<<refmem.stores.size()<<"\n";break;}
   commits++;dut.stores.clear();refmem.stores.clear();dut.io_reads.clear();io_cursor=0;
   if(d.commit_inst==0x00100073u){rc=d.debug_gpr[10]==0?0:1;result=rc?"BAD_TRAP":"GOOD_TRAP";}
  }
  refcycle=next_refcycle;if(d.cycle_counter!=refcycle)throw std::runtime_error("mcycle differs from independent cycle count");
  if(eventfile)eventfile<<cycles<<','<<std::hex<<before_pc<<std::dec<<','<<before_state<<','<<irq<<','<<unsigned(d.io_ifu_respValid)<<','<<lrq<<','<<unsigned(d.io_lsu_respValid)<<','<<lwrite<<','<<std::hex<<laddr<<std::dec<<','<<unsigned(d.commit_valid)<<','<<std::hex<<d.commit_inst<<std::dec<<'\n';
  if(result!="CYCLE_LIMIT")break;
  if(!until.empty()){auto pos=dut.uart.find(until,cursor);if(pos!=std::string::npos){cursor=pos+until.size();matches++;}if(matches>=until_count){result="BOUNDED_OUTPUT_OBSERVATION";rc=0;break;}}
 }
 double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count();
 std::cerr<<result<<" cycles="<<cycles<<" instructions="<<commits<<" IPC="<<double(commits)/cycles<<" wall="<<seconds<<"\n";
 if(!report.empty()){std::ofstream f(report);f<<"{\"result\":\""<<result<<"\",\"exit_code\":"<<rc<<",\"cycles\":"<<cycles<<",\"instructions\":"<<commits<<",\"ipc\":"<<std::setprecision(12)<<double(commits)/cycles<<",\"ifu_requests\":"<<irequests<<",\"lsu_requests\":"<<lrequests<<",\"responses\":"<<responses<<",\"wall_seconds\":"<<seconds<<",\"frequency_hz\":"<<freq<<",\"mode\":"<<mode<<",\"delay\":"<<delay<<",\"random_memory_delay\":"<<(random?"true":"false")<<",\"uart_bytes\":"<<dut.uart_writes<<",\"counter\":"<<d.cycle_counter<<",\"fault\":"<<unsigned(d.fault)<<",\"gpr\":[";for(int i=0;i<16;i++){if(i)f<<',';f<<d.debug_gpr[i];}f<<"]}\n";}
 if(vcd){vcd->close();}d.final();return rc;
 }catch(const std::exception&e){std::cerr<<"BUS_SIM_ERROR "<<e.what()<<"\n";return 2;}}
