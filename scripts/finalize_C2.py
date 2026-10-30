from evidence import *

def main():
    checks=['C2_native_io','C2_npc_io','C2_fceux_native','C2_fceux_ascii','C2_nemu_functional','C2_nemu_build','C2_nemu_driver_binding','C2_nemu_host_drivers','C2_nemu_mmio_boundary','C2_nemu_gui','C2_nemu_benchmarks','C2_pa2_compiler','C2_pa2_yemu']
    data={x:json.loads((ROOT/'reports'/f'{x}.json').read_text('utf8')) for x in checks}
    assert all(v['status'].startswith('PASS') for v in data.values())
    assert len(data['C2_nemu_gui']['runs'])==11
    spec=json.loads((ROOT/'C/runtime/nested_scope_review.json').read_text('utf8'))['C2_M008'];records=[]
    details={
    '01':('Real hello MMIO output with Spike comparison and explicit skips.','C2_nemu_functional'),
    '02':('Shared printf/sprintf core inherited unchanged from D, 5007 portable checks rerun on C NEMU.','C2_nemu_functional'),
    '03':('Original generated integer ALU tests return zero; original wrong program returns BAD_TRAP/nonzero. Float cases are disabled by the original generator.','C2_nemu_functional'),
    '04':('High-then-low NEMU RTC snapshot protocol, boundary controls and actual 1/2/3-second timer output.','C2_nemu_gui'),
    '05':('Original 500000 Dhrystone/1000 CoreMark iterations; MicroBench test and full ref. Separate performance binary disables TRACE/WATCHPOINT/DIFFTEST/CC_DEBUG.','C2_nemu_benchmarks'),
    '06':('Named device tracing, eight-record limit, serial inclusion, explicit exclusion and invalid-limit rejection.','C2_nemu_functional'),
    '07':('Keycode/down/up/none driver cases and real J/Left events.','C2_nemu_host_drivers'),
    '08':('Actual width/height and sync; isolated wrapped GPU initialization fb[i]=i agrees at every captured pixel.','C2_nemu_gui'),
    '09':('160 rectangle/crop/stride cases plus actual official video animation, sync and negative controls.','C2_nemu_host_drivers'),
    '10':('Seven application families actually ran, including CC0-ROM LiteNES/FCEUX input-driven color changes. Bounded observations and disabled GUI DiffTest explicitly stated.','C2_nemu_gui'),
    '11':('Full typing-game event path from SDL/queue/MMIO through AM to game state and synchronized framebuffer explained.','C2_nemu_gui'),
    '12-Q01':('Original YEMU trace is seven transitions: M[7]=49; later data execution makes R0=98 and opcode2 halts.','C2_pa2_yemu'),
    '12-Q02':('Fetch/decode/effective address/state update/trace/DiffTest/device sequence explained against real NEMU sources.','C2_nemu_functional'),
    '12-Q03':('Typing-game abstraction layers, data/control paths and debugging separation explained with real interaction.','C2_nemu_gui'),
    '12-Q04':('Actual NEMU static/inline variants; external duplicate definitions and -O0 unresolved inline call rejected.','C2_pa2_compiler'),
    '12-Q05':('Actual symbol count30 versus30; two initialized definitions rejected; isolated headers restored.','C2_pa2_compiler'),
    '12-Q06':('Actual AM build/dry-run dependency plan plus linked hello ELF and runtime proof.','C2_pa2_compiler')}
    for r in spec['records']:
        key=r['id'];suffix=key.removeprefix('PA-2.5-');required=key in spec['required_record_ids']
        if required:
            detail,report=details[suffix];status='PASS';evidence=['C/C2/PA2_NOTES.md','reports/'+report+'.json']
        else:
            status='REFERENCE_ONLY';detail='Original optional/background status retained; no claim of implementing every extension, watching all media, or official submission.';evidence=['C/runtime/nested_scope_review.json','C/C2/PA2_NOTES.md']
            if key in ['PA-2.5-AUX14','PA-2.5-AUX20','PA-2.5-AUX21']:
                status='PASS_BOUNDED_OBSERVATION';detail='Required application demonstrations also cover this optional viewing task within the documented bounded session.';evidence+=['reports/C2_nemu_gui.json']
        records.append({'id':key,'status':status,'requirement':r['requirement'],'details':detail,'evidence':evidence})
    dump(ROOT/'reports/C2_pa2_results.json',{'status':'PASS_REQUIRED_SCOPE','required_passed':17,'scope_records':48,'records':records,'personal_submission':'Excluded; no student identity or make submit.'})
    results=json.loads((ROOT/'reports/C_results.json').read_text('utf8'));mapping={r['id']:r for r in results['records']}
    mapping['C2-M008']={'id':'C2-M008','status':'PASS','details':'All17 nested PA2.5 required items accepted, including real NEMU IOE, complete app families, ref performance and six report questions.','evidence':['reports/C2_pa2_results.json','C/C2/PA2_NOTES.md','C/C2/snapshot/manifest.json']}
    for key in ('C2-O001','C2-O002'):
        mapping[key]={'id':key,'status':'REFERENCE_ONLY','details':'Original optional/background scope retained. Screensaver is an IO exercise; no physical screen-protection claim or independently submitted new game.','evidence':['C/C2/NOTES.md','C/C2/sources/C2.md']}
    for key,report,detail in [('C5-M001','C5_source_lock','Compatible official full SoC pinned at bcdcbc3e8d97a11c07d3007e14f33c6147c02a8e; archived incompatible2607 retained.'),('C5-M002','C5_generation','Actual make dev-init and Mill/Chisel/firtool make verilog,39 modules, real invalid-Scala negative and source restoration.')]:
        obj=json.loads((ROOT/'reports'/f'{report}.json').read_text('utf8'));assert obj['status'].startswith('PASS')
        mapping[key]={'id':key,'status':'PASS','details':detail,'evidence':['reports/'+report+'.json']}
    rows=[r for k,r in mapping.items() if k.startswith('C2-')];assert len(rows)==13 and all(mapping[f'C2-M{i:03}']['status']=='PASS' for i in range(1,12))
    dump(ROOT/'reports/C2_AUDIT.json',{'status':'PASS','stage_complete':True,'core_tasks':11,'scope_records':13,'nested_required':17,'records':rows,'checks':{k:sha(ROOT/'reports'/f'{k}.json') for k in checks},'snapshot':json.loads((ROOT/'C/C2/snapshot/manifest.json').read_text('utf8')),'limits':['GUI runs disable ISA DiffTest for speed; separate feature program checks compare against Spike.','NEMU sound optional and unimplemented; native PCM test is separate.','CoreMark run is not an official certified score; coarse timer and host/WSL scope.','CC0 ROMs selected through separate build manifests.','Some earliest failed GUI sessions kept outer traceback/input snapshots but partial screenshots were overwritten before session archival was fixed; final successful images are retained.']})
    dump(ROOT/'reports/C_results.json',{'status':'IN_PROGRESS','records':list(mapping.values())})
    ledger=json.loads((ROOT/'config/task_status.json').read_text('utf8'))
    for r in ledger['tasks']:
        if r['id'] in mapping:
            item=mapping[r['id']];r.update(status=item['status'],evidence=item['evidence'],result_details=item['details'])
    ledger.update(current_stage='C4',stage_status='IN_PROGRESS',stop_after='C');dump(ROOT/'config/task_status.json',ledger)
    print('C2_COMPLETE_REQUIRED17_TOP11; C5_SOURCE_GENERATION_ACCEPTED',flush=True)

if __name__=='__main__':main()
