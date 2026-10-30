#ifndef D_MEMORY_HPP
#define D_MEMORY_HPP
#include <cstdint>
#include <vector>
#include <string>
#include <fstream>
#include <chrono>
#include <stdexcept>
#include <cstdio>
class Memory {
public:
  static constexpr uint32_t base=0x80000000u;
  std::vector<uint8_t> bytes=std::vector<uint8_t>(128*1024*1024,0);
  uint64_t cycles=0,frequency=100000000,timer_offset=0,timer_latch=0,timer_sample=0;
  uint64_t writes=0,reads=0,uart_bytes=0,status_reads=0,status_not_ready=0;
  uint32_t rng=0x2607d8;bool random_uart=false,wall_timer=false,armed=true,latch_valid=false;
  std::string uart;
  std::chrono::steady_clock::time_point start=std::chrono::steady_clock::now();
  bool contains(uint32_t a,size_t n)const{return a>=base && uint64_t(a)-base+n<=bytes.size();}
  bool device(uint32_t a)const{return a==0x10000000u||a==0x10000004u||a==0x20000000u||a==0x20000004u;}
  static uint32_t advance(uint32_t x){x^=x<<13;x^=x>>17;x^=x<<5;return x;}
  void load(const std::string &path){
    std::ifstream f(path,std::ios::binary);if(!f)throw std::runtime_error("image open failed");
    f.seekg(0,std::ios::end);auto length=f.tellg();
    if(length<=0||uint64_t(length)>bytes.size())throw std::runtime_error("image length outside RAM budget");
    f.seekg(0);f.read(reinterpret_cast<char*>(bytes.data()),length);if(!f)throw std::runtime_error("image short read");
  }
  uint32_t read_ram(uint32_t a,unsigned n)const{
    if(!contains(a,n)||!(n==1||n==2||n==4))throw std::runtime_error("RAM read outside range or bad width");
    uint32_t value=0;for(unsigned i=0;i<n;i++)value|=uint32_t(bytes[a-base+i])<<(8*i);
    return value;
  }
  uint64_t time_us()const{
    if(wall_timer)return timer_offset+uint64_t(std::chrono::duration_cast<std::chrono::microseconds>(std::chrono::steady_clock::now()-start).count());
    return timer_offset+uint64_t((__uint128_t(cycles)*1000000)/frequency);
  }
  uint32_t peek(uint32_t a,unsigned n,int kind){
    if(contains(a,n))return read_ram(a,n);
    if(kind!=1||!device(a)||n!=4)throw std::runtime_error("unmapped, non-executable or wrong-width MMIO read");
    if(a==0x10000004u)return random_uart?((advance(rng)&7)==0):1;
    if(a==0x20000000u){timer_sample=time_us();return uint32_t(timer_sample);}
    if(a==0x20000004u)return uint32_t((latch_valid?timer_latch:time_us())>>32);
    throw std::runtime_error("UART data is write-only");
  }
  void consume(uint32_t a,unsigned n,uint32_t value){
    reads++;if(contains(a,n))return;
    if(!device(a)||n!=4)throw std::runtime_error("bad committed device read");
    if(a==0x10000004u){status_reads++;if(random_uart)rng=advance(rng);armed=value!=0;if(!armed)status_not_ready++;}
    if(a==0x20000000u){timer_latch=timer_sample;latch_valid=true;}
  }
  void write(uint32_t a,unsigned n,uint32_t value){
    if(!(n==1||n==2||n==4))throw std::runtime_error("bad write width");
    if(contains(a,n))for(unsigned i=0;i<n;i++)bytes[a-base+i]=uint8_t(value>>(8*i));
    else if(a==0x10000000u&&(n==1||n==4)){
      if(random_uart&&!armed)throw std::runtime_error("UART write while not ready");
      uart+=char(value&255);uart_bytes++;armed=!random_uart;std::fputc(int(value&255),stdout);std::fflush(stdout);
    }else throw std::runtime_error("unmapped or read-only memory write");
    writes++;
  }
};
#endif
