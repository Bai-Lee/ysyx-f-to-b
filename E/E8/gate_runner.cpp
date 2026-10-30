#include "Vgate_system.h"
#include "Vgate_system__Dpi.h"
#include "verilated.h"
#include "memory_model.hpp"
#include <iostream>
#include <memory>
static std::unique_ptr<GateMemory>mem;
unsigned gate_read(unsigned addr,int kind){try{return mem->read(addr,kind);}catch(const std::exception&e){mem->error=e.what();return 0;}}
void gate_write(unsigned addr,unsigned data,unsigned char mask){try{mem->write(addr,data,mask);}catch(const std::exception&e){mem->error=e.what();}}
void gate_tick(unsigned long long count){mem->tick(count);}
int gate_status(){return mem->status();}
int main(int argc,char**argv){try{
 std::string image,report;uint64_t max=500000000;
 for(int i=1;i<argc;i++){std::string a=argv[i];if(i+1>=argc)throw std::runtime_error("missing option");if(a=="--image")image=argv[++i];else if(a=="--report")report=argv[++i];else if(a=="--max-cycles")max=std::stoull(argv[++i]);else throw std::runtime_error("unknown option");}
 mem.reset(new GateMemory);mem->load(image);VerilatedContext ctx;ctx.commandArgs(argc,argv);Vgate_system d{&ctx};d.clock=0;d.reset=1;d.eval();
 for(int i=0;i<5;i++){d.clock=0;d.eval();ctx.timeInc(1);d.clock=1;d.eval();ctx.timeInc(1);}d.reset=0;
 uint64_t n=0;for(;n<max&&!d.done;n++){d.clock=0;d.eval();ctx.timeInc(1);d.clock=1;d.eval();ctx.timeInc(1);}
 int rc=!d.done?124:d.failed?1:0;std::string result=!d.done?"CYCLE_LIMIT":d.failed?"FAIL":"GOOD_TRAP";mem->report(report,rc,result);std::cerr<<result<<" cycles="<<n<<" "<<mem->error<<"\n";d.final();return rc;
 }catch(const std::exception&e){std::cerr<<"GATE_SIM_ERROR "<<e.what()<<"\n";return 2;}}
