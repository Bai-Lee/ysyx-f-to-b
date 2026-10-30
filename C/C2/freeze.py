"""Freeze the accepted C2 NEMU/device candidate without touching D history."""
from pathlib import Path
import sys,tarfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    d=ROOT/'C/C2/snapshot';d.mkdir(exist_ok=True);archive=d/'nemu-io-final.tar.gz'
    assert not archive.exists(),'Already frozen'
    n=BENCH/'nemu';pairs=[]
    for p in sorted(n.rglob('*')):
        rel=p.relative_to(n)
        if any(x in ('.git','build','repo','__pycache__') for x in rel.parts):continue
        if p.is_file() and not p.is_symlink():pairs.append((p,'nemu/'+rel.as_posix()))
    build=json.loads((ROOT/'reports/C2_nemu_build.json').read_text())
    for r in build['variants']:
        p=Path(r['executable']);assert sha(p)==r['sha256'];pairs.append((p,'bin/nemu-'+r['mode']))
    pairs += [(n/'tools/capstone/repo/libcapstone.so.5','bin/libcapstone.so.5'),(n/'tools/spike-diff/build/riscv32-spike-so','bin/spike-riscv32.so')]
    for directory in [BENCH/'abstract-machine/am/src/platform/nemu',BENCH/'abstract-machine/klib/src']:
        for p in sorted(directory.rglob('*')):
            if p.is_file():pairs.append((p,'am/'+p.relative_to(BENCH/'abstract-machine').as_posix()))
    rows=[]
    with tarfile.open(archive,'w:gz',dereference=True) as t:
        for p,name in pairs:
            t.add(p,arcname=name,recursive=False);rows.append({'path':name,'source':str(p),'bytes':p.stat().st_size,'sha256':sha(p)})
    with tarfile.open(archive) as t:
        assert len(t.getmembers())==len(rows)
        for r in rows:assert hashlib.sha256(t.extractfile(r['path']).read()).hexdigest()==r['sha256']
    dump(d/'manifest.json',{'status':'PASS','archive':str(archive.relative_to(ROOT)),'sha256':sha(archive),'members':rows,'scope':'C2 NEMU feature/performance source/binaries, actual device drivers and klib. Tests and frame captures stay in C2 artifacts. Not a whole C stage completion.'})
    print('C2_SNAPSHOT_PASS',len(rows),flush=True)

if __name__=='__main__':main()
