#include "Vapb_delayer.h"
#include "verilated.h"
#include "verilated_vcd_c.h"
#include <memory>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <stdexcept>
int main(int argc,char **argv) {
  Verilated::commandArgs(argc,argv);Verilated::traceEverOn(true);Vapb_delayer d;
  std::unique_ptr<VerilatedVcdC> wave;uint64_t timestamp=0;
  if(argc>2){wave=std::make_unique<VerilatedVcdC>();d.trace(wave.get(),3);wave->open(argv[2]);}
  unsigned ratio=argc>1?unsigned(std::strtoul(argv[1],nullptr,0)):256;
  uint64_t cycles=0;unsigned completions=0;
  auto edge=[&](){d.clock=0;d.eval();d.clock=1;d.eval();if(wave)wave->dump(++timestamp);cycles++;d.clock=0;d.eval();if(wave)wave->dump(++timestamp);};
  d.reset=1;d.in_psel=0;d.in_penable=0;d.out_pready=0;d.out_prdata=0;d.out_pslverr=0;
  d.in_paddr=0;d.in_pprot=0;d.in_pwrite=0;d.in_pwdata=0;d.in_pstrb=0;
  edge();edge();d.reset=0;
  try {
    for(unsigned test=0;test<100;test++) {
      unsigned service=1+(test*17)%33,accepted=0;
      d.in_psel=1;d.in_penable=0;d.in_paddr=0xa0000000+4*test;
      d.in_pprot=test&7;d.in_pwrite=test&1;d.in_pwdata=test^0x12345678;d.in_pstrb=test&15;
      d.out_pready=0;edge();uint64_t start=cycles;
      d.in_penable=1;unsigned elapsed=0;bool done=false;
      for(;elapsed<2000&&!done;) {
        elapsed++;d.out_pready=(elapsed==service);d.out_prdata=0x87654321u^test;d.out_pslverr=test%7==0;d.eval();
        if(d.out_psel&&d.out_penable&&d.out_pready)accepted++;
        if(d.out_psel&&(d.out_paddr!=d.in_paddr||d.out_pwrite!=d.in_pwrite||d.out_pwdata!=d.in_pwdata||d.out_pstrb!=d.in_pstrb))throw std::runtime_error("APB_FIELDS");
        if(d.in_pready){
          unsigned expected=(service*ratio+255)/256;
          if(elapsed!=expected||d.in_prdata!=(0x87654321u^test)||d.in_pslverr!=(test%7==0)||accepted!=1){
            std::fprintf(stderr,"APB_DELAY_MISMATCH ratio=%u k=%u expected=%u actual=%u accepted=%u\n",ratio,service,expected,elapsed,accepted);throw std::runtime_error("CALIBRATION");
          }
          completions++;done=true;
        }
        edge();
      }
      if(!done||cycles-start!=elapsed)throw std::runtime_error("TIMEOUT");
      // Back-to-back setup phases keep PSEL high; alternate idle gaps as well.
      if(test%2){d.in_psel=0;d.in_penable=0;d.out_pready=0;edge();}
    }
    if(wave)wave->close();std::printf("APB_CALIBRATION_PASS ratio_q=%u transactions=%u\n",ratio,completions);return 0;
  }catch(const std::exception&e){if(wave)wave->close();std::fprintf(stderr,"APB_TEST_FAIL %s\n",e.what());return 1;}
}
