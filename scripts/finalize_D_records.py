"""Reconcile the 103 frozen D scope records with concrete retained evidence."""
from evidence import *
from collections import Counter
import shutil

def load(name):return json.loads((ROOT/'reports'/f'{name}.json').read_text('utf8'))

def main():
    checks=['D1_experiments','D1_background','D2_expression','D2_sdb','D3_isa','D3_official_tests','D5_headers','D5_host_klib','D5_allocator','D5_portable','D6_logic','D6_pdk','D6_pvt','D7_trace','D7_regression','D8_reference','D8_reset','D8_front','D8_isa','D8_official_tests','D8_apps_test','D8_apps_train','D8_extra','D8_fileio','D8_alu','D8_prior_tests','D8_timer','D8_fceux_native','D8_fceux_ascii','D8_native_keyboard','D_runtime_export','D_offline_sources','D_final_bindings']
    data={name:load(name) for name in checks}
    assert all(x['status'].startswith('PASS') for x in data.values())
    assert data['D3_isa']['checks']==2392 and data['D3_official_tests']['positive_count']==81
    assert data['D7_regression']['program_count']==81 and data['D8_official_tests']['positive_count']==73
    assert data['D8_isa']['case_count']==1758 and data['D8_apps_test']['runs']==48 and data['D8_apps_train']['runs']==20
    assert data['D8_prior_tests']['case_count']==12 and data['D8_timer']['observed_seconds']==[1,2,3]
    specs=json.loads((ROOT/'D/runtime/course_specs.json').read_text('utf8'))
    rows={r['id']:r for r in load('D_results')['records']}
    def mark(key,detail,evidence=(),status='PASS'):
        stage=key.split('-')[0];rows[key]={'id':key,'status':status,'details':detail,'evidence':[f'D/{stage}/NOTES.md',*evidence]}
    mark('D3-M001','PA2 stage 1 RV32IM: independent 2392-case expectation generator + Spike, 81 original tests, explicit image/encoding/address negatives; all 81 rerun after D7 tracing. Native GUI/audio/key checked in D8.',['reports/D3_isa.json','reports/D3_official_tests.json','reports/D7_regression.json','reports/D8_fceux_native.json','reports/D8_native_keyboard.json'])
    mark('D5-M001','PA2 runtime/AM/klib: 21199 host comparisons, 10000 allocator operations + 512-fragment stress, 5007 checks on each of native/native-klib/RV32IM; sanitizer and wrong-result controls.',['reports/D5_host_klib.json','reports/D5_allocator.json','reports/D5_portable.json'])
    descriptions={
      1:'Independent event ordering and Icarus mixed-assignment result (5,1,1,3,3); NBA settles in the same time slot.',
      2:'Actual generated Verilator light C++ retained; trigger/evaluation/state-update explained.',
      3:'NBA samples old values and swaps deterministically; blocking race alternatives explained with explicit initial state.',
      4:'Actual display/strobe observations separated by event region; no claim one simulator enumerates all legal interleavings.',
      5:'All six coding claims evaluated against event semantics, including #0 before NBA, last same-block NBA and multi-writer limits.',
      6:'Actual Yosys read-stage RTLIL and DOT/SVG/PNG retained.',7:'Actual proc-stage processes lowered and graph retained.',
      8:'Actual opt-stage simplification and graph retained.',9:'Actual techmap-stage bit gates and graph retained.',
      10:'Actual dfflibmap mapped DFF cells and graph retained.',11:'Actual abc mapped netlist; 4096-cycle comparison and inverted-DFF negative control.',
      12:'Actual ECC synthesis logs/TCL preserved for three corners; flow and constraints inspected.',
      13:'IEEE 1364.1-2002 section 5 read with explicit synthesis restrictions and simulation distinctions.',
      14:'Race example analyzed by permitted event interleavings, including initial-state qualification.',
      15:'All 12 Annex B mismatch categories reviewed; five concrete executable categories and B.9 ambiguity qualified.',
      16:'Real ECC light synthesis/STA at 100 MHz, TT/SS/FF; pre-layout, no full external IO constraints.',
      17:'Actual power.rpt units/internal/switching/leakage inspected; vectorless/default activity limits stated.',
      18:'LEF seven routing entries parsed; six main metal layers distinguished from RDL.',
      19:'NAND2 CDL D/G/S/B topology rendered and switch-network truth checked.',
      20:'OAI22 LIB function parsed and compared against binary truth table.',
      21:'OAI22 eight-MOS topology matched to complementary network and LIB.',
      22:'NAND X1/X2/X4 transistor widths, area/capacitance and same-point timing interpolation compared.',
      23:'NAND 0.8x1.4 um versus data IO P65_1233_PBMUX 65x130 um, explicit selected cell.',
      24:'ADDF 28 MOS/6.72 um2 versus selected XOR/AND/OR implementation 42 MOS/10.64 um2; logic checked.',
      25:'747 LVT library entries indexed with CDL/LEF presence and authored categories.',
      26:'Same RTL/clock/strategy resynthesized at TT/SS/FF, actual area/timing/power and source hashes retained.',
      28:'1.4 um cell height / 0.2 um pitch = seven tracks, model assumptions explicit.',
      29:'FILLER1H7L 0.2x1.4 um exactly one core7 SITE.'}
    for n,detail in descriptions.items():
        reports=['reports/D6_logic.json'] if n<=11 or n in (13,14,15) else ['reports/D6_pvt.json'] if n in (12,16,17,26) else ['reports/D6_pdk.json']
        mark(f'D6-M{n:03}',detail,reports)
    mark('D6-M027','Original entry contains only todo; excluded by agreed source scope.',['D/D6/sources/D6.md'],status='EXCLUDED_SCOPE')
    mark('D7-M001','PA2 stage 2: itrace/mtrace/ftrace, ELF function parsing/tail calls/limits, 55 malformed/edge ELF cases with ASAN+UBSAN, ring history, actual NEMU addi mutant vs Spike and 81-test regression.',['reports/D7_trace.json','reports/D7_regression.json'])
    d8={
      1:('SDB single step, register/memory read, reused expression/watch core; three exact commit-boundary watch hits and bad-input checks.',['D8_front']),
      2:('Committed instruction/memory/function traces with Capstone, ELF names, tail calls and bounded logging.',['D8_front','D7_trace']),
      3:('Actual NEMU shared REF APIs tested in both copy directions; per-commit PC/GPR and RAM stores compared; real ADDI RTL mutation rejected.',['D8_reference','D8_front']),
      4:('Actual RVE ABI compilation, AM run/halt; dummy GOOD_TRAP and original wrong BAD_TRAP/make exit 2.',['D8_front']),
      5:('Complete authored single-cycle datapath, state/control/host observation, and textbook comparison explained.',['D8_alu']),
      6:('RV32E core: 1758 boundaries, 73 original programs, 48 native/RVE test runs, 20 train runs, 12 earlier fixtures, klib/timer/FCEUX; no M/CSR claim or inherited SoC/physical qualification.',['D8_reset','D8_isa','D8_official_tests','D8_apps_test','D8_apps_train','D8_prior_tests','D8_timer','D8_extra','D8_fceux_native','D8_fceux_ascii'])}
    for n,(detail,reports) in d8.items():mark(f'D8-M{n:03}',detail,[f'reports/{r}.json' for r in reports])
    # Background is tracked honestly; reading an index is not watching all videos.
    for task in specs['tasks']:
        key=task['id'];stage=key.split('-')[0]
        if key in rows:continue
        if '-R' in key:
            mark(key,'Method reminder reviewed against the implementation and limitations documented in this chapter.',['D/'+stage+'/sources/'+stage+'.md'],status='PASS_METHOD_REVIEW')
        else:
            mark(key,'Source background retained and scoped; no claim of completing every linked video, manual or article.',['D/'+stage+'/sources/'+stage+'.md'],status='REFERENCE_ONLY')
    for key,detail,report in [
      ('D6-O003','Area/fanout tradeoff explained without assuming shared logic always improves timing.','D6_logic'),
      ('D6-O004','Word-to-gate and gate-to-library mapping terminology distinguished.','D6_logic'),
      ('D6-O010','OAI22 naming and truth function independently checked.','D6_pdk'),
      ('D6-O011','AOI221 expression, LIB and MOS network checked.','D6_pdk'),
      ('D6-O012','Actual NAND2X2 widths compared with X1.','D6_pdk'),
      ('D6-O013','DFF CDL graph and 28-MOS count; two-latch phase explanation and model check. Extra raw ideal-MOS transient did not qualify; not SPICE/LVS.','D6_pdk'),
      ('D6-O014','Actual ADDF network and selected basic-gate area/transistor comparison.','D6_pdk'),
      ('D6-O015','TT versus SS/FF/SF/FS conceptual locations explained.','D6_pvt'),
      ('D6-O017','Cooling/PVT reasoning conditional on characterized models; no universal monotonic-temperature claim.','D6_pvt'),
      ('D6-O018','Operating environment and qualification corners distinguished; no unsupported vendor claim adopted.','D6_pvt'),
      ('D8-O001','NEMU chosen as NPC REF; independent Spike used for NEMU.','D8_reference'),
      ('D8-O002','Actual compilation: signed/unsigned add same encoding, SLT/SLTU distinct.','D8_extra'),
      ('D8-O003','Yosys four-bit ALU structures/gates and all 2048 combinations by SAT; wrong carry negative. No physical area claim.','D8_alu'),
      ('D8-O004','Software arithmetic helper path and actual C multiplication/division tests verified without M hardware.','D8_official_tests')]:mark(key,detail,['reports/'+report+'.json'],status='PASS_ANALYSIS')
    mark('D6-O016','Source marketing anecdote lacks verified evidence tying i3/i5/i7 to exact process corners; it is not adopted as a factual premise.',['D/D6/sources/D6.md'],status='SOURCE_CLAIM_NOT_ADOPTED')
    assert set(rows)=={x['id'] for x in specs['tasks']} and len(rows)==103
    ordered=[rows[x['id']] for x in specs['tasks']]
    core=[x for x in specs['tasks'] if x['classification']=='PUBLIC_CORE_TASK'];assert len(core)==55 and all(rows[x['id']]['status'].startswith('PASS') for x in core)
    for row in ordered:
        for evidence in row['evidence']:assert (ROOT/evidence).exists(),evidence
    dump(ROOT/'reports/D_results.json',{'status':'COMPLETE_ENGINEERING_WITH_DECLARED_LIMITS','core_passed':55,'scope_records':103,'records':ordered})
    for stage in [f'D{n}' for n in range(1,9)]:
        selected=[r for r in ordered if r['id'].startswith(stage+'-')]
        required=sum(x['id'].startswith(stage+'-') for x in core)
        audit={'status':'PASS','stage_complete':True,'core_tasks':required,'scope_records':len(selected),'records':selected,'report':f'D/{stage}/NOTES.md','qualification':'Public local engineering requirements only; reference-only background is not claimed completed learning.'}
        if stage=='D6':audit['declared_extra_failure']=data['D6_pdk']['dff_raw_switch_probe']
        dump(ROOT/'reports'/f'{stage}_AUDIT.json',audit)
    dump(ROOT/'reports/D9_AUDIT.json',{'status':'PASS_SCOPE_AUDIT','core_tasks':0,'scope_records':0,'source_status':'Original page only says under construction. No invented assignment.','evidence':'D/D9/SCOPE.md'})
    ledger=json.loads((ROOT/'config/task_status.json').read_text('utf8'));matched=set()
    for task in ledger['tasks']:
        if task['id'] in rows:
            r=rows[task['id']];task.update(status=r['status'],evidence=r['evidence'],result_details=r['details']);matched.add(task['id'])
    assert matched==set(rows)
    ledger.update(current_stage='D',stage_status='COMPLETE_ENGINEERING_WITH_DECLARED_LIMITS',stop_after='D');dump(ROOT/'config/task_status.json',ledger)
    lines=['# D 阶段逐项结果','','范围冻结为 103 条记录，其中 55 项公开核心工程任务。核心全部通过；参考背景、未采信说法和原文 todo 分别显示，不把它们合并为 103 项实验通过。','','| ID | 状态 | 任务与实际结果 | 证据 |','| --- | --- | --- | --- |']
    for spec in specs['tasks']:
        r=rows[spec['id']];text=spec['requirement'].replace('|','／').replace('\n',' ');text=text[:200]+('…' if len(text)>200 else '')
        links='、'.join(f'[{Path(e).name}](../{e})' for e in r['evidence'])
        lines.append(f"| {r['id']} | {r['status']} | {text}<br>{r['details'].replace('|','/')} | {links} |")
    lines += ['','各阶段必答题、推导和限制见链接的 NOTES.md；原始全文保存在固定 sources 目录，表格中的长背景仅为索引。D9 原文建设中，任务数为 0。']
    (ROOT/'reports/D_TASKS.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
    # Correct an output-field label; preserve its original bytes, do not rerun physics.
    path=ROOT/'reports/D6_logic.json';logic=load('D6_logic')
    if 'events' in logic:
        backup=ROOT/'artifacts/D6/logic/report_before_label_correction.json';backup.parent.mkdir(parents=True,exist_ok=True)
        if not backup.exists():shutil.copyfile(path,backup)
        logic['mismatch_examples_stdout']=logic.pop('events');logic['event_model_evidence']='artifacts/D6/logic';dump(path,logic)
    # One-shot diagnostic had hardcoded ended PIDs. Retain it as historical text.
    source=ROOT/'D/D8/diagnose_allocator.py';target=ROOT/'artifacts/D8/allocator_diagnosis/diagnose_allocator.py.txt'
    if source.exists():
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target);assert sha(source)==sha(target);source.unlink()
    print('D_103_RECORDS_RECONCILED',dict(Counter(x['status'] for x in ordered)),flush=True)

if __name__=='__main__':main()
