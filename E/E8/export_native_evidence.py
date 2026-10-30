from pathlib import Path
import sys,tarfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
 assert json.loads((ROOT/'reports/E8_AUDIT.json').read_text())['status']=='PASS'
 base=WORK/'physical/cpu_baseline';files=set()
 for name in ['config','home','origin','log']:files.update(p for p in (base/name).rglob('*') if p.is_file() and not p.name.endswith('.lock'))
 for step in base.glob('*_*'):
  if not step.is_dir():continue
  for name in ['log','analysis']:files.update(p for p in (step/name).rglob('*') if p.is_file())
  files.update(p for p in [step/'subflow.json',step/'checklist.json'] if p.is_file())
 target=ROOT/'E/E8/signoff/native-run-evidence.tar.gz';files=sorted(files)
 with tarfile.open(target,'w:gz') as archive:
  for path in files:archive.add(path,arcname=path.relative_to(base).as_posix(),recursive=False)
 expected={p.relative_to(base).as_posix():sha(p) for p in files};verified=0
 with tarfile.open(target,'r|gz') as archive:
  for member in archive:
   assert member.isfile() and member.name in expected;stream=archive.extractfile(member);h=hashlib.sha256()
   for chunk in iter(lambda:stream.read(1024*1024),b''):h.update(chunk)
   assert h.hexdigest()==expected[member.name];verified+=1
 assert verified==len(files)
 dump(ROOT/'reports/E8_native_evidence_export.json',{'status':'PASS','archive':str(target.relative_to(ROOT)),'sha256':sha(target),'files':[{'path':p,'sha256':h} for p,h in expected.items()],'scope':'Actualnativeflowlogs,configs,homeflow/checklistsandqualityanalysis. FinalGDS/DEF/LEF/LIB/SPEF/STA artifactsareintheengine-generatedsignoffpackage;intermediateworkingdatabasesremaininWSL.'})
 print('NATIVE_BACKEND_EVIDENCE_EXPORTED_AND_VERIFIED',verified,flush=True)
if __name__=='__main__':main()
