#pragma once
#include <cstdint>
#include <stdexcept>
#include <vector>
struct SpiPacket {uint32_t select=0,bits=0;uint64_t tx=0,rx=0,start=0,end=0;};
class SpiObserver {
  SpiPacket pending;
public:
  uint64_t transfers=0,total_bits=0;
  std::vector<SpiPacket> captured;
  SpiObserver(){captured.reserve(1024);}
  void event(unsigned kind,unsigned select,unsigned mosi,unsigned miso,uint64_t cycle){
    if(kind==0){
      if(!pending.bits){pending.select=select;pending.start=cycle;}
      if(pending.select!=select||pending.bits>=128)throw std::runtime_error("SPI_SAMPLE_SEQUENCE");
      pending.bits++;pending.tx=(pending.tx<<1)|(mosi&1);pending.rx=(pending.rx<<1)|(miso&1);
    }else if(kind==1){
      if(!pending.bits||pending.select!=select)throw std::runtime_error("SPI_EMPTY_OR_CHANGED_SELECTION");
      pending.end=cycle;transfers++;total_bits+=pending.bits;
      if(captured.size()<1024)captured.push_back(pending);pending={};
    }else throw std::runtime_error("SPI_OBSERVATION_KIND");
  }
  unsigned incomplete_bits()const{return pending.bits;}
};
