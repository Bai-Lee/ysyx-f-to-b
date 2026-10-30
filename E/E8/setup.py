from pathlib import Path
import sys,resource
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from install_prebuilt import install
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(40,40))
 source=WORK/'workbench-e7';dest=WORK/'workbench-e8';dest.mkdir(exist_ok=True)
 for name in ['abstract-machine','am-kernels']:
  if not (dest/name).exists():shutil.copytree(source/name,dest/name,ignore=shutil.ignore_patterns('.git','build','__pycache__','.result','Makefile.*'))
 am=dest/'abstract-machine';install(am,'minirv-npc','E8/klib')
 trm=am/'am/src/riscv/npc/trm.c';s=trm.read_text()
 if '0xf0000000u' not in s:s=s.replace('void halt(int code) {','void halt(int code) {\n  /* Testbench-only exit status for mapped netlists with no debug/GPR ports. */\n  *(volatile uint32_t *)0xf0000000u=(uint32_t)code;');trm.write_text(s)
 p=ROOT/'E/E8/software';p.mkdir(exist_ok=True);shutil.copyfile(trm,p/'trm.c');shutil.copyfile(am/'am/src/riscv/npc/timer.c',p/'timer.c')
 rows=[]
 for name in ['hello','microbench']:
  cwd=dest/'am-kernels'/('kernels/hello' if name=='hello' else 'benchmarks/microbench');image=cwd/'build'/(name+'-minirv-npc.bin')
  run('E8/software/'+name,['make','-j1','ARCH=minirv-npc','mainargs=test','insert-arg'],cwd=cwd,env={'AM_HOME':str(am),'NPC_HOME':str(dest/'npc')},inputs=[trm,am/'am/src/riscv/npc/timer.c',cwd/'Makefile'],outputs=[image],timeout=300)
  shutil.copyfile(image,p/image.name);rows.append({'name':name,'image':str(p/image.name),'sha256':sha(image)})
 dump(ROOT/'reports/E8_software.json',{'status':'BUILT','programs':rows,'instrumentation':'Only halt gains a testbench MMIO status store before the unchanged a0/ebreak sequence. Upstream application algorithms, input sizes and validation predicates unchanged. Memory model provides an 8-byte flash trampoline to the AM image at80000000; no SoC/controllers are included in these CPU-only netlist tests.'})
 print('E8_PROGRAM_IMAGES_BUILT',flush=True)
if __name__=='__main__':main()
