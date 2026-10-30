#pragma once
#include <array>
#include <cstdint>
#include <cstdio>
#include <ostream>
#include <stdexcept>

struct Performance {
  uint64_t cycles=0,last_retire=0,ifu_requests=0,ifu_responses=0;
  uint64_t lsu_requests=0,lsu_responses=0,exu_completions=0,lsu_latency_sum=0;
  uint64_t lsu_start=0,ifu_start=0,ifu_latency_sum=0;
  std::array<uint64_t,8> classes{},class_cycles{},states{};
  std::array<uint64_t,4> ifu_absence{};
  std::array<uint64_t,6> cache_events{};
  std::array<uint64_t,16> pipeline_events{};
  std::array<uint64_t,3> fetch_latency_by_kind{};
  std::array<uint64_t,4> data_counts{},data_latency{};
  unsigned next_fetch_kind=2,pending_fetch_kind=2;
  uint64_t last_data_latency=0;
  bool data_pending=false,fetch_pending=false;
  FILE *stream=nullptr;
  static unsigned category(uint32_t instruction) {
    switch(instruction&127){case 3:return 1;case 0x23:return 2;case 0x63:return 3;
      case 0x6f:return 4;case 0x67:return 5;case 0x73:return 6;case 0x0f:return 7;default:return 0;}
  }
  void tick(unsigned state,unsigned events) {
    cycles++;if(state>=states.size())throw std::runtime_error("PERF_STATE");states[state]++;
    bool ireq=events&1,iresp=events&2,dreq=events&4,dresp=events&8;
    if(iresp){if(!fetch_pending)throw std::runtime_error("PERF_UNOWNED_FETCH");fetch_pending=false;ifu_responses++;ifu_latency_sum+=cycles-ifu_start;fetch_latency_by_kind[pending_fetch_kind]+=cycles-ifu_start;}
    if(ireq){if(fetch_pending)throw std::runtime_error("PERF_DUPLICATE_FETCH");fetch_pending=true;ifu_start=cycles;ifu_requests++;pending_fetch_kind=next_fetch_kind;}
    if(dreq){if(data_pending)throw std::runtime_error("PERF_DUPLICATE_DATA");data_pending=true;lsu_start=cycles;lsu_requests++;}
    if(dresp){if(!data_pending)throw std::runtime_error("PERF_UNOWNED_DATA");data_pending=false;lsu_responses++;last_data_latency=cycles-lsu_start;lsu_latency_sum+=last_data_latency;}
    if((events&16)&&!(events&32))exu_completions++;
    if(!iresp){
      if(state==0)ifu_absence[0]++; // request phase / upstream bus unavailable
      else if(state==1)ifu_absence[(events&256)?2:1]++; // response backpressure / waiting
      else ifu_absence[3]++; // multi-cycle backend busy with data access
    }
  }
  void cache_tick(unsigned events){
    for(unsigned i=0;i<6;i++)if(events&(1u<<i))cache_events[i]++;
    if(events&1)next_fetch_kind=events&2?0:events&4?1:2;
  }
  void memory(uint32_t address,bool write){
    bool cached=(address>=0x30000000&&address<0x31000000)||(address>=0x80000000&&address<0x80400000)||(address>=0xa0000000&&address<0xa8000000);
    unsigned group=(cached?0:2)+(write?1:0);data_counts[group]++;data_latency[group]+=last_data_latency;
  }
  void retire(uint32_t pc,uint32_t instruction,uint32_t next_pc,uint32_t address,bool memory,bool write) {
    unsigned kind=category(instruction);classes[kind]++;class_cycles[kind]+=cycles-last_retire;last_retire=cycles;
    if(stream){uint32_t words[5]={pc,instruction,next_pc,address,uint32_t(memory)|(uint32_t(write)<<1)};
      if(std::fwrite(words,sizeof words,1,stream)!=1)throw std::runtime_error("PERF_TRACE_WRITE");}
  }
  void report(std::ostream&out) {
    out<<"{\"core_cycles\":"<<cycles<<",\"ifu_requests\":"<<ifu_requests<<",\"ifu_responses\":"<<ifu_responses
       <<",\"lsu_requests\":"<<lsu_requests<<",\"lsu_responses\":"<<lsu_responses<<",\"exu_completions\":"<<exu_completions
       <<",\"ifu_latency_sum\":"<<ifu_latency_sum<<",\"lsu_latency_sum\":"<<lsu_latency_sum;
    auto array=[&](const char*name,const auto&values){out<<",\""<<name<<"\":[";for(size_t i=0;i<values.size();i++){if(i)out<<',';out<<values[i];}out<<']';};
    array("class_counts",classes);array("class_cycles",class_cycles);array("state_cycles",states);array("ifu_absence",ifu_absence);array("cache_events",cache_events);array("fetch_latency_hit_miss_bypass",fetch_latency_by_kind);array("data_counts",data_counts);array("data_latency",data_latency);array("pipeline_events",pipeline_events);out<<'}';
  }
};
