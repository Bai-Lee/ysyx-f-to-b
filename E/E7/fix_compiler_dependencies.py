from common7 import *
from software_soc import SOFT,clock_config,build,environment
def main():
 am=SOFT/'abstract-machine';wrapper=am/'tools/minirv/minirv-common.sh';old=wrapper.read_text();backup=ROOT/'E/E7/upstream/minirv-common.before-dependency-fix.sh'
 if not backup.exists():backup.write_text(old)
 if 'dep_c=' not in old:
  s=old.replace('dst_S=${dst%.o}.S','dst_S=${dst%.o}.S\ndep_c=${dst%.o}.c.d\ndep_asm=${dst%.o}.asm.d\ndep_final=${dst%.o}.d')
  s=s.replace('riscv64-linux-gnu-$cc $flags -S -o $dst_S $src','riscv64-linux-gnu-$cc $flags -S -MMD -MF "$dep_c" -MT "$dst" -o "$dst_S" "$src"')
  s=s.replace('riscv64-linux-gnu-gcc -I$src_dir $flags -D_LUT_BIN_PATH=', 'riscv64-linux-gnu-gcc -I$src_dir $flags -MMD -MF "$dep_asm" -MT "$dst" -D_LUT_BIN_PATH=')
  s+='\n# Preserve both C-header and generated-assembly dependencies for the actual object.\nif [[ "$src" == *.S ]]; then\n  cat "$dep_asm" > "$dep_final"\n  printf "%s: %s\\n" "$dst" "$src" >> "$dep_final"\nelse\n  cat "$dep_c" "$dep_asm" > "$dep_final"\nfi\n';wrapper.write_text(s)
 for n in ['trm.c','timer.c']:(am/'am/src/riscv/npc'/n).touch()
 rows=[]
 for divisor in [13,27,13]:
  header=clock_config(25000000,divisor);image=build('dummy','E7-SOC','dependency_divisor_'+str(divisor));out=ROOT/'artifacts/E7/compiler_dependencies'/('divisor_'+str(divisor))/'result.json';exe=WORK/'build/E7/soc/sim'
  o,e,r=run('E7/compiler_dependencies/divisor_'+str(divisor),[exe,'--image',image,'--report',out,'--max-cycles','20000000'],inputs=[exe,image,header,wrapper],outputs=[out],timeout=30)
  d=json.loads(out.read_text());assert d['result']=='GOOD_TRAP' and d['uart_divisors']==[13,divisor],d
  dep=am/'am/build/minirv-ysyxsoc/src/riscv/npc/trm.d';assert 'e7_config.h' in dep.read_text() and 'trm.c' in dep.read_text()
  rows.append({'divisor':divisor,'result':d,'dependency_sha256':sha(dep),'image_sha256':sha(image)})
 dest=ROOT/'E/E7/runtime_patch/minirv-common.fixed.sh';shutil.copyfile(wrapper,dest)
 dump(ROOT/'reports/E7_compiler_dependencies.json',{'status':'PASS','cases':rows,'wrapper_sha256':sha(wrapper),'cause':'The two-stage C->assembly->object wrapper overwrote C-header dependencies during assembly. Changing only e7_config.h therefore left stale UART/timer code. Both dependency sets now target the object and are retained. RealSoCdummy verified13->27->13 changes without touching Csource between switches.'})
 print('COMPILER_HEADER_DEPENDENCIES_FIXED_AND_VERIFIED',flush=True)
if __name__=='__main__':main()
