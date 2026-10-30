"""Derive the C commit-scoped bus simulator without editing D's runner."""
from pathlib import Path
D=Path(__file__).parent;project=D.parents[1]
text=(project/'D/D8/runner.cpp').read_text().replace('Vnpc_sim','Vc4_sim')
text=text.replace('#include "memory.hpp"','#include "memory.hpp"\n#include "bus_backend.hpp"')
start=text.index('struct ReadEntry');end=text.index('void npc_finish',start)
text=text[:start]+'''static std::vector<Access> accesses;
static uint64_t dpi_commits=0;
static uint32_t dpi_pc=0,dpi_inst=0,stop_pc=0,stop_code=0;
static unsigned stop_calls=0;
void c4_data_commit(unsigned address,unsigned size,unsigned value,svBit write) {
  if(!(size==1||size==2||size==4))throw std::runtime_error("COMMIT_BAD_MEMORY_WIDTH");
  uint32_t mask=size==4?0xffffffffu:(1u<<(8*size))-1;
  accesses.push_back({address,value&mask,size,bool(write)});
}
'''+text[end:]
text=text.replace('bool interactive=false,no_diff=false,random_uart=false,wall=false;unsigned modes=0;',
'''bool interactive=false,no_diff=false,random_uart=false,wall=false;unsigned modes=0;
    unsigned latency=1,core_delays=0;uint32_t seed=0x2607c404;bool random_delay=false,backpressure=false;
''')
text=text.replace('else if(option=="--interactive")', '''else if(option=="--latency")latency=unsigned(integer(value()));
      else if(option=="--core-delays")core_delays=unsigned(integer(value()));
      else if(option=="--seed")seed=uint32_t(integer(value()));
      else if(option=="--random-delay")random_delay=true;
      else if(option=="--backpressure")backpressure=true;
      else if(option=="--interactive")''')
text=text.replace('Memory dm;memory=&dm;dm.load(image);','Memory dm;dm.load(image);')
old='VerilatedContext context;context.commandArgs(argc,argv);Vc4_sim dut{&context};dut.clock=0;dut.reset=1;dut.sim_cycle=0;dut.eval();dut.clock=1;dut.eval();dut.reset=0;'
new='''if(!latency||latency>1000||core_delays>7)throw std::runtime_error("invalid bus delay configuration");
    BusBackend bus(dm,C4_MODE,seed);bus.latency=latency;bus.randomized_latency=random_delay;bus.backpressure=backpressure;
    VerilatedContext context;context.commandArgs(argc,argv);Vc4_sim dut{&context};dut.clock=0;dut.reset=1;dut.sim_cycle=0;dut.delay_enable=core_delays;dut.lfsr_seed=seed;
    for(unsigned i=0;i<4;i++){dut.clock=0;bus.drive(dut,0);dut.eval();dut.clock=1;dut.eval();}
    dut.clock=0;dut.reset=0;dut.eval();'''
assert old in text;text=text.replace(old,new)
text=text.replace('uint64_t cycles=0,commits=0,checked=0,device_sync=0;', 'uint64_t cycles=0,commits=0,checked=0,device_sync=0,expected_uart_events=0;')
start=text.index('    auto step=[&]');end=text.index('    if(!interactive)',start)
text=text[:start]+'''    auto step=[&](bool print)->bool{
      if(dut.halted||rc)return false;
      State before=get_state(dut);uint64_t prior_commits=dpi_commits;accesses.clear();
      while(true) {
        if(cycles==max_cycles){rc=124;result="CYCLE_LIMIT";return false;}
        cycles++;dm.cycles=cycles;bus.begin_cycle();dut.sim_cycle=cycles;dut.clock=0;context.timeInc(5);
        for(unsigned settle=0;settle<4;settle++){bus.drive(dut,cycles);dut.eval();}
        bus.sample(dut,cycles);dut.clock=1;context.timeInc(5);dut.eval();
        if(C4_MODE==6&&dut.uart_tx_valid){dm.uart+=char(dut.uart_tx_data);dm.uart_bytes++;dm.writes++;std::fputc(dut.uart_tx_data,stdout);std::fflush(stdout);}
        if(dut.fault){std::fprintf(stderr,"NPC_FAULT pc=%08x code=%u\\n",dut.pc,dut.fault);rc=3;result="NPC_FAULT";return false;}
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
          if(data!=dm.read_ram(access.address,access.size)){std::fprintf(stderr,"DIFF_MEMORY pc=%08x address=%08x\\n",dpi_pc,access.address);rc=1;result="DIFF_FAIL";return false;}
        }
      }
      dtrace_commit(trace,dpi_pc,dpi_inst,dut.pc);
      for(auto access:accesses)dtrace_memory(trace,dpi_pc,access.write?'W':'R',access.address,access.size,access.value);
      bus.completed.clear();
      if(print)std::printf("STEP pc=0x%08x instruction=%08x next=0x%08x cycles=%llu %s\\n",dpi_pc,dpi_inst,dut.pc,(unsigned long long)cycles,disasm.c_str());
      watch_stop=d_wp_check(&watches,&expressions,stdout);
      if(stop_calls){rc=(stop_code==0&&stop_calls==1)?0:1;result=rc?"BAD_TRAP":"GOOD_TRAP";return false;}
      if(!until.empty()){
        auto position=dm.uart.find(until,output_cursor);
        if(position!=std::string::npos){output_cursor=position+until.size();output_matches++;}
        if(output_matches>=until_count){observed=true;result="BOUNDED_OUTPUT_OBSERVATION";return false;}
      }
      return !watch_stop;
    };
'''+text[end:]
old='for(unsigned j=0;j<4;j++){dut.sim_cycle=++cycles;dut.clock=0;dut.eval();dut.eval();dut.clock=1;dut.eval();dut.eval();}'
new='''for(unsigned j=0;j<4;j++){
        dut.sim_cycle=++cycles;dm.cycles=cycles;bus.begin_cycle();dut.clock=0;bus.drive(dut,cycles);dut.eval();bus.sample(dut,cycles);dut.clock=1;dut.eval();
        if(dut.uart_tx_valid||!bus.completed.empty())throw std::runtime_error("POST_HALT_BUS_SIDE_EFFECT");
      }'''
assert old in text;text=text.replace(old,new)
text=text.replace('out<<"{\\"result\\":\\""', 'out<<"{\\"mode\\":"<<C4_MODE<<",\\"latency\\":"<<latency<<",\\"random_delay\\":"<<(random_delay?"true":"false")<<",\\"backpressure\\":"<<(backpressure?"true":"false")<<",\\"seed\\":"<<seed<<",\\"bus_requests\\":"<<bus.request_count<<",\\"bus_responses\\":"<<bus.response_count<<",\\"mtime\\":"<<uint64_t(dut.mtime)<<",\\"result\\":\\""')
(D/'sim/runner.cpp').write_text(text,encoding='utf8',newline='\n')
print('C4_BUS_RUNNER_READY')
