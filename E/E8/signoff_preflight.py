from pathlib import Path
import sys,tarfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from ecc_rpc import Rpc
def main():
 workspace=WORK/'physical/light_preflight';review=json.loads((ROOT/'reports/E8_signoff_light_preflight.json').read_text());assert review['status'] in ['ready','attention']
 for risk in review['risks']:
  assert risk['severity']=='warning' and all(d['location']=='config/macro_locations.txt' for d in risk['details'])
 output=ROOT/'artifacts/E8/physical/light_preflight/signoff-preflight.tar.gz'
 staging=WORK/'exports/light-signoff-preflight.tar.gz';staging.parent.mkdir(exist_ok=True)
 with Rpc('E8/rpc/signoff_preflight_export') as rpc:
  opened=rpc.call('workspace.open',{'directory':str(workspace)});result=rpc.call('workspace.export_signoff',{'workspaceId':opened['workspaceId'],'outputPath':str(staging)},timeout=300);assert Path(result['outputPath'])==staging
 shutil.copyfile(staging,output);assert sha(staging)==sha(output)
 with tarfile.open(output) as archive:
  manifest_name=next(m.name for m in archive if m.name.endswith('/manifest.json'));prefix=manifest_name.rsplit('/',1)[0]+'/';manifest=json.load(archive.extractfile(manifest_name));summary=json.load(archive.extractfile(prefix+'summary.json'));assert summary['status']=='ok' and manifest['flow']['all_required_steps_success'] and not manifest['missing_required']
  for row in manifest['files']:
   member=archive.getmember(prefix+row['destination']);stream=archive.extractfile(member);h=hashlib.sha256()
   for chunk in iter(lambda:stream.read(1024*1024),b''):h.update(chunk)
   assert h.hexdigest()==row['sha256'] and member.size==row['size_bytes']
 dump(ROOT/'reports/E8_physical_preflight.json',{'status':'PASS_FULL_SMALL_DESIGN_FLOW_AND_EXPORT','workspace':str(workspace),'review':review,'export_manifest':manifest,'summary':summary,'archive_sha256':sha(output),'scope':'Smallcountertoolchainpreflightonly;doesnotqualifyCPU. Realengine12-stepflow,DRC0,LVS0,timinggatesandactualsignoffexport/manifesthashesverified.'})
 print('SMALL_DESIGN_FULL_FLOW_EXPORT_VERIFIED',len(manifest['files']),flush=True)
if __name__=='__main__':main()
