"""Rebuild original MicroBench and compare single-cycle and bus-based C DUTs."""
from pathlib import Path
import sys, argparse, re
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'runtime'))
from common import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', choices=['test', 'train'], default='test')
    parser.add_argument('--variants', default='single,axi')
    args = parser.parse_args()
    base = WORK / 'c4/workbench'; app = base / 'microbench'; am = base / 'abstract-machine'
    env = {'AM_HOME': str(am), 'NPC_HOME': str(base / 'npc')}
    ref = WORK / 'nemu-ref/build/riscv32-nemu-interpreter-so'
    variants = {'single': ('riscv32e-npc', BENCH / 'npc/build/sim'),
                'axi': ('riscv32e-npc', WORK / 'c4/build/mode5/sim'),
                'soc': ('riscv32e-c4', WORK / 'c4/build/mode6/sim')}
    source = [p for folder in [app, am] for p in sorted(folder.rglob('*'))
              if p.is_file() and 'build' not in p.relative_to(folder).parts and '.git' not in p.relative_to(folder).parts]
    report = ROOT / 'reports/C4_performance.json'
    rows = json.loads(report.read_text()).get('runs', []) if report.exists() else []
    for name in args.variants.split(','):
        arch, exe = variants[name]
        binary = app / 'build' / ('microbench-' + arch + '.bin')
        elf = binary.with_suffix('.elf')
        tag = 'C4/performance/' + name + '-' + args.size
        run(tag + '/build', ['make', '-j1', 'ARCH=' + arch, 'mainargs=' + args.size, 'insert-arg'],
            cwd=app, env=env, inputs=source, outputs=[binary, elf], timeout=300)
        out = ROOT / 'artifacts' / tag; out.mkdir(parents=True, exist_ok=True)
        sim_report = out / 'simulation.json'
        # Original benchmark validation remains active; DiffTest is on for the pilot.
        options = ['--ref', ref] if args.size == 'test' else ['--no-diff']
        text, error, evidence = run(tag + '/run', [exe, '--image', binary, '--elf', elf,
            '--report', sim_report, '--frequency', '100000000', '--max-cycles', '20000000000', *options],
            inputs=[exe, ref, binary, elf], outputs=[sim_report], timeout=3600)
        data = json.loads(sim_report.read_text())
        assert data['result'] == 'GOOD_TRAP' and data['a0'] == 0 and data['ebreak_calls'] == 1
        assert text.count(' Passed.') == 10 and 'MicroBench PASS' in text and 'Ignored' not in text and 'Failed.' not in text
        if args.size == 'test':
            assert data['diff_enabled'] and data['diff_checked'] + data['device_sync_checked'] == data['instructions']
        else:
            assert not data['diff_enabled']
        row = {'variant': name, 'size': args.size, 'status': 'PASS', 'simulation': data,
               'execution_cycles_excluding_post_halt_checks': data['cycles']-4, 'binary_sha256': sha(binary), 'elf_sha256': sha(elf), 'executable_sha256': sha(exe),
               'evidence': tag, 'benchmark_checks': '10 original validators, no skipped programs or modified workloads',
               'timing_lines': [line for line in text.splitlines() if 'time:' in line or 'time :' in line],
               'wall_elapsed_with_launch_seconds': evidence['elapsed_seconds']}
        rows = [r for r in rows if (r['variant'], r['size']) != (name, args.size)] + [row]
        dump(report, {'status': 'PASS_COMPLETED_RUNS', 'runs': rows,
             'scope': 'Single is the retained C-only rebuild of the D single-cycle core; AXI is mode5 CPU+adapters+arbiter with external DPI-backed memory/devices. Mode6 separately uses RTL UART/CLINT. All models have128MiB simulated RAM. The2x256x32 synthesis baseline is a structural timing exercise, not enough RAM to run MicroBench. Test uses NEMU DiffTest; train disables DiffTest and tracing but keeps original benchmark validators and bus monitors.'})
        print('C4_MICROBENCH_PASS', name, args.size, data['cycles'], data['wall_seconds'], flush=True)


if __name__ == '__main__':
    main()
