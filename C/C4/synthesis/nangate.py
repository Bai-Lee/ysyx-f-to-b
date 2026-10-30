"""Separate educational Nangate45 architecture assessment; no library benchmarking."""
from pathlib import Path
import sys, argparse, re
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'runtime'))
from common import *
from resource_policy import POLICY_PATH


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--only', choices=['single', 'axi'])
    args = parser.parse_args()
    source = Path('/workspace/downloads/ysyx_c_stage/nangate45')
    lock = json.loads((ROOT / 'reports/C4_nangate_library.json').read_text())
    lib = source / 'NangateOpenCellLibrary_typical.lib'
    license_file = source / 'OpenCellLibraryLicenseSi2.txt'
    assert sha(lib) == lock['local_sha256'] and license_file.stat().st_size > 1000
    output = ROOT / 'C/C4/synthesis/nangate'; output.mkdir(exist_ok=True)
    model = ROOT / 'C/C4/models/nangate45'; model.mkdir(parents=True, exist_ok=True)
    for p in [lib, license_file]:
        shutil.copyfile(p, model / p.name)
    lib = model / lib.name
    suite = Path('/home/USER/tools/e-stage/oss-20260821/oss-cad-suite')
    yosys = suite / 'bin/yosys'; sta = Path(json.loads((ROOT / 'reports/C4_opensta_toolchain.json').read_text())['binary'])
    guard = ROOT / 'C/runtime/budget_exec.py'
    env = {'PATH': str(suite / 'bin') + ':' + os.environ['PATH'], 'OMP_NUM_THREADS': '1'}
    rows = []
    # Small actual read/link/timing positive and negative controls for this new library.
    control = output / 'control.v'
    control.write_text('module control(input clock,a,output y);wire q;DFF_X1 ff(.CK(clock),.D(a),.Q(q));INV_X1 inv(.A(q),.ZN(y));endmodule\n')
    for name, period in [('positive', 10), ('negative', .001)]:
        script = output / ('control-' + name + '.tcl')
        script.write_text('read_liberty {' + str(lib) + '}\nread_verilog {' + str(control) + '}\nlink_design control\ncreate_clock -name clk -period ' + str(period) + ' [get_ports clock]\nset_input_delay -clock clk 1 [get_ports a]\nset_output_delay -clock clk 1 [get_ports y]\nreport_worst_slack -digits 6\nputs "NANGATE_CONTROL_DONE"\nexit\n')
        text, err, _ = run('C4/nangate/control-' + name, [sta, '-exit', script], inputs=[sta, lib, control, script], timeout=30)
        assert 'Error:' not in text + err and 'NANGATE_CONTROL_DONE' in text
        slack = float(re.search(r'worst slack\s+(-?[\d.]+)', text)[1])
        assert (slack >= 0) == (name == 'positive'), (name, slack)
        rows.append({'control': name, 'slack_ns': slack, 'status': 'PASS' if name == 'positive' else 'PASS_VIOLATION_DETECTED'})
    controls = rows; rows = []
    rtl = ROOT / 'C/C4/rtl'
    for name, top, files in [('single', 'single_with_memories', [rtl / 'rv32e_execute.sv', ROOT / 'C/C4/synthesis/single_with_memories.sv']),
                             ('axi', 'c4_axi_core', sorted(rtl.glob('*.sv')))]:
        if args.only and args.only != name:
            continue
        out = output / name; out.mkdir(exist_ok=True)
        mapped = out / 'mapped.v'; structure = out / 'mapped.json'; statistics = out / 'stat.json'
        script = out / 'synthesis.ys'
        script.write_text('read_liberty -lib ' + str(lib) + '\nread_verilog -sv ' + ' '.join(map(str, files)) + '\nsynth -top ' + top + ' -flatten\n'
            + 'dfflibmap -liberty ' + str(lib) + '\nabc -liberty ' + str(lib) + ' -D 10000\nclean\ncheck -assert\n'
            + 'tee -o ' + str(statistics) + ' stat -liberty ' + str(lib) + ' -json\nwrite_verilog -noattr -noexpr ' + str(mapped)
            + '\nwrite_json ' + str(structure) + '\n')
        budget = ROOT / 'artifacts/C4/nangate' / name / 'budget.json'
        run('C4/nangate/' + name, ['python3', guard, '--report', budget, '--', 'taskset', '-c', '0,1', yosys, '-s', script],
            inputs=[POLICY_PATH, guard, yosys, lib, script, *files], outputs=[mapped, structure, statistics], env=env, timeout=1800, resume=True)
        stats = json.loads(statistics.read_text())['modules']['\\' + top]
        module = json.loads(structure.read_text())['modules'][top]
        metadata = [c for c in module['cells'].values() if c['type'] == '$scopeinfo']
        assert all(not c['connections'] and not c['port_directions'] for c in metadata)
        logic_cells = [c for c in module['cells'].values() if c['type'] != '$scopeinfo']
        assert not module.get('memories') and all(not c['type'].startswith('$') for c in logic_cells)
        flops = [cell for cell in module['cells'].values() if cell['type'].startswith('DFF')]
        origins = {}
        if name == 'single':
            qbits = {bit for c in flops for bit in c['connections'].get('Q', [])}
            for kind in ['imem', 'dmem']:
                bits = {bit for net, info in module['netnames'].items() if net.startswith(kind + '[') for bit in info['bits']}
                origins[kind] = len(bits & qbits)
            assert origins == {'imem': 8192, 'dmem': 8192}, origins
        # Old portable OpenSTA cannot parse concatenated assignment LHS. Re-export
        # the exact mapped JSON with Yosys's documented syntax option; no remapping.
        sta_netlist = out / 'sta-netlist.v'; export = out / 'export.ys'
        export.write_text('read_json ' + str(structure) + '\nwrite_verilog -noattr -noexpr -simple-lhs ' + str(sta_netlist) + '\n')
        run('C4/nangate/' + name + '-export', [yosys, '-s', export], inputs=[yosys, structure, export],
            outputs=[sta_netlist], env=env, timeout=120, resume=True)
        sdc = out / 'model.sdc'; sdc.write_text('set_units -time ns -capacitance pF\n'+(ROOT / 'C/C4/synthesis' / name / 'model.sdc').read_text())
        analysis = out / 'analysis.tcl'
        analysis.write_text('read_liberty {' + str(lib) + '}\nread_verilog {' + str(sta_netlist) + '}\nlink_design ' + top + '\nread_sdc {' + str(sdc) + '}\ncheck_setup -verbose\nreport_checks -path_delay max -group_count 1 -digits 6\nreport_worst_slack -digits 6\nputs "HOLD_BEGIN"\nreport_checks -path_delay min -group_count 1 -digits 6\nputs "TRANSITION_BEGIN"\nreport_check_types -max_transition -all_violators -no_line_splits -digits 6\nputs "NANGATE_STA_DONE"\nexit\n')
        sta_budget = ROOT / 'artifacts/C4/nangate' / (name + '-sta') / 'budget.json'
        text, err, _ = run('C4/nangate/' + name + '-sta', ['python3', guard, '--report', sta_budget, '--', sta, '-exit', analysis],
            inputs=[POLICY_PATH, guard, sta, lib, sta_netlist, sdc, analysis], timeout=600)
        assert 'Error:' not in text + err and 'NANGATE_STA_DONE' in text
        setup = float(re.search(r'worst slack\s+(-?[\d.]+)', text)[1])
        hold = float(re.search(r'(-?[\d.]+)\s+slack\s+\((?:MET|VIOLATED)\)', text.split('HOLD_BEGIN', 1)[1])[1])
        assert 10 - setup > 0
        transition_violations=text.split('TRANSITION_BEGIN',1)[1].count('(VIOLATED)')
        (out / 'analysis.txt').write_text(text + err)
        row = {'name': name, 'status': 'PASS_MAPPING_AND_TIMING_ANALYSIS', 'cell_area_um2': stats['area'],
               'cell_count': stats['num_cells'], 'nonfunctional_scope_metadata_cells': len(metadata),
               'DFF_count': len(flops), 'memory_DFF_origins': origins,
               'setup_wns_ns': setup, 'hold_min_slack_ns': hold, 'constraint_mhz': 100,
               'setup_and_hold_met_at_100MHz': setup >= 0 and hold >= 0, 'timing_met_at_100MHz':setup >= 0 and hold >= 0 and transition_violations==0, 'max_transition_violations':transition_violations, 'frequency_estimate_qualified':False, 'setup_frequency_estimate_mhz': 1000 / (10 - setup),
               'netlist_sha256': sha(sta_netlist), 'mapped_json_sha256': sha(structure),
               'sdc_sha256': sha(sdc), 'evidence': 'artifacts/C4/nangate/' + name,
               'mapping_budget': json.loads(budget.read_text()), 'sta_budget': json.loads(sta_budget.read_text())}
        rows.append(row)
        dump(ROOT / 'reports/C4_nangate.json', {'status': 'PASS_COMPLETED_VARIANTS', 'library': lock, 'controls': controls,
             'variants': rows, 'scope': 'Educational comparison of two DUT architectures within this fixed Nangate45 library; no benchmark against other standard-cell libraries. Yosys default ABC mapping at10ns, independent OpenSTA with explicit IO delays, ideal clock, no routed parasitics. Setup frequency is algebraic only; any max-transition violation indicates the unbuffered mapping is outside transition limits. It is not a qualified clock or physical signoff. Single includes two real256x32 flop memories; larger simulated RAM only used for program cycles.'})
        print('C4_NANGATE_PASS', name, stats['area'], setup, hold, flush=True)


if __name__ == '__main__':
    main()
