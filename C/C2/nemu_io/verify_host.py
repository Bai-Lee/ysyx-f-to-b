from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *

def main():
    d=ROOT/'C/C2/nemu_io';out=WORK/'c2-host';out.mkdir(exist_ok=True)
    shim=out/'include';shim.mkdir(exist_ok=True)
    (shim/'am.h').write_text('''#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
typedef struct { bool present,has_accel;int width,height,vmemsz;} AM_GPU_CONFIG_T;
typedef struct {bool ready;} AM_GPU_STATUS_T;
typedef struct {int x,y,w,h;void *pixels;bool sync;} AM_GPU_FBDRAW_T;
typedef struct {uint64_t us;} AM_TIMER_UPTIME_T;
typedef struct {int year,month,day,hour,minute,second;} AM_TIMER_RTC_T;
typedef struct {bool keydown;int keycode;} AM_INPUT_KEYBRD_T;
''')
    (shim/'nemu.h').write_text('''#include <stdint.h>
extern uint32_t c2_framebuffer[];
#define FB_ADDR ((uintptr_t)(c2_framebuffer+1))
#define VGACTL_ADDR ((uintptr_t)0xa0000100u)
#define KBD_ADDR ((uintptr_t)0xa0000060u)
#define RTC_ADDR ((uintptr_t)0xa0000048u)
uint32_t inl(uintptr_t);
void outl(uintptr_t,uint32_t);
''')
    (shim/'klib.h').write_text('#include <assert.h>\n')
    (shim/'klib-macros.h').write_text('/* Real AM macros header does not declare assert. */\n')
    sources=[d/'host_driver_test.c',d/'am/gpu.c',d/'am/timer.c',d/'am/input.c'];exe=out/'drivers'
    base=['gcc','-std=c11','-O1','-g','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-fno-pie','-no-pie','-I',shim]
    run('C2/nemu_io/host/build',[*base,*sources,'-o',exe],inputs=[*sources,*shim.glob('*')],outputs=[exe])
    o,_,_=run('C2/nemu_io/host/positive',[exe],inputs=[exe],env={'ASAN_OPTIONS':'detect_leaks=1'});assert 'C2_DRIVER_PASS cases=467' in o
    run('C2/nemu_io/host/negative_dimensions',[exe,'bad'],inputs=[exe],expected=(-6,))
    mutant=out/'wrong_stride.c';text=(d/'am/gpu.c').read_text();assert '* sw +' in text;mutant.write_text(text.replace('* sw +','* (sw - 1) +'))
    bad=out/'wrong_stride';run('C2/nemu_io/host/mutant_build',[*base,sources[0],mutant,*sources[2:],'-o',bad],inputs=[sources[0],mutant,*sources[2:]],outputs=[bad])
    _,e,_=run('C2/nemu_io/host/mutant',[bad],inputs=[bad],expected=(-6,));assert 'memcmp' in e
    badtimer=out/'low_first.c';badtext=(d/'am/timer.c').read_text();badtimer.write_text(badtext.replace('uint32_t hi = inl(RTC_ADDR + 4);\n  uint32_t lo = inl(RTC_ADDR);','uint32_t lo = inl(RTC_ADDR);\n  uint32_t hi = inl(RTC_ADDR + 4);'))
    bad=out/'low_first';run('C2/nemu_io/host/low_first_build',[*base,sources[0],sources[1],badtimer,sources[3],'-o',bad],inputs=[sources[0],sources[1],badtimer,sources[3]],outputs=[bad])
    _,e,_=run('C2/nemu_io/host/low_first',[bad],inputs=[bad],expected=(-6,));assert 'time.us' in e
    rtcinc=out/'rtc_include';(rtcinc/'device').mkdir(parents=True,exist_ok=True)
    (rtcinc/'device/map.h').write_text('#include <stdint.h>\n#include <stdbool.h>\ntypedef void(*io_callback_t)(uint32_t,int,bool);\nuint8_t *new_space(int);\nvoid add_mmio_map(const char*,uint32_t,void*,uint32_t,io_callback_t);\n#define CONFIG_RTC_MMIO 0xa0000048u\n')
    (rtcinc/'device/alarm.h').write_text('/* Target AM build excludes host alarms. */\n')
    (rtcinc/'utils.h').write_text('#include <stdint.h>\n#include <stddef.h>\n#include <assert.h>\nuint64_t get_time(void);\n#define IFNDEF(k,...)\n')
    # Match the upstream timer compilation warning level; its callback deliberately does not use len.
    rtc=BENCH/'nemu/src/device/timer.c';rtcbin=out/'rtc-model';rtccmd=['gcc','-std=c11','-Wall','-Werror','-g','-fsanitize=address,undefined','-fno-pie','-no-pie','-DCONFIG_TARGET_AM','-I',rtcinc,d/'host_rtc_model.c',rtc,'-o',rtcbin]
    run('C2/nemu_io/host/rtc_build',rtccmd,inputs=[d/'host_rtc_model.c',rtc,*[p for p in rtcinc.rglob('*') if p.is_file()]],outputs=[rtcbin])
    ro,_,_=run('C2/nemu_io/host/rtc_model',[rtcbin],inputs=[rtcbin]);assert 'stale_low_high_detected=4' in ro
    run('C2/nemu_io/host/rtc_invalid_offset',[rtcbin,'bad'],inputs=[rtcbin],expected=(-6,))
    dump(ROOT/'reports/C2_nemu_host_drivers.json',{'status':'PASS','cases':467,'sanitizers':['ASAN','UBSAN'],'tests':['160 clipped rectangle cases with independent per-pixel oracle, row stride and guards','300 forced RTC low-half boundary changes between reads','Actual NEMU RTC C callback: five high-low cases and four wrong old-low/new-high combinations exposed','7 key-up/down/none events','sync-only zero-size flush','negative dimension assertion','wrong-stride and low-first-reader mutants rejected'],'sources':[{'path':str(p),'sha256':sha(p)} for p in [*sources,rtc]],'scope':'Real AM driver C and NEMU RTC C compiled against controlled host MMIO/clock shims; actual SDL/NEMU integration checked separately.','stdout':o,'rtc_stdout':ro})

if __name__=='__main__':main()
