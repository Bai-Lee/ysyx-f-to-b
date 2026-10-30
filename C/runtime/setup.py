"""Create a C-only workbench from the verified D source/runtime snapshot."""
from common import *
import tarfile

def extract(archive,target,strip=False):
    target=Path(target);target.mkdir(parents=True,exist_ok=True)
    with tarfile.open(archive) as t:
        for m in t:
            name=Path(m.name)
            if strip:
                if len(name.parts)==1:continue
                name=Path(*name.parts[1:])
            assert not name.is_absolute() and '..' not in name.parts
            m.name=str(name);dest=target/name;assert dest.resolve().is_relative_to(target.resolve())
            if m.issym() or m.islnk():
                assert not Path(m.linkname).is_absolute()
                assert ((dest.parent if m.issym() else target)/m.linkname).resolve().is_relative_to(target.resolve())
            if dest.exists() or dest.is_symlink():
                if m.isdir():assert dest.is_dir()
                elif m.issym():assert dest.is_symlink() and os.readlink(dest)==m.linkname
                elif m.isfile():assert dest.read_bytes()==t.extractfile(m).read(),dest
                else:raise AssertionError(m.name)
                continue
            t.extract(m,target)

def main():
    assert not (ROOT/'reports/C_runtime_setup.json').exists(),'Already initialized; use current C workbench.'
    lock=json.loads((ROOT/'reports/D_runtime_export.json').read_text());archive=ROOT/lock['archive'];assert sha(archive)==lock['sha256']
    extract(archive,WORK)
    adjusted=[]
    for p in sorted(BENCH.rglob('*')):
        if not p.is_file() or p.is_symlink():continue
        if p.suffix not in ('.c','.h','.cpp','.cc','.sv','.v','.mk','.sh','.py','.json') and p.name not in ('Makefile','.config','.config.old'):continue
        old=p.read_bytes();new=old.replace(b'/home/USER/d-stage',b'/home/USER/c-stage').replace(b'LOCAL_D_STAGE',b'LOCAL_C_STAGE')
        if new!=old:p.write_bytes(new);adjusted.append({'path':str(p),'before':hashlib.sha256(old).hexdigest(),'after':sha(p)})
    deps=json.loads((ROOT/'reports/D_offline_sources.json').read_text())['repositories']
    for name,sub in [('capstone','capstone'),('spike','spike-diff')]:
        row=next(r for r in deps if r.get('name')==name);archive=ROOT/row['delivery_path'];assert sha(archive)==row['sha256'];extract(archive,BENCH/'nemu/tools'/sub/'repo',True)
    cap=BENCH/'nemu/tools/capstone/repo';shutil.copyfile(WORK/'bin/libcapstone.so.5',cap/'libcapstone.so.5')
    (cap/'libcapstone.so').symlink_to('libcapstone.so.5')
    ref=WORK/'nemu-ref/build';ref.mkdir(exist_ok=True);shutil.copyfile(WORK/'bin/nemu-d8-ref.so',ref/'riscv32-nemu-interpreter-so')
    spike=BENCH/'nemu/tools/spike-diff/build';spike.mkdir(exist_ok=True);shutil.copyfile(WORK/'bin/spike-riscv32.so',spike/'riscv32-spike-so')
    for p in [ref/'riscv32-nemu-interpreter-so',WORK/'bin/npc-d8-linux',WORK/'bin/nemu-d7-linux']:p.chmod(0o755)
    # Keep independent coursework build tracing without modifying the D Git repo.
    run('C/setup/git_init',['git','init'],cwd=BENCH)
    run('C/setup/git_name',['git','config','user.name','Local C-stage engineering'],cwd=BENCH)
    run('C/setup/git_email',['git','config','user.email','local-c-stage@invalid.example'],cwd=BENCH)
    (BENCH/'.gitignore').write_text('**/build/\n**/obj_dir/\n**/*.o\n**/*.so*\n**/tools/capstone/repo/\n**/tools/spike-diff/repo/\n')
    run('C/setup/git_add',['git','add','.'],cwd=BENCH,timeout=120)
    run('C/setup/git_commit',['git','-c','gc.auto=0','commit','-m','Freeze independent C foundation from D final source'],cwd=BENCH,timeout=120)
    dump(ROOT/'reports/C_runtime_setup.json',{'status':'PASS_SOURCE_SETUP_NOT_NEW_FUNCTIONAL_VERDICT','D_source_archive_sha256':lock['sha256'],'C_workbench':str(BENCH),'adjusted_paths':adjusted,'reused_libraries':[{'path':str(p),'sha256':sha(p)} for p in [cap/'libcapstone.so.5',ref/'riscv32-nemu-interpreter-so',spike/'riscv32-spike-so']],'scope':'Independent source copies; D directories and frozen archives were not edited. Final D prebuilt libraries are bootstrap inputs, later C changes require new builds and acceptance.'})
    print('C_WORKBENCH_READY',flush=True)

if __name__=='__main__':main()
