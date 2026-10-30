from evidence import *


def main():
    names = ['C4_front', 'C4_regression', 'C4_negative_sdb', 'C4_cpu_cycles', 'C4_rtl_units',
             'C4_fabric', 'C4_performance', 'C4_clock_calibration', 'C4_mapped_timing', 'C4_nangate']
    reports = {name: json.loads((ROOT / 'reports' / (name + '.json')).read_text('utf-8')) for name in names}
    assert all(r['status'].startswith('PASS') for r in reports.values())
    regression = reports['C4_regression']
    assert len(regression['runs']) == 444 and regression['modes'] == [1, 2, 3, 4, 5, 6]
    assert all(sum(x['mode'] == mode for x in regression['runs']) == 74 for mode in range(1, 7))
    assert len(reports['C4_front']['runs']) == 25
    assert len(reports['C4_fabric']['rows']) == 6
    assert reports['C4_clock_calibration']['runs'][-1]['name'] == 'default-driver'
    assert .75 <= reports['C4_clock_calibration']['wall_to_AM_ratio'] <= 1.25
    performance = reports['C4_performance']['runs']
    assert {(r['variant'], r['size']) for r in performance} >= {('single','test'),('single','train'),('axi','test'),('axi','train')}
    timing = {r['name']: r for r in reports['C4_nangate']['variants']}
    assert set(timing) == {'single', 'axi'}
    assert timing['single']['memory_DFF_origins'] == {'imem': 8192, 'dmem': 8192}
    assert all(r['frequency_estimate_qualified'] is False for r in timing.values())
    details = {
        1: ('Real train cycles and two256x32 flop-memory synthesis. Separate fixed Nangate45 mapping/STA analyzed; transition violations explicitly prevent a qualified frequency claim.', ['C4_performance','C4_nangate']),
        2: ('One-cycle IFU backend, two clocks per instruction, four-state cycle controls and full program regressions.', ['C4_cpu_cycles','C4_front','C4_regression']),
        3: ('Synchronous LSU, two ordinary/three memory cycles, stable state while waiting and independent memory/ISA checks.', ['C4_cpu_cycles','C4_regression']),
        4: ('VALID request/response ownership and independent transaction counts; no retirement before completion.', ['C4_front','C4_regression']),
        5: ('Fixed5/10/20 latency plus recorded LFSR seeds and independent request delay controls.', ['C4_front','C4_regression']),
        6: ('READY/VALID payload stability under request and response backpressure; waveform and actual failure controls.', ['C4_front','C4_fabric','C4_regression']),
        7: ('Arm IHI0022H A3 handshake/dependency rules checked; Xbar READY dependency fixed with registered AR buffering and dedicated rejecting mutant.', ['C4_fabric']),
        8: ('Five-channel Lite adapters, independent AW/W, stalled responses, read-only IFU; RT-Thread is a separate prerequisite-dependent C5 integration.', ['C4_regression','C4_rtl_units','C4_fabric']),
        9: ('Owner locked to response completion;64 contended grants in sustained two-master demand, wrong-route/data/fixed-priority mutants rejected.', ['C4_fabric']),
        10: ('CPU+adapters+arbiter synthesis and complete train cycles; external DPI RAM excluded from area. Explicit IO STA and unqualified Nangate transition results retained.', ['C4_performance','C4_nangate','C4_mapped_timing']),
        11: ('RTL UART prints exactly once per accepted strobed write; Xbar boundaries, errors, reset and concurrent AR/AW/W tested.', ['C4_rtl_units','C4_fabric','C4_regression']),
        12: ('RTL64-bit mtime low-read high-latch rollover tested; actual AM conversion, measured calibration and default-driver1/2/3-second output.', ['C4_rtl_units','C4_clock_calibration']),
    }
    results = json.loads((ROOT / 'reports/C_results.json').read_text('utf-8'))
    mapping = {r['id']: r for r in results['records']}
    scope = [r for r in json.loads((ROOT / 'C/runtime/course_specs.json').read_text('utf-8'))['tasks'] if r['id'].startswith('C4-')]
    rows = []
    for task in scope:
        key = task['id']
        if key.startswith('C4-M'):
            detail, checks = details[int(key[-3:])]
            status = 'PASS_EVALUATION_WITH_DECLARED_LIMITS' if key in ['C4-M001','C4-M010'] else 'PASS'
            evidence = ['C/C4/NOTES.md'] + ['reports/' + name + '.json' for name in checks]
        elif key in ['C4-O005', 'C4-O008']:
            status = 'PASS'
            detail = 'Commit-only DiffTest or executable-region protection implemented and independently exercised; finite scope documented.'
            evidence = ['C/C4/NOTES.md', 'reports/C4_regression.json', 'reports/C4_fabric.json']
        else:
            status = 'REFERENCE_ONLY'
            detail = 'Original optional/background/method status retained; notes explain design choices, no claim of separate optional IDU or physical SRAM collision experiment.'
            evidence = ['C/C4/NOTES.md', 'C/C4/sources/C4.md']
        row = {'id': key, 'status': status, 'details': detail, 'evidence': evidence}
        rows.append(row); mapping[key] = row
    assert len(rows) == 24 and sum(r['id'].startswith('C4-M') for r in rows) == 12
    dump(ROOT / 'reports/C4_AUDIT.json', {'status': 'PASS_REQUIRED_ENGINEERING_WITH_DECLARED_LIMITS',
         'stage_complete': True, 'scope_records': len(rows), 'core_tasks': 12, 'records': rows,
         'checks': {name: sha(ROOT / 'reports' / (name + '.json')) for name in names},
         'rtl': [{'path': str(p.relative_to(ROOT)), 'sha256': sha(p)} for p in sorted((ROOT / 'C/C4/rtl').glob('*.sv'))],
         'limits': ['Finite functional simulation, not arbitrary-input or unbounded proof.',
                    'Icarus fabric attempt TIMEOUT retained; successful fabric tests are timed Verilator. Stage1/2 CPU and device tests are separate four-state Icarus evidence.',
                    'Nangate45 default-ABC baseline has max-transition violations; no qualified maximum frequency or reliable performance speedup claim. Assessment task completed with the failures reported.',
                    'Nangate45/OpenSTA is a declared alternative flow, not a claim of exact legacy yosys-sta/iSTA/DELAY4 reproduction.',
                    'Single2KiB synthesized memories cannot hold train; cycles measured in128MiB simulator. External DPI memory excluded from AXI CPU area.',
                    'Train disables DiffTest/trace, keeping original validators; test scale and ISA regressions use independent NEMU.',
                    'CLINT wall calibration depends on host load and workload; no physical clock measurement.',
                    'C5 full-SoC/RT-Thread and all B work are not covered.']})
    dump(ROOT / 'reports/C_results.json', {'status': 'IN_PROGRESS', 'records': list(mapping.values())})
    ledger = json.loads((ROOT / 'config/task_status.json').read_text('utf-8'))
    for task in ledger['tasks']:
        if task['id'] in mapping:
            row = mapping[task['id']]
            task.update(status=row['status'], evidence=row['evidence'], result_details=row['details'])
    ledger.update(current_stage='C5', stage_status='IN_PROGRESS', stop_after='C')
    dump(ROOT / 'config/task_status.json', ledger)
    print('C4_COMPLETE_12_CORE_WITH_DECLARED_TIMING_LIMITS; C5_IN_PROGRESS')


if __name__ == '__main__':
    main()
