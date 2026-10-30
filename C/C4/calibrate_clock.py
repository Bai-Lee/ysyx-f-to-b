"""Calibrate AM's RTL mtime tick rate against this simulator's measured wall rate."""
from pathlib import Path
import sys, re
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'runtime'))
from common import *


def main():
    subprocess.run(['python3',str(ROOT/'C/C4/prepare_apps.py')],check=True)
    base = WORK / 'c4/workbench'; am = base / 'abstract-machine'; app = base / 'clock-probe'
    env = {'AM_HOME': str(am), 'NPC_HOME': str(base / 'npc')}
    exe = WORK / 'c4/build/mode6/sim'; image = app / 'build/clock-probe-riscv32e-c4.bin'; elf = image.with_suffix('.elf')
    ref = WORK / 'nemu-ref/build/riscv32-nemu-interpreter-so'
    rows = []
    hz = 1000000
    for name in ['pilot', 'calibrated', 'default-driver']:
        if name=='default-driver':
            hz=rows[-1]['configured_tick_hz']
            dump(ROOT/'C/C4/clock_config.json',{'ticks_hz':hz,'source':'reports/C4_clock_calibration.json','mode':'calibrated host simulation with NEMU DiffTest; override for frequency-model benchmarks'})
            subprocess.run(['python3',str(ROOT/'C/C4/prepare_apps.py')],check=True)
        tag = 'C4/clock/' + name
        run(tag + '/build', ['make', '-j1', 'ARCH=riscv32e-c4', 'mainargs=' + ('' if name=='default-driver' else str(hz)), 'insert-arg'], cwd=app, env=env,
            inputs=[app / 'main.c', am / 'am/src/riscv/npc/timer.c',am/'scripts/riscv32e-c4.mk'], outputs=[image, elf], timeout=120)
        report = ROOT / 'artifacts' / tag / 'simulation.json'; report.parent.mkdir(parents=True, exist_ok=True)
        text, err, _ = run(tag + '/run', [exe, '--image', image, '--elf', elf, '--ref', ref, '--report', report, '--max-cycles', '300000000'],
            inputs=[exe, image, elf, ref], outputs=[report], timeout=120)
        result = json.loads(report.read_text()); assert result['result'] == 'GOOD_TRAP' and result['diff_enabled']
        assert re.findall(r'C4_CLOCK (\d+)', text) == ['1', '2', '3']
        assert result['diff_checked'] + result['device_sync_checked'] == result['instructions']
        rate = result['cycles'] / result['wall_seconds']
        rows.append({'name': name, 'configured_tick_hz': hz, 'measured_simulation_cycles_per_wall_second': rate,
                     'AM_elapsed_seconds': 3, 'wall_elapsed_seconds': result['wall_seconds'], 'simulation': result,
                     'image_sha256': sha(image), 'evidence': tag})
        hz = max(1, round(rate))
    ratio = rows[-1]['wall_elapsed_seconds'] / 3
    assert .75 <= ratio <= 1.25, ratio
    dump(ROOT / 'reports/C4_clock_calibration.json', {'status': 'PASS_BOUNDED_WALL_CALIBRATION', 'runs': rows,
         'wall_to_AM_ratio': ratio, 'acceptance': 'Three1-second AM waits complete within25percent of3wall seconds on this host run.',
         'scope': 'Actual RTL mtime increments each CPU clock; C AM reads low then latched high. The calibrated coefficient is this host simulation throughput with NEMU DiffTest, not silicon frequency. Host load and workload change throughput; performance experiments separately use100MHz modeled time.'})
    print('C4_CLOCK_CALIBRATED', rows[-1]['configured_tick_hz'], ratio, flush=True)


if __name__ == '__main__':
    main()
