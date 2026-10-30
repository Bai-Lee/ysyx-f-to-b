"""Export a strict public-fixture whitelist; never copy SSH private keys."""
from pathlib import Path
import sys,json,shutil,subprocess,hashlib,tarfile,datetime
P=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(P/'E/E3/ms'))
from common import run,sha,dump,LAB,PROJECT,OUT

def main():
    out=PROJECT/'E/E3/offline';out.mkdir(exist_ok=True);files=[];repos=[]
    def copy(src,rel):
        data=src.read_bytes()
        assert b'-----BEGIN OPENSSH PRIVATE KEY-----' not in data and b'-----BEGIN PRIVATE KEY-----' not in data
        dst=out/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data)
        files.append({'original':str(src),'path':str(dst.relative_to(PROJECT)),'bytes':len(data),'sha256':sha(dst)})
    for name in ['iris.data','tmux.conf','endings.txt','selected.words','marco.sh','rare.sh','rare.stderr','rare.stdout','session.history','html-files.zip']:
        copy(LAB/name,'ms/'+name)
    for root in ['dotfiles','vim-lab']:
        for f in sorted((LAB/root).rglob('*')):
            if f.is_file() and '.git' not in f.relative_to(LAB/root).parts:
                copy(f,'ms/'+str(f.relative_to(LAB)))
    for name in ['vimrc','example-data.xml','regexone.html','tmux.html','tmux-config.html']:
        copy(LAB/'resources'/name,'resources/'+name)
    for src,rel in [(Path('/tmp/missing/semester'),'ms/semester'),(Path('/tmp/missing/headers.txt'),'ms/headers.txt'),(Path('/home/USER/last-modified.txt'),'ms/last-modified.txt'),(LAB/'ssh/harden.vim','ms/harden.vim')]:copy(src,rel)
    lock=json.loads((OUT/'resources/lock.json').read_text())
    # Bundles retain course history; shallow plugin snapshots preserve commits and licenses.
    for row in lock['repos']:
        root=Path(row['path']);commit=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip();assert commit==row['commit']
        if row['shallow']:
            dest=out/'resources'/(row['name']+'.tar.gz')
            run('export/archive_'+row['name'],['git','-C',str(root),'archive','--format=tar.gz','-o',str(dest),'HEAD'])
        else:
            dest=out/'resources'/(row['name']+'.bundle')
            run('export/bundle_'+row['name'],['git','-C',str(root),'bundle','create',str(dest),'--all'],timeout=90)
            run('export/verify_'+row['name'],['git','-C',str(root),'bundle','verify',str(dest)],inputs=[dest])
        repos.append({**row,'archive':str(dest.relative_to(PROJECT)),'sha256':sha(dest),'bytes':dest.stat().st_size})
    dot=LAB/'dotfiles';bundle=out/'ms/dotfiles.bundle'
    run('export/dotfiles_bundle',['git','-C',str(dot),'bundle','create',str(bundle),'--all'])
    dump(out/'manifest.json',{'status':'PASS','timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':files,'repos':repos,'dotfiles_bundle':{'path':str(bundle.relative_to(PROJECT)),'sha256':sha(bundle)},'excluded':'SSH private keys, mosh session keys, account secrets, unrelated home files; tools and WSL VHDX are external prerequisites.'})
    print('PUBLIC_EXPORT_COMPLETE',len(files),flush=True)

if __name__=='__main__':main()
