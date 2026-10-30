#pragma once
#include <array>
#include <cstdint>
#include <fstream>
#include <map>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
struct PinObserver {
  bool enabled=false,previous_ps2_clock=true;
  unsigned ps2_bit=0;uint16_t ps2_frame=0,last_led=0;
  std::array<uint8_t,8> segments{};
  std::vector<std::pair<uint64_t,unsigned>> leds,scan_codes;
  std::map<unsigned,uint64_t> switches;
  uint64_t ps2_errors=0,frames=0,changed_frames=0,frame_hash=1469598103934665603ull,last_hash=0;
  unsigned pixels=0;std::vector<uint32_t> frame,last_frame;
  std::vector<uint64_t> hashes;
  void configure(bool active){enabled=active;if(active){frame.resize(640*480);last_frame.resize(640*480);}}
  void memory(uint32_t address,unsigned value,bool writing){if(enabled&&!writing&&address==0x10002004u)switches[value&65535]++;}
  template<typename Top> void sample(const Top& dut,uint64_t cycle){
    if(!enabled)return;
    if(dut.externalPins_gpio_out!=last_led){last_led=dut.externalPins_gpio_out;if(leds.size()<4096)leds.emplace_back(cycle,last_led);}
    segments={dut.externalPins_gpio_seg_0,dut.externalPins_gpio_seg_1,dut.externalPins_gpio_seg_2,dut.externalPins_gpio_seg_3,dut.externalPins_gpio_seg_4,dut.externalPins_gpio_seg_5,dut.externalPins_gpio_seg_6,dut.externalPins_gpio_seg_7};
    bool ps2_clock=dut.externalPins_ps2_clk,level=dut.externalPins_ps2_data;
    if(previous_ps2_clock&&!ps2_clock){
      if(ps2_bit==0){if(!level){ps2_frame=0;ps2_bit=1;}}
      else if(ps2_bit<=9){ps2_frame|=uint16_t(level)<<(ps2_bit-1);ps2_bit++;}
      else{
        unsigned parity=0;for(unsigned i=0;i<9;i++)parity^=(ps2_frame>>i)&1;
        if(!level||parity!=1)ps2_errors++;
        else if(scan_codes.size()<65536)scan_codes.emplace_back(cycle,ps2_frame&255);
        ps2_bit=0;
      }
    }
    previous_ps2_clock=ps2_clock;
    if(dut.externalPins_vga_valid){
      uint32_t pixel=(uint32_t(dut.externalPins_vga_r)<<16)|(uint32_t(dut.externalPins_vga_g)<<8)|dut.externalPins_vga_b;
      frame[pixels++]=pixel;frame_hash=(frame_hash^pixel)*1099511628211ull;
      if(pixels==640*480){
        frames++;if(frames==1||frame_hash!=last_hash)changed_frames++;
        last_hash=frame_hash;if(hashes.size()<64)hashes.push_back(last_hash);last_frame=frame;
        pixels=0;frame_hash=1469598103934665603ull;
      }
    }
  }
  void save_frame(const std::string& path)const{
    if(path.empty())return;
    if(!enabled||!frames)throw std::runtime_error("NO_COMPLETE_PIN_VIDEO_FRAME");
    std::ofstream out(path,std::ios::binary);if(!out)throw std::runtime_error("PIN_VIDEO_OPEN");out<<"P6\n640 480\n255\n";
    for(auto pixel:last_frame){char rgb[3]={char(pixel>>16),char(pixel>>8),char(pixel)};out.write(rgb,3);}
  }
  void write(std::ostream& out)const{
    out<<"{\"enabled\":"<<(enabled?"true":"false")<<",\"led_changes\":[";
    for(size_t i=0;i<leds.size();i++){if(i)out<<',';out<<'['<<leds[i].first<<','<<leds[i].second<<']';}
    out<<"],\"segments\":[";for(size_t i=0;i<segments.size();i++){if(i)out<<',';out<<unsigned(segments[i]);}
    out<<"],\"switch_reads\":[";bool comma=false;for(auto [value,count]:switches){if(comma)out<<',';comma=true;out<<'['<<value<<','<<count<<']';}
    out<<"],\"ps2_scans\":[";for(size_t i=0;i<scan_codes.size();i++){if(i)out<<',';out<<'['<<scan_codes[i].first<<','<<scan_codes[i].second<<']';}
    out<<"],\"ps2_frame_errors\":"<<ps2_errors<<",\"vga_frames\":"<<frames<<",\"vga_changed_frames\":"<<changed_frames<<",\"vga_last_hash\":"<<last_hash<<",\"vga_hashes\":[";
    for(size_t i=0;i<hashes.size();i++){if(i)out<<',';out<<hashes[i];}out<<"]}";
  }
};
