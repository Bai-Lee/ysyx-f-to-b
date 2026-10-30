#include "memory.hpp"
#include <cassert>
int main(){
  for(unsigned mask=0;mask<16;mask++){
    Memory m(0,64);std::fill(m.bytes.begin(),m.bytes.end(),0xaa);m.write_mask(35,0x44332211,mask);
    for(unsigned i=0;i<4;i++)assert(m.bytes[32+i]==((mask&(1u<<i))?0x11u*(i+1):0xaa));
    assert(m.bytes[31]==0xaa&&m.bytes[36]==0xaa&&m.writes==unsigned(mask!=0));
    assert(m.peek_word(35,1)==m.read_ram(32,4));
  }
  puts("PASS all16 bus write masks, aligned reads, neighbor preservation");
}
