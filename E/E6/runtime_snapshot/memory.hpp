#ifndef E_MEMORY_HPP
#define E_MEMORY_HPP
#include <cstdint>
#include <vector>
#include <string>
#include <fstream>
#include <stdexcept>
#include <chrono>
#include <cstdio>
#include <cstring>
struct StoreEvent{uint32_t address,data;unsigned size;};
struct IORead{uint32_t address,word;};
class Memory {
public:
  uint32_t base;std::vector<uint8_t> bytes;bool devices=false,quiet=false,random_uart=false;
  bool armed=true;uint32_t rng=260706;uint64_t cycles=0,frequency=100000000,timer_offset=0,timer_latch=0;
  uint64_t writes=0,read_commits=0,uart_writes=0,status_reads=0,status_not_ready=0;bool latch_valid=false,wall_timer=false;
  mutable uint64_t timer_sample=0;
  std::string uart;std::vector<StoreEvent> stores;std::vector<IORead> io_reads;
  std::chrono::steady_clock::time_point start=std::chrono::steady_clock::now();
  Memory(uint32_t b,size_t n):base(b),bytes(n,0){}
  bool contains(uint32_t a,unsigned n)const{return a>=base && uint64_t(a)-base+n<=bytes.size();}
  bool device(uint32_t a)const{return devices&&(a==0x10000000u||a==0x10000004u||a==0x20000000u||a==0x20000004u);}
  uint64_t time_us()const{return timer_offset+(wall_timer?uint64_t(std::chrono::duration_cast<std::chrono::microseconds>(std::chrono::steady_clock::now()-start).count()):uint64_t((__uint128_t(cycles)*1000000)/frequency));}
  static uint32_t advance_rng(uint32_t n){n^=n<<13;n^=n>>17;n^=n<<5;return n;}
  void load(const std::string&path){std::ifstream f(path,std::ios::binary);if(!f)throw std::runtime_error("cannot open image");f.seekg(0,std::ios::end);auto n=f.tellg();if(n<0||uint64_t(n)>bytes.size())throw std::runtime_error("image too large");f.seekg(0);f.read(reinterpret_cast<char*>(bytes.data()),n);if(!f)throw std::runtime_error("image read failed");}
  uint32_t read_ram(uint32_t a,unsigned n)const{
    if(!contains(a,n))throw std::runtime_error("unmapped memory read");uint32_t v=0;
    for(unsigned i=0;i<n;i++)v|=uint32_t(bytes[size_t(a-base)+i])<<(8*i);return v;
  }
  uint32_t peek_word(uint32_t raw,int kind)const{
    uint32_t a=raw&~3u;if(contains(a,4))return read_ram(a,4);
    if(kind==0||!device(a))throw std::runtime_error("unmapped or non-executable address");
    if(a==0x10000004u)return random_uart?((advance_rng(rng)&7)==0):1;
    if(a==0x20000000u){timer_sample=time_us();return uint32_t(timer_sample);}
    if(a==0x20000004u)return uint32_t((latch_valid?timer_latch:time_us())>>32);
    throw std::runtime_error("UART data register is write-only in this model");
  }
  void consume_read(uint32_t raw,uint32_t word){
    ++read_commits;uint32_t a=raw&~3u;
    if(contains(a,4))return;
    if(!device(a))throw std::runtime_error("invalid committed read");
    io_reads.push_back({raw,word});
    if(a==0x10000004u){status_reads++;if(random_uart)rng=advance_rng(rng);armed=word!=0;if(!armed)status_not_ready++;}
    if(a==0x20000000u){timer_latch=timer_sample;latch_valid=true;}
  }
  void write(uint32_t a,unsigned n,uint32_t v){
    if(contains(a,n)){for(unsigned i=0;i<n;i++){uint8_t byte=uint8_t(v>>(8*i));bytes[size_t(a-base)+i]=byte;stores.push_back({a+i,byte,1});}}
    else if(devices&&a==0x10000000u&&(n==1||n==4)){
      if(random_uart&&!armed)throw std::runtime_error("UART write while not ready");
      uart.push_back(char(v&255));uart_writes++;armed=!random_uart;
      if(!quiet){fputc(int(v&255),stdout);fflush(stdout);}
      stores.push_back({a,v&255,1});
    }else throw std::runtime_error("unmapped or read-only write");
    writes++;
  }
  void write_mask(uint32_t raw,uint32_t data,unsigned mask){
    uint32_t aligned=raw&~3u;
    if(mask>15)throw std::runtime_error("invalid bus mask width");
    if(!mask)return;
    if(contains(aligned,4)){
      for(unsigned i=0;i<4;i++)if(mask&(1u<<i)){uint8_t byte=uint8_t(data>>(8*i));bytes[size_t(aligned-base)+i]=byte;stores.push_back({aligned+i,byte,1});}
      writes++;return;
    }
    if(devices&&aligned==0x10000000u){if(mask&1)write(aligned,1,data&255);return;}
    throw std::runtime_error("unmapped or read-only masked write");
  }
};
#endif
