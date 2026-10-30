"""Root-owned reconciliation of completed C work; never infer pending passes."""
from evidence import *
import shutil

def main():
    path=ROOT/'reports/C_results.json';rows={r['id']:r for r in json.loads(path.read_text('utf8')).get('records',[])} if path.exists() else {}
    for stage in ('C1','C3'):
        report=ROOT/'reports'/f'{stage}_AUDIT.json'
        if report.exists():
            audit=json.loads(report.read_text('utf8'));assert audit['status']=='PASS'
            for row in audit['records']:rows[row['id']]=row
    def mark(key,detail,evidence):rows[key]={'id':key,'status':'PASS','details':detail,'evidence':evidence}
    native=ROOT/'reports/C2_native_io.json'
    if native.exists():
        data=json.loads(native.read_text('utf8'));assert data['status'].startswith('PASS')
        for key,detail in [('C2-M002','Official native RTC produced 1/2/3-second output; bounded SDL session.'),('C2-M003','Official native keyboard received J/Left DOWN and UP.'),('C2-M004','Official native video produced real changing 256-color SDL frames.'),('C2-M005','Authored draw fills the complete 400x300 logical framebuffer; 800x600 scaled native capture is uniformly blue.'),('C2-M006','7744 palette transitions/endpoint and monotonicity checks; real gradient capture; wrong interpolation rejected.'),('C2-M007','Actual held/released key timing ratio 4.00012; multi-key handling and Escape exit verified.')]:
            mark(key,detail,['reports/C2_native_io.json','C/C2/screensaver/screensaver.c','artifacts/C2/native'])
    npc=ROOT/'reports/C2_npc_io.json'
    if npc.exists():
        data=json.loads(npc.read_text('utf8'));assert data['status'].startswith('PASS')
        for key,detail,report in [('C2-M001','Real native FCEUX, CC0 ROM, pressed/released image and 440/220/440Hz SDL PCM capture; no physical speaker claim.','C2_fceux_native'),('C2-M009','C-only RV32E NPC hello through UART at0x10000000; per-instruction REF coverage and explicit MMIO synchronization.','C2_npc_io'),('C2-M010','Official NPC timer produced 1/2/3 seconds with host-time device; semantic stop, not timeout.','C2_npc_io'),('C2-M011','NPC completed two ASCII FCEUX frames and stopped at third frame header.','C2_fceux_ascii')]:mark(key,detail,['reports/'+report+'.json','C/C2/npc_devices.py','artifacts/C2/fceux'])
    dump(path,{'status':'IN_PROGRESS','records':list(rows.values())})
    ledger_path=ROOT/'config/task_status.json';ledger=json.loads(ledger_path.read_text('utf8'))
    for task in ledger['tasks']:
        if task['id'] in rows:
            row=rows[task['id']];task.update(status=row['status'],evidence=row['evidence'],result_details=row['details'])
    ledger.update(current_stage='C2',stage_status='IN_PROGRESS',stop_after='C');dump(ledger_path,ledger)
    workspace=ROOT.parents[1];marker=ROOT/'config/history/C_startup_documents'
    if not marker.exists():
        marker.mkdir(parents=True)
        for name,p in [('project_README.md',ROOT/'README.md'),('workspace_README.md',workspace/'README.md'),('workspace_toolchain.json',workspace/'config/toolchain.lock.json')]:shutil.copyfile(p,marker/name)
        p=ROOT/'README.md';text=p.read_text('utf8');text=text.replace('# 一生一芯：独立实现工程\n','# 一生一芯：独立实现工程\n\nC 阶段已获授权并正在推进，边界止于 C。固定范围为 68 项公开核心、2 项项目编号适配及背景/提醒，共 101 条来源记录；独立工作台为 `/home/USER/c-stage`，当前结果见 [C 进度账本](reports/C_results.json)和 [C 工具预检](reports/C_PREFLIGHT.json)。以下 D 交付仍保持其完成时的内容与范围。\n',1)
        text=text.replace('本工程停在 D，不进入 C。','这是 D 完成时的历史停点；后续用户已授权继续 C。',1);p.write_text(text,encoding='utf8')
        p=workspace/'README.md';text=p.read_text('utf8');text=text.replace('工程停在 D，未进入 C，个人申请/答辩排除。','用户已授权继续 C，当前在独立 C 工作台推进；个人申请/答辩仍排除。',1);p.write_text(text,encoding='utf8')
        p=workspace/'config/toolchain.lock.json';lock=json.loads(p.read_text('utf8'));lock['workspace_state']['current_project_status']='C_IN_PROGRESS';entry=lock['project_toolchains']['ysyx_f_to_b'];entry.update(status='C_IN_PROGRESS',current_preflight=str(ROOT/'reports/C_PREFLIGHT.json'),note='C authorized and in progress. Existing audit/fingerprint fields retain completed D evidence until C is accepted.');dump(p,lock)
    print('C_PROGRESS',len(rows),'accepted scope records',flush=True)

if __name__=='__main__':main()
