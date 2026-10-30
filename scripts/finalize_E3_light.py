"""Audit a partial E3 checkpoint. A successful audit is NOT whole-E3 completion."""
from evidence import *
import zipfile,re,shutil
from collections import Counter

def audit_run(r,current=True):
    assert r['status']=='PASS' and r['inputs_unchanged'],r['name']
    folder=ROOT/'artifacts'/r['name'];assert json.loads((folder/'run.json').read_text('utf8'))==r
    for stream in ('stdout','stderr'):assert sha(folder/(stream+'.log'))==r[stream+'_sha256']
    if r['inputs']:
        with zipfile.ZipFile(folder/'input_snapshot.zip') as z:
            for i,item in enumerate(r['inputs']):
                assert hashlib.sha256(z.read(f'{i:02d}_{Path(item["path"]).name}')).hexdigest()==item['sha256']
                if current:assert sha(item['path'])==item['sha256'],item['path']

def main():
    assert json.loads((ROOT/'config/execution_policy.json').read_text('utf8')).get('temporary_resource_limit',{}).get('active'), 'Historical light-only checkpoint superseded; use finalize_E3.py'
    spec=json.loads((ROOT/'E/E3/course_specs.json').read_text('utf8'))
    for ch in spec['chapters']:
        assert sha(ch['source'])==ch['source_sha256']
        for b in ch['blocks']:assert sha(b['path'])==b['sha256']
    tool=json.loads((ROOT/'reports/E3_toolchain.json').read_text('utf8'));assert tool['status']=='PASS'
    work=json.loads((ROOT/'reports/E3_workbench.json').read_text('utf8'));assert work['status']=='PASS'
    records=tool['runs']+[work['clone'],work['verification']]
    early=json.loads((ROOT/'reports/E3_LCT_early_results.json').read_text('utf8'));assert early['status']=='PASS_TEST_BATCH_NOT_WHOLE_CHAPTER_COMPLETION'
    records += [r['execution'] for r in early['cases']]
    for name in ['E3_LCT_early_extra_results','E3_LCT_editor_results','E3_LCT_literals','E3_xxd_build','E3_LCT_array_variants']:
        j=json.loads((ROOT/'reports'/(name+'.json')).read_text('utf8'));assert j['status']=='PASS';records+=j['runs']
    downloads=json.loads((ROOT/'reports/E3_valgrind_source_download.json').read_text('utf8'))
    records += [downloads['enable_source_indexes'],downloads['download']]
    for r in records:audit_run(r)
    assert len({r['name'] for r in records})==len(records)
    layout=json.loads((ROOT/'reports/E3_valgrind_source_layout.json').read_text('utf8'))
    for row in layout['manifest_hashes_matched']:assert sha(row['path'])==row['sha256']
    assert layout['build_status']=='DEFERRED_BY_USER_LIGHT_ONLY_BUDGET'
    auth=json.loads((ROOT/'config/E3_authorization.json').read_text('utf8'))
    assert auth['low_memory_exception']['answer']=='允许临时 1GB 上限做轻量验收'
    budget=json.loads((ROOT/'reports/E3_low_memory_budget.json').read_text('utf8'))
    assert budget['temporary_memory_gib']==1 and sha(budget['config'])==budget['config_sha256']
    code="""import json,os,pwd,platform,subprocess
from pathlib import Path
m={a.split(':')[0]:int(a.split()[1]) for a in Path('/proc/meminfo').read_text().splitlines() if ':' in a}
w='/home/USER/ysyx-workbench'
print(json.dumps({'user':pwd.getpwuid(os.getuid()).pw_name,'uid':os.getuid(),'kernel':platform.release(),'processors':os.cpu_count(),'mem_total_kib':m['MemTotal'],'swap_total_kib':m['SwapTotal'],'workbench_commit':subprocess.check_output(['git','-C',w,'rev-parse','HEAD'],text=True).strip(),'workbench_dirty':subprocess.check_output(['git','-C',w,'status','--porcelain'],text=True)}))
"""
    current=run('E3/current_environment',['wsl.exe','-d','YSYX-Linux','-u','ysyx','--exec','python3','-c',code],[ROOT/'config/E3_authorization.json',ROOT/'reports/E3_low_memory_budget.json'],timeout=30)
    assert current['status']=='PASS'
    environment=json.loads((ROOT/'artifacts/E3/current_environment/stdout.log').read_text('utf8'))
    assert environment['user']=='ysyx' and environment['uid']!=0
    assert environment['processors']==4 and 512*1024<environment['mem_total_kib']<=1024*1024 and environment['swap_total_kib']==2*1024*1024
    assert environment['workbench_commit']=='a839def3f3b046f730537ea420d3075e725d27ce' and not environment['workbench_dirty']
    audit_run(current);records.append(current)
    now=datetime.now(timezone.utc).isoformat()
    note=ROOT/'E/E3/lcthw/notes/00-09.md';assert note.exists()
    selected=[r for r in spec['lcthw_records'] if r['chapter']<=9];assert len(selected)==54
    adapted={'LCT-05-X01','LCT-06-BASE','LCT-07-BASE','LCT-08-BASE','LCT-09-X05'}
    ledger_path=ROOT/'config/task_status.json';ledger=json.loads(ledger_path.read_text('utf8'))
    backup=ROOT/'config/history'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f');backup.mkdir(parents=True);shutil.copyfile(ledger_path,backup/'task_status.json')
    selected_ids={r['id'] for r in selected};details={}
    for row in selected:
        status='RESOURCE_LIMIT' if row['id']=='LCT-04-BASE' else 'PASS_ADAPTED' if row['id'] in adapted else 'PASS'
        details[row['id']]={'id':row['id'],'status':status,'requirement':row['requirement'],'evidence':[str(note),str(ROOT/'reports/E3_LCT_early_results.json'),str(ROOT/'reports/E3_LCT_early_extra_results.json'),str(ROOT/'reports/E3_LCT_literals.json'),str(ROOT/'reports/E3_LCT_array_variants.json'),str(ROOT/'reports/E3_LCT_editor_results.json'),str(ROOT/'reports/E3_xxd_build.json'),str(ROOT/'reports/E3_valgrind_source_layout.json')]}
    for row in ledger['tasks']:
        if row['id'] in details:
            d=details[row['id']]
            explanation='Complete source build of Valgrind deferred by direct user light-only/1GB authorization; original faulty example, repaired example and source inspection completed.' if d['status']=='RESOURCE_LIMIT' else 'Completed the scoped source example/extra or documented observation. Intentionally erroneous programs are not claimed correct; source errata and digital-note substitutions are identified in the explanation.'
            row.update(status=d['status'],implementation_status=d['status'],evidence=d['evidence'],result_details=explanation,updated=now)
        elif row['id']=='E3-M004':
            row.update(status='IN_PROGRESS',implementation_status='IN_PROGRESS',evidence=[str(ROOT/'reports/E3_REPORT.md')],result_details='53/180 subitems complete or explicitly adapted; exercise4 source build deferred;126 later subitems not yet executed.',updated=now)
    ledger.update(current_stage='E3',stage_status='IN_PROGRESS',next_stage='E3-M003 and remaining E3-M004',stop_after_F=False);dump(ledger_path,ledger)
    counts=Counter(x['status'] for x in details.values())
    audit={'status':'PASS','audit_scope':'Evidence consistency for the E3 light-work checkpoint only','stage_complete':False,'stage_status':'IN_PROGRESS','timestamp':now,'linux_environment':environment,'validated_run_records':len(records),'lcthw_total':180,'lcthw_pass':counts['PASS'],'lcthw_pass_adapted':counts['PASS_ADAPTED'],'lcthw_resource_limited':1,'lcthw_not_run':126,'missing_semester_total':54,'missing_semester_completed':0,'completed_core_tasks':['E3-M001','E3-M002'],'incomplete_core_tasks':['E3-M003','E3-M004'],'deferred_by_user':'Complete Valgrind source build and other heavy compilation; current authorization is temporary1GB and light command-line work only.','source_originals_preserved':True,'run_names':[r['name'] for r in records],'notes_sha256':sha(note)}
    dump(ROOT/'reports/E3_AUDIT.json',audit);dump(ROOT/'reports/E3_LCT_early_task_status.json',{'scope':'0-9 only; does not complete E3-M004','records':list(details.values())})
    index=['# E3：LCTHW 0–9逐项验收','',f'共54项：PASS {counts["PASS"]}，PASS_ADAPTED {counts["PASS_ADAPTED"]}，RESOURCE_LIMIT 1。剩余章节126项未执行。','', '每条需求全文在[E3冻结清单](../E/E3/course_specs.json)，[实现说明与勘误](../E/E3/lcthw/notes/00-09.md)逐章解释。PASS在故意错误实验中表示错误得到正确复现/记录，不表示错误程序正确。','', '| 项目 | 实现要求（原文首段） | 交付物与验收 | 状态 |','|---|---|---|']
    for d in details.values():
        req=d['requirement'].splitlines()[0].replace('|','\\|')
        verify='例程及修复已运行；Valgrind完整源码构建暂缓' if d['status']=='RESOURCE_LIMIT' else '原始/派生C、真实日志、独立预期或错误诊断、逐章解释'
        index.append(f'| {d["id"]} | {req} | {verify}；见[证据索引](E3_LCT_early_task_status.json) | {d["status"]} |')
    (ROOT/'reports/E3_LCT_EARLY_INDEX.md').write_text('\n'.join(index)+'\n',encoding='utf8')
    report=f'''# E3 Linux环境与轻量课程检查点

当前E3尚未完成。本检查点证据审计PASS只表示已执行部分可核验；E3-M003和E3-M004仍未全部完成。更新时间：{now}。

| 项目 | 当前结果 |
|---|---|
| E3-M001 Linux开发环境 | PASS：真实Ubuntu22.04.5、C/Make/GDB/Git/Valgrind正反例 |
| E3-M002官方工作台 | PASS：独立Linux克隆，固定提交a839def3f3b046f730537ea420d3075e725d27ce，fsck/干净状态/子模块清单核对 |
| E3-M003 Missing Semester | 0/54逐题验收，尚未完成 |
| E3-M004 LCTHW | 53/180完成或明确替代；1项部分完成但受限；126项未执行 |
| 当前轻量证据审计 | {len(records)}份实际运行记录及输入快照、日志SHA-256核对 |

Linux发行版名为YSYX-Linux，存储在/workspace/tools/wsl/YSYX-Linux，工作台在Linux的/home/USER/ysyx-workbench。专用普通用户为ysyx。实际内核{environment['kernel']}，4个处理器，内存上限临时1GB、swap2GB并位于D盘。当前配置及两个明确授权见[授权记录](../config/E3_authorization.json)和[资源预算](E3_low_memory_budget.json)。

在线WSL更新曾TIMEOUT，随后按[微软官方离线内核安装方法](https://learn.microsoft.com/en-us/windows/wsl/install-manual)下载并验证Microsoft有效签名的MSI，安装返回0，系统实际报告内核已就绪。WSL和VirtualMachinePlatform本来已启用；没有重启Windows，也没有修改Windows更新偏好或全局PATH。Ubuntu341,130,963字节的官方镜像与官方SHA256SUMS相符。

[工具链证据](E3_toolchain.json)包括原生Linux构建、20,000次链表操作、GDB真实断点/参数检查、Valgrind正确程序零错误与故意越界/泄漏被拒绝，以及本地Git操作。[框架证据](E3_workbench.json)保留精确提交；根仓库没有Git子模块，init.sh选择的后续子项目按阶段初始化，未冒称全部已初始化。

LCTHW0–9的[逐项索引](E3_LCT_EARLY_INDEX.md)、[说明与勘误](../E/E3/lcthw/notes/00-09.md)和实际原始/修正版C文件已保存。实验包含坏ELF、格式参数错误、未初始化值、字符串终止符、数组越界、类型提升、整数范围、ABI对照、Vim实际编辑及Make正反例。Valgrind没有检出的若干栈/全局数组问题，被ASan检出；这些差异保留在报告中。未把无报错等同于C程序正确。

已手工构建官方xxd并完成262字节往返校验。Valgrind源码已下载，两个源码归档与发布清单的SHA-256一致，目录和构建入口已阅读；其完整源码编译/安装仍按用户“1GB仅轻量验收”的要求暂缓。这是LCT-04-BASE的剩余步骤，包管理器安装没有冒充源码构建。

轻量重放入口：[Run-E3-Light.ps1](../scripts/Run-E3-Light.ps1)。不重新安装系统、不修改当前资源配置、不编译完整Valgrind，也不启动后续处理器的大型构建。原始安装、失败和修复记录仍保留，初始安装方案属于历史计划而非当前状态。

F、E1和E2已完成的历史记录保留；E2选择的是原文允许的独立链表能力分支，未把72道未做的CEX题标成通过。当前没有官方在线课程/学籍/流片验收结论。
'''
    (ROOT/'reports/E3_REPORT.md').write_text(report,encoding='utf8')
    print('E3_LIGHT_CHECKPOINT_AUDIT PASS; E3 STAGE STILL IN_PROGRESS;',dict(counts),flush=True)

if __name__=='__main__':main()
