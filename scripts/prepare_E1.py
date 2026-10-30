"""Freeze the E1 problem set and explicitly record the user's resume instruction."""
from evidence import *
from bs4 import BeautifulSoup
import shutil

ARCHIVE=ROOT.parents[1]/'YSYX_F_B_Archive'
def backup(p):
    dst=ROOT/'config/history'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')/p.relative_to(ROOT)
    dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dst)
def main():
    for d in ['E/E1/rtl','E/E1/tests','E/E1/vectors','E/E1/notes','E/E1/export','artifacts/E1','temp/E1','scripts/e1']:(ROOT/d).mkdir(parents=True,exist_ok=True)
    p=ROOT/'config/execution_policy.json';backup(p);policy=json.loads(p.read_text('utf8'));policy.update(current_scope='Resume from E1 under direct user instruction; proceed through public engineering coursework, preserving F completion.',stop_after=None,advance_to_E=True,source_instruction='2026-10-24 user: 从 E1 接续. Previous stop-after-F is explicitly superseded.',current_model='GPT-6 Astra',allow_logisim_gui=False,computer_use_logisim=False);dump(p,policy)
    matrix=json.loads((ARCHIVE/'inventory/assignment_matrix.json').read_text('utf8'))
    catalog={x['id']:x for x in json.loads((ARCHIVE/'temp/assignment_review/hdlbits_all.json').read_text('utf8'))}
    records=[]
    for item in matrix['records']:
        if not item['id'].startswith('HDL-'):continue
        row=catalog[item['id']];source=ARCHIVE/row['raw']
        if sha(source)!=row['sha256']:raise ValueError('Raw source fingerprint changed: '+row['id'])
        doc=BeautifulSoup(source.read_bytes(),'lxml');body=doc.select_one('.mw-parser-output')
        if body is None:raise ValueError('Source body missing')
        decl=body.select_one('#portlistbox')
        if decl is None:raise ValueError('Interface missing: '+row['id'])
        for el in body.select('form,textarea,script:not([type="WaveDrom"]),#hintbox,.printfooter,.mw-editsection'):
            el.decompose()
        records.append({'id':row['id'],'slug':row['url'].rsplit('/',1)[-1],'title':row['title'],'group':row['group'],'scope':item['classification'],'source_url':row['url'],'source_path':str(source),'source_sha256':row['sha256'],'source_markdown':str(ARCHIVE/row['markdown']),'interface':decl.get_text(),'statement':body.get_text(' ',strip=True),'status':'NOT_RUN'})
    if len(records)!=112:raise ValueError('E1 scope changed; review required')
    dump(ROOT/'E/E1/specs.json',{'source_matrix':str(ARCHIVE/'inventory/assignment_matrix.json'),'source_matrix_sha256':sha(ARCHIVE/'inventory/assignment_matrix.json'),'required_path':69,'suggested':43,'records':records})
    lock=json.loads((ROOT.parents[1]/'config/toolchain.lock.json').read_text('utf8'));tools={}
    for key in ('iverilog','vvp','yosys'):
        entry=lock['tools'][key];actual=sha(entry['executable'])
        if actual!=entry['sha256']:raise ValueError('Tool changed: '+key)
        tools[key]={'path':entry['executable'],'sha256':actual,'version':entry['version']}
    dump(ROOT/'reports/preflight_E1.json',{'status':'PREPARED_CONTROLS_PENDING','task':'Combinational and sequential RTL, FSM and cell-array exercises, circuit-to-Verilog export','tools':tools,'source_count':112,'method':'Icarus four-state simulation with independent mathematical/state/graph reference models; exact interfaces, asynchronous and synchronous reset, directed boundary sequences and seeded random streams; mutation rejection controls. Small combinational spaces exhaustive.','budget':{'parallel_jobs':1,'heavy_jobs':0,'per_process_soft_mib':256,'compile_timeout_seconds':30,'simulation_timeout_seconds':60},'resource_note':'Initial free physical memory about2.85GiB; only small single-process Icarus jobs, no new heavy compilation/VM jobs.','authorization':'User resumed E; no computer-use Logisim, no account/OJ login necessary for public local self-verification.'})
    p=ROOT/'config/task_status.json';backup(p);state=json.loads(p.read_text('utf8'));state.update(current_stage='E1',stage_status='IN_PROGRESS',stop_after_F=False);dump(p,state)
    p=ROOT/'README.md';backup(p);txt=p.read_text('utf8');txt=txt.replace('当前目标：F阶段已完成并通过最终审计；按用户要求在F结束后停止，由GPT-6 Astra接续。不要继续E，不要恢复computer-use操作Logisim。','当前目标：用户已授权由GPT-6 Astra从E1接续。F阶段完成记录保留；E1正在实施，继续采用命令行路线。禁止恢复computer-use操作Logisim。');p.write_text(txt,encoding='utf8')
    print('E1_SCOPE_READY',len(records),'problems',flush=True)
if __name__=='__main__':main()
