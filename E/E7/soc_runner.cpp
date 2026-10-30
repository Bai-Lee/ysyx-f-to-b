#include "VSimTop.h"
#include "VSimTop__Dpi.h"
#include "verilated.h"
#include "verilated_vcd_c.h"
#include "ref.h"
#include <vector>
#include <string>
#include <fstream>
#include <iostream>
#include <sstream>
#include <iomanip>
#include <chrono>
#include <memory>
#include <cassert>
#include <cstring>
#include <array>
#include <set>
#include <map>
#include <thread>
#include <sys/select.h>
#include <unistd.h>
#ifdef ENABLE_NVBOARD
#include <nvboard.h>
void nvboard_bind_all_pins(VSimTop*);
#endif
struct ByteEvent {uint32_t address;uint8_t value;};
struct Transaction {uint32_t addr=0,data=0;uint8_t mask=0;bool write=false,active=false,responded=false;};
static std::vector<uint8_t>flash(16*1024*1024),ram(8*1024*1024);
static std::vector<ByteEvent>dut_writes,ref_writes;
static Transaction transaction;
static MiniState ref;
static uint64_t expected_counter=0,last_counter=0,commits=0,app_commits=0,app_start=0,trap_cycle=0,flash_reads=0;
static bool app_started=false,finished=false,assert_flash=false,core_reset_seen=false;
static uint32_t trap_code=0,last_pc=0;
static std::string failure,uart_expected,uart_serial;
static uint8_t uart_lcr=0,uart_dll=1,uart_dlm=0;
static uint64_t reqs=0,resps=0;
static std::vector<unsigned>divisors;
static std::array<uint32_t,64>recent_pc{};
static std::map<unsigned,uint64_t>switch_reads;
static bool region(uint32_t a,unsigned n,uint32_t base,size_t size){return a>=base&&uint64_t(a)-base+n<=size;}
static uint32_t bytes(const std::vector<uint8_t>&m,size_t off,unsigned n){uint32_t v=0;for(unsigned i=0;i<n;i++)v|=uint32_t(m[off+i])<<(8*i);return v;}
static int read_ref(void*,uint32_t a,unsigned n,int kind,uint32_t*v){
 if(region(a,n,0x30000000,flash.size())){*v=bytes(flash,a-0x30000000,n);return 0;}
 if(region(a,n,0x80000000,ram.size())){*v=bytes(ram,a-0x80000000,n);return 0;}
 if(kind==1&&transaction.active&&!transaction.write&&transaction.responded&&a==transaction.addr){*v=n==1?(transaction.data>>(8*(a&3)))&255:transaction.data;return 0;}
 return -1;
}
static int write_ref(void*,uint32_t a,unsigned n,uint32_t v){
 for(unsigned i=0;i<n;i++){uint8_t b=v>>(8*i);ref_writes.push_back({a+i,b});if(region(a+i,1,0x80000000,ram.size()))ram[a+i-0x80000000]=b;}
 return 0;
}
extern "C" void flash_read(int addr,int*data){
 flash_reads++;if(assert_flash){std::cerr<<"EXPECTED_FIRST_FLASH_READ addr="<<std::hex<<uint32_t(addr)<<std::dec<<"\n";std::abort();}
 uint32_t a=uint32_t(addr);if(a>flash.size()-4){failure="flash address outside 16MB";*data=0;return;}*data=int(bytes(flash,a,4));
}
extern "C" void soc_request(unsigned addr,unsigned data,unsigned char mask,svBit wen){
 if(transaction.active){failure="duplicate LSU request before prior commit";return;}
 transaction={addr,data,mask,wen!=0,true,false};reqs++;
 if(wen){
  for(unsigned i=0;i<4;i++)if(mask&(1u<<i))dut_writes.push_back({(addr&~3u)+i,uint8_t(data>>(8*i))});
  if(addr>=0x10000000&&addr<0x10000008){
   uint8_t value=uint8_t(data>>(8*(addr&3)));unsigned off=addr-0x10000000;
   if(off==3)uart_lcr=value;
   else if((uart_lcr&0x80)&&off==0){uart_dll=value;divisors.push_back(unsigned(uart_dll)|(unsigned(uart_dlm)<<8));}
   else if((uart_lcr&0x80)&&off==1)uart_dlm=value;
   else if(off==0){if((uart_lcr&0x7f)!=3)failure="UART transmission is not configured8N1";uart_expected.push_back(char(value));}
  }
 }
}
extern "C" void soc_response(unsigned data){
 if(!transaction.active||transaction.responded){failure="unexpected/repeated LSU response";return;}
 transaction.responded=true;if(!transaction.write)transaction.data=data;resps++;
 if(!transaction.write&&transaction.addr==0x20001004u)switch_reads[data&65535u]++;
}
extern "C" void soc_fetch_request(unsigned addr){if(!app_started&&addr==0x80000000){app_started=true;app_start=expected_counter;}}
extern "C" void soc_fault(unsigned pc,unsigned code){std::ostringstream s;s<<"CPU fault pc="<<std::hex<<pc<<" code="<<code;failure=s.str();}
extern "C" void soc_tick(svBit reset,unsigned long long observed){
 if(reset){minirv_reset(&ref,0x30000000);expected_counter=last_counter=0;core_reset_seen=true;transaction={};dut_writes.clear();ref_writes.clear();return;}
 if(!core_reset_seen){failure="core ran without reset";return;}
 if(observed!=expected_counter){std::ostringstream s;s<<"mcycle mismatch actual="<<observed<<" expected="<<expected_counter;failure=s.str();}
 last_counter=expected_counter;expected_counter++;
}
extern "C" void soc_commit(unsigned pc,unsigned inst,unsigned next_pc,const svBitVecVal*gpr,unsigned long long counter){
 (void)counter;last_pc=pc;
 uint32_t fetched=0;if(read_ref(nullptr,ref.pc,4,0,&fetched)||ref.pc!=pc||fetched!=inst){std::ostringstream s;s<<"instruction mismatch pc="<<std::hex<<pc<<" refpc="<<ref.pc<<" dut="<<inst<<" ref="<<fetched;failure=s.str();return;}
 MiniBus bus{nullptr,read_ref,write_ref};MiniEvent ev{};int error=0;
 if((inst&0x707f)==0x2073){
  unsigned rd=(inst>>7)&31,rs=(inst>>15)&31,csr=inst>>20;uint32_t v=0;
  if(rd>=16||rs>=16)error=1;else if(csr==0xf11)v=0x79737978u;else if(csr==0xf12)v=26070001u;else if(csr==0xb00)v=uint32_t(last_counter);else if(csr==0xb80)v=uint32_t(last_counter>>32);else error=1;
  if(rs){if(csr==0xb00)expected_counter=(last_counter&0xffffffff00000000ull)|(v|ref.r[rs]);else if(csr==0xb80)expected_counter=(uint64_t(v|ref.r[rs])<<32)|uint32_t(last_counter);else error=1;}
  if(rd<16&&rd)ref.r[rd]=v;ref.pc+=4;
 }else error=minirv_step(&ref,&bus,&ev);
 bool good=error==0&&ref.pc==next_pc&&dut_writes.size()==ref_writes.size();
 for(unsigned i=0;i<16;i++)if(gpr[i]!=ref.r[i]){good=false;std::cerr<<"REG_DIFF x"<<i<<" actual="<<std::hex<<gpr[i]<<" ref="<<ref.r[i]<<std::dec<<"\n";}
 for(size_t i=0;good&&i<dut_writes.size();i++)if(dut_writes[i].address!=ref_writes[i].address||dut_writes[i].value!=ref_writes[i].value)good=false;
 if((ev.load||ev.store)&&(!transaction.active||!transaction.responded))good=false;
 if(!good){std::ostringstream s;s<<"DIFF pc="<<std::hex<<pc<<" inst="<<inst<<std::dec<<" step="<<commits<<" reference_fault="<<ref.fault;failure=s.str();return;}
 recent_pc[commits%64]=pc;commits++;if(region(pc,4,0x80000000,ram.size()))app_commits++;
 transaction={};dut_writes.clear();ref_writes.clear();
 if(inst==0x00100073u){finished=true;trap_code=gpr[10];trap_cycle=expected_counter-1;}
}
static uint64_t number(const char*s){size_t n;auto v=std::stoull(s,&n,0);if(s[n])throw std::runtime_error("bad numeric argument");return v;}
struct SerialReceiver{
 bool prev=true,active=false;unsigned wait=0,bit=0,period=0,framing_errors=0;uint8_t data=0;
 void sample(bool tx){
  if(!active){if(prev&&!tx){active=true;period=16*(unsigned(uart_dll)|(unsigned(uart_dlm)<<8));if(!period){failure="UART divisor zero on TX start";active=false;return;}wait=period+period/2;bit=0;data=0;}}
  else if(--wait==0){if(bit<8){data|=uint8_t(tx)<<bit;bit++;wait=period;}else{if(tx)uart_serial.push_back(char(data));else framing_errors++;active=false;}}
  prev=tx;
 }
};
int main(int argc,char**argv){try{
 std::string image,report,trace,until;uint64_t max=2000000000ull,frequency=0;unsigned ratio=1;bool gui=false,auto_gpio=false,require_loop=false,hold_gui=false;uint64_t trace_limit=20000;
 for(int i=1;i<argc;i++){std::string a=argv[i];auto value=[&](){if(i+1>=argc)throw std::runtime_error("missing argument");return argv[++i];};
  if(a=="--image")image=value();else if(a=="--report")report=value();else if(a=="--trace")trace=value();else if(a=="--until-output")until=value();else if(a=="--ratio")ratio=number(value());else if(a=="--frequency")frequency=number(value());else if(a=="--max-cycles")max=number(value());else if(a=="--trace-cycles")trace_limit=number(value());else if(a=="--assert-flash")assert_flash=true;else if(a=="--gui")gui=true;else if(a=="--auto-gpio")auto_gpio=true;else if(a=="--require-loop")require_loop=true;else if(a=="--hold-gui")hold_gui=true;else throw std::runtime_error("unknown option "+a);
 }
 if((image.empty()&&!assert_flash)||ratio<1||ratio>100)throw std::runtime_error("invalid configuration");
 if(!frequency)frequency=25000000ull*ratio;if(frequency>10000000000ull)throw std::runtime_error("frequency exceeds time resolution budget");
 if(!image.empty()){std::ifstream f(image,std::ios::binary);if(!f)throw std::runtime_error("image open failed");f.seekg(0,std::ios::end);auto n=f.tellg();if(n<0||uint64_t(n)>flash.size())throw std::runtime_error("image exceeds flash");f.seekg(0);f.read(reinterpret_cast<char*>(flash.data()),n);if(!f)throw std::runtime_error("image read failed");}
 minirv_reset(&ref,0x30000000);VerilatedContext ctx;ctx.commandArgs(argc,argv);if(!trace.empty())ctx.traceEverOn(true);VSimTop d{&ctx};std::unique_ptr<VerilatedVcdC>vcd;
 if(!trace.empty()){vcd.reset(new VerilatedVcdC);d.trace(vcd.get(),8);vcd->open(trace.c_str());}
 d.clock=0;d.cpuClock=0;d.reset=1;d.coreSel=0;d.externalPins_uart0_rx=1;d.externalPins_mygpio_in=0;d.eval();
#ifdef ENABLE_NVBOARD
 if(gui){nvboard_bind_all_pins(&d);nvboard_init();}
#else
 if(gui)throw std::runtime_error("binary built without NVBoard");
#endif
 SerialReceiver serial;uint64_t half=0,cpu_cycles=0,soc_cycles=0,drain_start=0,gpio_wait_start=0;unsigned previous_led=0;std::vector<std::pair<uint64_t,unsigned>>leds;std::string result="CYCLE_LIMIT";int rc=124;auto start=std::chrono::steady_clock::now();
 for(;cpu_cycles<max;half++){
  bool oldslow=d.clock;d.cpuClock=half&1;d.clock=(half/ratio)&1;
  d.reset=(cpu_cycles<110ull*ratio);uint64_t stamp=uint64_t((__uint128_t(half+1)*500000000000ull)/frequency);ctx.timeInc(stamp-ctx.time());d.eval();
  if(vcd&&cpu_cycles<trace_limit)vcd->dump(ctx.time());
  if(d.cpuClock)cpu_cycles++;
  if(!oldslow&&d.clock){
   soc_cycles++;if(!d.reset)serial.sample(d.externalPins_uart0_tx);
#ifdef ENABLE_NVBOARD
   if(gui)nvboard_update();
#endif
   if(d.externalPins_mygpio_out!=previous_led){previous_led=d.externalPins_mygpio_out;leds.push_back({expected_counter,previous_led});}
   if(auto_gpio&&uart_expected.find("LOCKED:")!=std::string::npos){if(!gpio_wait_start)gpio_wait_start=soc_cycles;auto elapsed=soc_cycles-gpio_wait_start;if(elapsed>50000)d.externalPins_mygpio_in=0xa55a;else if(elapsed>25000)d.externalPins_mygpio_in=0xffff;}
  }
  if(!failure.empty()){rc=1;result="DIFF_OR_PROTOCOL_FAILURE";break;}
  if(finished||(!until.empty()&&uart_expected.find(until)!=std::string::npos)){
   if(!drain_start)drain_start=soc_cycles;
   bool loop_seen=finished||!require_loop||(commits>=64&&std::set<uint32_t>(recent_pc.begin(),recent_pc.end()).size()<=4);
   if(uart_serial==uart_expected&&!serial.active&&loop_seen){rc=finished?(trap_code==0?0:1):0;result=finished?(rc?"BAD_TRAP":"GOOD_TRAP"):"BOUNDED_OUTPUT_OBSERVATION";if(serial.framing_errors){rc=1;result="UART_FRAMING_ERROR";}break;}
   if(soc_cycles-drain_start>100000){rc=1;result="UART_SERIAL_DRAIN_FAILED";break;}
  }
 }
 double wall=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();uint64_t measured=finished?trap_cycle:expected_counter,app_cycles=app_started?measured-app_start:0;
 std::cerr<<result<<" pc="<<std::hex<<last_pc<<std::dec<<" cycles="<<measured<<" commits="<<commits<<" app="<<app_commits<<" uart="<<uart_expected.size()<<" serial="<<uart_serial.size()<<" wall="<<wall<<" "<<failure<<"\n";
 if(!report.empty()){std::ofstream f(report);f<<"{\"result\":\""<<result<<"\",\"exit_code\":"<<rc<<",\"cycles\":"<<measured<<",\"instructions\":"<<commits<<",\"ipc\":"<<std::setprecision(12)<<(measured?double(commits)/measured:0)<<",\"application_cycles\":"<<app_cycles<<",\"application_instructions\":"<<app_commits<<",\"application_ipc\":"<<(app_cycles?double(app_commits)/app_cycles:0)<<",\"cpu_soc_ratio\":"<<ratio<<",\"assumed_cpu_frequency_hz\":"<<frequency<<",\"flash_reads\":"<<flash_reads<<",\"lsu_requests\":"<<reqs<<",\"lsu_responses\":"<<resps<<",\"uart_bytes\":"<<uart_expected.size()<<",\"serial_bytes\":"<<uart_serial.size()<<",\"serial_matches\":"<<(uart_serial==uart_expected?"true":"false")<<",\"serial_framing_errors\":"<<serial.framing_errors<<",\"wall_seconds\":"<<wall<<",\"uart_divisors\":[";
  for(size_t i=0;i<divisors.size();i++){if(i)f<<',';f<<divisors[i];}f<<"],\"led_sequence\":[";for(size_t i=0;i<leds.size();i++){if(i)f<<',';f<<"["<<leds[i].first<<","<<leds[i].second<<"]";}f<<"],\"segments\":["<<unsigned(d.externalPins_mygpio_seg_0)<<','<<unsigned(d.externalPins_mygpio_seg_1)<<','<<unsigned(d.externalPins_mygpio_seg_2)<<','<<unsigned(d.externalPins_mygpio_seg_3)<<','<<unsigned(d.externalPins_mygpio_seg_4)<<','<<unsigned(d.externalPins_mygpio_seg_5)<<','<<unsigned(d.externalPins_mygpio_seg_6)<<','<<unsigned(d.externalPins_mygpio_seg_7)<<"]}\n";
  std::ofstream uart(report+".uart.txt",std::ios::binary);uart<<uart_expected;std::ofstream wire(report+".serial.txt",std::ios::binary);wire<<uart_serial;
  std::ofstream sw(report+".switches.json");sw<<'{';bool first=true;for(auto entry:switch_reads){if(!first)sw<<',';first=false;sw<<'"'<<entry.first<<"\":"<<entry.second;}sw<<"}\n";
 }
 if(vcd)vcd->close();d.final();
#ifdef ENABLE_NVBOARD
 if(gui&&hold_gui){
  std::cout<<"\nSOC_DONE_HOLD\n"<<std::flush;
  auto end=std::chrono::steady_clock::now()+std::chrono::seconds(60);
  while(std::chrono::steady_clock::now()<end){
   // NVBoard adapts its repaint countdown to simulation call frequency. Keep
   // pumping its public update API after the CPU stops so the last UART line
   // reaches the window; a single call per10ms can leave a large countdown.
   for(unsigned pump=0;pump<100000;pump++)nvboard_update();
   fd_set fds;FD_ZERO(&fds);FD_SET(STDIN_FILENO,&fds);timeval tv{0,10000};
   if(select(STDIN_FILENO+1,&fds,nullptr,nullptr,&tv)>0){char ch;auto n=::read(STDIN_FILENO,&ch,1);if(n<=0||ch=='q')break;}
  }
 }
 if(gui)nvboard_quit();
#endif
 return rc;
 }catch(const std::exception&e){std::cerr<<"SOC_SIMULATOR_ERROR "<<e.what()<<"\n";return 2;}}
