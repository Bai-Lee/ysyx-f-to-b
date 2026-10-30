#include "Vnpc_sim.h"
#include "Vnpc_sim__Dpi.h"
#include "verilated.h"
#include "ref.h"
#include "memory.hpp"
#include <memory>
#include <tuple>
#include <sstream>
#include <iomanip>
static Memory *dut_memory,*ref_memory;
static bool stopped=false;static unsigned stop_calls=0;static uint32_t stop_code=0,stop_pc=0;
static std::string memory_error;
// A bounded cache avoids allocating/freeing map nodes on every simulated cycle.
// Overflow is an explicit simulator error; no read or assertion is skipped.
struct ReadEntry { uint64_t cycle;int kind;uint32_t address,value; };
static ReadEntry cache[32];static unsigned cache_size=0;
static ReadEntry* cached(uint64_t cycle,int kind,uint32_t address){
  for(unsigned i=0;i<cache_size;i++)if(cache[i].cycle==cycle&&cache[i].kind==kind&&cache[i].address==address)return &cache[i];
  return nullptr;
}
static size_t ref_io_cursor=0;
unsigned int pmem_read(unsigned int a,int kind,unsigned long long cycle){
  try{
    auto*it=cached(cycle,kind,a);if(it)return it->value;
    if(cache_size==32)throw std::runtime_error("read-cache overflow");
    uint32_t v=dut_memory->peek_word(a,kind);cache[cache_size++]={cycle,kind,a,v};return v;
  }catch(const std::exception&e){memory_error=e.what();return 0;}
}
void pmem_write(unsigned int a,unsigned int d,unsigned char mask,unsigned long long cycle){
  (void)cycle;try{dut_memory->write_mask(a,d,mask);}catch(const std::exception&e){memory_error=e.what();}
}
void pmem_load_commit(unsigned int a,unsigned int pc,unsigned long long cycle){
  (void)pc;try{auto*it=cached(cycle,1,a);if(!it)throw std::runtime_error("load committed without settled read");dut_memory->consume_read(a,it->value);}catch(const std::exception&e){memory_error=e.what();}
}
void npc_finish(unsigned int pc,unsigned int code){stopped=true;stop_calls++;stop_pc=pc;stop_code=code;}
static int reference_read(void*opaque,uint32_t a,unsigned n,int kind,uint32_t*out){
  auto*m=static_cast<Memory*>(opaque);
  try{
    if(m->contains(a,n)){*out=m->read_ram(a,n);return 0;}
    if(kind!=1||!m->device(a&~3u)||ref_io_cursor>=dut_memory->io_reads.size())return -1;
    auto ev=dut_memory->io_reads[ref_io_cursor++];if(ev.address!=a)return -1;
    *out=n==1?(ev.word>>(8*(a&3)))&255:ev.word;return 0;
  }catch(...){return -1;}
}
static int reference_write(void*opaque,uint32_t a,unsigned n,uint32_t value){
  auto*m=static_cast<Memory*>(opaque);try{m->write(a,n,value);return 0;}catch(...){return -1;}
}
static bool compare(Vnpc_sim&d,MiniState&r,uint64_t step){
  bool ok=true;
  if(d.pc!=r.pc){fprintf(stderr,"DIFF step=%llu pc_before=%08x inst=%08x PC dut=%08x ref=%08x\n",(unsigned long long)step,d.commit_pc,d.commit_inst,d.pc,r.pc);ok=false;}
  for(unsigned i=0;i<16;i++)if(d.debug_gpr[i]!=r.r[i]){fprintf(stderr,"DIFF step=%llu pc_before=%08x inst=%08x x%u dut=%08x ref=%08x\n",(unsigned long long)step,d.commit_pc,d.commit_inst,i,d.debug_gpr[i],r.r[i]);ok=false;}
  if(dut_memory->stores.size()!=ref_memory->stores.size())ok=false;
  else for(size_t i=0;i<dut_memory->stores.size();i++){auto a=dut_memory->stores[i],b=ref_memory->stores[i];if(a.address!=b.address||a.size!=b.size||a.data!=b.data)ok=false;}
  if(!ok)fprintf(stderr,"DIFF transactions dut=%zu ref=%zu\n",dut_memory->stores.size(),ref_memory->stores.size());
  return ok;
}
static uint64_t integer(const char*s){size_t used=0;auto v=std::stoull(s,&used,0);if(s[used])throw std::runtime_error("bad numeric argument");return v;}
int main(int argc,char**argv){
 try{
  std::string image,report,trace_path,until_output;uint32_t base=0,expect=0;uint64_t limit=100000000,steps=0,freq=100000000,offset=0;size_t mem_mb=1,until_count=1;
  bool devices=false,random_uart=false,wall=false,no_diff=false;
  for(int i=1;i<argc;i++){
    std::string a=argv[i];auto value=[&](){if(i+1>=argc)throw std::runtime_error("missing option value");return argv[++i];};
    if(a=="--image")image=value();else if(a=="--report")report=value();else if(a=="--trace")trace_path=value();
    else if(a=="--base")base=uint32_t(integer(value()));else if(a=="--expect")expect=uint32_t(integer(value()));
    else if(a=="--max-cycles")limit=integer(value());else if(a=="--steps")steps=integer(value());
    else if(a=="--mem-mb")mem_mb=integer(value());else if(a=="--frequency")freq=integer(value());
    else if(a=="--timer-offset")offset=integer(value());else if(a=="--until-output")until_output=value();else if(a=="--until-count")until_count=integer(value());else if(a=="--devices")devices=true;
    else if(a=="--uart-random")random_uart=true;else if(a=="--wall-timer")wall=true;else if(a=="--no-diff")no_diff=true;
    else throw std::runtime_error("unknown option: "+a);
  }
  if(image.empty()||!freq||mem_mb<1||mem_mb>256)throw std::runtime_error("invalid run configuration");
  Memory dm(base,mem_mb*1024*1024),rm(base,mem_mb*1024*1024);dm.load(image);rm.bytes=dm.bytes;
  dm.devices=rm.devices=devices;dm.random_uart=random_uart;dm.frequency=freq;dm.wall_timer=wall;dm.timer_offset=offset;rm.quiet=true;
  dut_memory=&dm;ref_memory=&rm;
  MiniState ref;minirv_reset(&ref,base);MiniBus bus{&rm,reference_read,reference_write};
  VerilatedContext ctx;ctx.commandArgs(argc,argv);Vnpc_sim d{&ctx};d.clock=0;d.reset=1;d.sim_cycle=0;d.eval();d.clock=1;d.eval();d.reset=0;
  if(d.pc!=base)throw std::runtime_error("reset PC does not match image base");
  FILE*trace=trace_path.empty()?nullptr:fopen(trace_path.c_str(),"w");if(!trace_path.empty()&&!trace)throw std::runtime_error("trace open failed");
  uint64_t cycles=0,commits=0,expected_loads=0;int rc=0;std::string result="NOT_RUN";auto start=std::chrono::steady_clock::now();
  size_t output_cursor=0,output_matches=0;bool observed=false;
  for(;cycles<limit;){
    cycles++;dm.cycles=cycles;cache_size=0;dm.stores.clear();rm.stores.clear();dm.io_reads.clear();ref_io_cursor=0;
    d.sim_cycle=cycles;d.clock=0;ctx.timeInc(5);d.eval();d.clock=1;ctx.timeInc(5);d.eval();
    if(!memory_error.empty()){fprintf(stderr,"MEMORY_ERROR pc=%08x %s\n",d.commit_pc,memory_error.c_str());rc=3;result="MEMORY_ERROR";break;}
    if(d.fault){fprintf(stderr,"NPC_FAULT pc=%08x code=%u\n",d.pc,d.fault);rc=3;result="NPC_FAULT";break;}
    if(d.commit_valid){
      MiniEvent ev{};
      if(!no_diff&&(minirv_step(&ref,&bus,&ev)||!compare(d,ref,commits)||ref_io_cursor!=dm.io_reads.size())){fprintf(stderr,"REFERENCE_OR_DIFF_FAILURE pc=%08x fault=%u\n",ev.pc,ref.fault);rc=1;result="DIFF_FAIL";break;}
      if(!no_diff){expected_loads+=ev.load;if(expected_loads!=dm.read_commits){rc=1;result="LOAD_TRANSACTION_MISMATCH";break;}}
      commits++;
      if(trace){fprintf(trace,"%llu,%08x,%08x,%08x",(unsigned long long)commits,d.commit_pc,d.commit_inst,d.pc);for(int r=0;r<16;r++)fprintf(trace,",%08x",d.debug_gpr[r]);fputc('\n',trace);}
    }
    if(stopped){rc=stop_code==expect&&stop_calls==1?0:1;result=rc?"BAD_TRAP":expect?"EXPECTED_TRAP":"GOOD_TRAP";break;}
    if(!until_output.empty()){
      auto pos=dm.uart.find(until_output,output_cursor);
      if(pos!=std::string::npos){output_cursor=pos+until_output.size();output_matches++;}
      if(output_matches>=until_count){observed=true;result="BOUNDED_OUTPUT_OBSERVATION";break;}
    }
    if(steps&&commits>=steps){rc=d.debug_gpr[10]==expect?0:1;result=rc?"BAD_BOUND_OBSERVATION":"REQUESTED_STEPS_COMPLETE";break;}
  }
  if(!stopped&&!observed&&!(steps&&commits>=steps)&&rc==0){rc=124;result="CYCLE_LIMIT";}
  if(stopped){
    uint32_t finalpc=d.pc;uint64_t finalwrites=dm.writes;
    for(int i=0;i<4;i++){d.sim_cycle=cycles+1+i;d.clock=0;d.eval();d.eval();d.clock=1;d.eval();d.eval();}
    if(stop_calls!=1||d.commit_valid||d.pc!=finalpc||dm.writes!=finalwrites){rc=1;result="POST_HALT_SIDE_EFFECT";}
  }
  double wall_seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  fprintf(stderr,"%s pc=%08x a0=%u expected=%u cycles=%llu instructions=%llu dpi_ebreak_calls=%u wall=%.6f\n",result.c_str(),stopped?stop_pc:d.pc,d.debug_gpr[10],expect,(unsigned long long)cycles,(unsigned long long)commits,stop_calls,wall_seconds);
  if(!report.empty()){
    std::ofstream o(report);o<<"{\"result\":\""<<result<<"\",\"exit_code\":"<<rc<<",\"pc\":"<<d.pc<<",\"a0\":"<<d.debug_gpr[10]<<",\"cycles\":"<<cycles<<",\"instructions\":"<<commits<<",\"frequency_hz\":"<<freq<<",\"wall_seconds\":"<<std::setprecision(12)<<wall_seconds<<",\"ebreak_calls\":"<<stop_calls<<",\"memory_writes\":"<<dm.writes<<",\"load_commits\":"<<dm.read_commits<<",\"uart_bytes\":"<<dm.uart_writes<<",\"uart_polls\":"<<dm.status_reads<<",\"uart_not_ready\":"<<dm.status_not_ready<<",\"gpr\":[";
    for(int i=0;i<16;i++){if(i)o<<',';o<<d.debug_gpr[i];}o<<"]}\n";
  }
  if(trace)fclose(trace);d.final();return rc;
 }catch(const std::exception&e){fprintf(stderr,"SIMULATOR_ERROR %s\n",e.what());return 2;}
}
