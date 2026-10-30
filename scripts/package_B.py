"""Create one cumulative B delivery and verify every ZIP member CRC and SHA."""
from evidence import *
import zipfile
from verify_B_delivery import verify_zip,zip_controls

def files():
    excluded={'B_delivery_manifest.json','B_delivery_archive.json','B_delivery_verification.json'}
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file():continue
        relative=path.relative_to(ROOT)
        if any(part in {'.git','temp','__pycache__','.pytest_cache'} for part in relative.parts):continue
        if relative.parts[:2]==('config','history'):continue
        if path.suffix.lower() in {'.vvp','.autosave'} or path.name.endswith('.zip.sha256'):continue
        if relative.parts[0]=='reports' and path.name in excluded:continue
        if path.suffix.lower()=='.zip':
            allowed=relative.parts[0]=='artifacts' and path.name.endswith('_snapshot.zip')
            allowed|=relative.parts[:3] in {('E','E3','offline'),('C','offline','sources'),('B','offline','sources')}
            if not allowed:continue
        yield path,relative.as_posix()

def main():
    audit=json.loads((ROOT/'reports/B_AUDIT.json').read_text('utf8'));assert audit['status']=='PASS' and audit['stage_complete'] and audit['stop_after']=='B'
    assert json.loads((ROOT/'reports/B_host_memory_monitor.json').read_text('utf8'))['status']=='PASS_FINAL_SESSION_STOPPED'
    controls=zip_controls();target=ROOT/'YSYX_B_DELIVERY.zip';assert not target.exists(),'Do not overwrite a delivery'
    manifest=ROOT/'reports/B_delivery_manifest.json';entries=[];packed={'.zip','.gz','.xz','.bz2','.7z','.png','.jpg','.jpeg','.mp4','.pdf'}
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=3,allowZip64=True) as archive:
        for path,name in files():
            info=zipfile.ZipInfo.from_file(path,name);info.compress_type=zipfile.ZIP_STORED if path.suffix.lower() in packed else zipfile.ZIP_DEFLATED;info._compresslevel=3
            h=hashlib.sha256();count=0
            with path.open('rb') as source,archive.open(info,'w',force_zip64=True) as output:
                for block in iter(lambda:source.read(1048576),b''):output.write(block);h.update(block);count+=len(block)
            assert count==info.file_size,'File changed during packaging: '+name
            entries.append({'path':name,'bytes':count,'sha256':h.hexdigest()})
            if len(entries)%5000==0:print('B_PACKAGED',len(entries),'files',flush=True)
        assert len(entries)==len({r['path'] for r in entries})
        dump(manifest,{'label':'B','timestamp':datetime.now(timezone.utc).isoformat(),'entries':entries,
            'scope':'Cumulative F/E/D/C/B sources, reports, retained command snapshots and frozen runtimes. Prior delivery ZIPs, Git objects, temporary data and configuration backups excluded. Installed toolchains/OS libraries and the full original course archive remain separate locked dependencies.'})
        archive.write(manifest,manifest.relative_to(ROOT).as_posix())
    value=sha(target);target.with_suffix('.zip.sha256').write_text(value+'  '+target.name+'\n',encoding='ascii')
    print('B_ARCHIVE_WRITTEN_VERIFYING',len(entries)+1,flush=True)
    receipt=verify_zip(target,entries,sha(manifest),current_files=True)
    receipt.update(label='B',archive=str(target),bytes=target.stat().st_size,sha256=value,manifest_sha256=sha(manifest),checker_controls=controls,timestamp=datetime.now(timezone.utc).isoformat())
    dump(ROOT/'reports/B_delivery_archive.json',receipt);print('B_ARCHIVE_VERIFIED',receipt['verified_entries'],receipt['bytes'],value,flush=True)

if __name__=='__main__':main()
