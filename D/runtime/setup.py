from common import *
import tarfile

def linux_path(s):
    s=s.replace('\\','/')
    return Path('/mnt/'+s[0].lower()+s[2:]) if len(s)>2 and s[1]==':' else Path(s)

def extract(archive,target,strip=False):
    target=Path(target)
    target.mkdir(parents=True,exist_ok=True)
    with tarfile.open(archive) as t:
        for m in t.getmembers():
            name=Path(m.name)
            if strip:
                if len(name.parts)==1:continue
                name=Path(*name.parts[1:])
            assert not name.is_absolute() and '..' not in name.parts
            m.name=str(name)
            final=target/name
            assert final.resolve().is_relative_to(target.resolve()),str(final)
            if m.issym() or m.islnk():
                assert not Path(m.linkname).is_absolute()
                linkbase=final.parent if m.issym() else target
                assert (linkbase/m.linkname).resolve().is_relative_to(target.resolve()),m.name
            if final.exists() or final.is_symlink():
                if m.isdir():assert final.is_dir()
                elif m.issym():assert final.is_symlink() and os.readlink(final)==m.linkname
                elif m.isfile():assert final.read_bytes()==t.extractfile(m).read(),str(final)
                else:raise RuntimeError('unsupported existing member '+m.name)
                continue
            t.extract(m,target)

def main():
    BENCH.mkdir(exist_ok=True);rows=[]
    inherited=json.loads((ROOT/'reports/E_source_lock_canonical.json').read_text())['repositories']
    names={'NJU-ProjectN__abstract-machine__ics2026':'abstract-machine','NJU-ProjectN__am-kernels__ics2026':'am-kernels','NJU-ProjectN__riscv-tests-am__master':'riscv-tests','OSCPU__archbench__main':'archbench','NJU-ProjectN__fceux-am__ics2021':'fceux-am'}
    own=json.loads((ROOT/'reports/D_source_lock.json').read_text())['repositories']
    names['NJU-ProjectN__nemu__ics2024']='nemu'
    for row in inherited+own:
        if row['name'] not in names:continue
        archive=linux_path(row['archive']);assert sha(archive)==row['sha256']
        target=BENCH/names[row['name']];extract(archive,target)
        rows.append({'name':row['name'],'commit':row['commit'],'archive_sha256':row['sha256'],'runtime':str(target)})
    # Keep the original workbench git-recording macro, but use a new local repository.
    with tarfile.open(linux_path(next(x for x in inherited if x['name']=='OSCPU__ysyx-workbench')['archive'])) as t:
        for name in ['Makefile','README.md','AGENTS.md']:
            (BENCH/name).write_bytes(t.extractfile(name).read())
    run('D/setup/git_init',['git','init'],cwd=BENCH)
    run('D/setup/git_name',['git','config','user.name','Local D-stage engineering'],cwd=BENCH)
    run('D/setup/git_email',['git','config','user.email','local-d-stage@invalid.example'],cwd=BENCH)
    (BENCH/'.gitignore').write_text('**/build/\n**/obj_dir/\n**/*.o\n**/*.so*\n**/tools/capstone/repo/\n**/tools/spike-diff/repo/\n')
    run('D/setup/git_add',['git','add','.'],cwd=BENCH,timeout=120)
    run('D/setup/git_commit',['git','commit','-m','Freeze official inputs for independent D-stage work'],cwd=BENCH,timeout=120)
    deps=json.loads((ROOT/'reports/D_additional_sources.json').read_text())['repositories']
    for row in deps:
        archive=linux_path(row['archive']);assert sha(archive)==row['sha256']
        target=BENCH/'nemu/tools'/('capstone' if row['name']=='capstone' else 'spike-diff')/'repo';extract(archive,target,True)
        row['runtime']=str(target)
    dump(ROOT/'reports/D_runtime_setup.json',{'status':'PASS_SOURCE_SETUP_NOT_FUNCTIONAL_VERDICT','repositories':rows,'dependencies':deps,'root':str(BENCH),'E_runtime_changed':False})
    print('D_RUNTIME_SOURCE_SETUP_PASS',flush=True)

if __name__=='__main__':main()
