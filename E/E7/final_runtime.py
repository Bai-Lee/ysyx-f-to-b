"""Freeze the corrected build wrappers and check both platform entry paths."""
from common7 import *
from software_soc import SOFT
import resource
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(60,70));patch=ROOT/'E/E7/runtime_patch';am=BENCH7/'abstract-machine'
 for name in ['trm.c','timer.c']:
  source=SOFT/'abstract-machine/am/src/riscv/npc'/name;shutil.copyfile(source,patch/name);shutil.copyfile(source,am/'am/src/riscv/npc'/name)
 wrapper=am/'tools/minirv/minirv-common.sh';before=ROOT/'E/E7/upstream/minirv-common.standalone-before-fixes.sh'
 if not before.exists():shutil.copyfile(wrapper,before)
 shutil.copyfile(patch/'minirv-common.fixed.sh',wrapper)
 make=BENCH7/'npc/Makefile';s=make.read_text().replace('ifeq ($(NPC_MODE),soc)','ifneq ($(filter soc soc_gui,$(NPC_MODE)),)').replace(' --report "$(IMAGE).npc.json" --max-cycles',' --report "$(IMAGE).npc.json" $(if $(filter soc_gui,$(NPC_MODE)),--gui,) --max-cycles',1);make.write_text(s);shutil.copyfile(make,patch/'NPC.Makefile')
 probe=WORK/'build/E7/final_runtime';probe.mkdir(exist_ok=True);bad=probe/'bad.c';bad.write_text('#error intentional_final_compiler_probe\n');output=probe/'bad.o';assert not output.exists()
 o,e,r=run('E7/final_runtime/compiler_negative',[am/'tools/minirv/minirv-gcc','-march=rv32e_zicsr','-mabi=ilp32e','-c','-o',output,bad],env={**env7(),'PATH':str(am/'tools/minirv')+':'+os.environ['PATH']},inputs=[wrapper,bad],expected=(1,));assert not output.exists() and 'intentional_final_compiler_probe' in e
 rows=[]
 for name,cwd in [('hello',BENCH7/'am-kernels/kernels/hello'),('microbench',BENCH7/'am-kernels/benchmarks/microbench')]:
  exe=WORK/'build/E7/valid/sim';o,e,r=run('E7/final_runtime/'+name,['make','-j1','ARCH=minirv-npc','NPC_MODE=valid','mainargs=test','run'],cwd=cwd,env=env7(),inputs=[wrapper,make,am/'am/src/riscv/npc/timer.c',exe],timeout=180)
  image=next((cwd/'build').glob('*-minirv-npc.bin'));data=json.loads(Path(str(image)+'.npc.json').read_text());assert data['result']=='GOOD_TRAP'
  if name=='microbench':assert 'MicroBench PASS' in o
  rows.append({'name':name,'result':data,'image_sha256':sha(image),'simulator_sha256':sha(exe)})
 for mode in ['soc','soc_gui']:
  o,e,r=run('E7/final_runtime/select_'+mode,['make','-n','sim','PLATFORM=ysyxsoc','NPC_MODE='+mode,'IMAGE=probe.bin'],cwd=BENCH7/'npc',env=env7(),inputs=[make]);assert '--image "probe.bin"' in o and '--mode ' not in o
  if mode=='soc_gui':assert '--gui' in o
 dump(ROOT/'reports/E7_final_runtime.json',{'status':'PASS','standalone_programs':rows,'soc_actual_evidence':'E7_soc_software.json and E7_soc_tests.json','compiler_wrapper_sha256':sha(wrapper),'makefile_sha256':sha(make),'policy':'CopiedalreadyverifiedSoCcompiler/headerfixesintostandaloneworkingcopy; originalwrapperpreserved. Standalonefullmicrobench/hello rerun; SoCactualexecutionsretained. GUIselectoralsocheckedthroughmake-n.'})
 mark(['E7-M030'],'PASS',['reports/E7_final_runtime.json','reports/E7_soc_software.json','reports/E7_standalone.json','E/E7/runtime_patch/NPC.Makefile'],'OneNPCMakefile selectsindependentbusCPUoractualSoC; bothactuallyexecuteAMapplications. Correctcompiler/headerdependencyfixesfrozenandrecheckedwithfullmicrobench; GUIselectorpassescorrectarguments.')
 print('FINAL_PLATFORM_BUILD_ENTRY_CHECK_PASS',flush=True)
if __name__=='__main__':main()
