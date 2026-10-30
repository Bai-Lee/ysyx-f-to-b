#pragma once
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <dlfcn.h>
#include <stdexcept>
#include <string>
#include <vector>

struct CpuState { uint32_t r[32]{}; uint32_t pc=0; };
static_assert(sizeof(CpuState)==132,"Reference GPR/PC ABI");
struct MemoryAccess {bool valid=false,write=false;uint32_t pc=0,address=0,size=0,value=0;};
static bool reference_memory(uint32_t address,unsigned size) {
#ifdef B_STANDALONE
  constexpr uint64_t regions[][2]={{0x0f000000,0x2000},{0x20000000,0x1000},{0x30000000,0x1000000},{0x80000000,0x8000000}};
#else
  constexpr uint64_t regions[][2]={{0x0f000000,0x2000},{0x20000000,0x1000},{0x30000000,0x1000000},
    {0x80000000,0x400000},{0xa0000000,0x8000000},{0xc0000000,0x1000}};
#endif
  for(auto &r:regions)if(address>=r[0]&&uint64_t(address)+size<=r[0]+r[1])return true;
  return false;
}
static uint32_t sign_extend(uint32_t value,unsigned bits) {uint32_t sign=1u<<(bits-1);return (value^sign)-sign;}
static void validate_access(const CpuState& before,uint32_t inst,const MemoryAccess& access) {
  unsigned op=inst&127,f3=(inst>>12)&7,rs1=(inst>>15)&31,rs2=(inst>>20)&31;
  bool memory=op==3||op==0x23;
  if(memory!=access.valid)throw std::runtime_error("MEMORY_OBSERVATION_COUNT");
  if(!memory)return;
  uint32_t immediate=sign_extend(op==3?inst>>20:((inst>>25)<<5)|((inst>>7)&31),12);
  unsigned size=1u<<(f3&3);
  if(rs1>=16||size>4||access.pc!=before.pc||access.address!=before.r[rs1]+immediate||access.size!=size||access.write!=(op==0x23))throw std::runtime_error("MEMORY_ADDRESS_WIDTH_DIRECTION");
  if(access.write){
    uint32_t mask=size==4?0xffffffffu:(1u<<(8*size))-1;
    if(rs2>=16||access.value!=(before.r[rs2]&mask))throw std::runtime_error("MEMORY_STORE_DATA");
  }
}
struct Transaction {bool write;uint32_t address,data,size,strobe,error;};
class BusMonitor {
  bool read_pending=false,aw_pending=false,w_pending=false;
  uint32_t raddr=0,rsize=0,waddr=0,wsize=0,wdata=0,wstrb=0,rid=0,rlength=0,rbeat=0;
public:
  std::vector<Transaction> completed;
  BusMonitor(){completed.reserve(2);}
  void accept(unsigned channel,uint32_t address,uint32_t data,uint32_t attr){
    if(channel==0||channel==2){
      unsigned id=(attr>>15)&15,len=(attr>>7)&255,size=(attr>>4)&7,burst=(attr>>2)&3;
      if(id>1||len>7||(id==1&&len)||size>2||burst!=1||(address&((1u<<size)-1)))throw std::runtime_error("AXI4_ADDRESS_FIELDS");
      if(channel==0){if(read_pending||aw_pending||w_pending)throw std::runtime_error("AXI4_OVERLAPPING_READ");read_pending=true;raddr=address;rsize=1u<<size;rid=id;rlength=len;rbeat=0;}
      else {if(id!=1||len||aw_pending||read_pending)throw std::runtime_error("AXI4_DUPLICATE_AW");aw_pending=true;waddr=address;wsize=1u<<size;}
    } else if(channel==1){
      if(!read_pending||((attr>>3)&15)!=rid||bool(attr&4)!=(rbeat==rlength))throw std::runtime_error("AXI4_READ_RESPONSE_FIELDS");
      if(rid==1)completed.push_back({false,raddr,data,rsize,0,attr&3});
      if(rbeat==rlength)read_pending=false;else rbeat++;
    } else if(channel==3){
      if(w_pending||read_pending||!(attr&16))throw std::runtime_error("AXI4_WRITE_DATA_FIELDS");
      w_pending=true;wdata=data;wstrb=attr&15;
    } else if(channel==4){
      if(!aw_pending||!w_pending||((attr>>2)&15)!=1)throw std::runtime_error("AXI4_WRITE_RESPONSE_FIELDS");
      completed.push_back({true,waddr,wdata,wsize,wstrb,attr&3});aw_pending=w_pending=false;
    } else throw std::runtime_error("AXI4_CHANNEL");
  }
  void retire(uint32_t pc,uint32_t inst,const MemoryAccess& access){
    bool local=access.valid&&(access.address>>16)==0x0200;
    (void)pc;(void)inst;
    if(completed.size()!=(access.valid&&!local?1u:0u))throw std::runtime_error("AXI4_RETIRE_TRANSACTION_COUNT");
    if(access.valid&&!local){
      const auto& txn=completed[0];unsigned shift=8*(access.address&3);
      uint32_t mask=access.size==4?0xffffffffu:(1u<<(8*access.size))-1;
      if(txn.address!=access.address||txn.size!=access.size||txn.write!=access.write||txn.error||((txn.data>>shift)&mask)!=access.value)throw std::runtime_error("AXI4_DATA_MISMATCH");
      if(txn.write&&txn.strobe!=(((1u<<access.size)-1)<<(access.address&3)))throw std::runtime_error("AXI4_WSTRB_MISMATCH");
    }
    completed.clear();
  }
};
class Reference {
  void *handle=nullptr;
  void (*initialize)(int)=nullptr;
  void (*memory)(uint32_t,void*,size_t,bool)=nullptr;
  void (*registers)(void*,bool)=nullptr;
  void (*execute)(uint64_t)=nullptr;
  void (*tick)(int)=nullptr;
public:
  uint64_t checked=0,devices=0;
  Reference(const std::string& file,uint32_t pc,const std::vector<uint8_t>& rom,const std::vector<uint8_t>& flash,bool corrupt_rom=false){
    handle=dlopen(file.c_str(),RTLD_NOW|RTLD_LOCAL);if(!handle)throw std::runtime_error(dlerror());
    initialize=reinterpret_cast<decltype(initialize)>(dlsym(handle,"difftest_init"));
    memory=reinterpret_cast<decltype(memory)>(dlsym(handle,"difftest_memcpy"));
    registers=reinterpret_cast<decltype(registers)>(dlsym(handle,"difftest_regcpy"));
    execute=reinterpret_cast<decltype(execute)>(dlsym(handle,"difftest_exec"));
    tick=reinterpret_cast<decltype(tick)>(dlsym(handle,"b_reference_clock"));
    if(!initialize||!memory||!registers||!execute||!tick)throw std::runtime_error("REFERENCE_ABI_MISSING");
    initialize(0);memory(0x20000000,const_cast<uint8_t*>(rom.data()),rom.size(),true);
    memory(0x30000000,const_cast<uint8_t*>(flash.data()),flash.size(),true);
    if(corrupt_rom){uint32_t instruction=0;memory(0x20000000,&instruction,4,false);instruction^=0x00100000u;memory(0x20000000,&instruction,4,true);}
    CpuState state;state.pc=pc;registers(&state,true);
  }
  ~Reference(){if(handle)dlclose(handle);}
  void load(uint32_t address,const std::vector<uint8_t>& bytes){memory(address,const_cast<uint8_t*>(bytes.data()),bytes.size(),true);}
  void clock_tick(bool reset){tick(reset?1:0);}
  bool compare(const CpuState& before,const CpuState& actual,uint32_t inst,const MemoryAccess& access){
    uint32_t reference_instruction=0;memory(before.pc,&reference_instruction,4,false);
    if(reference_instruction!=inst){std::fprintf(stderr,"DIFF_INSTRUCTION pc=%08x dut=%08x ref=%08x\n",before.pc,inst,reference_instruction);return false;}
    CpuState expected;
    if(access.valid&&!reference_memory(access.address,access.size)){
      expected=before;expected.pc+=4;
      unsigned op=inst&127,rd=(inst>>7)&31,f3=(inst>>12)&7;
      if(op==3){uint32_t value=access.value;if(f3==0)value=sign_extend(value,8);if(f3==1)value=sign_extend(value,16);if(rd)expected.r[rd]=value;}
      registers(&expected,true);devices++;
    }else{
      execute(1);registers(&expected,false);checked++;
      if(access.valid){
        uint32_t value=0;memory(access.address,&value,access.size,false);
        if(value!=access.value){std::fprintf(stderr,"DIFF_MEMORY pc=%08x address=%08x dut=%08x ref=%08x\n",before.pc,access.address,access.value,value);return false;}
      }
    }
    bool ok=true;
    if(actual.pc!=expected.pc){std::fprintf(stderr,"DIFF_PC pc=%08x inst=%08x dut=%08x ref=%08x\n",before.pc,inst,actual.pc,expected.pc);ok=false;}
    for(unsigned i=0;i<32;i++)if(actual.r[i]!=expected.r[i]){std::fprintf(stderr,"DIFF_GPR pc=%08x inst=%08x x%u dut=%08x ref=%08x\n",before.pc,inst,i,actual.r[i],expected.r[i]);ok=false;}
    return ok;
  }
};
