"""Canonical export of already pinned recursive framework sources (read-only originals)."""
from pathlib import Path
import sys,json,subprocess
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from evidence import ROOT,sha,dump,run
from bootstrap_downloads import fetch

def main():
    out=ROOT.parents[1]/'downloads/ysyx_c_stage/sources';out.mkdir(parents=True,exist_ok=True)
    git='D:/Git/Git/cmd/git.exe';lock=json.loads((ROOT/'reports/E_source_lock_canonical.json').read_text('utf8'))
    source=next(x for x in lock['repositories'] if x['name']=='OSCPU__ysyxSoC__2607');base=Path(source['source']);rows=[]
    for row in source['submodules_verified_in_original_archive']:
        path=Path(row['path']);head=subprocess.check_output([git,'-C',str(path),'rev-parse','HEAD'],text=True).strip();assert head==row['commit']
        gitdir=subprocess.check_output([git,'-C',str(path),'rev-parse','--absolute-git-dir'],text=True).strip();rel=path.relative_to(base).as_posix()
        dest=out/(rel.replace('/','__')+'-'+head+'.tar.gz')
        if not dest.exists():
            result=run('C5/bootstrap/sources/'+rel.replace('/','__'),[git,'-c','core.autocrlf=false','-C',path,'archive','--format=tar.gz','-o',dest,'HEAD'],timeout=120);assert result['status']=='PASS'
        rows.append({'path':rel,'source':str(path),'gitdir':gitdir,'commit':head,'archive':str(dest),'sha256':sha(dest),'bytes':dest.stat().st_size})
    meta=fetch('https://api.github.com/repos/OSCPU/ysyxSoC/git/commits/bcdcbc3e8d97a11c07d3007e14f33c6147c02a8e',out/'ysyxSoC-bcdcbc-commit.json');remote=json.loads(meta.read_text('utf8'));assert remote['sha']=='bcdcbc3e8d97a11c07d3007e14f33c6147c02a8e'
    archive=out/'ysyxSoC-bcdcbc3e8d97a11c07d3007e14f33c6147c02a8e.tar.gz';assert archive.exists()
    dump(ROOT/'reports/C5_source_lock.json',{'status':'PASS_CANONICAL_EXPORT_NOT_GENERATION','repository':'https://github.com/OSCPU/ysyxSoC','ref':'ysyx6','commit':remote['sha'],'tree':remote['tree']['sha'],'archive':str(archive),'sha256':sha(archive),'upstream_commit_metadata':str(meta),'commit_metadata_sha256':sha(meta),'submodules':rows,'scope':'Top source acquired from official fixed-commit codeload; recursive exact Git commits exported canonically from existing read-only originals. Git metadata will be copied independently for actual dev-init.'})
    print('C5_RECURSIVE_SOURCES_READY',len(rows),flush=True)

if __name__=='__main__':main()
