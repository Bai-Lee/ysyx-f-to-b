"""Reconstruct missing snapshots only when bytes match the recorded execution hash.

Historical run.json is never rewritten. Provenance explicitly says reconstructed,
not captured at execution. This also detects overwritten generated inputs.
"""
from pathlib import Path
import json,hashlib,zipfile,datetime,re
ROOT=Path(__file__).resolve().parents[2]
def sha_bytes(b):return hashlib.sha256(b).hexdigest()
def native(s):
    if re.match(r'^[A-Za-z]:',s):return Path('/mnt/'+s[0].lower()+s[2:].replace('\\','/'))
    return Path(s)
def main():
    specs=json.loads((ROOT/'E/E3/course_specs.json').read_text())
    frozen={}
    for c in specs['chapters']:
        for b in c['blocks']:
            p=native(b['path']);data=p.read_bytes();assert sha_bytes(data)==b['sha256'];frozen[b['sha256']]=(p,data)
    prior=ROOT/'reports/E3_input_recovery.json'
    previous=json.loads(prior.read_text()) if prior.exists() else {}
    recovered_by_path={r['record']:r for r in previous.get('reconstructed',[])}
    rows=[];missing=[];checked=0
    for f in sorted((ROOT/'artifacts/E3').rglob('run.json')):
        if 'attempts' in f.parts:continue
        d=json.loads(f.read_text());inputs=d.get('inputs',[])
        if not inputs:continue
        target=f.parent/'input_snapshot.zip'
        if target.exists():
            with zipfile.ZipFile(target) as z:
                for i,x in enumerate(inputs):
                    name=f'{i:02d}_{native(x["path"]).name}'
                    assert sha_bytes(z.read(name))==x['sha256'],f
            checked+=1;continue
        recovered=[]
        for i,x in enumerate(inputs):
            p=native(x['path']);wanted=x['sha256']
            if p.is_file() and sha_bytes(p.read_bytes())==wanted:data=p.read_bytes();origin=str(p)
            elif wanted in frozen:origin=str(frozen[wanted][0]);data=frozen[wanted][1]
            else:missing.append({'record':str(f.relative_to(ROOT)),'input':x});continue
            assert b'-----BEGIN OPENSSH PRIVATE KEY-----' not in data
            recovered.append((f'{i:02d}_{p.name}',data,origin,wanted))
        if len(recovered)!=len(inputs):continue
        with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
            for name,data,origin,wanted in recovered:z.writestr(name,data)
        rows.append({'record':str(f.relative_to(ROOT)),'snapshot':str(target.relative_to(ROOT)),'provenance':'Reconstructed from byte-identical current or frozen sources after execution; original recorded hashes unchanged.','entries':[{'name':n,'from':o,'sha256':s} for n,b,o,s in recovered]})
    for row in rows:recovered_by_path[row['record']]=row
    result={'status':'PASS' if not missing else 'FAIL','timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'existing_verified':checked,'newly_reconstructed':len(rows),'reconstructed':list(recovered_by_path.values()),'missing':missing}
    (ROOT/'reports/E3_input_recovery.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print('INPUT_SNAPSHOTS',result['status'],'existing',checked,'recovered',len(rows),'missing',len(missing),flush=True)
    if missing:print(json.dumps(missing,indent=2));raise SystemExit(1)
if __name__=='__main__':main()
