"""Stream a project checkpoint ZIP, then verify every archived entry's SHA-256."""
from evidence import *
import argparse,zipfile

def main():
    p=argparse.ArgumentParser();p.add_argument('--label',required=True);args=p.parse_args();label=args.label
    if not __import__('re').fullmatch(r'[A-Z][0-9]?',label):raise ValueError('Invalid checkpoint label')
    audit=json.loads((ROOT/'reports'/(label+'_AUDIT.json')).read_text('utf8'))
    if audit['status']!='PASS':raise ValueError('An audited checkpoint is required')
    if label=='E' and audit.get('stage_complete') is not True:raise ValueError('The whole-E engineering audit must be complete before delivery')
    manifest=ROOT/'reports'/(label+'_delivery_manifest.json');archive_report=ROOT/'reports'/(label+'_delivery_archive.json')
    suffix='CHECKPOINT' if audit.get('stage_complete') is False else 'DELIVERY'
    target=ROOT/('YSYX_'+label+'_'+suffix+'.zip')
    entries=[]
    for file in sorted(ROOT.rglob('*')):
        if not file.is_file():continue
        rel=file.relative_to(ROOT)
        if any(part in {'.git','temp','__pycache__'} for part in rel.parts) or rel.parts[:2]==('config','history'):continue
        fixture_zip=rel.parts[:3]==('E','E3','offline')
        if (file.suffix.lower()=='.zip' and not fixture_zip) or file.suffix.lower() in {'.vvp','.autosave'} or file.name.endswith('.zip.sha256') or file in (manifest,archive_report):continue
        # Input snapshots are evidence despite being ZIP files themselves.
        entries.append({'path':rel.as_posix(),'bytes':file.stat().st_size,'sha256':sha(file)})
    # Include per-command input snapshot ZIPs, but never recursively include deliveries.
    for file in sorted(p for p in (ROOT/'artifacts').rglob('*_snapshot.zip') if p.name in {'input_snapshot.zip','output_snapshot.zip'}):
        entries.append({'path':file.relative_to(ROOT).as_posix(),'bytes':file.stat().st_size,'sha256':sha(file)})
    assert len(entries)==len({x['path'] for x in entries})
    dump(manifest,{'label':label,'timestamp':datetime.now(timezone.utc).isoformat(),'scope':'Project source, real local evidence, selected offline sources/runtime and physical signoff package. Complete original course repositories and installed tool/PDK assets remain at their locked D:/WSL locations.','entries':entries})
    print('MANIFEST_READY',len(entries),'files',sum(x['bytes'] for x in entries),'bytes',flush=True)
    if target.exists():
        backup=ROOT/'artifacts/deliveries/history'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f');backup.mkdir(parents=True)
        __import__('shutil').copyfile(target,backup/target.name)
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for row in entries:z.write(ROOT/row['path'],row['path'])
        z.write(manifest,manifest.relative_to(ROOT).as_posix())
    print('ARCHIVE_WRITTEN_VERIFYING_ALL_MEMBERS',flush=True)
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        for row in entries:
            h=hashlib.sha256()
            with z.open(row['path']) as f:
                for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
            assert h.hexdigest()==row['sha256'] and sha(ROOT/row['path'])==row['sha256'],row['path']
        assert hashlib.sha256(z.read(manifest.relative_to(ROOT).as_posix())).hexdigest()==sha(manifest)
    digest=sha(target);(target.with_suffix('.zip.sha256')).write_text(digest+'  '+target.name+'\n',encoding='ascii')
    result={'status':'PASS','label':label,'archive':str(target),'bytes':target.stat().st_size,'sha256':digest,'verified_entries':len(entries)+1,'all_member_sha256_verified':True,'manifest_sha256':sha(manifest),'crc_verified':True,'timestamp':datetime.now(timezone.utc).isoformat()};dump(archive_report,result)
    print(json.dumps(result,ensure_ascii=False),flush=True)

if __name__=='__main__':main()
