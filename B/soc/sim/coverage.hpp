#pragma once
#include <array>
#include <cstdint>
#include <stdexcept>
#include <vector>
class MemoryCoverage {
  uint64_t start=0,length=0;
  std::vector<uint8_t> reads,writes;
public:
  uint64_t read_bytes=0,write_bytes=0;
  std::array<uint64_t,3> read_ops{},write_ops{};
  void configure(uint64_t base,uint64_t size){
    if(size>128ull*1024*1024||base+size>0x100000000ull)throw std::runtime_error("COVERAGE_RANGE");
    start=base;length=size;reads.assign((size+7)/8,0);writes.assign((size+7)/8,0);
  }
  void observe(uint32_t address,unsigned size,bool write){
    if(!length||uint64_t(address)+size<=start||address>=start+length)return;
    (write?write_ops:read_ops)[size==1?0:size==2?1:2]++;
    for(unsigned i=0;i<size;i++){
      uint64_t at=uint64_t(address)+i;if(at<start||at>=start+length)continue;
      auto offset=at-start;auto mask=uint8_t(1u<<(offset&7));auto &bits=write?writes:reads;
      if(!(bits[offset>>3]&mask)){bits[offset>>3]|=mask;(write?write_bytes:read_bytes)++;}
    }
  }
};
