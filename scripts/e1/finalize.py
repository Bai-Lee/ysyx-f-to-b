"""Fail-closed E1 evidence audit, task ledger and human-readable acceptance index."""
from common import *
from datetime import datetime,timezone
from collections import Counter
import shutil,platform,zipfile


def check_run(record):
    folder=ROOT/'artifacts'/record['name']
    assert record['status']=='PASS' and record['inputs_unchanged'],record['name']
    assert json.loads((folder/'run.json').read_text('utf8'))==record,record['name']+' run record differs'
    for stream in ('stdout','stderr'):assert sha(folder/(stream+'.log'))==record[stream+'_sha256']
    assert record['inputs']==record['inputs_after']
    with zipfile.ZipFile(folder/'input_snapshot.zip') as z:
        for i,item in enumerate(record['inputs']):
            p=Path(item['path']);assert sha(p)==item['sha256'],str(p)+' changed since run'
            assert hashlib.sha256(z.read(f'{i:02d}_{p.name}')).hexdigest()==item['sha256']
    return record['name']


def main():
    now=datetime.now(timezone.utc).isoformat();stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
    specs=json.loads((OUT/'specs.json').read_text('utf8'));jobs=json.loads((OUT/'jobs.json').read_text('utf8'));results=json.loads((ROOT/'reports/E1_results.json').read_text('utf8'));structure=json.loads((ROOT/'reports/E1_structure.json').read_text('utf8'));faults=json.loads((ROOT/'reports/E1_faults.json').read_text('utf8'));export=json.loads((ROOT/'reports/E1_export.json').read_text('utf8'));preflight=json.loads((ROOT/'reports/preflight_E1.json').read_text('utf8'))
    expected={x['slug'] for x in specs['records']};assert len(expected)==112
    assert sha(specs['source_matrix'])==specs['source_matrix_sha256']
    assert all(len(d['records'])==112 and {x['slug'] for x in d['records']}==expected for d in (jobs,results,structure))
    assert Counter(x['scope'] for x in specs['records'])=={'基础路径指定题':60,'基础路径指定题；九题自检之一':9,'原文建议的语法基础题':43}
    assert preflight['status']=='PASS'
    for tool in preflight['tools'].values():assert sha(tool['path'])==tool['sha256']
    checked_runs=[];by_slug={x['slug']:x for x in results['records']};struct={x['slug']:x for x in structure['records']}
    for row in jobs['records']:
        slug=row['slug'];r=by_slug[slug];s=SPECS[slug]
        assert r['status']=='PASS' and r['semantic_sentinel_pass'] and r['mutation'] is None
        assert sha(s['source_path'])==s['source_sha256']==row['source_sha256']==r['source_sha256']
        assert ports(s['interface'])==row['interface']==r['interface']
        for field in ('dut','vectors','testbench','support','syntax_support'):assert sha(row[field])==r[field+'_sha256'],slug+' '+field
        assert row['cases']==r['cases'] and row['outputs_checked']==r['outputs_checked'] and row['mask_reasons']==r['mask_reasons']
        assert all(0<n<=row['cases'] for n in row['outputs_checked'].values())
        count=sum(1 for _ in Path(row['vectors']).open('r',encoding='ascii'));assert count==row['cases']
        for part in ('syntax','compile','simulation'):checked_runs.append(check_run(r[part]))
        log=(ROOT/'artifacts'/r['simulation']['name']/'stdout.log').read_text('utf8')
        assert f'PASS {slug} checks={count}' in log and 'MISMATCH' not in log
        sr=struct[slug];assert sr['status']=='PASS' and all(c['pass'] for c in sr['checks'])
        assert sha(sr['netlist_path'])==sr['netlist_sha256'];checked_runs.append(check_run(sr['execution']))
        row['status']='PASS'
    assert faults['status']=='PASS' and len(faults['records'])==14
    for r in faults['records']:
        assert r['fault_rejected'] and r['semantic_sentinel_pass'] and r['simulation']['exit_code']==1
        for part in ('syntax','compile','simulation'):checked_runs.append(check_run(r[part]))
        assert 'MISMATCH' in (ROOT/'artifacts'/r['simulation']['name']/'stdout.log').read_text('utf8')
    assert export['status']=='PASS_ADAPTED' and export['source_unchanged']
    assert sha(export['source'])==export['source_sha256'] and sha(export['export'])==export['export_sha256']
    assert export['disconnected_output_control']['status']=='PASS'
    assert sha(export['disconnected_output_control']['input'])==export['disconnected_output_control']['input_sha256']
    for r in export['runs']:
        checked_runs += [check_run(r['compile']),check_run(r['simulation'])]
    assert all(x['status']=='PASS' for x in structure['records'])
    # Lock the local picture dependencies too; these are archive snapshots, not an upstream signature.
    images=[]
    for row in json.loads((OUT/'source_images.json').read_text('utf8')):
        for path in row['images']:images.append({'slug':row['slug'],'path':path,'sha256':sha(path)})
    dump(OUT/'source_assets.lock.json',{'measured_at':now,'meaning':'Local archived asset hashes; no claim of upstream cryptographic authentication.','records':images})
    checked=sum(x['cases'] for x in jobs['records']);assert checked==800825
    audit={'status':'PASS','timestamp':now,'node':'E1','required_path':69,'suggested_language':43,'total_problems':112,'test_sampling_points':checked,'validated_run_records':len(checked_runs),'mutation_rejections':14,'schematic_export':'PASS_ADAPTED','source_versions':'v26.07 course scope + unversioned HDLBits captured sources; no v23.06 substitution needed for E1.','official_OJ_submission':False,'whole_E_stage_complete':False,'checks':['All selected source raw hashes and external interfaces','Actual Icarus syntax/compile/runtime logs and snapshot input hashes','Every output checked; all masking explicitly declared','Yosys process conversion/check, latch rejection, required helpers and clocks','14 behaviorally rejected compiled mutations','Original F circuit preserved; structural export + four truth cases + two negative controls','Existing tool executable fingerprints'],'scope_limits':['Large input spaces use directed/seeded simulation; not a universal equivalence proof.','No official hidden-test verdict or physical timing/area/power claim.','Native XML connectivity export substitutes GUI HDL export under user authorization.','Undefined pre-reset or non-done data and explicitly unused encodings are masked only as documented.'],'tools':preflight['tools'],'python':{'executable':sys.executable,'version':sys.version,'sha256':sha(sys.executable)},'platform':platform.platform(),'run_names':checked_runs}
    dump(ROOT/'reports/E1_AUDIT.json',audit);results.update(status='PASS',validated_at=now);dump(ROOT/'reports/E1_results.json',results);dump(OUT/'jobs.json',jobs)
    backup=ROOT/'config/history'/stamp;backup.mkdir(parents=True)
    status_path=ROOT/'config/task_status.json';shutil.copyfile(status_path,backup/'task_status.json')
    state=json.loads(status_path.read_text('utf8'));by_id={r['id']:r for r in results['records']}
    for t in state['tasks']:
        if t['id'] in by_id:
            r=by_id[t['id']];t.update(status='PASS',implementation_status='PASS',evidence=[r['dut'],r['testbench'],r['vectors'],str(ROOT/'artifacts/E1'/r['slug']/'simulate/run.json'),str(ROOT/'reports/E1_structure.json')],result_details=f"Local public-spec verification: {r['cases']} input/clock sampling points; exact ports; Yosys process check PASS. Not an official OJ verdict.",updated=now)
        elif t['id']=='E1-M001':t.update(status='PASS',implementation_status='PASS',evidence=[str(ROOT/'reports/E1_REPORT.md'),str(ROOT/'reports/E1_AUDIT.json')],result_details='69 course basic-path +43 recommended language problems=112; nine advanced self-checks included, not counted twice. All local tests PASS.',updated=now)
        elif t['id']=='E1-M002':t.update(status='PASS_ADAPTED',implementation_status='PASS_ADAPTED',evidence=[str(ROOT/'reports/E1_export.json'),str(OUT/'export/tutorial_export.v'),str(OUT/'notes/实现与验收说明.md')],result_details='Actual F .circ -> native net-graph translator -> structural Verilog, 4/4 truth cases; disconnected net and wrong gate controls rejected. GUI export replaced per user instruction.',updated=now)
    state.update(current_stage='E1',stage_status='PASS',next_stage='E2',stop_after_F=False);dump(status_path,state)
    # Reviewable per-problem index, linked to code, tests, oracle, raw logs and declared masks.
    lines=['# E1 逐题交付与验收索引','',f'完成时间：{now}。112题全部本地自验PASS；采样点总数{checked:,}。时序题通常每拍检查沿前、沿后两次，不能把这个数等同于独立测试场景数。','', '原题接口与说明见 [冻结规格](../E/E1/specs.json)；实际结果见 [机器结果](E1_results.json)。原题网页/图片保留在既有离线资料库，未把其他人的解答当作实现。','', '| ID / 原题 | 实现交付物 | 验收采样点 | 被检查输出 | 备注 |','|---|---|---:|---|---|']
    for r in results['records']:
        slug=r['slug'];note=r['explanation'] or '原题接口、功能与位宽按独立参考向量检查。'
        masks='；'.join(k+': '+v for k,v in r['mask_reasons'].items())
        if masks:note+=' 屏蔽范围：'+masks
        note=note.replace('|','\\|').replace('\n',' ')
        counts=', '.join(k+'='+str(v) for k,v in r['outputs_checked'].items())
        lines.append(f"| {r['id']} [{r['title']}]({SPECS[slug]['source_url']}) | [RTL](../E/E1/rtl/{slug}.v) · [TB](../E/E1/tests/{slug}_tb.sv) · [向量](../E/E1/vectors/{slug}.txt) · [日志](../artifacts/E1/{slug}/simulate/stdout.log) | {r['cases']:,} | {counts} | {note} |")
    (ROOT/'reports/E1_PROBLEMS.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
    report=f'''# E1 硬件描述语言验收报告

E1已完成公开技术要求的本地实现与验收：E1-M001为PASS；E1-M002采用用户允许的命令行替代方案，记为PASS_ADAPTED。更新时间：{now}。

| 交付/检查 | 真实运行结果 |
|---|---|
| HDLBits指定基础路径 | 69/69 PASS，包含9道高级自检题 |
| 建议的入门及语言题 | 43/43 PASS |
| Icarus语法、编译、四态仿真 | 112/112 PASS；{checked:,}个采样点 |
| Yosys过程转换与结构检查 | 112/112 PASS；端口、位宽、非零数组下标、指定模块数/共用时钟与无锁存器 |
| 故障注入 | 14/14编译成功后被行为断言拒绝 |
| 原理图到Verilog | 8个部件、7条电气网络；4种输入全通过；断线和错门对照检出 |
| 证据审计 | {len(checked_runs)}份当前运行记录、输入快照、输出日志及SHA-256一致 |

[逐题交付与验收索引](E1_PROBLEMS.md)列出全部112题；[实现说明](../E/E1/notes/实现与验收说明.md)解释关键设计和测试边界；[机器审计](E1_AUDIT.json)记录工具指纹、完整性和限制。

复验入口是[scripts/Run-E1.ps1](../scripts/Run-E1.ps1)。它重建RTL/向量，实际运行Icarus和Yosys、故障对照及导出，再重新审计。使用现有D盘工具及Python，无需联网或操作Logisim GUI。原始命令、cwd、版本/指纹、输入快照、退出码、日志、耗时与超时限制保存在artifacts/E1，历史失败保留在attempts目录。

本次修复并保留证据的问题包括：SystemVerilog保留字checker不能用作实例名；两道计数器中数字常量紧贴问号造成Yosys解析歧义，已加括号和空格。更早的试运行失败也保留原始日志，没有删除断言或改题面条件来通过。

E1-M002的原始电路是[F阶段教程电路](../F/circuits/tutorial_reference_complete.circ)。本次从真实XML连线关系生成门级Verilog，没有调用Logisim GUI导出器，也不把这一替代过程说成官方导出功能。

验收范围是v26.07课程列出的公开要求与已归档的HDLBits题面。HDLBits是无版本号的第三方题库；本节点未用v23.06冒充新版。没有提交官方OJ，没有获得隐藏测试或课程资格认证。大位宽和长时序使用定向加固定种子测试，不能宣称全输入无界证明；Yosys结构转换不代表实物PPA或流片完成。

F历史完成记录保留。E1-O001的扩展书籍/视频及需注册OJ属于选读，未冒称全部学习或提交。下一节点为E2；本报告仅完成E1，不代表整个E阶段已完成。
'''
    (ROOT/'reports/E1_REPORT.md').write_text(report,encoding='utf8')
    print('E1_FINAL_AUDIT PASS',checked,'sampling points',len(checked_runs),'verified run records',flush=True)


if __name__=='__main__':main()
