"""Read-only hash audit of all previously delivered stage evidence."""
from evidence import *
import re

def main():
    baseline=json.loads((ROOT/'reports/B_baseline.json').read_text('utf8'))
    manifest_path=ROOT/'reports/C_delivery_manifest.json'
    assert sha(manifest_path)==baseline['C_manifest_sha256']
    manifest=json.loads(manifest_path.read_text('utf8'));checked=[]
    for row in manifest['entries']:
        parts=Path(row['path']).parts
        keep=parts[0] in {'F','E','D','C'}
        keep|=parts[0]=='artifacts' and len(parts)>1 and bool(re.match(r'^[FEDC](?:\d|$)',parts[1]))
        keep|=parts[0]=='reports' and bool(re.match(r'^[FEDC](?:\d|_)',Path(row['path']).name))
        if not keep:continue
        path=ROOT/row['path'];assert path.is_file() and path.stat().st_size==row['bytes'] and sha(path)==row['sha256'],row['path']
        checked.append(row)
        if len(checked)%5000==0:print('B_PRIOR_FILES_VERIFIED',len(checked),flush=True)
    archives=[]
    for name in ['YSYX_D_DELIVERY.zip','YSYX_C_DELIVERY.zip']:
        path=ROOT/name;assert path.is_file();expected=(path.with_suffix('.zip.sha256')).read_text().split()[0]
        assert sha(path)==expected
        if name=='YSYX_C_DELIVERY.zip':assert expected==baseline['C_zip_sha256'] and path.stat().st_size==baseline['C_zip_bytes']
        archives.append({'path':name,'sha256':expected,'bytes':path.stat().st_size})
    dump(ROOT/'reports/B_history_preservation.json',{'status':'PASS','timestamp':datetime.now(timezone.utc).isoformat(),
        'baseline_manifest_sha256':baseline['C_manifest_sha256'],'checked_files':len(checked),'checked_bytes':sum(x['bytes'] for x in checked),
        'checked_list_sha256':hashlib.sha256(json.dumps(checked,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        'archives':archives,'scope':'Every F/E/D/C source, stage report and command artifact present in the prior C manifest is byte-identical. New early-B telemetry sessions under artifacts/C are additions outside that frozen set; subsequent telemetry is B-owned. Root project status/configuration changes are separately backed up and authorized by B scope.'})
    print('B_HISTORY_PRESERVATION_PASS',len(checked),flush=True)

if __name__=='__main__':main()
