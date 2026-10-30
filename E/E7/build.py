from common7 import *
import argparse
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--mode',choices=['ifu','lsu','valid','random','soc','soc_gui'],default='soc');parser.add_argument('--prepare-only',action='store_true');args=parser.parse_args();p=ROOT/'E/E7';rt=ROOT/'E/runtime'
 obj=WORK/'build/E7/ref.o';obj.parent.mkdir(parents=True,exist_ok=True)
 if not obj.exists() or obj.stat().st_mtime<(rt/'ref.c').stat().st_mtime:run('E7/ref_compile',['gcc','-std=c11','-O3','-g','-Wall','-Wextra','-Werror','-c',rt/'ref.c','-o',obj],inputs=[rt/'ref.c',rt/'ref.h'])
 npc=BENCH7/'npc'
 for f in [ROOT/'E/E5/rtl/minirv_decode.sv',ROOT/'E/E5/rtl/minirv_regfile.sv',*sorted((p/'rtl').glob('*'))]:
  if f.is_file():shutil.copyfile(f,npc/'vsrc'/f.name)
 for f in [p/'soc_runner.cpp',p/'bus_runner.cpp',rt/'ref.c',rt/'ref.h',rt/'memory.hpp']:shutil.copyfile(f,npc/'csrc'/f.name)
 (npc/'.gitignore').write_text('*\n!Makefile\n!.gitignore\n!csrc/\n!vsrc/\n!*.cpp\n!*.c\n!*.h\n!*.hpp\n!*.sv\n!*.v\n')
 sources=[npc/'vsrc/minirv_decode.sv',npc/'vsrc/minirv_regfile.sv',npc/'vsrc/minirv_bus.sv']
 if args.mode in ['soc','soc_gui']:
  soc=BENCH7/'ysyxSoC';shutil.copyfile(p/'rtl/mygpio_top_apb.v',soc/'perip/gpio/mygpio_top_apb.v');sources+=[npc/'vsrc/ysyx_00000000.sv',soc/'ready-to-run/minirv/ElaborateTop.v',*sorted((soc/'perip').rglob('*.v')),*sorted((soc/'perip').rglob('*.sv'))]
  flags=['--trace','--timescale','1ns/1ps','--no-timing','-D__VERILOG__','-DPDK_BEHAV','-D__UART_TO_CONSOLE__','-I'+str(soc/'perip/uart16550/rtl'),'-I'+str(soc/'perip/spi/rtl'),'-Wno-fatal','-MAKEFLAGS','OPT_FAST=-O3 OPT_SLOW=-O3','-CFLAGS','-O3 -I'+str(rt)]
  cpp=[npc/'csrc/soc_runner.cpp'];extra=[obj]
  if args.mode=='soc_gui':
   nv=BENCH7/'nvboard';uart=nv/'src/uart.cpp';text=uart.read_text();text=text.replace('divisor(16)','divisor(208)');uart.write_text(text)
   run('E7/nvboard/build',['make','-f',nv/'scripts/nvboard.mk','-j1','nvboard-archive'],cwd=WORK,env=env7({'NVBOARD_HOME':str(nv)}),inputs=[uart],timeout=300)
   bind=WORK/'build/E7/auto_bind.cpp';run('E7/nvboard/bind',['python3',nv/'scripts/auto_pin_bind.py',p/'constr/soc.nxdc',bind],inputs=[p/'constr/soc.nxdc'],env={'NVBOARD_HOME':str(nv)})
   cpp.append(bind);extra += [nv/'build/nvboard.a','-LDFLAGS','-lSDL2 -lSDL2_image -lSDL2_ttf'];flags[-1]+=' -DENABLE_NVBOARD -I'+str(nv/'usr/include')+' '+subprocess.check_output(['sdl2-config','--cflags'],text=True).strip()
  if args.prepare_only:
   target=WORK/'build/E7'/args.mode;target.mkdir(parents=True,exist_ok=True)
   run('E7/'+args.mode+'/prepare',[VERILATOR,'--cc','--exe','--assert','-Wall','--top-module','SimTop','--Mdir',target,'-o','sim',*flags,*sources,*cpp,*extra],inputs=[*sources,*cpp,rt/'ref.h'],timeout=90)
   print('E7_SOC_TRANSLATED_NOT_BUILT',target,flush=True);return
  exe=build('E7/'+args.mode,'SimTop',sources,cpp,extra=extra,flags=flags,additional_inputs=[rt/'ref.h'])
 else:
  mode={'ifu':1,'lsu':2,'valid':3,'random':3}[args.mode]
  exe=build('E7/'+args.mode,'minirv_bus',sources,[npc/'csrc/bus_runner.cpp'],extra=[obj],flags=['--trace','--timescale','1ns/1ns','-GMODE='+str(mode),'-GRANDOM_DELAY='+str(int(args.mode=='random')),'-MAKEFLAGS','OPT_FAST=-O3 OPT_SLOW=-O3','-CFLAGS','-O3 -I'+str(rt)],additional_inputs=[rt/'memory.hpp',rt/'ref.h'])
 print('E7_BUILT',exe,flush=True)
if __name__=='__main__':main()
