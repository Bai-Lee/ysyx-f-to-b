"""Freeze B source workbenches and accepted runtime inputs without altering them."""
from common import *
import argparse,tarfile,posixpath

def inventory():
    pairs={}
    def add(path,role,destination=None):
        path=Path(path);name=destination or path.relative_to(WORK).as_posix()
        assert not name.startswith('/') and '..' not in Path(name).parts
        if name in pairs:assert pairs[name][0]==path;return
        pairs[name]=(path,role)
    roots=['workbench','nemu-ref','fast-nemu-ref','rt-thread-am','soc/workbench','soc-generation/ysyxSoC','b1/apps']
    for name in roots:
        base=WORK/name;assert base.is_dir(),base
        for path in sorted(base.rglob('*')):
            parts=path.relative_to(base).parts
            if any(p in {'.git','build','out','obj_dir','__pycache__','.pytest_cache'} for p in parts):continue
            if 'repo' in parts and any(p in {'capstone','spike-diff'} for p in parts):continue
            if path.is_symlink() and os.readlink(path).startswith('/'):
                assert path==WORK/'soc-generation/ysyxSoC/patch/firtool' and path.resolve()==Path('/home/USER/tools/c-stage/firtool')
                for tool in sorted(path.resolve().rglob('*')):
                    if tool.is_file():add(tool,'materialized_locked_firtool',path.relative_to(WORK).as_posix()+'/'+tool.relative_to(path.resolve()).as_posix())
                continue
            if path.is_file() or path.is_symlink():add(path,'source_or_data')
    for name in ['B_soc_soc_build','B_standalone_builds','B1_nemu_build']:
        document=json.loads((ROOT/'reports'/f'{name}.json').read_text())
        for row in document['variants']:
            path=Path(row['executable']);assert sha(path)==row['sha256'],path;add(path,'recorded_binary')
    spike=json.loads((ROOT/'reports/B1_spike_environment.json').read_text());path=Path(spike['executable']);assert sha(path)==spike['sha256'];add(path,'recorded_reference_binary')
    add(WORK/'fast-nemu-ref/build/riscv32-nemu-interpreter-so','recorded_reference_binary')
    for name in ['b3/tools/cachesim','b4/tools/branchsim','b5/rtl/cpu.vvp','b5/rtl-bad-reset/cpu.vvp','b5/netlist/cpu.vvp']:
        path=WORK/name;assert path.is_file();add(path,'checker_or_four_state_program')
    for name in ['workbench','soc/workbench','rt-thread-am','b1/apps','b3/images','b5']:
        base=WORK/name
        for path in sorted(base.rglob('*')):
            if not path.is_file() or '.git' in path.parts:continue
            if path.suffix in {'.bin','.elf'} or path.suffix=='.hex' and name=='b5':add(path,'firmware')
    return [(path,name,role) for name,(path,role) in sorted(pairs.items())]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--inventory',action='store_true');args=parser.parse_args();pairs=inventory()
    if args.inventory:
        print(json.dumps({'members':len(pairs),'regular_bytes':sum(p.stat().st_size for p,_,_ in pairs if not p.is_symlink()),'symlinks':sum(p.is_symlink() for p,_,_ in pairs)},indent=2));return
    for name in ['B_final_regressions','B5_ACCEPTANCE','B4_full128','B_performance_analysis']:
        assert json.loads((ROOT/'reports'/f'{name}.json').read_text())['status'].startswith('PASS'),name
    out=ROOT/'B/offline';out.mkdir(exist_ok=True);archive=out/'b-final-runtime.tar.gz';assert not archive.exists(),'Do not overwrite a frozen runtime'
    members=[]
    with tarfile.open(archive,'w:gz',compresslevel=3,dereference=False) as tar:
        for path,destination,role in pairs:
            row={'path':destination,'source':str(path),'role':role}
            if path.is_symlink():
                target=os.readlink(path);resolved=posixpath.normpath(posixpath.join(posixpath.dirname(destination),target))
                assert not target.startswith('/') and not resolved.startswith('../'),(path,target)
                tar.add(path,arcname=destination,recursive=False);row.update(kind='symlink',target=target)
            else:
                row.update(kind='file',bytes=path.stat().st_size,sha256=sha(path));info=tar.gettarinfo(str(path),arcname=destination)
                with path.open('rb') as source:tar.addfile(info,source)
            members.append(row)
            if len(members)%5000==0:print('B_RUNTIME_MEMBERS_WRITTEN',len(members),flush=True)
    expected={r['path']:r for r in members};seen=set()
    with tarfile.open(archive,'r|gz') as tar:
        for item in tar:
            assert item.name in expected and item.name not in seen;seen.add(item.name);row=expected[item.name]
            if row['kind']=='symlink':assert item.issym() and item.linkname==row['target']
            else:
                assert item.isfile() and item.size==row['bytes'];h=hashlib.sha256()
                with tar.extractfile(item) as stream:
                    for block in iter(lambda:stream.read(1048576),b''):h.update(block)
                assert h.hexdigest()==row['sha256'],item.name
    assert seen==set(expected)
    dump(ROOT/'reports/B_runtime_export.json',{'status':'PASS','archive':archive.relative_to(ROOT).as_posix(),'sha256':sha(archive),'bytes':archive.stat().st_size,'members':members,
        'scope':'B source workbenches, generator sources, accepted simulator profiles, final references, Icarus programs and firmware. Build objects and caches omitted; prior stage sources/archives unchanged. Installed system loader/libraries, compiler toolchains and cached Maven/JDK dependencies remain separately locked external dependencies.'})
    print('B_RUNTIME_FREEZE_PASS',len(members),archive.stat().st_size,flush=True)

if __name__=='__main__':main()
