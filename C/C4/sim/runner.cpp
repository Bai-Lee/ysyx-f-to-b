#include "Vc4_sim.h"
#include "Vc4_sim__Dpi.h"
#include "verilated.h"
#include "memory.hpp"
#include "bus_backend.hpp"
#include "debug_core.h"
#include "trace_core.h"
#include <capstone/capstone.h>
#include <dlfcn.h>
#include <array>
#include <cstring>
#include <iostream>
#include <sstream>
#include <iomanip>
#include <memory>
#include <limits>

struct State{uint32_t r[32],pc;};
struct Reference{
  void *handle=nullptr;
  void (*init)(int)=nullptr;
  void (*copy)(uint32_t,void*,size_t,bool)=nullptr;
  void (*regs)(void*,bool)=nullptr;
  void (*exec)(uint64_t)=nullptr;
  explicit Reference(const std::string &path){
    handle=dlopen(path.c_str(),RTLD_NOW|RTLD_LOCAL);if(!handle)throw std::runtime_error(dlerror());
    init=reinterpret_cast<decltype(init)>(dlsym(handle,"difftest_init"));
    copy=reinterpret_cast<decltype(copy)>(dlsym(handle,"difftest_memcpy"));
    regs=reinterpret_cast<decltype(regs)>(dlsym(handle,"difftest_regcpy"));
    exec=reinterpret_cast<decltype(exec)>(dlsym(handle,"difftest_exec"));
    if(!init||!copy||!regs||!exec)throw std::runtime_error("incomplete NEMU reference API");
  }
  ~Reference(){if(handle)dlclose(handle);}
};
struct Access{uint32_t address,value;unsigned size;bool write;};
static std::vector<Access> accesses;
static uint64_t dpi_commits=0;
static uint32_t dpi_pc=0,dpi_inst=0,stop_pc=0,stop_code=0;
static unsigned stop_calls=0;
void c4_data_commit(unsigned address,unsigned size,unsigned value,svBit write) {
  if(!(size==1||size==2||size==4))throw std::runtime_error("COMMIT_BAD_MEMORY_WIDTH");
  uint32_t mask=size==4?0xffffffffu:(1u<<(8*size))-1;
  accesses.push_back({address,value&mask,size,bool(write)});
}
void npc_finish(unsigned pc,unsigned code){stop_calls++;stop_pc=pc;stop_code=code;}
void npc_commit(unsigned pc,unsigned instruction){dpi_commits++;dpi_pc=pc;dpi_inst=instruction;}
static uint64_t integer(const std::string &s){
  if(s.empty()||s[0]=='-')throw std::runtime_error("invalid nonnegative integer");
  size_t used=0;auto value=std::stoull(s,&used,0);if(used!=s.size())throw std::runtime_error("trailing numeric characters");return value;
}
static std::string trim(const std::string &s){auto first=s.find_first_not_of(" \t\r\n");if(first==std::string::npos)return {};return s.substr(first,s.find_last_not_of(" \t\r\n")-first+1);}
static const char *names[16]={"zero","ra","sp","gp","tp","t0","t1","t2","s0","s1","a0","a1","a2","a3","a4","a5"};
struct Debug{Vc4_sim *dut;Memory *memory;};
static bool read_reg(void *opaque,const char *name,uint32_t *value){
  auto &d=*static_cast<Debug*>(opaque)->dut;
  if(!std::strcmp(name,"pc")){*value=d.pc;return true;}
  if(!std::strcmp(name,"0")||!std::strcmp(name,"$0")){*value=0;return true;}
  if(!std::strcmp(name,"fp")){*value=d.debug_gpr[8];return true;}
  for(unsigned i=0;i<16;i++)if(!std::strcmp(name,names[i])){*value=d.debug_gpr[i];return true;}
  try{if(name[0]=='x'&&name[1]){auto i=integer(name+1);if(i<16){*value=d.debug_gpr[i];return true;}}}catch(...){return false;}
  return false;
}
static bool read_mem(void *opaque,uint32_t address,uint32_t *value){
  auto &m=*static_cast<Debug*>(opaque)->memory;if(!m.contains(address,4))return false;
  *value=m.read_ram(address,4);return true;
}
static State get_state(const Vc4_sim &d){State s{};for(unsigned i=0;i<16;i++)s.r[i]=d.debug_gpr[i];s.pc=d.pc;return s;}
static bool compare(const Vc4_sim &d,const State &r,uint64_t commit){
  bool ok=true;
  if(d.pc!=r.pc){std::fprintf(stderr,"DIFF_MISMATCH step=%llu pc=%08x instruction=%08x next_pc dut=%08x ref=%08x\n",(unsigned long long)commit,dpi_pc,dpi_inst,d.pc,r.pc);ok=false;}
  for(unsigned i=0;i<32;i++){
    uint32_t actual=i<16?d.debug_gpr[i]:0;
    if(actual!=r.r[i]){std::fprintf(stderr,"DIFF_MISMATCH step=%llu pc=%08x instruction=%08x x%u dut=%08x ref=%08x\n",(unsigned long long)commit,dpi_pc,dpi_inst,i,actual,r.r[i]);ok=false;}
  }
  return ok;
}
static uint32_t sext(uint32_t x,unsigned bits){uint32_t sign=1u<<(bits-1);return (x^sign)-sign;}
static State device_effect(const State &old,uint32_t inst,const Access &access){
  State expected=old;expected.pc+=4;unsigned op=inst&127,rd=(inst>>7)&31,rs1=(inst>>15)&31,rs2=(inst>>20)&31,f3=(inst>>12)&7;
  if(rs1>=16||!(op==3||op==0x23)||access.write!=(op==0x23))throw std::runtime_error("device synchronization opcode mismatch");
  unsigned n=1u<<(f3&3);uint32_t imm=sext(op==3?inst>>20:((inst>>25)<<5)|((inst>>7)&31),12);
  if(access.address!=old.r[rs1]+imm||access.size!=n)throw std::runtime_error("device synchronization address/width mismatch");
  if(op==3){
    if(rd>=16)throw std::runtime_error("device destination outside RV32E");
    uint32_t value=access.value;if(f3==0)value=sext(value,8);if(f3==1)value=sext(value,16);
    if(rd)expected.r[rd]=value;
  }else{
    if(rs2>=16)throw std::runtime_error("device source outside RV32E");
    uint32_t mask=n==4?0xffffffffu:(1u<<(8*n))-1;
    if(access.value!=(old.r[rs2]&mask))throw std::runtime_error("device store data mismatch");
  }
  return expected;
}
int main(int argc,char **argv){
  try{
    std::string image,ref_path,report,trace_file,elf,until;uint64_t max_cycles=1000000000,trace_limit=10000,frequency=100000000,offset=0,until_count=1;
    bool interactive=false,no_diff=false,random_uart=false,wall=false;unsigned modes=0;
    unsigned latency=1,core_delays=0;uint32_t seed=0x2607c404;bool random_delay=false,backpressure=false;

    for(int i=1;i<argc;i++){
      std::string option=argv[i];auto value=[&](){if(i+1>=argc)throw std::runtime_error("missing argument for "+option);return std::string(argv[++i]);};
      if(option=="--image")image=value();else if(option=="--ref")ref_path=value();else if(option=="--report")report=value();
      else if(option=="--elf")elf=value();else if(option=="--trace")trace_file=value();else if(option=="--trace-limit")trace_limit=integer(value());
      else if(option=="--trace-modes"){for(char c:value()){if(c=='i')modes|=1;else if(c=='m')modes|=2;else if(c=='f')modes|=4;else throw std::runtime_error("unknown trace mode");}}
      else if(option=="--max-cycles")max_cycles=integer(value());else if(option=="--frequency")frequency=integer(value());
      else if(option=="--timer-offset")offset=integer(value());else if(option=="--until-output")until=value();else if(option=="--until-count")until_count=integer(value());
      else if(option=="--latency")latency=unsigned(integer(value()));
      else if(option=="--core-delays")core_delays=unsigned(integer(value()));
      else if(option=="--seed")seed=uint32_t(integer(value()));
      else if(option=="--random-delay")random_delay=true;
      else if(option=="--backpressure")backpressure=true;
      else if(option=="--interactive")interactive=true;else if(option=="--no-diff")no_diff=true;else if(option=="--uart-random")random_uart=true;else if(option=="--wall-timer")wall=true;
      else throw std::runtime_error("unknown option "+option);
    }
    if(image.empty()||(!no_diff&&ref_path.empty())||!frequency||!max_cycles||!until_count)throw std::runtime_error("invalid run configuration");
    Memory dm;dm.load(image);dm.frequency=frequency;dm.timer_offset=offset;dm.wall_timer=wall;dm.random_uart=random_uart;
    if(!latency||latency>1000||core_delays>7)throw std::runtime_error("invalid bus delay configuration");
    BusBackend bus(dm,C4_MODE,seed);bus.latency=latency;bus.randomized_latency=random_delay;bus.backpressure=backpressure;
    VerilatedContext context;context.commandArgs(argc,argv);Vc4_sim dut{&context};dut.clock=0;dut.reset=1;dut.sim_cycle=0;dut.delay_enable=core_delays;dut.lfsr_seed=seed;
    for(unsigned i=0;i<4;i++){dut.clock=0;bus.drive(dut,0);dut.eval();dut.clock=1;dut.eval();}
    dut.clock=0;dut.reset=0;dut.eval();
    if(dut.pc!=Memory::base)throw std::runtime_error("reset PC mismatch");
    std::unique_ptr<Reference> reference;
    if(!no_diff){reference=std::make_unique<Reference>(ref_path);reference->init(0);reference->copy(Memory::base,dm.bytes.data(),dm.bytes.size(),true);State s=get_state(dut);reference->regs(&s,true);}
    csh capstone=0;if(cs_open(CS_ARCH_RISCV,CS_MODE_RISCV32,&capstone)!=CS_ERR_OK)throw std::runtime_error("Capstone initialization failed");
    cs_insn *decoded=cs_malloc(capstone);if(!decoded)throw std::runtime_error("Capstone allocation failed");
    auto assembly=[&](uint32_t pc,uint32_t inst){
      uint8_t bytes[4];std::memcpy(bytes,&inst,4);const uint8_t *code=bytes;size_t size=4;uint64_t address=pc;
      if(cs_disasm_iter(capstone,&code,&size,&address,decoded))return std::string(decoded->mnemonic)+" "+decoded->op_str;
      return std::string("<undecoded>");
    };
    char trace_error[256];dtrace_context *trace=dtrace_create(trace_file.empty()?nullptr:trace_file.c_str(),elf.empty()?nullptr:elf.c_str(),modes,trace_limit,trace_error,sizeof trace_error);
    if(!trace)throw std::runtime_error(trace_error);
    Debug debug{&dut,&dm};DExprContext expressions{read_reg,read_mem,&debug};DWatchPool watches;d_wp_init(&watches);
    uint64_t cycles=0,commits=0,checked=0,device_sync=0,expected_uart_events=0;int rc=0;std::string result="STOP";bool observed=false,watch_stop=false;
    size_t output_cursor=0,output_matches=0;auto start=std::chrono::steady_clock::now();
    auto step=[&](bool print)->bool{
      if(dut.halted||rc)return false;
      State before=get_state(dut);uint64_t prior_commits=dpi_commits;accesses.clear();
      while(true) {
        if(cycles==max_cycles){rc=124;result="CYCLE_LIMIT";return false;}
        cycles++;dm.cycles=cycles;bus.begin_cycle();dut.sim_cycle=cycles;dut.clock=0;context.timeInc(5);
        for(unsigned settle=0;settle<4;settle++){bus.drive(dut,cycles);dut.eval();}
        bus.sample(dut,cycles);dut.clock=1;context.timeInc(5);dut.eval();
        if(C4_MODE==6&&dut.uart_tx_valid){dm.uart+=char(dut.uart_tx_data);dm.uart_bytes++;dm.writes++;std::fputc(dut.uart_tx_data,stdout);std::fflush(stdout);}
        if(dut.fault){std::fprintf(stderr,"NPC_FAULT pc=%08x code=%u\n",dut.pc,dut.fault);rc=3;result="NPC_FAULT";return false;}
        if(dut.commit_valid)break;
        State waiting=get_state(dut);
        if(std::memcmp(&waiting,&before,sizeof before)||dpi_commits!=prior_commits||!accesses.empty())throw std::runtime_error("STATE_CHANGED_BEFORE_RETIREMENT");
      }
      uint32_t instruction=dut.commit_inst;
      if(dpi_commits!=prior_commits+1||dpi_pc!=before.pc||dpi_inst!=instruction||dut.commit_pc!=before.pc||dut.commit_next_pc!=dut.pc)throw std::runtime_error("DPI commit boundary mismatch");
      commits++;
      std::string disasm=(modes&1)||print?assembly(before.pc,instruction):"";
      dtrace_instruction(trace,before.pc,instruction,disasm.c_str());
      const unsigned op=instruction&127;bool mem=op==3||op==0x23;
      if(bus.completed.size()!=size_t(mem?2:1))throw std::runtime_error("WRONG_TRANSACTION_COUNT_FOR_INSTRUCTION");
      const auto &fetch=bus.completed[0];
      if(!fetch.instruction||fetch.write||fetch.error||fetch.address!=before.pc||fetch.data!=instruction)throw std::runtime_error("IFETCH_TRANSACTION_MISMATCH");
      if(accesses.size()!=size_t(mem))throw std::runtime_error("MEMORY_COMMIT_COUNT_MISMATCH");
      if(mem) {
        unsigned f3=(instruction>>12)&7,rs1=(instruction>>15)&31,rs2=(instruction>>20)&31;
        unsigned n=1u<<(f3&3);uint32_t immediate=sext(op==3?instruction>>20:((instruction>>25)<<5)|((instruction>>7)&31),12);
        uint32_t address=before.r[rs1]+immediate,mask=n==4?0xffffffffu:(1u<<(8*n))-1;
        const auto &txn=bus.completed[1];const auto &a=accesses[0];
        if(txn.instruction||txn.error||txn.write!=(op==0x23)||txn.address!=(address&~3u)||a.address!=address||a.size!=n||a.write!=txn.write)throw std::runtime_error("DATA_TRANSACTION_ADDRESS_WIDTH_MISMATCH");
        unsigned shift=8*(address&3),strobe=((1u<<n)-1)<<(address&3);
        uint32_t value=txn.write?(before.r[rs2]&mask):((txn.data>>shift)&mask);
        if(a.value!=value)throw std::runtime_error("DATA_RETURN_OR_COMMIT_MISMATCH");
        if(txn.write&&(txn.strobe!=strobe||((txn.data^(value<<shift))&(mask<<shift))))throw std::runtime_error("BUS_WRITE_LANE_MISMATCH");
        if(C4_MODE==6&&txn.write&&address==0x10000000u){expected_uart_events++;if(dm.uart_bytes!=expected_uart_events||uint8_t(dm.uart.back())!=(value&255))throw std::runtime_error("RTL_UART_SIDE_EFFECT_MISMATCH");}
      }
      if(reference){
        State expected{};bool device=!accesses.empty()&&!dm.contains(accesses[0].address,accesses[0].size);
        if(device){expected=device_effect(before,instruction,accesses[0]);reference->regs(&expected,true);device_sync++;}
        else{reference->exec(1);reference->regs(&expected,false);checked++;}
        if(!compare(dut,expected,commits)){rc=1;result="DIFF_FAIL";return false;}
        for(auto access:accesses)if(access.write&&dm.contains(access.address,access.size)){
          uint32_t data=0;reference->copy(access.address,&data,access.size,false);
          if(data!=dm.read_ram(access.address,access.size)){std::fprintf(stderr,"DIFF_MEMORY pc=%08x address=%08x\n",dpi_pc,access.address);rc=1;result="DIFF_FAIL";return false;}
        }
      }
      dtrace_commit(trace,dpi_pc,dpi_inst,dut.pc);
      for(auto access:accesses)dtrace_memory(trace,dpi_pc,access.write?'W':'R',access.address,access.size,access.value);
      bus.completed.clear();
      if(print)std::printf("STEP pc=0x%08x instruction=%08x next=0x%08x cycles=%llu %s\n",dpi_pc,dpi_inst,dut.pc,(unsigned long long)cycles,disasm.c_str());
      watch_stop=d_wp_check(&watches,&expressions,stdout);
      if(stop_calls){rc=(stop_code==0&&stop_calls==1)?0:1;result=rc?"BAD_TRAP":"GOOD_TRAP";return false;}
      if(!until.empty()){
        auto position=dm.uart.find(until,output_cursor);
        if(position!=std::string::npos){output_cursor=position+until.size();output_matches++;}
        if(output_matches>=until_count){observed=true;result="BOUNDED_OUTPUT_OBSERVATION";return false;}
      }
      return !watch_stop;
    };
    if(!interactive){while(step(false)){};}
    else{
      std::string line;
      while(std::cout<<"(npc) "&&std::getline(std::cin,line)){
        line=trim(line);if(line.empty())continue;auto split=line.find_first_of(" \t");std::string command=line.substr(0,split),args=split==std::string::npos?"":trim(line.substr(split+1));
        try{
          if(command=="q"){if(result=="STOP")result="USER_QUIT";break;}
          else if(command=="help")std::puts("c | q | si [N] | info r | info w | x N EXPR | p EXPR | w EXPR | d ID");
          else if(command=="si"||command=="c"){
            uint64_t n=command=="c"?std::numeric_limits<uint64_t>::max():(args.empty()?1:integer(args));
            if((command=="c"&&!args.empty())||(command=="si"&&(!n||n>1000000)))throw std::runtime_error("invalid step count/arguments");
            if(dut.halted||rc)std::puts("PROGRAM_ENDED");else for(uint64_t i=0;i<n;i++)if(!step(command=="si"&&n<10))break;
          }else if(command=="info"){
            if(args=="r"){for(unsigned i=0;i<16;i++)std::printf("REG x%-2u %-4s 0x%08x %u\n",i,names[i],dut.debug_gpr[i],dut.debug_gpr[i]);std::printf("PC 0x%08x\n",dut.pc);}
            else if(args=="w")d_wp_info(&watches,stdout);else throw std::runtime_error("info r|w");
          }else if(command=="p"){
            uint32_t value;char error[256];if(d_expr(args.c_str(),&expressions,&value,error,sizeof error))std::printf("EXPR_VALUE %u 0x%08x\n",value,value);else std::printf("EXPR_ERROR %s\n",error);
          }else if(command=="w"){
            char error[256];int id=d_wp_add(&watches,args.c_str(),&expressions,error,sizeof error);if(id<0)std::printf("WATCH_ERROR %s\n",error);else std::printf("WATCH_ADDED %d\n",id);
          }else if(command=="d"){
            auto id=integer(args);if(id>=32||!d_wp_delete(&watches,int(id)))throw std::runtime_error("invalid watchpoint id");std::printf("WATCH_DELETED %llu\n",(unsigned long long)id);
          }else if(command=="x"){
            auto space=args.find_first_of(" \t");if(space==std::string::npos)throw std::runtime_error("x N EXPR");
            auto n=integer(args.substr(0,space));if(!n||n>256)throw std::runtime_error("invalid scan count");
            uint32_t address;char error[256];if(!d_expr(trim(args.substr(space+1)).c_str(),&expressions,&address,error,sizeof error)){std::printf("EXPR_ERROR %s\n",error);continue;}
            for(uint64_t i=0;i<n;i++){uint32_t value;if(uint64_t(address)+4*i>UINT32_MAX||!read_mem(&debug,address+uint32_t(4*i),&value)){std::puts("MEMORY_ERROR outside RAM");break;}std::printf("MEMORY 0x%08x: 0x%08x\n",address+uint32_t(4*i),value);}
          }else throw std::runtime_error("unknown command");
        }catch(const std::exception &e){std::printf("COMMAND_ERROR %s\n",e.what());}
      }
    }
    if(stop_calls){
      uint32_t finalpc=dut.pc;auto finalwrites=dm.writes,finalcommits=dpi_commits;
      for(unsigned j=0;j<4;j++){
        dut.sim_cycle=++cycles;dm.cycles=cycles;bus.begin_cycle();dut.clock=0;bus.drive(dut,cycles);dut.eval();bus.sample(dut,cycles);dut.clock=1;dut.eval();
        if(dut.uart_tx_valid||!bus.completed.empty())throw std::runtime_error("POST_HALT_BUS_SIDE_EFFECT");
      }
      if(stop_calls!=1||dut.commit_valid||dut.pc!=finalpc||dm.writes!=finalwrites||dpi_commits!=finalcommits){rc=1;result="POST_HALT_SIDE_EFFECT";}
    }
    if(rc)dtrace_dump_ring(trace,stderr);
    double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
    std::fprintf(stderr,"%s pc=%08x a0=%u cycles=%llu instructions=%llu diff=%llu device_sync=%llu wall=%.6f\n",result.c_str(),stop_calls?stop_pc:dut.pc,dut.debug_gpr[10],(unsigned long long)cycles,(unsigned long long)commits,(unsigned long long)checked,(unsigned long long)device_sync,seconds);
    if(!report.empty()){
      std::ofstream out(report);if(!out)throw std::runtime_error("result report open failed");
      out<<"{\"mode\":"<<C4_MODE<<",\"latency\":"<<latency<<",\"random_delay\":"<<(random_delay?"true":"false")<<",\"backpressure\":"<<(backpressure?"true":"false")<<",\"seed\":"<<seed<<",\"bus_requests\":"<<bus.request_count<<",\"bus_responses\":"<<bus.response_count<<",\"mtime\":"<<uint64_t(dut.mtime)<<",\"result\":\""<<result<<"\",\"exit_code\":"<<rc<<",\"pc\":"<<dut.pc<<",\"a0\":"<<dut.debug_gpr[10]<<",\"cycles\":"<<cycles<<",\"instructions\":"<<commits<<",\"diff_enabled\":"<<(no_diff?"false":"true")<<",\"diff_checked\":"<<checked<<",\"device_sync_checked\":"<<device_sync<<",\"ebreak_calls\":"<<stop_calls<<",\"memory_writes\":"<<dm.writes<<",\"load_commits\":"<<dm.reads<<",\"uart_bytes\":"<<dm.uart_bytes<<",\"uart_polls\":"<<dm.status_reads<<",\"uart_not_ready\":"<<dm.status_not_ready<<",\"frequency_hz\":"<<frequency<<",\"wall_seconds\":"<<std::setprecision(12)<<seconds<<",\"bounded_output\":"<<(observed?"true":"false")<<",\"gpr\":[";
      for(unsigned i=0;i<16;i++){if(i)out<<',';out<<dut.debug_gpr[i];}out<<"]}\n";
    }
    dtrace_destroy(trace);cs_free(decoded,1);cs_close(&capstone);dut.final();return rc;
  }catch(const std::exception &e){std::fprintf(stderr,"SIMULATOR_ERROR %s\n",e.what());return 2;}
}
