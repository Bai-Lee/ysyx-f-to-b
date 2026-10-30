"""Create the cumulative C delivery and verify CRC/SHA-256 in one read pass."""
from evidence import *
import zipfile
from verify_C_delivery import verify_zip


def files():
    excluded = {'C_delivery_manifest.json', 'C_delivery_archive.json', 'C_delivery_verification.json'}
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in {'.git', 'temp', '__pycache__', '.pytest_cache'} for part in rel.parts):
            continue
        if rel.parts[:2] == ('config', 'history'):
            continue
        if path.suffix.lower() in {'.vvp', '.autosave'} or path.name.endswith('.zip.sha256'):
            continue
        if rel.parts[0] == 'reports' and path.name in excluded:
            continue
        if path.suffix.lower() == '.zip':
            allowed = rel.parts[0] == 'artifacts' and path.name.endswith('_snapshot.zip')
            allowed |= rel.parts[:3] in {('E', 'E3', 'offline'), ('C', 'offline', 'sources')}
            if not allowed:
                continue
        yield path, rel.as_posix()


def main():
    audit = json.loads((ROOT/'reports/C_AUDIT.json').read_text('utf8'))
    assert audit['status'] == 'PASS' and audit['stage_complete'] and audit['stop_after'] == 'C'
    target = ROOT/'YSYX_C_DELIVERY.zip'
    assert not target.exists(), 'Do not overwrite an existing delivery; preserve and inspect it first.'
    manifest = ROOT/'reports/C_delivery_manifest.json'
    entries = []
    packed = {'.zip', '.gz', '.xz', '.bz2', '.7z', '.png', '.jpg', '.jpeg', '.mp4', '.pdf'}
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=3, allowZip64=True) as archive:
        for path, name in files():
            info = zipfile.ZipInfo.from_file(path, name)
            info.compress_type = zipfile.ZIP_STORED if path.suffix.lower() in packed else zipfile.ZIP_DEFLATED
            info._compresslevel = 3
            h = hashlib.sha256(); count = 0
            with path.open('rb') as source, archive.open(info, 'w', force_zip64=True) as output:
                for block in iter(lambda: source.read(1048576), b''):
                    output.write(block); h.update(block); count += len(block)
            assert count == info.file_size, 'File size changed during packaging: '+name
            entries.append({'path': name, 'bytes': count, 'sha256': h.hexdigest()})
            if len(entries) % 5000 == 0:
                print('C_PACKAGED', len(entries), 'files', flush=True)
        assert len(entries) == len({r['path'] for r in entries})
        dump(manifest, {'label': 'C', 'timestamp': datetime.now(timezone.utc).isoformat(),
            'scope': 'Cumulative F/E/D/C source and retained evidence, including current and historical input/output snapshots, frozen runtimes and selected pristine sources. Prior delivery ZIP files, Git objects, temporary/build caches and configuration backups are excluded. Installed toolchains, Maven/JDK/system libraries and the complete original course archive remain separate locked dependencies.',
            'entries': entries})
        archive.write(manifest, manifest.relative_to(ROOT).as_posix())
    print('C_ARCHIVE_WRITTEN_VERIFYING', len(entries)+1, 'members', flush=True)
    digest = sha(target)
    target.with_suffix('.zip.sha256').write_text(digest+'  '+target.name+'\n', encoding='ascii')
    result = verify_zip(target, entries, sha(manifest), current_files=True)
    result.update(label='C', archive=str(target), bytes=target.stat().st_size, sha256=digest,
        manifest_sha256=sha(manifest), timestamp=datetime.now(timezone.utc).isoformat())
    dump(ROOT/'reports/C_delivery_archive.json', result)
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
