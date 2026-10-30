"""Export only after the real ECC checklist permits it, then verify every file."""
from pathlib import Path,PurePosixPath
import sys,tarfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from ecc_rpc import Rpc
def main():
 workspace=WORK/'physical/cpu_baseline';dest=ROOT/'E/E8/signoff';dest.mkdir(exist_ok=True);output=dest/'cpu-baseline-signoff.tar.gz'
 staging=WORK/'exports/cpu-baseline-signoff.tar.gz';staging.parent.mkdir(exist_ok=True)
 assert json.loads((ROOT/'reports/E8_final_mapped.json').read_text())['status']=='PASS'
 with Rpc('E8/rpc/final_signoff') as rpc:
  opened=rpc.call('workspace.open',{'directory':str(workspace)});review=rpc.call('workspace.inspect_signoff',{'workspaceId':opened['workspaceId']},timeout=300)
  dump(ROOT/'reports/E8_final_signoff_review.json',review);assert review['status'] in ['ready','attention'],review['status']
  for risk in review['risks']:
   assert risk['severity']!='blocked'
   for detail in risk['details']:
    assert detail['location']=='config/macro_locations.txt' and 'macro' in detail['label'].lower(),detail
  if output.exists():
   history=ROOT/'artifacts/E8/signoff_history'/str(time.time_ns());history.mkdir(parents=True);shutil.copyfile(output,history/output.name)
  result=rpc.call('workspace.export_signoff',{'workspaceId':opened['workspaceId'],'outputPath':str(staging)},timeout=600);assert Path(result['outputPath'])==staging
 shutil.copyfile(staging,output);assert sha(staging)==sha(output)
 with tarfile.open(output) as archive:
  members=archive.getmembers();assert members
  for member in members:
   path=PurePosixPath(member.name);assert not path.is_absolute() and '..' not in path.parts and not member.issym() and not member.islnk(),member.name
  manifest_name=next(x.name for x in members if x.name.endswith('/manifest.json'));prefix=manifest_name.rsplit('/',1)[0]+'/'
  manifest=json.load(archive.extractfile(manifest_name));summary=json.load(archive.extractfile(prefix+'summary.json'));assert summary['status']=='ok' and not manifest['missing_required'] and not summary['missing_required'] and manifest['flow']['all_required_steps_success']
  assert manifest['top_module']=='ysyx_00000000';verified=[]
  for entry in manifest['files']:
   name=prefix+entry['destination'];member=archive.getmember(name);stream=archive.extractfile(member);assert stream is not None;h=hashlib.sha256()
   for chunk in iter(lambda:stream.read(1024*1024),b''):h.update(chunk)
   assert h.hexdigest()==entry['sha256'] and member.size==entry['size_bytes'],name
   verified.append({'path':entry['destination'],'role':entry['role'],'bytes':member.size,'sha256':h.hexdigest()})
  # Preview exactly the exported design image; never substitute a mock layout.
  image_name=summary['final']['image'];image=archive.extractfile(prefix+image_name);assert image is not None
  (dest/'layout.png').write_bytes(image.read());dump(dest/'summary.json',summary);dump(dest/'manifest.json',manifest)
 dump(ROOT/'reports/E8_signoff_export.json',{'status':'PASS','archive':str(output.relative_to(ROOT)),'sha256':sha(output),'verified_files':verified,'all_manifest_file_hashes_verified':True,'review':review,'summary':summary,'scope':'ActualECCengineexportaftercurrentchecklistinspection, theneverymanifestmemberhash/sizeverified. Localphysicalsignoffpackage, notmanufacturingorofficialadmission.'})
 print('ACTUAL_SIGNOFF_EXPORT_AND_ALL_MEMBER_HASHES_PASS',len(verified),flush=True)
if __name__=='__main__':main()
