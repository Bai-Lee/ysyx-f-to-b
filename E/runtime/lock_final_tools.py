"""Record the actual executable and PDK inputs used by the completed E flow."""
from common import *
import re
def main():
 lock=json.loads((ROOT/'reports/E_backend_compatible_tools.json').read_text());ecc=Path(lock['ecc']);base=ecc.parent
 binaries=[VERILATOR,VROOT/'bin/verilator_bin',Path('/usr/bin/iverilog'),Path('/usr/bin/vvp'),Path(lock['yosys_root'])/'bin/yosys',Path(lock['yosys_root'])/'libexec/yosys',Path('/home/USER/tools/e-stage/oss-20261022/oss-cad-suite/bin/iverilog'),Path('/home/USER/tools/e-stage/oss-20261022/oss-cad-suite/libexec/iverilog'),Path('/home/USER/tools/e-stage/oss-20261022/oss-cad-suite/bin/vvp'),Path('/home/USER/tools/e-stage/oss-20261022/oss-cad-suite/libexec/vvp'),ecc,base/'chip-viewer-native',base.parents[1]/'ecos-studio-bin']
 for folder in [base/'_internal/ecc_tools_bin',base/'_internal/dreamplace']:
  binaries += list(folder.rglob('*.so'))
 binaries += [p for p in Path('/home/USER/tools/e-stage/gui-libs/usr/lib/x86_64-linux-gnu').glob('*.so*') if p.is_file()]
 models=set();workspace=WORK/'physical/cpu_baseline'
 for logfile in workspace.glob('*_*/log/*.log'):
  for value in re.findall(r'/home/USER/tools/icsprout55-e-stage/[^\s\x1b\x00]+?\.(?:lib|lef|gds|ict|json|v)',logfile.read_text(errors='replace')):
   file=Path(value)
   if file.is_file():models.add(file)
 def collect(value):
  if isinstance(value,dict):
   for v in value.values():collect(v)
  elif isinstance(value,list):
   for v in value:collect(v)
  elif isinstance(value,str) and value.startswith('/home/USER/tools/icsprout55-e-stage/') and Path(value).is_file():models.add(Path(value))
 for folder in ['config','home','origin']:
  for file in (workspace/folder).glob('*.json'):collect(json.loads(file.read_text()))
 for item in json.loads((ROOT/'reports/E8_mapped_preflight.json').read_text())['library_models']:
  file=Path(item['path']);assert sha(file)==item['sha256'];models.add(file)
 def records(files):
  result=[]
  for file in sorted(set(files)):
   assert file.is_file(),file;result.append({'path':str(file),'bytes':file.stat().st_size,'sha256':sha(file),'mtime_utc':datetime.datetime.fromtimestamp(file.stat().st_mtime,datetime.timezone.utc).isoformat()})
  return result
 libs=[x for x in models if x.suffix=='.lib'];assert len(libs)>=10
 data={'status':'PASS_LOCKED_AFTER_FLOW','captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'binary_fingerprints':records(binaries),'physical_model_fingerprints':records(models),'installed_bundle_versions':json.loads((ROOT/'reports/E_backend_bundle_version.json').read_text()),'official_assets_evidence':'reports/E_backend_assets.json','compatibility_evidence':'reports/E_backend_compatible_tools.json','qualification':['reports/E7_AUDIT.json','reports/E8_AUDIT.json'],'scope':'ActuallauncherandELF/shared-libraryhashesplusPDKfilesnamedbythenativeflowlogs. Capturedafterthesuccessfulflow;officialreleaseassetdigestsandinstallationreceiptsremainseparate. NoPDKmodelwaseditedduringtheCPUflow.'};dump(ROOT/'reports/E_toolchain_final.json',data);print('FINAL_TOOL_AND_MODEL_FINGERPRINTS_LOCKED',len(binaries),len(models),flush=True)
if __name__=='__main__':main()
