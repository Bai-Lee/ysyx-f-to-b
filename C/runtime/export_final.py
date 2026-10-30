"""Inventory/freeze the C runtime; all previous stage archives stay untouched."""
from pathlib import Path
import sys,argparse,tarfile,posixpath
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *


def local(value):
    text=str(value).replace('\\','/')
    if len(text)>2 and text[1]==':':return Path('/mnt/'+text[0].lower()+text[2:])
    return Path(text)


def inventory():
    roots=['workbench','nemu-ref','c2-native','c2-npc-apps','c2-nemu-apps','c4/workbench','c4/fixtures',
           'c5/workbench','c5/nemu-ref','c5/rt-thread-am','c5/rt-thread-interactive','c5/nvboard',
           'soc-generation/ysyxSoC','c5/chiplink/ysyxSoC']
    pairs=[]
    for relative in roots:
        base=WORK/relative;assert base.is_dir(),base
        for path in sorted(base.rglob('*')):
            parts=path.relative_to(base).parts
            if any(part in {'.git','build','out','obj_dir','__pycache__','.pytest_cache'} for part in parts):continue
            if 'repo' in parts and any(part in {'capstone','spike-diff'} for part in parts):continue
            if path.is_symlink() and os.readlink(path).startswith('/'):
                assert path==WORK/'soc-generation/ysyxSoC/patch/firtool' and path.resolve()==Path('/home/USER/tools/c-stage/firtool')
                for tool in sorted(path.resolve().rglob('*')):
                    if tool.is_file():pairs.append((tool,relative+'/'+path.relative_to(base).as_posix()+'/'+tool.relative_to(path.resolve()).as_posix(),'materialized_locked_firtool_dependency'))
                continue
            if path.is_file() or path.is_symlink():pairs.append((path,relative+'/'+path.relative_to(base).as_posix(),'runtime_source_or_data'))
    # Bind the generated RT application translation unit as well as its source template.
    extra=[WORK/'c5/nvboard_bind.cpp',WORK/'c5/rt-thread-interactive/bsp/abstract-machine/build/c5-am-apps.c']
    for path in extra:assert path.is_file();pairs.append((path,'generated/'+path.name,'generated_source'))
    for path in sorted((WORK/'bin').glob('*')):
        if path.is_file():pairs.append((path,'bin/base/'+path.name,'binary'))
    for row in json.loads((ROOT/'reports/C5_soc_build.json').read_text())['variants']:
        path=Path(row['executable']);assert sha(path)==row['sha256'];pairs.append((path,'bin/C5/'+path.parent.name+'/sim','binary'))
    for path in sorted((WORK/'c4/build').rglob('sim')):pairs.append((path,'bin/C4/'+path.relative_to(WORK/'c4/build').as_posix(),'binary'))
    for name,path in [('c5-nemu-ref.so',WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so'),('c4-nemu-ref.so',WORK/'nemu-ref/build/riscv32-nemu-interpreter-so'),('nvboard-c5.a',WORK/'c5/nvboard/build/nvboard.a')]:
        assert path.is_file(),path;pairs.append((path,'bin/'+name,'binary'))
    for job in json.loads((ROOT/'reports/C5_app_builds.json').read_text())['builds']:
        for key in ['image','elf']:
            path=Path(job[key]);assert sha(path)==job[key+'_sha256'];pairs.append((path,'firmware/apps/'+job['name']+'/'+job['memory']+'/'+(job['arguments'].replace(' ','_') or 'empty')+'/'+path.name,'firmware'))
    rt=json.loads((ROOT/'reports/C5_rtthread_apps_sdram128.json').read_text())
    for key in ['image','elf']:
        path=Path(rt[key]);assert sha(path)==rt[key+'_sha256'];pairs.append((path,'firmware/rtthread-apps/'+path.name,'firmware'))
    for relative in ['sdram32x2-134217728-asm','sdram16x1-33554432-asm','psram-sweep-4194304','chiplink-test']:
        for path in sorted((WORK/'c5/workbench'/relative/'build').glob('*')):
            if path.suffix in ['.bin','.elf']:pairs.append((path,'firmware/memory/'+relative+'/'+path.name,'firmware'))
    # Preserve final scripted RT boot binaries separately from the interactive one.
    for path in sorted((WORK/'c5/rt-thread-am/bsp/abstract-machine/build').glob('rtthread-*.elf')):
        pairs.extend([(path,'firmware/rtthread-boot/'+path.name,'firmware'),(path.with_suffix('.bin'),'firmware/rtthread-boot/'+path.with_suffix('.bin').name,'firmware')])
    phase_builds=ROOT/'reports/C5_parallel_sdram_builds.json'
    if phase_builds.exists():
        for row in json.loads(phase_builds.read_text())['builds']:
            if row['bytes']!=134217728 or row['corrupt']:continue
            for key in ['image','elf']:
                path=Path(row[key]);assert sha(path)==row[key+'_sha256'];pairs.append((path,f'firmware/parallel-sdram/phase-{row["phase"]}/'+path.name,'firmware'))
    names=[dest for _,dest,_ in pairs]
    from collections import Counter
    assert len(names)==len(set(names)),[name for name,count in Counter(names).items() if count>1]
    return pairs


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--inventory',action='store_true');args=parser.parse_args();pairs=inventory()
    if args.inventory:
        total=sum(path.stat().st_size for path,_,_ in pairs if not path.is_symlink())
        print(json.dumps({'files':len(pairs),'uncompressed_bytes':total,'symlinks':[{'source':str(path),'target':os.readlink(path)} for path,_,_ in pairs if path.is_symlink()]},indent=2),flush=True);return
    rows=json.loads((ROOT/'reports/C5_sdram_sweep.json').read_text())['runs'];serial=any(r['width']==32 and r['ranks']==2 and r['bytes']==134217728 and not r['corrupt'] and r['status']=='PASS' for r in rows)
    parallel=ROOT/'reports/C5_sdram_full_parallel.json'
    assert serial or (parallel.exists() and json.loads(parallel.read_text())['status']=='PASS_FULL_CAPACITY_PARALLEL_PATTERNS'),'Do not freeze before full128 acceptance'
    out=ROOT/'C/offline';out.mkdir(parents=True,exist_ok=True);archive=out/'c-final-runtime.tar.gz';assert not archive.exists(),'Never overwrite a frozen runtime'
    members=[]
    with tarfile.open(archive,'w:gz',compresslevel=3,dereference=False) as tar:
        for path,destination,role in pairs:
            row={'path':destination,'source':str(path),'role':role}
            if path.is_symlink():
                target=os.readlink(path);resolved=posixpath.normpath(posixpath.join(posixpath.dirname(destination),target));assert not target.startswith('/') and not resolved.startswith('../'),(path,target)
                tar.add(path,arcname=destination,recursive=False);row.update(kind='symlink',target=target)
            else:
                row.update(kind='file',bytes=path.stat().st_size,sha256=sha(path));info=tar.gettarinfo(str(path),arcname=destination)
                with path.open('rb') as stream:tar.addfile(info,stream)
            members.append(row)
    expected={row['path']:row for row in members};seen=set()
    with tarfile.open(archive,'r|gz') as tar:
        for item in tar:
            assert item.name in expected and item.name not in seen;seen.add(item.name);row=expected[item.name]
            if row['kind']=='symlink':assert item.issym() and item.linkname==row['target']
            else:
                assert item.isfile() and item.size==row['bytes'];h=hashlib.sha256()
                with tar.extractfile(item) as stream:
                    for block in iter(lambda:stream.read(1048576),b''):h.update(block)
                assert h.hexdigest()==row['sha256'],item.name
    assert seen==set(expected)
    dump(ROOT/'reports/C_runtime_export.json',{'status':'PASS','archive':archive.relative_to(ROOT).as_posix(),'sha256':sha(archive),'bytes':archive.stat().st_size,'members':members,'scope':'FinalCworkbench/app/ref/RT/NVBoard andbothSoCgenerator sourcecopies plusrecordedbinaryprofilesandselectedfirmware. Git/build/out intermediates omitted. Historicalcommandinputs remain separatelysnapshotted; olderbinaryprofiles retain their own acceptedbuildsources. No F/E/D source orarchive modified.'})
    locks=json.loads((ROOT/'reports/C5_source_lock.json').read_text());sources=[{'archive':locks['archive'],'sha256':locks['sha256'],'commit':locks['commit'],'repository':locks['repository']},*locks['submodules']]
    sources += json.loads((ROOT/'reports/C_additional_sources.json').read_text())['items']
    # The educational cell library is also present in command snapshots. Keep
    # its license beside an explicit source copy for downstream inspection.
    nangate=json.loads((ROOT/'reports/C4_nangate_library.json').read_text())
    sources += [{'archive':nangate['local_file'],'sha256':nangate['local_sha256'],'repository':nangate['repository'],'commit':nangate['commit'],'url':nangate['download_url']},
                {'archive':nangate['license']['path'],'sha256':nangate['license']['sha256'],'repository':nangate['repository'],'commit':nangate['commit']}]
    copied=[];seen_paths=set();source_dir=out/'sources';source_dir.mkdir(exist_ok=True)
    for row in sources:
        if 'archive' not in row:continue
        path=local(row['archive']);assert sha(path)==row['sha256']
        if str(path) in seen_paths:continue
        seen_paths.add(str(path));target=source_dir/path.name;assert not target.exists();shutil.copyfile(path,target);assert sha(target)==row['sha256']
        copied.append({'source':str(path),'path':target.relative_to(ROOT).as_posix(),'sha256':row['sha256'],'bytes':target.stat().st_size,'repository':row.get('repository'),'commit':row.get('commit'),'url':row.get('url')})
    dump(ROOT/'reports/C_offline_sources.json',{'status':'PASS','files':copied,'inherited_pristine_sources':['reports/E_offline_sources.json','reports/D_offline_sources.json'],'scope':'FixedCfullSoCandrecursive source archives/additional documents copiedandhashed. ExistingbaseNEMU/AM/kernel/FCEUX source archives remaininthecumulativeF/E/D delivery tree. Installedtools/Maven/JDK/systemlibraries remain separatelylocked dependencies.'})
    print('C_RUNTIME_FREEZE_PASS',len(members),archive.stat().st_size,flush=True)


if __name__=='__main__':main()
