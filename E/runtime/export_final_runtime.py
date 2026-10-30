"""Archive only the working sources/resources needed to replay the delivered CPU."""
from common import *
import tarfile
def main():
 assert json.loads((ROOT/'reports/E7_AUDIT.json').read_text())['status']=='PASS'
 assert json.loads((ROOT/'reports/E8_final_mapped.json').read_text())['status']=='PASS'
 bench7=WORK/'workbench-e7';soft=WORK/'software-soc';entries=[]
 bases=[('npc',bench7/'npc'),('am_npc',bench7/'abstract-machine'),('am_soc',soft/'abstract-machine'),('am_timer',WORK/'software-timer-npc/abstract-machine'),('am_gate',WORK/'workbench-e8/abstract-machine'),('nvboard',bench7/'nvboard'),('soc/perip',bench7/'ysyxSoC/perip'),('soc/ready-to-run/minirv',bench7/'ysyxSoC/ready-to-run/minirv'),('soc/spec',bench7/'ysyxSoC/spec'),('timer_program',WORK/'software-timer-npc/timer')]
 for prefix,base in bases:
  assert base.exists(),base
  for path in sorted(base.rglob('*')):
   rel=path.relative_to(base)
   if any(x in ['build','.git','__pycache__'] for x in rel.parts) or path.suffix in ['.o','.pyc'] or not path.is_file():continue
   assert path.resolve().is_relative_to(base.resolve()),path
   entries.append((path,prefix+'/'+rel.as_posix()))
 for prefix,am in [('am_npc',bench7/'abstract-machine'),('am_soc',soft/'abstract-machine'),('am_timer',WORK/'software-timer-npc/abstract-machine'),('am_gate',WORK/'workbench-e8/abstract-machine')]:
  for f in sorted((am/'klib/build').glob('klib-*.a')):entries.append((f,prefix+'/klib/build/'+f.name))
 for name in ['README.md','LICENSE','LICENSE.txt']:
  file=bench7/'ysyxSoC'/name
  if file.is_file():entries.append((file,'soc/'+name))
 for source,name in [(WORK/'build/E8/mapped_baseline/sim','gate/netlist-verilator-linux'),(WORK/'build/E8/profile/14/udp.vvp','gate/netlist-icarus14.vvp'),(WORK/'build/E8/profile/14/vpi_memory.vpi','gate/vpi_memory.vpi'),(WORK/'workbench/fceux-am/build/fceux-minirv-npc.bin','fceux/fceux-minirv-npc.bin')]:assert source.is_file();entries.append((source,name))
 target=ROOT/'E/offline/patched-runtime.tar.gz';assert len(entries)==len({n for _,n in entries})
 with tarfile.open(target,'w:gz',compresslevel=6,dereference=True) as archive:
  for file,name in entries:archive.add(file,arcname=name,recursive=False)
 records=[]
 with tarfile.open(target) as archive:
  for file,name in entries:
   member=archive.getmember(name);assert member.isfile();stream=archive.extractfile(member);h=hashlib.sha256()
   for chunk in iter(lambda:stream.read(1024*1024),b''):h.update(chunk)
   digest=sha(file);assert h.hexdigest()==digest and member.size==file.stat().st_size,name
   records.append({'path':name,'bytes':member.size,'sha256':digest,'source':str(file)})
 dump(ROOT/'reports/E_runtime_export.json',{'status':'PASS','archive':str(target.relative_to(ROOT)),'sha256':sha(target),'members':records,'all_members_verified':True,'scope':'PatchedAM/NPC/SoCinterface/peripheral/NVBoardresourcesandselectedexecutables. Sourcesretainupstreamlicensefiles. Existinginstalledtoolruntimes/PDKreleaseassetsremainseparatelylocked; thisisnotanOSinstaller.'})
 print('PATCHED_RUNTIME_OFFLINE_EXPORT_PASS',len(records),flush=True)
if __name__=='__main__':main()
