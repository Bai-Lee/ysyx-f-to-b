from pathlib import Path
import sys,json,re,resource,os
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'ms'))
import common
common.LAB=Path('/home/USER/e3-lab/lcthw');common.LAB.mkdir(parents=True,exist_ok=True)
common.OUT=common.PROJECT/'artifacts/E3/LCT';common.OUT.mkdir(parents=True,exist_ok=True)
from common import run,shell,sha,dump,PROJECT
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
SPECS=json.loads((PROJECT/'E/E3/course_specs.json').read_text())
CH={r['chapter']:r for r in SPECS['chapters']}
SRC=PROJECT/'E/E3/lcthw/solutions/continued';SRC.mkdir(parents=True,exist_ok=True)
BIN=common.OUT/'bin';BIN.mkdir(exist_ok=True)
def block(ch,index=0):
    row=next(b for b in CH[ch]['blocks'] if b['index']==index);p=Path('/mnt/d'+row['path'][2:].replace('\\','/'));assert sha(p)==row['sha256'];return p.read_text()
def write(name,text):p=SRC/name;p.write_text(text);return p
def build(name,text=None,files=None,flags=(),strict=False,expected=(0,)):
    if text is not None:files=[write(name+'.c',text)]
    exe=BIN/(name+'.elf')
    out,err,r=run(name+'/compile',['gcc','-std=gnu17','-Wall','-O0','-g',*(['-Werror'] if strict else []),*flags,*map(str,files),'-o',str(exe)],inputs=files,expected=expected,timeout=60)
    return exe,out,err
def execute(name,exe,args=(),expected=(0,),vg=False,stdin=None,timeout=30):
    command=(['valgrind','--error-exitcode=99','--leak-check=full','--show-leak-kinds=all'] if vg else [])+[str(exe),*args]
    return run(name+'/run',command,inputs=[exe],expected=expected,timeout=timeout,stdin=stdin)
def verdict(ids,status,evidence,details):
    p=PROJECT/'reports/E3_LCT_continued.json';d=json.loads(p.read_text()) if p.exists() else {'records':[]};r={v['id']:v for v in d['records']}
    for i in ids:r[i]={'id':i,'status':status,'evidence':evidence,'details':details}
    dump(p,{'status':'IN_PROGRESS','records':sorted(r.values(),key=lambda x:x['id'])})
