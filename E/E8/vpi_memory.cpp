#include <vpi_user.h>
#include "memory_model.hpp"
#include <memory>
#include <cstdlib>
static std::unique_ptr<GateMemory>memory;
static std::string image,report;
static std::vector<vpiHandle> arguments(){
 std::vector<vpiHandle>a;vpiHandle it=vpi_iterate(vpiArgument,vpi_handle(vpiSysTfCall,nullptr));if(!it)return a;vpiHandle h;while((h=vpi_scan(it)))a.push_back(h);return a;
}
static uint64_t integer(vpiHandle h){
 s_vpi_value v{};v.format=vpiVectorVal;vpi_get_value(h,&v);unsigned bits=vpi_get(vpiSize,h);if(bits>64)throw std::runtime_error("VPI argument exceeds64bits");
 uint64_t n=0;for(unsigned i=0;i<(bits+31)/32;i++){if(v.value.vector[i].bval)throw std::runtime_error("X/Z memory argument");n|=uint64_t(uint32_t(v.value.vector[i].aval))<<(32*i);}return n;
}
static void return32(uint32_t x){s_vpi_value v{};s_vpi_vecval vec{};vec.aval=x;vec.bval=0;v.format=vpiVectorVal;v.value.vector=&vec;vpi_put_value(vpi_handle(vpiSysTfCall,nullptr),&v,nullptr,vpiNoDelay);}
static PLI_INT32 sized(PLI_BYTE8*){return 32;}
static PLI_INT32 init(PLI_BYTE8*){try{
 s_vpi_vlog_info info{};vpi_get_vlog_info(&info);for(int i=0;i<info.argc;i++){std::string a=info.argv[i];if(a.rfind("+image=",0)==0)image=a.substr(7);if(a.rfind("+report=",0)==0)report=a.substr(8);}
 if(image.empty())throw std::runtime_error("missing +image argument");memory.reset(new GateMemory);memory->load(image);
 }catch(const std::exception&e){vpi_printf("VPI_INIT_ERROR %s\n",e.what());std::exit(2);}return 0;}
static PLI_INT32 read(PLI_BYTE8*){try{auto a=arguments();if(a.size()!=2)throw std::runtime_error("read requires address,kind");return32(memory->read(integer(a[0]),integer(a[1])));}catch(const std::exception&e){memory->error=e.what();vpi_printf("VPI_READ_ERROR %s\n",e.what());return32(0);}return 0;}
static PLI_INT32 write(PLI_BYTE8*){try{auto a=arguments();if(a.size()!=3)throw std::runtime_error("write requires address,data,mask");memory->write(integer(a[0]),integer(a[1]),integer(a[2]));}catch(const std::exception&e){memory->error=e.what();vpi_printf("VPI_WRITE_ERROR %s\n",e.what());}return 0;}
static PLI_INT32 tick(PLI_BYTE8*){try{auto a=arguments();if(a.size()!=1)throw std::runtime_error("tick requires count");memory->tick(integer(a[0]));}catch(const std::exception&e){memory->error=e.what();}return 0;}
static PLI_INT32 status(PLI_BYTE8*){return32(memory?memory->status():uint32_t(-1));return 0;}
static PLI_INT32 finish(PLI_BYTE8*){try{auto a=arguments();if(a.size()!=1)throw std::runtime_error("report requires failed");int failed=integer(a[0]);memory->report(report,failed,failed?"FAIL":"GOOD_TRAP");}catch(const std::exception&e){vpi_printf("REPORT_ERROR %s\n",e.what());std::exit(2);}return 0;}
static void add(const char*name,PLI_INT32(*fn)(PLI_BYTE8*),bool value=false){s_vpi_systf_data tf{};tf.type=value?vpiSysFunc:vpiSysTask;tf.sysfunctype=vpiSizedFunc;tf.tfname=const_cast<char*>(name);tf.calltf=fn;tf.sizetf=value?sized:nullptr;vpi_register_systf(&tf);}
static void start(){add("$pmem_init",init);add("$pmem_read",read,true);add("$pmem_write",write);add("$pmem_tick",tick);add("$pmem_status",status,true);add("$pmem_report",finish);}
extern "C" {void (*vlog_startup_routines[])()={start,nullptr};}
