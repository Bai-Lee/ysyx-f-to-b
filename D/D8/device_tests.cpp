#include "memory.hpp"
#include <cassert>
#include <iostream>
int main(){
  Memory m;m.random_uart=true;unsigned ready=0;
  for(unsigned i=0;i<100000;i++){
    auto before=m.rng;auto v=m.peek(0x10000004,4,1);assert(v==m.peek(0x10000004,4,1)&&m.rng==before);
    m.consume(0x10000004,4,v);ready+=v;
  }
  assert(ready>12000&&ready<13000);m.armed=false;
  bool caught=false;try{m.write(0x10000000,1,'!');}catch(...){caught=true;}assert(caught);
  m.armed=true;m.write(0x10000000,1,'A');assert(m.uart=="A"&&m.uart_bytes==1&&!m.armed);
  m.frequency=1000000;m.timer_offset=0xffffffffull-2;m.cycles=1;
  uint32_t lo=m.peek(0x20000000,4,1);m.consume(0x20000000,4,lo);m.cycles=10;
  assert(lo==0xfffffffeu&&m.peek(0x20000004,4,1)==0);
  lo=m.peek(0x20000000,4,1);m.consume(0x20000000,4,lo);assert(lo==7&&m.peek(0x20000004,4,1)==1);
  m.frequency=100000000;m.timer_offset=0;m.cycles=123456789;assert(m.time_us()==1234567);
  m.frequency=1000000000;assert(m.time_us()==123456);
  m.write(0x80000000,4,0x11223344);m.write(0x80000001,1,0xaa);assert(m.read_ram(0x80000000,4)==0x1122aa44);
  m.write(0x87ffffff,1,0xfe);assert(m.read_ram(0x87ffffff,1)==0xfe);
  caught=false;try{m.read_ram(0x87ffffff,4);}catch(...){caught=true;}assert(caught);
  caught=false;try{m.peek(0x20000000,4,0);}catch(...){caught=true;}assert(caught);
  std::cout<<"\nDEVICE_PASS polls=100000 ready="<<ready<<" rollover byte_lanes bounds executable_range\n";
}
