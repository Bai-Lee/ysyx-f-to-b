"""Recover immutable, actually compiled baseline RTL from recorded input ZIPs."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[2]
def digest(b):return hashlib.sha256(b).hexdigest()
def main():
    rows=[]
    for name in ['pipeline-stall','pipeline-forward']:
        origin=ROOT/'artifacts/B/standalone/build'/name;record=json.loads((origin/'run.json').read_text());assert record['status']=='PASS'
        before=record['inputs'];after={r['path']:r['sha256'] for r in record['inputs_after']};folder=ROOT/'B/B4/snapshots'/name/'rtl';folder.mkdir(parents=True,exist_ok=True);files=[]
        with zipfile.ZipFile(origin/'input_snapshot.zip') as archive:
            for i,item in enumerate(before):
                if '/B/soc/rtl/' not in item['path']:continue
                assert after[item['path']]==item['sha256']
                filename=Path(item['path']).name;b=archive.read(f'{i:03d}_{filename}');assert digest(b)==item['sha256'];dest=folder/filename
                if dest.exists():assert dest.read_bytes()==b
                else:dest.write_bytes(b)
                files.append({'path':str(dest.relative_to(ROOT)),'source':item['path'],'sha256':digest(b)})
        assert any(r['path'].endswith('ysyx_00000000_pipe.sv') for r in files)
        rows.append({'variant':name,'input_snapshot_sha256':digest((origin/'input_snapshot.zip').read_bytes()),'run_record_sha256':digest((origin/'run.json').read_bytes()),'files':files})
    (ROOT/'reports/B4_baseline_sources.json').write_text(json.dumps({'status':'PASS_IMMUTABLE_BASELINE_SOURCES','variants':rows,'scope':'Exact RTL bytes used by the accepted baseline builds; input hashes were unchanged during compilation. Full SoC comparison rebuilds these copies under distinct labels.'},indent=2),encoding='utf8')
    print('B4_BASELINE_SOURCES_FROZEN')
if __name__=='__main__':main()
