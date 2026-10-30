"""Replay selected accepted binaries after extracting them from the final C tar.

No compiler, download or source-workbench binary is used by the replayed DUTs.
The installed Linux loader/libraries and the existing budget recorder are reused.
"""
from pathlib import Path, PurePosixPath
import sys, tarfile
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import *


CASES = {
    'microbench': 'C5/sdram-apps/microbench-32x1',
    'rtthread': 'C5/rtthread/sdram32',
    'chiplink': 'C5/chiplink/positive',
    'chiplink-bad-read': 'C5/chiplink/bad-read',
}


def main():
    frozen = json.loads((ROOT/'reports/C_runtime_export.json').read_text())
    archive = ROOT/frozen['archive']
    assert sha(archive) == frozen['sha256']
    members = {r['path']: r for r in frozen['members']}
    by_source = {r['source']: r for r in frozen['members'] if r['kind'] == 'file'}
    selected = set()
    originals = {}
    for case, evidence in CASES.items():
        original = json.loads((ROOT/'artifacts'/evidence/'run/run.json').read_text())
        command = original['command'][original['command'].index('--')+1:]
        for index, arg in enumerate(command):
            if index and command[index-1] == '--report':
                continue
            if str(arg).startswith('/'):
                assert arg in by_source, ('Replay would use an external runtime input', arg)
                selected.add(by_source[arg]['path'])
        originals[case] = (original, command)
    destination = WORK/'offline-replay'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f')
    destination.mkdir(parents=True, exist_ok=False)
    seen = set()
    with tarfile.open(archive, 'r|gz') as tar:
        for item in tar:
            name = PurePosixPath(item.name)
            assert not name.is_absolute() and '..' not in name.parts and '\\' not in item.name
            if item.name not in selected:
                continue
            assert item.isfile() and item.name not in seen
            seen.add(item.name)
            target = destination/item.name
            target.parent.mkdir(parents=True, exist_ok=True)
            with tar.extractfile(item) as source, target.open('xb') as output:
                shutil.copyfileobj(source, output, 1048576)
            target.chmod(item.mode & 0o777)
            assert sha(target) == members[item.name]['sha256']
    assert seen == selected
    rows = []
    for case, evidence in CASES.items():
        original, command = originals[case]
        folder = ROOT/'artifacts/C/offline-replay'/case
        folder.mkdir(parents=True, exist_ok=True)
        inputs = []
        for index, arg in enumerate(command):
            if index and command[index-1] == '--report':
                command[index] = str(folder/'simulation.json')
            elif arg in by_source:
                command[index] = str(destination/by_source[arg]['path'])
                inputs.append(Path(command[index]))
        # Every replayed executable/firmware/reference input must be extracted.
        assert all(p.is_relative_to(destination) for p in inputs)
        o, e, run_record = run('C/offline-replay/'+case+'/run',
            ['python3', ROOT/'C/runtime/budget_exec.py', '--report', folder/'resources.json', '--', *command],
            inputs=inputs, outputs=[folder/'simulation.json', folder/'resources.json'],
            cwd=destination, timeout=240, expected=tuple(original['expected_exit']))
        current = json.loads((folder/'simulation.json').read_text())
        prior = json.loads((ROOT/'artifacts'/evidence/'simulation.json').read_text())
        fields = ['result', 'exit_code', 'cycles', 'instructions', 'diff_checked', 'device_sync_checked', 'gpr', 'coverage', 'uart']
        compared = [key for key in fields if key in prior]
        assert all(current[key] == prior[key] for key in compared), (case, 'replay differs')
        assert current['diff_checked'] + current['device_sync_checked'] == current['instructions']
        rows.append({'case': case, 'status': 'PASS', 'result': current['result'],
            'cycles': current['cycles'], 'instructions': current['instructions'],
            'compared_fields': compared, 'original_evidence': 'artifacts/'+evidence,
            'evidence': folder.relative_to(ROOT).as_posix(),
            'inputs': [{'member': str(p.relative_to(destination)), 'sha256': sha(p)} for p in inputs],
            'run_sha256': sha(folder/'run/run.json')})
    assert rows[-1]['result'] == 'DIFF_FAIL'
    dump(ROOT/'reports/C_offline_replay.json', {'status': 'PASS', 'archive_sha256': frozen['sha256'],
        'extraction_directory': str(destination), 'extracted_members': sorted(selected), 'runs': rows,
        'scope': 'Actual execution of extracted C5 simulator/reference/firmware files. MicroBench test, scripted RT-Thread and ChipLink positive/negative reproduce their accepted results and deterministic counters. Installed Linux system libraries are reused. This is selected binary replay, not a clean-machine source rebuild or a repeat of the multi-hour memory sweeps.'})
    print('C_OFFLINE_REPLAY_PASS', len(rows), flush=True)


if __name__ == '__main__':
    main()
