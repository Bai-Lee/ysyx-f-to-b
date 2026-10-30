#pragma once
#include <cstdint>
#include <string>
class UartDecoder {
  unsigned period=0,phase=0,index=0;
  bool previous=true;
  uint64_t next_sample=0;
  uint8_t value=0;
public:
  uint64_t frames=0,errors=0;
  std::string bytes;
  void configure(unsigned cycles_per_bit){period=cycles_per_bit;}
  void sample(uint64_t cycle,bool level){
    if(!period)return;
    if(phase==0){
      if(previous&&!level){phase=1;next_sample=cycle+period/2;value=0;index=0;}
    }else if(cycle>=next_sample){
      if(phase==1){
        if(level){errors++;phase=0;}
        else {phase=2;next_sample+=period;}
      }else if(phase==2){
        value|=uint8_t(level)<<index;index++;next_sample+=period;
        if(index==8)phase=3;
      }else{
        if(!level)errors++;
        else {frames++;if(bytes.size()<1024*1024)bytes+=char(value);}
        phase=0;
      }
    }
    previous=level;
  }
};
