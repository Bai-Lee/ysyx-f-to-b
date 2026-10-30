#ifndef E8_PROFILE_MEMORY_HPP
#define E8_PROFILE_MEMORY_HPP
#include "memory_model.hpp"
#include <chrono>
class ProfileMemory: public GateMemory {
 std::chrono::steady_clock::time_point start=std::chrono::steady_clock::now();
 std::ofstream progress;
 size_t uart_position=0;
 std::string line;
 void note(const char* event,const std::string& text="") {
  if(progress) { progress<<cycles<<'\t'<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<'\t'<<event<<'\t'<<text<<'\n';progress.flush(); }
 }
public:
 void open_profile(const std::string& path){progress.open(path);progress<<"cycles\twall_seconds\tevent\ttext\n";note("start");}
 void tick(uint64_t c){GateMemory::tick(c);if(c%100000==0)note("progress");}
 void write(uint32_t a,uint32_t v,unsigned mask){
  GateMemory::write(a,v,mask);
  while(uart_position<memory.uart.size()) { char ch=memory.uart[uart_position++];if(ch=='\n'){note("uart",line);line.clear();}else if(ch=='\t')line+="\\t";else if(ch!='\r')line+=ch; }
 }
 void report(const std::string& path,int code,const std::string& result){GateMemory::report(path,code,result);note("finish",result);}
};
#endif
