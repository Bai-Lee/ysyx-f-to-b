"""Boot once, execute every unchanged official test body on the real SoC.

Namespacing copied ELF objects avoids symbol collisions. Every allocated code
and data section is byte-compared before/after objcopy. Assembly tests retain
their original pass/fail code; only their external halt relocation returns to
a dispatcher that checks the same0/nonzero status. A separate wrong batch
proves failure propagation. No test predicate/input/instruction is removed.
"""
from common7 import *
from install_prebuilt import install
import struct,re,resource
SOFT=WORK/'software-soc'
def allocations(path):
 b=Path(path).read_bytes();assert b[:6]==b'\x7fELF\x01\x01';offset=struct.unpack_from('<I',b,32)[0];size,count,names_index=struct.unpack_from('<HHH',b,46)
 sh=[struct.unpack_from('<10I',b,offset+i*size) for i in range(count)];ns=sh[names_index];strings=b[ns[4]:ns[4]+ns[5]];out={}
 for h in sh:
  if h[2]&2:
   name=strings[h[0]:].split(b'\0',1)[0].decode();out[name]=(h[1],h[2],h[5],None if h[1]==8 else hashlib.sha256(b[h[4]:h[4]+h[5]]).hexdigest())
 return {'flags':struct.unpack_from('<I',b,36)[0],'allocated_sections':out}
