"""Package only the implementation and evidence, never the external knowledge archive."""
from evidence import *
import zipfile,shutil

def main():
    summary=json.loads((ROOT/'reports/F_stage_summary.json').read_text('utf8'));audit=json.loads((ROOT/'reports/F_final_audit.json').read_text('utf8'))
    if summary['status']!='F_COMPLETE' or audit['status']!='PASS':raise ValueError('F is not complete')
    workspace=ROOT.parents[1];backups=ROOT/'config/workspace_baseline_backup';backups.mkdir(exist_ok=True)
    readme=workspace/'README.md'
    if not (backups/'README.md').exists():shutil.copyfile(readme,backups/'README.md')
    text=readme.read_text('utf8').replace('后续课题待定，目前没有开展正式课题研究。','当前课题为“一生一芯”独立实现；F阶段已完成自验，按用户要求暂停在F，E阶段由后续模型接续。')
    text=text.replace('`projects` / `models`：将来各课题的代码、原始材料与器件模型，目前为空。','`projects` / `models`：按课题隔离代码和模型；当前项目为 [一生一芯实现与F阶段证据](projects/ysyx_f_to_b/README.md)。')
    readme.write_text(text,encoding='utf8')
    lock=workspace/'config/toolchain.lock.json'
    if not (backups/'toolchain.lock.json').exists():shutil.copyfile(lock,backups/'toolchain.lock.json')
    data=json.loads(lock.read_text('utf8'));data.setdefault('project_toolchains',{})['ysyx_f_to_b']={'lock':'/workspace/projects/ysyx_f_to_b/config/toolchain.json','status':'F_COMPLETE','note':'Optional Logisim4.0.0/Java and existing RTL tool fingerprints; no GUI continuation, no E stage started.'};dump(lock,data)
    (ROOT/'reports/F_WORKSPACE_LINK_UPDATE.json').write_text(json.dumps({'status':'PASS','root_readme':str(readme),'root_lock':str(lock),'backups':str(backups),'existing_tool_entries_unchanged':data['tools']==json.loads((backups/'toolchain.lock.json').read_text('utf8'))['tools']},ensure_ascii=False,indent=2),encoding='utf8')
    zpath=ROOT/'YSYX_F_STAGE_DELIVERY.zip';excluded={'F_STAGE_FILES.sha256','reports/F_package.json'};files=[]
    for folder in ['F','scripts','config','reports','artifacts']:
        for p in (ROOT/folder).rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.autosave','.part','.writing') and p.relative_to(ROOT).as_posix() not in excluded:files.append(p)
    files += [ROOT/'README.md',ROOT/'.gitignore',ROOT/'.gitattributes']
    files=sorted(set(files));hashes={p.relative_to(ROOT).as_posix():sha(p) for p in files};manifest=''.join(hashes[n]+'  '+n+'\n' for n in sorted(hashes));(ROOT/'F_STAGE_FILES.sha256').write_text(manifest,encoding='utf8')
    hashes['F_STAGE_FILES.sha256']=sha(ROOT/'F_STAGE_FILES.sha256')
    temp=zpath.with_suffix('.zip.writing')
    with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in files+[ROOT/'F_STAGE_FILES.sha256']:z.write(p,p.relative_to(ROOT).as_posix())
    bad=[]
    with zipfile.ZipFile(temp) as z:
        for name in z.namelist():
            if hashlib.sha256(z.read(name)).hexdigest()!=hashes[name]:bad.append(name)
        count=len(z.namelist())
        if count!=len(hashes) or bad:raise ValueError('ZIP member SHA/CRC failure '+str(bad))
    temp.replace(zpath);result={'status':'PASS','path':str(zpath),'bytes':zpath.stat().st_size,'sha256':sha(zpath),'members':count,'crc_and_member_sha256':'PASS','scope':'Independent F implementation, notes, vectors, reports and raw evidence. Temp compilation products/.git/installed tools/external source archive omitted; replay recompiles from retained sources.','next_stage':'Stopped at F; E not started.'};dump(ROOT/'reports/F_package.json',result)
    print('F_PACKAGE',json.dumps(result,ensure_ascii=False),flush=True)
if __name__=='__main__':sys.exit(main())
