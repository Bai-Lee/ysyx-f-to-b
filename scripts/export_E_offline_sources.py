from evidence import *
import shutil
def main():
    lock=json.loads((ROOT/'reports/E_source_lock_canonical.json').read_text('utf8'));dest=ROOT/'E/offline/sources';dest.mkdir(parents=True,exist_ok=True);rows=[]
    for row in lock['repositories']:
        source=Path(row['archive']);assert sha(source)==row['sha256'];target=dest/source.name
        if not target.exists():shutil.copyfile(source,target)
        assert sha(target)==row['sha256'];rows.append({**row,'delivery_path':str(target.relative_to(ROOT)).replace('\\','/')})
    source=ROOT.parents[1]/'YSYX_F_B_Archive/assets/offline/ysyx.oscc.cc/slides/resources/archive/klib-minirv-npc.tar.bz2';target=dest/source.name
    if not target.exists():shutil.copyfile(source,target)
    assert sha(target)==sha(source)
    result={'status':'PASS','repositories':rows,'provided_klib':{'path':str(target.relative_to(ROOT)).replace('\\','/'),'sha256':sha(target)},'scope':'Canonicaltop-levelGitarchivesandtheexactprovidedklib. OriginalfullGit/submodulerepos,installedtools,andPDKreleaseassetsremainintheirlockedexistinglocations. Noexternalupload.'};dump(ROOT/'reports/E_offline_sources.json',result)
    lines=['# E 阶段源码快照','','这些归档保留各上游项目原有许可文件。Git 提交与逐文件来源由锁定记录追踪；导出强制使用仓库提交的规范字节，避免 Windows 换行转换影响测试输入。','', '| 源 | 固定提交 | 归档 SHA-256 |','|---|---|---|']
    for r in rows:lines.append('| '+r['name']+' | '+r['commit']+' | '+r['sha256']+' |')
    lines += ['','提供的 klib 另以原 tar.bz2 保存并校验。以上为顶层仓库快照；完整 Git 历史及子模块仍在原课程归档中。工具安装包与 PDK 发布资产不在此重复打包，路径、版本、下载摘要见项目工具锁定及后端安装报告。仿真采用已提供的生成后 SoC Verilog，不宣称从这些顶层快照重新生成了全部 Chisel 依赖。']
    (ROOT/'E/offline/SOURCES.md').write_text('\n'.join(lines)+'\n',encoding='utf8');print('OFFLINE_CANONICAL_SOURCE_EXPORT_PASS',len(rows),flush=True)
if __name__=='__main__':main()