def environment():return env7({'AM_HOME':str(SOFT/'abstract-machine')})
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(40,40))
 SOFT.mkdir(exist_ok=True);am=SOFT/'abstract-machine'
 if not am.exists():shutil.copytree(BENCH7/'abstract-machine',am,ignore=shutil.ignore_patterns('build','.git','__pycache__'))
 link=SOFT/'ysyxSoC'
 if not link.exists():link.symlink_to(BENCH7/'ysyxSoC',target_is_directory=True)
 for arch in ['minirv-npc','minirv-ysyxsoc']:install(am,arch,'E7/batch/klib/'+arch)
 root=SOFT/'batch';root.mkdir(exist_ok=True);objects=root/'objects';objects.mkdir(exist_ok=True);manifest=[]
 official=json.loads((ROOT/'reports/E6_official_tests.json').read_text())
 tests=[]
 for suite in sorted(official['suites'],key=lambda x:x['suite']):
  for item in suite['tests']:
   name=item['test'];iscpu=suite['suite']=='cpu-tests';prefix='cpu' if iscpu else 'isa';tag=prefix+'_'+name.replace('-','_')
   source=(BENCH/'am-kernels/tests/cpu-tests/build/minirv-npc/tests' if iscpu else BENCH/'riscv-tests/build/minirv-npc/isa/rv32ui')/(name+'.o')
   tests.append((prefix+':'+name,tag,source,not iscpu,item['image_sha256']))
 wrong=BENCH/'am-kernels/tests/cpu-tests/build/minirv-npc/tests/wrong.o';tests.append(('cpu:wrong','cpu_wrong',wrong,False,None))
 for name,tag,src,isasm,solo_hash in tests:
  assert src.exists(),src
  nm=subprocess.check_output(['riscv64-linux-gnu-nm','-g','--defined-only',src],text=True)
  symbols=[]
  for line in nm.splitlines():
   fields=line.split()
   if len(fields)==3 and fields[1].upper() not in ['W','V']:symbols.append(fields[2])
  assert 'main' in symbols
  mappings=[(s,tag+'__'+s) for s in symbols]
  if isasm:mappings.append(('halt','batch_return'))
  mapfile=objects/(tag+'.symbols');mapfile.write_text(''.join(a+' '+b+'\n' for a,b in mappings));dest=objects/(tag+'.o')
  before=sha(src);run('E7/batch/namespace/'+tag,['riscv64-linux-gnu-objcopy','--redefine-syms='+str(mapfile),src,dest],inputs=[src,mapfile],outputs=[dest]);assert sha(src)==before and allocations(src)==allocations(dest)
  row={'id':name,'symbol':tag+'__main','asm':isasm,'original_object':str(src),'original_sha256':before,'namespaced_object':str(dest),'namespaced_sha256':sha(dest),'allocated_sections_unchanged':True,'allocated_sections':allocations(src),'prior_individual_passed_image_sha256':solo_hash,'mapping':[list(x) for x in mappings]};manifest.append(row)
 for kind,selected in [('all',[x for x in manifest if x['id']!='cpu:wrong']),('wrong',[x for x in manifest if x['id']=='cpu:wrong'])]:
  directory=root/kind;directory.mkdir(exist_ok=True);shutil.copyfile(ROOT/'E/E7/batch_bridge.S',directory/'batch_bridge.S')
  declarations='\n'.join('extern int '+x['symbol']+'(void);' for x in selected)
  table=',\n'.join('{"'+x['id']+'", '+x['symbol']+', '+str(int(x['asm']))+'}' for x in selected)
  source='''#include <am.h>
#include <klib.h>
extern int batch_call(int (*fn)(void));
'''+declarations+'''
struct test_case {const char *name;int (*fn)(void);int assembly;};
static const struct test_case cases[]={
'''+table+'''};
static uint64_t count(void){uint32_t h,l,h2;do{asm volatile("csrr %0,mcycleh":"=r"(h));asm volatile("csrr %0,mcycle":"=r"(l));asm volatile("csrr %0,mcycleh":"=r"(h2));}while(h!=h2);return ((uint64_t)h<<32)|l;}
int main(const char *args){(void)args;for(unsigned i=0;i<sizeof(cases)/sizeof(cases[0]);i++){
 printf("[CASE] %s BEGIN\\n",cases[i].name);uint64_t start=count();
 int code=cases[i].assembly?batch_call(cases[i].fn):cases[i].fn();uint64_t elapsed=count()-start;
 if(code){printf("[CASE] %s FAIL code=%d\\n",cases[i].name,code);halt(code);}
 printf("[CASE] %s PASS cycles=%llu\\n",cases[i].name,elapsed);
 }printf("BATCH_ALL_PASSED %u\\n",(unsigned)(sizeof(cases)/sizeof(cases[0])));return 0;}
'''
  (directory/'main.c').write_text(source);(directory/'Makefile').write_text('NAME=official-batch-'+kind+'\nSRCS=main.c batch_bridge.S\nLINKAGE += '+' '.join(x['namespaced_object'] for x in selected)+'\ninclude $(AM_HOME)/Makefile\n')
  for arch in ['minirv-npc','minirv-ysyxsoc']:
   image=directory/'build'/('official-batch-'+kind+'-'+arch+'.bin');elf=image.with_suffix('.elf')
   run('E7/batch/build/'+kind+'_'+arch,['make','-j1','ARCH='+arch,'mainargs=test','insert-arg'],cwd=directory,env=environment(),inputs=[directory/'main.c',directory/'batch_bridge.S',directory/'Makefile',am/'am/src/riscv/npc/trm.c'],outputs=[image,elf],timeout=300)
   # AM linked address range must fit the actual8MiB PSRAM, not the flat128MiB model.
   syms=subprocess.check_output(['riscv64-linux-gnu-nm','-n',elf],text=True);end=int(re.search(r'^([0-9a-f]+)\s+\w\s+_heap_start$',syms,re.M)[1],16);assert end<0x80800000
   dest=ROOT/'E/E7/batch'/kind;dest.mkdir(parents=True,exist_ok=True);shutil.copyfile(image,dest/image.name);shutil.copyfile(elf,dest/elf.name);shutil.copyfile(directory/'main.c',dest/'main.c');shutil.copyfile(directory/'batch_bridge.S',dest/'batch_bridge.S')
  image=directory/'build'/('official-batch-'+kind+'-minirv-npc.bin');exe=WORK/'build/E7/valid/sim';out=ROOT/'artifacts/E7/batch/flat'/kind/'result.json'
  o,e,r=run('E7/batch/flat/'+kind,[exe,'--image',image,'--report',out,'--uart-random','--max-cycles','100000000'],inputs=[exe,image],outputs=[out],expected=(1,) if kind=='wrong' else (0,),timeout=40)
  d=json.loads(out.read_text())
  if kind=='all':
   passed=re.findall(r'^\[CASE\] (\S+) PASS cycles=(\d+)$',o,re.M);assert [n for n,c in passed]==[x['id'] for x in selected] and all(int(c)>0 for n,c in passed);assert d['result']=='GOOD_TRAP' and 'BATCH_ALL_PASSED 73' in o
  else:assert d['result']=='BAD_TRAP' and '[CASE] cpu:wrong FAIL code=1' in o
 dump(ROOT/'reports/E7_batch_integrity.json',{'status':'PASS_OBJECT_PRESERVATION_AND_FLAT_RUN','tests':manifest,'positive_count':73,'negative_count':1,'policy':'Exact object code/data from individually passed E6 tests; onlystrong-symbol namespacing and assemblyhalt relocation change. All allocatedsections byte-identical. C failure checks still call realhalt. Assembly pass/fail status returned through a state-restoring bridge and checked. This batches SoC execution, not test assertions; completeSoC run remains pending.'})
 print('OFFICIAL_BATCH73_BUILT_AND_FLAT_VALIDATED',flush=True)
if __name__=='__main__':main()
