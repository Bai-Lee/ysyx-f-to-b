from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *
d=ROOT/'C/C2/nemu_io';rows=[]
for source in sorted((d/'am').glob('*.c')):
    rel=Path('abstract-machine/am/src/platform/nemu/ioe')/source.name
    target=BENCH/rel;before=sha(target)
    if before!=sha(source):
        backup=ROOT/'artifacts/C2/nemu_io/driver_revisions'/str(time.time_ns())/source.name
        backup.parent.mkdir(parents=True);shutil.copyfile(target,backup)
        shutil.copyfile(source,target)
    installed=d/'installed'/rel;installed.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,installed)
    rows.append({'source':str(source),'installed':str(target),'sha256':sha(target),'before_sha256':before})
dump(ROOT/'reports/C2_nemu_driver_binding.json',{'status':'PASS','drivers':rows})
