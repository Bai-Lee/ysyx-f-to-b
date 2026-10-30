from common import *
import tarfile
def path(s):return Path(s.replace('D:\\','/mnt/d/').replace('D:/','/mnt/d/').replace('\\','/'))
def extract(archive,dest):
    dest.mkdir(parents=True,exist_ok=True)
    with tarfile.open(archive) as t:
        for m in t.getmembers():
            assert (dest/m.name).resolve().is_relative_to(dest.resolve()),m.name
            if m.issym():assert (dest/m.name).parent.joinpath(m.linkname).resolve().is_relative_to(dest.resolve()),m.linkname
        t.extractall(dest)
def main():
    lock=ROOT/'reports/E_source_lock_canonical.json'
    if not lock.exists():lock=ROOT/'reports/E_source_lock.json'
    locked=json.loads(lock.read_text())
    mappings={'OSCPU__ysyx-workbench':BENCH,'NJU-ProjectN__abstract-machine__ics2026':BENCH/'abstract-machine','NJU-ProjectN__am-kernels__ics2026':BENCH/'am-kernels','NJU-ProjectN__riscv-tests-am__master':BENCH/'riscv-tests','NJU-ProjectN__fceux-am__ics2021':BENCH/'fceux-am','OSCPU__archbench__main':BENCH/'archbench','OSCPU__ysyxSoC__2607':BENCH/'ysyxSoC','openecos-projects__icsprout55-pdk__unconfirmed':Path('/home/USER/tools/icsprout55-e-stage')}
    for row in locked['repositories']:
        a=path(row['archive']);assert sha(a)==row['sha256'];dest=mappings[row['name']];marker=dest/'.ysyx-source.json'
        if marker.exists():assert json.loads(marker.read_text())['commit']==row['commit'];continue
        assert not dest.exists() or not any(dest.iterdir()),dest
        extract(a,dest);dump(marker,row)
    # Create a local root history; no hosted-account publication or student identity.
    if not (BENCH/'.git').exists():
        for tag,args in [('init',['init','-b','main']),('name',['config','user.name','YSYX Autonomous E Engineering']),('email',['config','user.email','e-stage@example.invalid'])]:run('E/framework/'+tag,['git',*args],cwd=BENCH)
        p=BENCH/'.gitignore';text=p.read_text()+'\n/abstract-machine\n/am-kernels\n/riscv-tests\n/fceux-am\n/archbench\n/ysyxSoC\n/.ysyx-source.json\n';p.write_text(text)
        run('E/framework/add',['git','add','.'],cwd=BENCH);run('E/framework/commit',['git','commit','-m','Initialize local E-stage workspace from pinned official snapshot'],cwd=BENCH)
    print('E_WORKSPACE_SOURCE_READY',flush=True)
if __name__=='__main__':main()
