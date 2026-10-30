"""Freeze the final D workbench without altering any F/E snapshot."""
from common import *
import tarfile,posixpath

def local(p):
    s=str(p).replace('\\','/')
    return Path('/mnt/'+s[0].lower()+s[2:]) if len(s)>2 and s[1]==':' else Path(s)

def main():
    out=ROOT/'D/offline';out.mkdir(parents=True,exist_ok=True)
    archive=out/'d-final-runtime.tar.gz'
    if archive.exists():raise RuntimeError('Frozen archive already exists; do not overwrite')
    pairs=[]
    for base,prefix in [(BENCH,'workbench'),(WORK/'nemu-ref','nemu-ref')]:
        for p in sorted(base.rglob('*')):
            rel=p.relative_to(base);parts=rel.parts
            if any(x in ('.git','build','__pycache__','obj_dir') for x in parts):continue
            if parts[:3] in [('nemu','tools','capstone'),('nemu','tools','spike-diff')]:
                if 'repo' in parts:continue
            if p.is_symlink() or p.is_file():pairs.append((p,prefix+'/'+rel.as_posix(),'source'))
    license=BENCH/'nemu/LICENSE'
    if not (WORK/'nemu-ref/LICENSE').exists():pairs.append((license,'nemu-ref/LICENSE','upstream_license'))
    b8=json.loads((ROOT/'reports/D8_build.json').read_text());b7=json.loads((ROOT/'reports/D7_build.json').read_text())
    for name,path in [('npc-d8-linux',b8['executable']),('nemu-d7-linux',b7['nemu']),('nemu-d8-ref.so',b8['reference']),('spike-riscv32.so',b7['spike']),('libcapstone.so.5',b8['capstone'])]:
        pairs.append((Path(path),'bin/'+name,'binary'))
    pairs += [(Path(b8['executable']).parent.parent/'Makefile','build-config/NPC.Makefile','build_config')]
    rows=[]
    with tarfile.open(archive,'w:gz',compresslevel=6,dereference=False) as tar:
        for p,dest,role in pairs:
            row={'path':dest,'source':str(p),'role':role}
            if p.is_symlink() and role=='source':
                target=os.readlink(p);resolved=posixpath.normpath(posixpath.join(posixpath.dirname(dest),target))
                assert not target.startswith('/') and not resolved.startswith('../'),(dest,target)
                row.update(kind='symlink',target=target)
                tar.add(p,arcname=dest,recursive=False)
            else:
                resolved=p.resolve();row.update(kind='file',bytes=resolved.stat().st_size,sha256=sha(resolved))
                info=tar.gettarinfo(str(resolved),arcname=dest)
                with resolved.open('rb') as f:tar.addfile(info,f)
            rows.append(row)
    # Validate every byte and link immediately after closing the stream.
    seen=set();expected={r['path']:r for r in rows};assert len(expected)==len(rows)
    with tarfile.open(archive,'r|gz') as tar:
        for m in tar:
            assert m.name in expected and m.name not in seen;seen.add(m.name);r=expected[m.name]
            if r['kind']=='symlink':assert m.issym() and m.linkname==r['target']
            else:
                assert m.isfile() and m.size==r['bytes'];h=hashlib.sha256()
                with tar.extractfile(m) as f:
                    for data in iter(lambda:f.read(1048576),b''):h.update(data)
                assert h.hexdigest()==r['sha256'],m.name
    assert seen==set(expected)
    dump(ROOT/'reports/D_runtime_export.json',{'status':'PASS','archive':str(archive.relative_to(ROOT)),'sha256':sha(archive),'bytes':archive.stat().st_size,'members':rows,'scope':'Final patched sources, data and five actual binaries. Build folders/Git history omitted; Capstone/Spike source repos supplied separately. Link targets preserved. NEMU REF license copied from its exact upstream source.'})
    sources=[];dest=out/'sources';dest.mkdir(exist_ok=True)
    for report in ['D_source_lock','D_additional_sources']:
        for row in json.loads((ROOT/'reports'/f'{report}.json').read_text())['repositories']:
            source=local(row['archive']);assert sha(source)==row['sha256'];target=dest/source.name
            assert not target.exists();shutil.copyfile(source,target);assert sha(target)==row['sha256']
            sources.append({**row,'delivery_path':str(target.relative_to(ROOT))})
    dump(ROOT/'reports/D_offline_sources.json',{'status':'PASS','repositories':sources,'inherited_pristine_sources':'reports/E_offline_sources.json','scope':'NEMU, Capstone and Spike exact source archives; AM/kernels/archbench/FCEUX/riscv-tests pristine archives are retained under E/offline/sources and included in this cumulative delivery.'})
    finish(archive,rows,b8,b7)

def finish(archive,rows,b8,b7):
    current=[]
    mappings=[(ROOT/'D/D8'/n,BENCH/'npc/vsrc'/n) for n in ['rv32e_core.sv','npc_sim.sv']]
    mappings += [(ROOT/'D/D8'/n,BENCH/'npc/csrc'/n) for n in ['runner.cpp','memory.hpp']]
    mappings += [(ROOT/'D/runtime'/n,BENCH/'npc/csrc'/n) for n in ['debug_core.c','debug_core.h','trace_core.c','trace_core.h']]
    mappings += [(p,BENCH/'abstract-machine/klib/src'/p.name) for p in (ROOT/'D/klib_overlay').glob('*.c')]
    for a,b in mappings:
        recipe='byte-identical'
        if a.name=='stdio.c':
            original=ARCHIVE/'repos/NJU-ProjectN__abstract-machine__ics2026/klib/src/stdio.c'
            upstream=original.read_text();expected=a.read_text().rsplit('#endif',1)[0]+upstream[upstream.index('int __am_vsscanf_internal'):]
            assert expected.encode()==b.read_bytes(),(a,b)
            recipe='Authored formatted-output prefix plus original __am_vsscanf_internal tail, exactly as D5/setup_am.py.'
        else:assert sha(a)==sha(b),(a,b)
        current.append({'path':str(a.relative_to(ROOT)),'runtime_source':str(b),'sha256':sha(a),'runtime_sha256':sha(b),'recipe':recipe})
    binaryrows=[r for r in rows if r['role']=='binary']
    assert next(r['sha256'] for r in binaryrows if r['path']=='bin/npc-d8-linux')==b8['sha256']
    assert sha(b8['executable'])==json.loads((ROOT/'reports/D8_official_tests.json').read_text())['executable_sha256']
    assert sha(b7['nemu'])==json.loads((ROOT/'reports/D7_regression.json').read_text())['nemu_sha256']
    dump(ROOT/'reports/D_final_bindings.json',{'status':'PASS','runtime_archive_sha256':sha(archive),'authored_current_sources':current,'binaries':binaryrows,'qualification':'Final actual source/binary binding. Earlier stage reports keep their historical candidates; no claim that every historical hash is the final hash.'})
    print('D_SOURCE_BINARY_FREEZE_PASS',len(rows),archive.stat().st_size,flush=True)

if __name__=='__main__':
    if '--complete-bindings' in sys.argv:
        prior=json.loads((ROOT/'reports/D_runtime_export.json').read_text());archive=ROOT/prior['archive'];assert sha(archive)==prior['sha256']
        finish(archive,prior['members'],json.loads((ROOT/'reports/D8_build.json').read_text()),json.loads((ROOT/'reports/D7_build.json').read_text()))
    else:main()
