#include "memory.hpp"
#include <cassert>
#include <iostream>
int main(){
 Memory m(0x80000000u,4096);m.devices=true;m.quiet=true;m.random_uart=true;
 unsigned ready=0;for(int i=0;i<100000;i++){
  uint32_t r=m.rng,v=m.peek_word(0x10000004,1);
  assert(m.peek_word(0x10000004,1)==v&&m.rng==r);
  m.consume_read(0x10000004,v);ready+=v;
  if(v)m.write(0x10000000,1,'A');
 }
 assert(ready>12000&&ready<13000&&m.uart_writes==ready);
 m.armed=false;bool caught=false;try{m.write(0x10000000,1,'!');}catch(...){caught=true;}assert(caught);
 m.frequency=1000000;m.timer_offset=0xffffffffull-2;m.cycles=1;
 uint32_t lo=m.peek_word(0x20000000,1);m.cycles=10;m.consume_read(0x20000000,lo);
 assert(lo==0xfffffffeu&&m.peek_word(0x20000004,1)==0);
 lo=m.peek_word(0x20000000,1);m.consume_read(0x20000000,lo);assert(lo==7&&m.peek_word(0x20000004,1)==1);
 m.frequency=100000000;m.timer_offset=0;m.cycles=123456789;assert(m.time_us()==1234567);
 m.frequency=1000000000;assert(m.time_us()==123456);
 std::cout<<"PASS side_effect_free_peek UART_ready="<<ready<<"/100000 blocked_write_rejected timer_rollover_latched cycle_scaling\n";
}
