"""Prepare final documentation, visual records and preservation proof."""
from evidence import *
import shutil

def main():
    timestamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
    backup=ROOT/'config/history'/('D_final_'+timestamp);backup.mkdir(parents=True)
    workspace=ROOT.parents[1]
    for name,path in [('project_README.md',ROOT/'README.md'),('workspace_README.md',workspace/'README.md'),('project_toolchain.json',ROOT/'config/toolchain.json'),('workspace_toolchain.json',workspace/'config/toolchain.lock.json')]:shutil.copyfile(path,backup/name)
    path=ROOT/'README.md';text=path.read_text('utf8');tail=text[text.index('- [F阶段验收报告]'):]
    prefix='''# 一生一芯：独立实现工程

D 阶段公开工程范围已完成：55 项核心任务通过，103 条来源记录逐项归档。实现 RV32IM NEMU、RV32E NPC、AM/klib、SDB/trace/DiffTest，并完成编译语义、RTL 综合与工艺库分析。D9 原页建设中，D6 todo 排除；本工程停在 D，不进入 C。

从 [D 总报告](reports/D_REPORT.md)、[逐项清单](reports/D_TASKS.md)、[机器审计](reports/D_AUDIT.json)进入。交付为 `YSYX_D_DELIVERY.zip` 与 `.zip.sha256`；[Verify-D.ps1](scripts/Verify-D.ps1)只读核验保留证据和归档完整性。最终源码与 Linux 二进制见 [D 离线说明](D/offline/README.md)。

F/E 历史结果与旧 ZIP 保留。E 阶段原 CPU 在锁定库、约束与寄生模型下完成 50 MHz 物理流程、DRC 0、LVS 0；这个结论仅属于旧 CPU，不是 D8 新 CPU 的物理签核。D6 额外 DFF 理想 MOS 瞬态模型未通过，具体限制见 D 总报告。个人材料、申请和答辩继续排除；WSL 内存上限沿用已授权的 4 GiB，禁止恢复 computer-use 操作 Logisim。

'''
    tail=tail.replace('旧stop-after-F已撤销','当前授权止于 D，旧 F/E 停点保留为历史')
    tail=tail.replace('当前已进入E，不直接重跑它的最终停点审计','当前已完成 D，不直接重跑它的最终停点审计')
    tail += '\nE 的 Verify-E.ps1 保留当时停在 E 的账本条件；当前 D 账本下不直接执行其终点断言。D 核验器会按原 E 交付清单核对历史文件，旧 ZIP 仍对应 E 完成时的完整状态。D 工作台与快照位于独立目录，不用历史初始化脚本覆盖最终运行候选。\n'
    path.write_text(prefix+tail,encoding='utf8')
    path=workspace/'README.md';text=path.read_text('utf8');parts=text.split('\n\n',2)
    paragraph='这是已完成工具准备的本地电路研究工作区。“一生一芯”独立实现已完成 D 阶段公开工程范围：55 项核心任务通过、103 条来源记录逐一归档，详见 [D 交付报告](projects/ysyx_f_to_b/reports/D_REPORT.md)。F/E 原源码、运行快照和旧交付包保留；E 的旧 CPU 物理签核结论不移用于 D8 新 CPU。工程停在 D，未进入 C，个人申请/答辩排除。WSL 内存上限沿用已授权的 4 GiB。'
    path.write_text(parts[0]+'\n\n'+paragraph+'\n\n'+parts[2],encoding='utf8')
    path=ROOT/'config/toolchain.json';tool=json.loads(path.read_text('utf8'));tool['D_stage']={'status':'COMPLETE_ENGINEERING_WITH_DECLARED_LIMITS','audit':'reports/D_AUDIT.json','final_binary_and_model_lock':'reports/D_toolchain_final.json','final_sources':'reports/D_final_bindings.json','new_dependencies':['portable Clang 15.0.7','Capstone 5.0.6','locked NJU Spike fork','portable dtc/libfdt'],'workspace':'/home/USER/d-stage','qualification':'RV32IM/RV32E finite functional verification and D6 pre-layout library analysis; no new D CPU physical signoff.'};dump(path,tool)
    path=workspace/'config/toolchain.lock.json';lock=json.loads(path.read_text('utf8'));entry=lock['project_toolchains']['ysyx_f_to_b']
    entry.update(status='D_COMPLETE_ENGINEERING_WITH_DECLARED_LIMITS',note='D core 55/55 complete. F/E history preserved. D8 CPU has no physical signoff; E physical conclusions remain tied to E candidate.',audit=str(ROOT/'reports/D_AUDIT.json'),fingerprints=str(ROOT/'reports/D_toolchain_final.json'))
    lock['workspace_state']['current_project_status']=entry['status'];lock['last_updated_utc']=datetime.now(timezone.utc).isoformat();dump(path,lock)
    images=[]
    for name in ['read','proc','opt','techmap','dfflibmap','abc']:
        images.append((f'D/D6/results/{name}.png','Inspected actual Yosys graph; stage labels, ports and topology visible. Functional comparison is separate.'))
    for name in ['NAND2X1H7L','OAI22X1H7L','DFFX1H7L','ADDFX1H7L']:
        images.append((f'D/D6/results/pdk/{name}.png','Inspected CDL connectivity graph. Dense DFF/ADDF networks require zooming the retained SVG; not a physical layout or LVS certificate.'))
    images.append(('D/D8/architecture.png','Inspected final single-cycle datapath including PC+4 writeback, PC operands, RF observation and commit/halt paths.'))
    for name,desc in [('released','Blue checkerboard'),('pressed','Red checkerboard while J is down'),('released_again','Blue checkerboard restored')]:
        images.append((f'artifacts/D8/fceux/native_session/{name}.png',desc+' in the actual final-candidate SDL/Xvfb capture.'))
    dump(ROOT/'reports/D_visual_review.json',{'status':'PASS','scope':'Actual saved images inspected. Pixel and audio tests are separately logged; no physical speaker claim.','images':[{'path':p,'sha256':sha(ROOT/p),'observation':d} for p,d in images]})
    manifest=json.loads((ROOT/'reports/E_delivery_manifest.json').read_text('utf8'));preserved=[]
    for row in manifest['entries']:
        p=row['path']
        if p.startswith(('E/','F/','reports/E','reports/F')):
            assert sha(ROOT/p)==row['sha256'],p;preserved.append(row)
    baseline=json.loads((ROOT/'reports/D_baseline.json').read_text('utf8'))
    assert sha(ROOT/'YSYX_E_DELIVERY.zip')==baseline['E_zip_sha256']
    assert sha(ROOT/'reports/E_AUDIT.json')==baseline['E_audit_sha256']
    dump(ROOT/'reports/D_history_preservation.json',{'status':'PASS','E_zip_sha256':baseline['E_zip_sha256'],'E_audit_sha256':baseline['E_audit_sha256'],'preserved_files':preserved,'scope':'Every F/E source/report/frozen artifact listed by the prior E delivery manifest is unchanged. Shared README/config state advances to D; E ZIP remains byte-identical.'})
    print('D_METADATA_AND_HISTORY_PASS',len(preserved),'files',flush=True)

if __name__=='__main__':main()
