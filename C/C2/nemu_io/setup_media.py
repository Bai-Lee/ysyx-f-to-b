"""Portable Ubuntu FFmpeg dependency extraction, no package installation."""
from pathlib import Path
import sys,re,hashlib,shlex
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *

def main():
    download=Path('/workspace/downloads/ysyx_c_stage/media');download.mkdir(parents=True,exist_ok=True)
    root=Path('/home/USER/tools/c-stage/media');root.mkdir(parents=True,exist_ok=True)
    o,_,_=run('C2/nemu_io/media/dependency_plan',['apt-get','-s','--no-install-recommends','install','ffmpeg'],timeout=90)
    require=re.findall(r'^Inst (\S+) ',o,re.M)
    assert 'ffmpeg' in require and not re.search(r'^Remv ',o,re.M)
    # The displayed plan is only queried. Never execute its install action.
    o,_,_=run('C2/nemu_io/media/official_uris',['apt-get','--print-uris','download',*require],timeout=90)
    packages=[]
    for line in o.splitlines():
        if not line.startswith("'"):continue
        url,filename,size,expected=shlex.split(line)
        assert url.startswith(('http://archive.ubuntu.com/ubuntu/','http://security.ubuntu.com/ubuntu/','https://archive.ubuntu.com/ubuntu/','https://security.ubuntu.com/ubuntu/'))
        algorithm,digest=expected.split(':',1);assert algorithm in ('SHA256','SHA512')
        packages.append({'url':url,'filename':filename,'bytes':int(size),'official_digest_algorithm':algorithm,'official_digest':digest})
    assert len(packages)==len(require),(len(packages),len(require))
    missing=[name for name,row in zip(require,packages) if not (download/row['filename']).exists()]
    if missing:run('C2/nemu_io/media/download',['apt-get','-qq','download',*require],cwd=download,timeout=600)
    for row in packages:
        path=download/row['filename'];h=hashlib.new(row['official_digest_algorithm'].lower())
        with path.open('rb') as f:
            for part in iter(lambda:f.read(1048576),b''):h.update(part)
        assert path.stat().st_size==row['bytes'] and h.hexdigest()==row['official_digest'],path
        row.update(archive=str(path),sha256=sha(path),official_digest_match=True)
        run('C2/nemu_io/media/extract/'+path.name,['dpkg-deb','-x',path,root],inputs=[path],timeout=45,resume=True)
    executable=root/'usr/bin/ffmpeg';env={'LD_LIBRARY_PATH':str(root/'usr/lib/x86_64-linux-gnu')}
    o,e,_=run('C2/nemu_io/media/version',[executable,'-version'],inputs=[executable],env=env)
    assert 'ffmpeg version' in o
    dump(ROOT/'reports/C2_nemu_media.json',{'status':'PASS_EXTRACTION_VERSION_ONLY','executable':str(executable),'sha256':sha(executable),'environment':env,'packages':packages,'scope':'Official Ubuntu packages downloaded to D and extracted into task-local directory. All package digests matched the configured Ubuntu APT metadata. No global install, CUDA or system changes. Actual MP4 conversion/negative input validation follows when runtime budget is available.'})
    print('C2_PORTABLE_FFMPEG_READY',len(packages),sum(p['bytes'] for p in packages),flush=True)

if __name__=='__main__':main()
