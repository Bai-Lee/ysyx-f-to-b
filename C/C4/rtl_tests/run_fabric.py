from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'runtime'))
from common import *
OUT = WORK / 'c4-fabric'; OUT.mkdir(exist_ok=True)


def compile_run(name, sources, expected=0, marker=None, top='fabric_tb'):
    build = OUT / name; build.mkdir(exist_ok=True)
    exe = build / 'sim'
    run('C4/fabric/' + name + '/build', [VERILATOR, '--binary', '--timing', '--trace', '--assert',
        '-j', '1', '-Wno-fatal', '--top-module', top, '--Mdir', build, '-o', 'sim', *sources],
        inputs=sources, outputs=[exe], timeout=180)
    wave = ROOT / 'C/C4/results' / (name + '.vcd')
    options = ['+VCD=' + str(wave)] if expected == 0 and top=='fabric_tb' else []
    out, err, row = run('C4/fabric/' + name + '/run', [exe, *options], inputs=[exe],
                        outputs=[wave] if options else [], expected=(expected,), timeout=30)
    assert marker in out + err, (name, out, err)
    return {'name': name, 'status': 'PASS', 'run': row, 'stdout': out, 'stderr': err}


def main():
    rtl = ROOT / 'C/C4/rtl'; tb = ROOT / 'C/C4/rtl_tests/fabric_tb.sv'
    arb = rtl / 'axil_arbiter2.sv'; xbar = rtl / 'axil_xbar3.sv'
    rows = [compile_run('fabric', [arb, xbar, tb], marker='FABRIC_PASS')]
    mutants = [('wrong-read-data', arb, 's0_rdata=m_rdata;', 's0_rdata=m_rdata^32\'b1;', 'READ_RESPONSE'),
               ('wrong-uart-route', xbar, "decode=1;", "decode=2;", 'XBAR_READ_TARGET'),
               ('fixed-priority', arb, 'want0&&want1?turn:want1', "want0&&want1?1'b0:want1", 'ROUND_ROBIN_STARVATION')]
    for name, original, old, new, marker in mutants:
        source = original.read_text(); assert old in source
        bad = OUT / (name + '.sv'); bad.write_text(source.replace(old, new))
        files = [bad if p == original else p for p in [arb, xbar, tb]]
        rows.append(compile_run('fabric-' + name, files, expected=1, marker=marker))
    overlap = tb.parent / 'xbar_overlap_tb.sv'
    rows.append(compile_run('overlap', [xbar, overlap], marker='XBAR_OVERLAP_PASS', top='xbar_overlap_tb'))
    text = xbar.read_text(); assert 's_arready=!ar_have;' in text
    bad = OUT / 'ready-dependency.sv'; bad.write_text(text.replace('s_arready=!ar_have;', 's_arready=!ar_have&&!s_awvalid&&!s_wvalid;'))
    rows.append(compile_run('overlap-ready-mutant', [bad, overlap], expected=1, marker='COMBINATIONAL_VALID_TO_READY', top='xbar_overlap_tb'))
    dump(ROOT / 'reports/C4_fabric.json', {'status': 'PASS_INDEPENDENT_CONTENTION_RESET_AND_MUTANTS',
         'rows': rows, 'sources': [{'path': str(p.relative_to(ROOT)), 'sha256': sha(p)} for p in [arb, xbar, tb, overlap]],
         'scope': 'Verilator timed simulation of two independently driven masters,48 mixed transactions and32 continuously queued reads each, bounded service and contended round-robin ownership; independent fake endpoint signatures, all3 targets, DECERR/SLVERR/execute protection, address boundaries,16WSTRB masks, AW-first/W-first/simultaneous launches, stalled AR/AW/W/R/B payload checks, reset after partial AW and while R is pending. Finite simulation, not unrestricted protocol or four-state proof. Original Icarus attempt timed out at cycle11 with a delta-event scheduling loop; retained under artifacts/C4/rtl_unit/fabric, not counted as a pass.'})
    print('C4_FABRIC_PASS', flush=True)


if __name__ == '__main__':
    main()
