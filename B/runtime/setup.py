"""Fork only the accepted C inputs needed by B; never edit the C workbench."""
from pathlib import Path
import shutil, json, hashlib, datetime, subprocess

ROOT = Path('/workspace/projects/ysyx_f_to_b')
OLD = Path('/home/USER/c-stage')
WORK = Path('/home/USER/b-stage')

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    record = ROOT/'reports/B_runtime_setup.json'
    if record.exists():
        print('B workbench already initialized; preserving edits.'); return
    WORK.mkdir(exist_ok=True)
    rows=[]
    def copytree(source, target, excluded=('.git','build','obj_dir','__pycache__')):
        target.mkdir(parents=True,exist_ok=True)
        for origin in sorted(source.rglob('*')):
            relative=origin.relative_to(source)
            if any(part in excluded for part in relative.parts):continue
            p=target/relative
            if origin.is_dir():p.mkdir(parents=True,exist_ok=True)
            elif origin.is_file():
                p.parent.mkdir(parents=True,exist_ok=True)
                if p.exists():assert sha(p)==sha(origin),p
                else:shutil.copyfile(origin,p)
                if str(p).startswith('/home/'):p.chmod(origin.stat().st_mode & 0o777)
                rows.append({'source':str(origin),'target':str(p),'sha256':sha(p)})
    for name in ['common.py','resource_policy.py','budget_exec.py','launch_detached.py']:
        source=ROOT/'C/runtime'/name;target=ROOT/'B/runtime'/name
        text=source.read_text().replace('YSYX_C_WORK','YSYX_B_WORK').replace('/home/USER/c-stage','/home/USER/b-stage').replace('reports/C_results.json','reports/B_results.json').replace("limits['C_jvm_heap_MiB']","limits['B_jvm_heap_MiB']")
        text=text.replace("'compile_jobs': 1", "'compile_jobs': limits['compile_jobs_default']").replace("MAKEFLAGS='-j1'","MAKEFLAGS='-j4'").replace("'-j','1'","'-j','4'").replace('Compile j1;','Compile j4;')
        target.write_text(text)
        rows.append({'source':str(source),'target':str(target),'source_sha256':sha(source),'sha256':sha(target)})
    for sub in ['rtl','sim','am','programs','perip','generation']:
        copytree(ROOT/'C/C5'/sub,ROOT/'B/soc'/sub)
    for name in ['build_soc.py','sdram_wiring.py','chiplink_wiring.py','support.py','project_config.json']:
        source=ROOT/'C/C5'/name;target=ROOT/'B/soc'/name
        text=source.read_text().replace('C/C5','B/soc').replace('C/runtime','B/runtime').replace('reports/C5_','reports/B_soc_').replace("WORK/'c5/","WORK/'soc/").replace("tag='C5/","tag='B/soc/").replace("'-j','1'","'-j','4'")
        if name=='build_soc.py':
            text=text.replace("    subprocess.run(['python3',str(base/'make_cpu_wrapper.py')],check=True)\n",'')
            text=text.replace(",base/'make_cpu_wrapper.py'",'')
        target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
    bench=WORK/'workbench';bench.mkdir(exist_ok=True)
    for name in ['nemu','abstract-machine']:
        copytree(OLD/'workbench'/name,bench/name)
    for sub in ['benchmarks/microbench','tests/am-tests','tests/cpu-tests']:
        copytree(OLD/'workbench/am-kernels'/sub,bench/'am-kernels'/sub)
    copytree(OLD/'c5/nemu-ref',WORK/'nemu-ref')
    copytree(OLD/'c5/workbench/abstract-machine',WORK/'soc/workbench/abstract-machine')
    copytree(OLD/'c5/rt-thread-am',WORK/'rt-thread-am')
    for name in ['hello','csr-positive','cte-positive','cte-bad-restore']:
        copytree(OLD/'c5/workbench'/name,WORK/'soc/workbench'/name)
    copytree(OLD/'c5/workbench/am-kernels/benchmarks/microbench',WORK/'soc/workbench/microbench')
    # Qualified shared libraries are copied byte-for-byte; sources remain above.
    for sub in ['tools/capstone/repo/libcapstone.so.5','tools/spike-diff/build/riscv32-spike-so']:
        p=bench/'nemu'/sub;p.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(OLD/'workbench/nemu'/sub,p)
    cap=bench/'nemu/tools/capstone/repo/libcapstone.so'
    if not cap.exists():cap.symlink_to('libcapstone.so.5')
    adjusted=[]
    for root in [bench,WORK/'nemu-ref',WORK/'soc/workbench',WORK/'rt-thread-am']:
        for p in root.rglob('*'):
            if not p.is_file() or p.is_symlink():continue
            if p.suffix not in ('.c','.h','.S','.cpp','.mk','.sh','.py','.json') and p.name not in ('Makefile','.config','.config.old'):continue
            old=p.read_bytes();new=old.replace(b'/home/USER/c-stage/c5',b'/home/USER/b-stage/soc').replace(b'/home/USER/c-stage',b'/home/USER/b-stage')
            if old!=new:p.write_bytes(new);adjusted.append(str(p))
    (bench/'npc').mkdir(exist_ok=True);(WORK/'soc/workbench/npc').mkdir(exist_ok=True)
    subprocess.run(['git','init'],cwd=bench,check=True,capture_output=True)
    subprocess.run(['git','config','user.name','Local B-stage engineering'],cwd=bench,check=True)
    subprocess.run(['git','config','user.email','local-b-stage@invalid.example'],cwd=bench,check=True)
    (bench/'.gitignore').write_text('**/build/\n**/obj_dir/\n**/*.so*\n**/*.o\n**/tools/*/repo/\n')
    subprocess.run(['git','add','.'],cwd=bench,check=True)
    subprocess.run(['git','-c','gc.auto=0','commit','-m','Preserve accepted C sources as independent B baseline'],cwd=bench,check=True,capture_output=True)
    record.write_text(json.dumps({'status':'PASS_SOURCE_COPY_ONLY','timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':rows,'adjusted_paths':adjusted,'workbench':str(WORK),'scope':'No new functional verdict. C source and accepted binaries remain unchanged.'},indent=2))
    print('B_RUNTIME_SOURCE_COPY_PASS',len(rows))

if __name__=='__main__': main()
