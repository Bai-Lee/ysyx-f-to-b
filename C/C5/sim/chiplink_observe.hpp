#pragma once
#include <array>
#include <cstdint>
#include <stdexcept>
#include <vector>
#include "coverage.hpp"
struct ChipLinkObserver {
  std::array<uint64_t,2> words{},hashes{1469598103934665603ull,1469598103934665603ull};
  std::array<std::vector<std::array<uint64_t,2>>,2> samples;
  MemoryCoverage memory;
  uint64_t reads=0,writes=0,write_bytes=0,first_cycle=0,last_cycle=0;
  uint32_t maximum_address=0;
  void configure(){memory.configure(0xc0000000,4096);}
  void word(unsigned direction,unsigned data,uint64_t cycle){
    if(direction>1)throw std::runtime_error("CHIPLINK_DIRECTION");words[direction]++;
    hashes[direction]=(hashes[direction]^data)*1099511628211ull;
    if(samples[direction].size()<64)samples[direction].push_back({cycle,data});
  }
  void access(unsigned kind,unsigned address,unsigned data,unsigned mask,uint64_t cycle){
    (void)data;
    if(kind>1||address<0xc0000000u||(address&3)||mask>15)throw std::runtime_error("REMOTE_MEMORY_OBSERVATION");
    if(!first_cycle)first_cycle=cycle;last_cycle=cycle;
    if(kind==0){reads++;memory.observe(address,4,false);}
    else{
      writes++;
      for(unsigned byte=0;byte<4;byte++)if(mask&(1u<<byte)){write_bytes++;memory.observe(address+byte,1,true);}
    }
    if(address+3>maximum_address)maximum_address=address+3;
  }
  void write(std::ostream& out)const{
    out<<"{\"words\":["<<words[0]<<','<<words[1]<<"],\"hashes\":["<<hashes[0]<<','<<hashes[1]<<"],\"samples\":[";
    for(unsigned direction=0;direction<2;direction++){
      if(direction)out<<',';out<<'[';
      for(size_t i=0;i<samples[direction].size();i++){if(i)out<<',';out<<'['<<samples[direction][i][0]<<','<<samples[direction][i][1]<<']';}out<<']';
    }
    out<<"],\"remote_read_requests\":"<<reads<<",\"remote_write_requests\":"<<writes<<",\"remote_written_bytes\":"<<write_bytes<<",\"remote_unique_read_bytes\":"<<memory.read_bytes<<",\"remote_unique_written_bytes\":"<<memory.write_bytes<<",\"maximum_remote_byte_address\":"<<maximum_address<<",\"first_memory_cycle\":"<<first_cycle<<",\"last_memory_cycle\":"<<last_cycle<<"}";
  }
};
