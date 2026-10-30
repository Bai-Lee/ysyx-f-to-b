"""Prepare the isolated implementation project; never modify the source archive."""
from pathlib import Path
import hashlib,json,os,platform,subprocess,sys,time,zipfile,shutil
import requests

ROOT=Path(__file__).resolve().parents[1]
WORKSPACE=ROOT.parents[1]
ARCHIVE=WORKSPACE/'YSYX_F_B_Archive'
def digest(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def save(p,data):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
def main():
    for d in ['config','reports','artifacts','F/circuits','F/programs','F/notes','F/vectors','F/analysis','E','D','C','B','tests','scripts','temp']:(ROOT/d).mkdir(parents=True,exist_ok=True)
    src=ARCHIVE/'inventory/assignment_matrix.json';matrix=json.loads(src.read_text('utf8'))
    if not (ROOT/'config/task_status.json').exists():
        save(ROOT/'config/task_status.json',{'source':str(src),'source_sha256':digest(src),'created':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'tasks':[{**r,'status':('EXCLUDED_SCOPE' if r['implementation_status']=='NOT_APPLICABLE' or '排除' in r['classification'] else 'NOT_RUN'),'evidence':[]} for r in matrix['records']]})
    downloads=WORKSPACE/'downloads/ysyx';downloads.mkdir(parents=True,exist_ok=True)
    metadata=requests.get('https://api.github.com/repos/logisim-evolution/logisim-evolution/releases/tags/v4.0.0',timeout=45);metadata.raise_for_status();release=metadata.json();save(downloads/'logisim-v4.0.0-release.json',release)
    asset=next(a for a in release['assets'] if a['name']=='logisim-evolution-4.0.0-all.jar');path=downloads/asset['name'];expected=asset['digest'].removeprefix('sha256:')
    if not path.exists() or digest(path)!=expected:
        with requests.get(asset['browser_download_url'],stream=True,timeout=(20,120)) as r:
            r.raise_for_status()
            with path.with_suffix('.part').open('wb') as f:
                for chunk in r.iter_content(1024*1024):f.write(chunk)
        if digest(path.with_suffix('.part'))!=expected:raise ValueError('Official SHA256 mismatch')
        path.with_suffix('.part').replace(path)
    dest=WORKSPACE/'tools/logisim-evolution-4.0.0';dest.mkdir(exist_ok=True);jar=dest/path.name
    if not jar.exists() or digest(jar)!=expected:shutil.copyfile(path,jar)
    existing=ROOT/'config/toolchain.json'
    java=json.loads(existing.read_text('utf8'))['java']['executable'] if existing.exists() else r'D:\jdk-26\bin\java.exe'
    p=subprocess.run([java,'-Xmx512m','-jar',str(jar),'--help'],capture_output=True,text=True,encoding='utf8',errors='replace',timeout=45)
    (ROOT/'artifacts/logisim_help.stdout.txt').write_text(p.stdout,encoding='utf8');(ROOT/'artifacts/logisim_help.stderr.txt').write_text(p.stderr,encoding='utf8')
    print(p.stdout,p.stderr,flush=True)
    lock={'logisim':{'version':'4.0.0','jar':str(jar),'sha256':expected,'official_digest_match':True,'release_api':'https://api.github.com/repos/logisim-evolution/logisim-evolution/releases/tags/v4.0.0'},'java':{'executable':java,'sha256':digest(java),'existing_runtime':True},'python':{'executable':sys.executable,'sha256':digest(sys.executable)},'workspace_toolchain':str(WORKSPACE/'config/toolchain.lock.json'),'archive_untouched':True}
    save(ROOT/'config/toolchain.json',lock)
    with zipfile.ZipFile(jar) as z:
        names=z.namelist();save(ROOT/'config/logisim_jar_catalog.json',names)
        docs=[n for n in names if n.startswith('doc/en/') or n.endswith('.circ')]
        for n in docs:
            destpath=dest/n
            if not destpath.resolve().is_relative_to(dest.resolve()):raise ValueError(n)
            if not n.endswith('/'):destpath.parent.mkdir(parents=True,exist_ok=True);destpath.write_bytes(z.read(n))
        print('EXTRACTED_TOOL_DOCUMENTATION',len(docs),flush=True)
    preflight={'date':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'scope':'F stages: Logisim structural circuits, transistor-switch reasoning, sequential state machines, sISA CPU and IO. No claim of physical chip PPA/metastability.','capability':'Logisim 4.0.0 downloaded and official digest checked; minimal positive/negative circuit control still required before bulk implementation','limits':{'jvm_heap_mib':512,'heavy_jobs':1,'compile_jobs_max':4,'free_memory_floor_gib':3},'source_archive':str(ARCHIVE),'source_task_hash':digest(src),'verification':'Combinational exhaustive vectors; sequential state/clock/reset traces; independent ISA reference and instruction commit comparison; injected faults; GUI open/save/reopen and IO observations','ambiguities':['F3 transistor/latch source images must be inspected before interpreting topology','Original sISA R0 writable, enhanced branch uses PC+signext(offset), arithmetic wraps 8 bits','Digital oscillation is not an analog metastability measurement'],'status':'TOOL_CONTROL_PENDING'}
    save(ROOT/'reports/preflight_F.json',preflight)
    git=r'D:\Git\Git\cmd\git.exe'
    if not (ROOT/'.git').exists():
        for args in [['init','-b','main'],['config','user.name','Codex YSYX Engineering'],['config','user.email','codex-local@example.invalid']]:
            q=subprocess.run([git,*args],cwd=ROOT,capture_output=True,text=True,timeout=30)
            if q.returncode:raise RuntimeError(q.stderr)
    (ROOT/'.gitignore').write_text('temp/\n**/__pycache__/\n*.vvp\nE/obj_dir/\n',encoding='utf8')
    return 0
if __name__=='__main__':sys.exit(main())
