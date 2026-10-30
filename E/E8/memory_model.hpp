#ifndef E8_MEMORY_MODEL_HPP
#define E8_MEMORY_MODEL_HPP
#include "memory.hpp"
#include <sstream>
class GateMemory {
public:
 Memory memory{0x80000000,128*1024*1024};
 bool exit_seen=false;uint32_t exit_value=0;unsigned exit_writes=0;
 std::string error;uint64_t cycles=0;
 void load(const std::string&image){memory.devices=true;memory.random_uart=true;memory.load(image);}
 uint32_t read(uint32_t a,int kind){
  if(kind==0&&a==0x30000000)return 0x800000b7u; // lui x1,0x80000
  if(kind==0&&a==0x30000004)return 0x00008067u; // jalr x0,x1,0
  auto value=memory.peek_word(a,kind);if(kind==1)memory.consume_read(a,value);return value;
 }
 void write(uint32_t a,uint32_t v,unsigned mask){
  if(a==0xf0000000u){if(mask!=15||exit_seen)throw std::runtime_error("invalid/repeated tohost transaction");exit_seen=true;exit_value=v;exit_writes++;return;}
  memory.write_mask(a,v,mask);
 }
 int status()const{return !error.empty()?-1:exit_seen?(exit_value==0?1:2):0;}
 void tick(uint64_t c){cycles=c;memory.cycles=c;memory.stores.clear();memory.io_reads.clear();}
 void report(const std::string&path,int code,const std::string&result){
  if(path.empty())return;std::ofstream f(path);f<<"{\"result\":\""<<result<<"\",\"exit_code\":"<<code<<",\"cycles\":"<<cycles<<",\"exit_writes\":"<<exit_writes<<",\"tohost_value\":"<<exit_value<<",\"uart_bytes\":"<<memory.uart_writes<<",\"uart_polls\":"<<memory.status_reads<<",\"uart_not_ready\":"<<memory.status_not_ready<<",\"memory_writes\":"<<memory.writes<<"}\n";
  std::ofstream out(path+".uart.txt",std::ios::binary);out<<memory.uart;
 }
};
#endif
