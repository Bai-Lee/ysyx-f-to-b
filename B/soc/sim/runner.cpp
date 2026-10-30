#include "VysyxSoCFull.h"
#include "VysyxSoCFull__Dpi.h"
#include "verilated.h"
#include "verilated_vcd_c.h"
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>
#include "reference.hpp"
#include "coverage.hpp"
#include "uart_decode.hpp"
#include "spi_observe.hpp"
#include "pin_observe.hpp"
#include "chiplink_observe.hpp"
#include "performance.hpp"
#ifdef C5_ENABLE_NVBOARD
#include <nvboard.h>
void nvboard_bind_all_pins(VysyxSoCFull*);
bool c5_nvboard_should_close();
#endif
#ifndef C5_START_PC
#define C5_START_PC 0x20000000u
#endif

static std::vector<uint8_t> mrom(4096,0),flash(16*1024*1024,255);
static uint64_t cycles=0,commits=0,mrom_calls=0,flash_calls=0,memories=0;
static std::array<uint64_t,5> channels{};
static std::array<uint32_t,16> registers{};
static uint32_t last_pc=0,next_pc=0,last_inst=0,fault_code=0;
static bool stopped=false;
static FILE *trace=nullptr;
static uint64_t trace_limit=10000,trace_rows=0;
static CpuState before_state;
static MemoryAccess pending_access;
static BusMonitor bus;
static std::unique_ptr<Reference> reference;
void b_clock(svBit reset_active){if(reference)reference->clock_tick(reset_active);}
static bool diff_failed=false;
static Performance performance;
void b_perf_tick(unsigned state,unsigned events){performance.tick(state,events);}
void b_cache_tick(unsigned events){performance.cache_tick(events);}
void b_pipeline_tick(unsigned events){for(unsigned i=0;i<16;i++)if(events&(1u<<i))performance.pipeline_events[i]++;}
static MemoryCoverage coverage;
static UartDecoder uart_decoder;
static SpiObserver spi_observer;
static PinObserver pin_observer;
static UartDecoder uart_rx_decoder;
static ChipLinkObserver chiplink_observer;
void c5_chiplink_word(unsigned direction,unsigned data){chiplink_observer.word(direction,data,cycles);}
void c5_remote_memory(unsigned kind,unsigned address,unsigned data,unsigned mask){chiplink_observer.access(kind,address,data,mask,cycles);}
static std::array<uint64_t,7> retired_regions{};
static std::array<uint64_t,4> psram_commands{};
static uint64_t psram_read_bytes=0,psram_write_bytes=0,psram_qpi_entries=0,psram_qpi_exits=0;
static uint32_t psram_max_address=0;
static std::array<uint64_t,4> sdram_reads{},sdram_writes{};
static std::array<uint32_t,4> sdram_max_address{};
static uint64_t ecalls=0,mrets=0;
static uint32_t minimum_nonzero_sp=0xffffffffu;
static std::array<uint64_t,4> ps2_queue_counts{};
static uint64_t ps2_queue_maximum=0;
void c5_ps2_queue(unsigned kind,unsigned value,unsigned occupancy) {
  (void)value;
  if(kind>=4||occupancy>16)throw std::runtime_error("PS2_QUEUE_OBSERVATION");
  ps2_queue_counts[kind]++;if(occupancy>ps2_queue_maximum)ps2_queue_maximum=occupancy;
}
void c5_sdram_event(int chip,int kind,int address,int value,int mask) {
  (void)value;
  if(chip<0||chip>=4||(kind!=1&&kind!=2)||address<0||address>=33554432||mask<0||mask>3)throw std::runtime_error("SDRAM_OBSERVATION_FIELDS");
  for(unsigned byte=0;byte<2;byte++)if(!(mask&(1<<byte))){
    if(kind==1)sdram_reads[chip]++;else sdram_writes[chip]++;
    if(unsigned(address)+byte>sdram_max_address[chip])sdram_max_address[chip]=unsigned(address)+byte;
  }
}
void c5_psram_event(unsigned kind,unsigned mode,unsigned command,unsigned address,unsigned value) {
  (void)value;
  if(kind==0){
    if(mode>1||!(command==0xeb||command==0x38||command==2))throw std::runtime_error("PSRAM_OBSERVATION_COMMAND");
    psram_commands[mode*2+(command==0xeb?0:1)]++;
  }else if(kind==1||kind==2){
    if(kind==1)psram_write_bytes++;else psram_read_bytes++;
    if(address>psram_max_address)psram_max_address=address;
  }else if(kind==3){
    if(command==0x35)psram_qpi_entries++;else if(command==0xf5)psram_qpi_exits++;else throw std::runtime_error("PSRAM_MODE_COMMAND");
  }else throw std::runtime_error("PSRAM_OBSERVATION_KIND");
}
void c5_spi_event(unsigned kind,unsigned select,unsigned mosi,unsigned miso) {
  spi_observer.event(kind,select,mosi,miso,cycles);
}
static uint64_t uart_attempts=0,uart_accepted=0,uart_dropped=0,uart_max_occupancy=0;
static std::string uart_stream;
static constexpr size_t uart_capture_limit=1024*1024;
void c5_uart_fifo(unsigned kind,unsigned value,unsigned occupancy) {
  if(occupancy>uart_max_occupancy)uart_max_occupancy=occupancy;
  if(kind==0)uart_attempts++;
  else if(kind==1){uart_accepted++;if(uart_stream.size()<uart_capture_limit)uart_stream+=char(value&255);}
  else if(kind==2)uart_dropped++;
  else throw std::runtime_error("UART_OBSERVATION_KIND");
  if(trace&&trace_rows++<trace_limit)std::fprintf(trace,"U %llu %u %02x %u\n",(unsigned long long)cycles,kind,value&255,occupancy);
}
static uint32_t read32(const std::vector<uint8_t>&bytes,uint32_t at) {
  if(uint64_t(at)+4>bytes.size())throw std::runtime_error("MODEL_READ_OUT_OF_RANGE");
  return uint32_t(bytes[at])|(uint32_t(bytes[at+1])<<8)|(uint32_t(bytes[at+2])<<16)|(uint32_t(bytes[at+3])<<24);
}
void mrom_read(int addr,int *data) {
  uint32_t a=uint32_t(addr);if(a<0x20000000u||a>=0x20001000u)throw std::runtime_error("MROM_ADDRESS");
  *data=int(read32(mrom,(a-0x20000000u)&~3u));mrom_calls++;
}
void flash_read(int addr,int *data) {*data=int(read32(flash,uint32_t(addr)));flash_calls++;}
void c5_retire(unsigned at_pc,unsigned inst,unsigned after_pc,const svBitVecVal *gpr) {
  if(at_pc!=before_state.pc)throw std::runtime_error("COMMIT_PC_SEQUENCE");
  validate_access(before_state,inst,pending_access);bus.retire(at_pc,inst,pending_access);
  last_pc=at_pc;last_inst=inst;next_pc=after_pc;std::memcpy(registers.data(),gpr,64);commits++;
  performance.retire(at_pc,inst,after_pc,pending_access.address,pending_access.valid,pending_access.write);
  if(inst==0x00000073u)ecalls++;
  if(inst==0x30200073u)mrets++;
  if(registers[2]&&registers[2]<minimum_nonzero_sp)minimum_nonzero_sp=registers[2];
  unsigned region=at_pc>=0x20000000u&&at_pc<0x20001000u?0:at_pc>=0x0f000000u&&at_pc<0x0f002000u?1:
    at_pc>=0x30000000u&&at_pc<0x31000000u?2:at_pc>=0x80000000u&&at_pc<0x80400000u?3:
    at_pc>=0xa0000000u&&at_pc<0xa8000000u?4:at_pc>=0xc0000000u&&at_pc<0xc0001000u?5:6;
  retired_regions[region]++;
  CpuState actual;actual.pc=after_pc;std::memcpy(actual.r,gpr,64);
  if(actual.r[0])throw std::runtime_error("X0_NOT_ZERO");
  if(reference&&!reference->compare(before_state,actual,inst,pending_access)){diff_failed=true;stopped=true;}
  before_state=actual;pending_access={};
  if(trace&&trace_rows++<trace_limit)std::fprintf(trace,"I %llu %08x %08x %08x\n",(unsigned long long)cycles,at_pc,inst,after_pc);
  if(inst==0x00100073u)stopped=true;
}
void c5_fault(unsigned at_pc,unsigned code) {last_pc=at_pc;fault_code=code;stopped=true;}
void c5_memory(unsigned at_pc,unsigned addr,unsigned bytes,unsigned value,svBit write_op) {
  performance.memory(addr,write_op);
  memories++;if(!(bytes==1||bytes==2||bytes==4))throw std::runtime_error("BAD_MEMORY_WIDTH");
  if(pending_access.valid)throw std::runtime_error("MULTIPLE_MEMORY_OBSERVATIONS");
  uint32_t mask=bytes==4?0xffffffffu:(1u<<(8*bytes))-1;
  pending_access={true,bool(write_op),at_pc,addr,bytes,value&mask};
  pin_observer.memory(addr,value,bool(write_op));
  coverage.observe(addr,bytes,bool(write_op));
  if(trace&&trace_rows++<trace_limit)std::fprintf(trace,"M %llu %08x %c %08x %u %08x\n",(unsigned long long)cycles,at_pc,write_op?'W':'R',addr,bytes,value);
}
void c5_bus(unsigned channel,unsigned addr,unsigned value,unsigned attr) {
  if(channel>=channels.size())throw std::runtime_error("BAD_BUS_CHANNEL");
  channels[channel]++;
  bus.accept(channel,addr,value,attr);
  if(trace&&trace_rows++<trace_limit)std::fprintf(trace,"B %llu %u %08x %08x %08x\n",(unsigned long long)cycles,channel,addr,value,attr);
}
static uint64_t integer(const std::string& s) {
  size_t count=0;if(s.empty()||s[0]=='-')throw std::runtime_error("BAD_NUMBER");
  auto value=std::stoull(s,&count,0);if(count!=s.size())throw std::runtime_error("BAD_NUMBER_SUFFIX");return value;
}
static void load(const std::string& file,std::vector<uint8_t>& bytes) {
  std::ifstream f(file,std::ios::binary|std::ios::ate);if(!f)throw std::runtime_error("IMAGE_OPEN");
  auto size=f.tellg();if(size<=0||uint64_t(size)>bytes.size())throw std::runtime_error("IMAGE_SIZE");
  f.seekg(0);f.read(reinterpret_cast<char*>(bytes.data()),size);if(!f)throw std::runtime_error("IMAGE_READ");
}
int main(int argc,char**argv) {
  try {
    std::string rom,flash_image,report,trace_file,wave_file,ref_file,vga_output,perf_trace;uint64_t max_cycles=1000000,coverage_base=0,coverage_size=0,progress_interval=0;unsigned uart_bit_cycles=0;bool buffered=false,no_diff=false,corrupt_reference=false,gui=false,observe_pins=false,gui_closed=false;
    for(int i=1;i<argc;i++) {
      std::string option=argv[i];auto value=[&](){if(++i>=argc)throw std::runtime_error("MISSING_ARGUMENT");return std::string(argv[i]);};
      if(option=="--mrom")rom=value();else if(option=="--flash")flash_image=value();
      else if(option=="--report")report=value();else if(option=="--trace")trace_file=value();else if(option=="--wave")wave_file=value();
      else if(option=="--perf-trace")perf_trace=value();
      else if(option=="--max-cycles")max_cycles=integer(value());else if(option=="--trace-limit")trace_limit=integer(value());
      else if(option=="--ref")ref_file=value();else if(option=="--no-diff")no_diff=true;
      else if(option=="--corrupt-reference-rom")corrupt_reference=true;
      else if(option=="--coverage-base")coverage_base=integer(value());else if(option=="--coverage-size")coverage_size=integer(value());
      else if(option=="--uart-bit-cycles")uart_bit_cycles=unsigned(integer(value()));
      else if(option=="--progress-cycles")progress_interval=integer(value());
      else if(option=="--gui")gui=true;else if(option=="--observe-pins")observe_pins=true;
      else if(option=="--vga-ppm")vga_output=value();
      else if(option=="--buffered")buffered=true;else throw std::runtime_error("UNKNOWN_OPTION "+option);
    }
    if(rom.empty()&&flash_image.empty())throw std::runtime_error("NO_IMAGE");
    if(ref_file.empty()&&!no_diff)throw std::runtime_error("REFERENCE_REQUIRED_OR_EXPLICIT_NO_DIFF");
    if(!ref_file.empty()&&no_diff)throw std::runtime_error("AMBIGUOUS_DIFF_CONFIGURATION");
    if(no_diff&&corrupt_reference)throw std::runtime_error("CORRUPTION_CONTROL_REQUIRES_REFERENCE");
    coverage.configure(coverage_base,coverage_size);
    chiplink_observer.configure();
    if(gui&&!uart_bit_cycles)uart_bit_cycles=16;
    pin_observer.configure(gui||observe_pins||!vga_output.empty());
#ifndef C5_ENABLE_NVBOARD
    if(gui)throw std::runtime_error("NVBOARD_NOT_BUILT");
#endif
    if(uart_bit_cycles&&uart_bit_cycles<4)throw std::runtime_error("UART_SAMPLE_PERIOD");
    uart_decoder.configure(uart_bit_cycles);
    uart_rx_decoder.configure(uart_bit_cycles);
    if(!rom.empty())load(rom,mrom);
    if(!flash_image.empty())load(flash_image,flash);
    std::setvbuf(stdout,nullptr,buffered?_IOLBF:_IONBF,0);
    before_state.pc=C5_START_PC;
    if(!no_diff)reference=std::make_unique<Reference>(ref_file,C5_START_PC,mrom,flash,corrupt_reference);
    if(!trace_file.empty()){trace=std::fopen(trace_file.c_str(),"w");if(!trace)throw std::runtime_error("TRACE_OPEN");}
    if(!perf_trace.empty()){performance.stream=std::fopen(perf_trace.c_str(),"wb");if(!performance.stream)throw std::runtime_error("PERF_TRACE_OPEN");}
    VerilatedContext context;context.commandArgs(argc,argv);context.traceEverOn(!wave_file.empty());
    VysyxSoCFull dut{&context};std::unique_ptr<VerilatedVcdC> wave;
    if(!wave_file.empty()){wave=std::make_unique<VerilatedVcdC>();dut.trace(wave.get(),6);wave->open(wave_file.c_str());}
    dut.clock=0;dut.reset=1;dut.externalPins_gpio_in=0;dut.externalPins_ps2_clk=1;dut.externalPins_ps2_data=1;dut.externalPins_uart_rx=1;dut.eval();
#ifdef C5_ENABLE_NVBOARD
    if(gui){nvboard_bind_all_pins(&dut);nvboard_init();}
#endif
    auto edge=[&](bool clock) {
      auto target=context.time()+5;
#if VM_TIMING
      while(dut.eventsPending()&&dut.nextTimeSlot()<target){context.time(dut.nextTimeSlot());dut.eval();}
#endif
      context.time(target);dut.clock=clock;dut.eval();if(wave)wave->dump(context.time());
    };
    for(unsigned i=0;i<16;i++){edge(true);edge(false);}dut.reset=0;dut.eval();
    auto start=std::chrono::steady_clock::now();
    uint64_t next_progress=progress_interval;
    while(!stopped&&cycles<max_cycles&&!context.gotFinish()){
      cycles++;edge(true);edge(false);uart_decoder.sample(cycles,dut.externalPins_uart_tx!=0);
      uart_rx_decoder.sample(cycles,dut.externalPins_uart_rx!=0);pin_observer.sample(dut,cycles);
#ifdef C5_ENABLE_NVBOARD
      if(gui){nvboard_update();if(c5_nvboard_should_close()){gui_closed=true;break;}}
#endif
      if(progress_interval&&cycles>=next_progress){
        std::fprintf(stderr,"C5_PROGRESS cycles=%llu instructions=%llu written=%llu read=%llu r8=%llu r16=%llu r32=%llu\n",(unsigned long long)cycles,(unsigned long long)commits,(unsigned long long)coverage.write_bytes,(unsigned long long)coverage.read_bytes,(unsigned long long)coverage.read_ops[0],(unsigned long long)coverage.read_ops[1],(unsigned long long)coverage.read_ops[2]);
        next_progress+=progress_interval;
      }
    }
    if(uart_attempts!=uart_accepted+uart_dropped)throw std::runtime_error("UART_FIFO_ACCOUNTING");
    int rc=fault_code?3:diff_failed?1:gui_closed?0:!stopped?124:registers[10]?1:0;
    std::string result=fault_code?"NPC_FAULT":diff_failed?"DIFF_FAIL":gui_closed?"GUI_OBSERVATION_STOP":!stopped?"CYCLE_LIMIT":registers[10]?"BAD_TRAP":"GOOD_TRAP";
    auto wall=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
    std::fprintf(stderr,"%s pc=%08x inst=%08x a0=%u fault=%u cycles=%llu instructions=%llu wall=%.6f\n",result.c_str(),last_pc,last_inst,registers[10],fault_code,(unsigned long long)cycles,(unsigned long long)commits,wall);
    if(!report.empty()) {
      std::ofstream out(report);if(!out)throw std::runtime_error("REPORT_OPEN");
      out<<"{\"result\":\""<<result<<"\",\"exit_code\":"<<rc<<",\"pc\":"<<last_pc<<",\"next_pc\":"<<next_pc<<",\"instruction\":"<<last_inst<<",\"a0\":"<<registers[10]<<",\"fault\":"<<fault_code<<",\"cycles\":"<<cycles<<",\"instructions\":"<<commits<<",\"wall_seconds\":"<<wall<<",\"reset_cycles\":16,\"mrom_dpi_calls\":"<<mrom_calls<<",\"flash_dpi_calls\":"<<flash_calls<<",\"memory_operations\":"<<memories<<",\"diff_enabled\":"<<(reference?"true":"false")<<",\"diff_checked\":"<<(reference?reference->checked:0)<<",\"device_sync_checked\":"<<(reference?reference->devices:0)<<",\"axi_channels\":[";
      for(size_t i=0;i<channels.size();i++){if(i)out<<',';out<<channels[i];}out<<"],\"gpr\":[";
      for(size_t i=0;i<registers.size();i++){if(i)out<<',';out<<registers[i];}
      out<<"],\"coverage\":{\"base\":"<<coverage_base<<",\"size\":"<<coverage_size<<",\"unique_read_bytes\":"<<coverage.read_bytes<<",\"unique_written_bytes\":"<<coverage.write_bytes<<",\"read_ops_by_width\":[";
      for(size_t i=0;i<3;i++){if(i)out<<',';out<<coverage.read_ops[i];}out<<"],\"write_ops_by_width\":[";
      for(size_t i=0;i<3;i++){if(i)out<<',';out<<coverage.write_ops[i];}
      out<<"]},\"uart\":{\"attempted\":"<<uart_attempts<<",\"accepted\":"<<uart_accepted<<",\"dropped\":"<<uart_dropped<<",\"maximum_fifo_occupancy\":"<<uart_max_occupancy<<",\"capture_truncated\":"<<(uart_accepted>uart_stream.size()?"true":"false")<<",\"hex\":\"";
      static const char hex[]="0123456789abcdef";
      for(unsigned char c:uart_stream){out<<hex[c>>4]<<hex[c&15];}
      out<<"\"},\"uart_pin\":{\"cycles_per_bit\":"<<uart_bit_cycles<<",\"frames\":"<<uart_decoder.frames<<",\"framing_errors\":"<<uart_decoder.errors<<",\"hex\":\"";
      for(unsigned char c:uart_decoder.bytes){out<<hex[c>>4]<<hex[c&15];}
      out<<"\"},\"retired_by_region\":[";
      for(size_t i=0;i<retired_regions.size();i++){if(i)out<<',';out<<retired_regions[i];}
      out<<"],\"spi\":{\"transfers\":"<<spi_observer.transfers<<",\"sampled_bits\":"<<spi_observer.total_bits<<",\"incomplete_bits\":"<<spi_observer.incomplete_bits()<<",\"capture_truncated\":"<<(spi_observer.transfers>spi_observer.captured.size()?"true":"false")<<",\"packets\":[";
      for(size_t i=0;i<spi_observer.captured.size();i++){
        const auto &p=spi_observer.captured[i];if(i)out<<',';
        out<<"{\"select\":"<<p.select<<",\"bits\":"<<p.bits<<",\"tx_low64\":"<<p.tx<<",\"rx_low64\":"<<p.rx<<",\"start_cycle\":"<<p.start<<",\"end_cycle\":"<<p.end<<"}";
      }
      out<<"]},\"psram\":{\"commands_spi_read_write_qpi_read_write\":[";
      for(size_t i=0;i<4;i++){if(i)out<<',';out<<psram_commands[i];}
      out<<"],\"bytes_presented_read\":"<<psram_read_bytes<<",\"bytes_committed_write\":"<<psram_write_bytes<<",\"maximum_byte_address\":"<<psram_max_address<<",\"qpi_entries\":"<<psram_qpi_entries<<",\"qpi_exits\":"<<psram_qpi_exits<<"},\"traps\":{\"ecall\":"<<ecalls<<",\"mret\":"<<mrets<<"},\"sdram_chips\":[";
      for(unsigned i=0;i<4;i++){if(i)out<<',';out<<"{\"read_bytes\":"<<sdram_reads[i]<<",\"write_bytes\":"<<sdram_writes[i]<<",\"maximum_byte_address\":"<<sdram_max_address[i]<<"}";}
      out<<"],\"minimum_nonzero_sp\":"<<minimum_nonzero_sp<<",\"pins\":";pin_observer.write(out);
      out<<",\"uart_rx_pin\":{\"frames\":"<<uart_rx_decoder.frames<<",\"framing_errors\":"<<uart_rx_decoder.errors<<",\"hex\":\"";
      for(unsigned char c:uart_rx_decoder.bytes)out<<hex[c>>4]<<hex[c&15];
      out<<"\"},\"ps2_queue\":{\"accepted\":"<<ps2_queue_counts[0]<<",\"dropped\":"<<ps2_queue_counts[1]<<",\"invalid\":"<<ps2_queue_counts[2]<<",\"popped\":"<<ps2_queue_counts[3]<<",\"maximum_occupancy\":"<<ps2_queue_maximum<<"},\"chiplink\":";
      chiplink_observer.write(out);out<<",\"performance\":";performance.report(out);out<<"}\n";
    }
    if(trace)std::fclose(trace);
    if(performance.stream&&std::fclose(performance.stream)!=0)throw std::runtime_error("PERF_TRACE_CLOSE");
    if(wave)wave->close();
    pin_observer.save_frame(vga_output);
#ifdef C5_ENABLE_NVBOARD
    if(gui)nvboard_quit();
#endif
    dut.final();return rc;
  } catch(const std::exception& e) {std::fprintf(stderr,"C5_SIMULATOR_ERROR %s\n",e.what());return 2;}
}
