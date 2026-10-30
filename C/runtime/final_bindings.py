"""Bind final C sources and Linux binaries to their accepted builds and freeze."""
from pathlib import Path
import sys
import argparse,re
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import *


def read(name):
    return json.loads((ROOT/'reports'/f'{name}.json').read_text())


def local(value):
    text = str(value).replace('\\', '/')
    if len(text) > 2 and text[1] == ':':
        return Path('/mnt/'+text[0].lower()+text[2:])
    return Path(text) if text.startswith('/') else ROOT/text


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--live-preview',action='store_true');args=parser.parse_args()
    if args.live_preview:
        from export_final import inventory
        frozen={'sha256':None,'members':[{'path':destination,'source':str(path),'kind':'file','role':role,'sha256':sha(path)} for path,destination,role in inventory() if not path.is_symlink()]}
    else:
        frozen = read('C_runtime_export')
    output=ROOT/'temp/C-binding-preview' if args.live_preview else ROOT/'reports'
    runtime = {r['source']: r for r in frozen['members'] if r['kind'] == 'file'}
    binaries = []
    for report in ['C4_sim_build', 'C5_soc_build']:
        for row in read(report)['variants']:
            source = row['executable']; current = sha(source)
            assert current == row['sha256'] == runtime[source]['sha256'], source
            binaries.append({'report': report, 'source': source, 'member': runtime[source]['path'], 'sha256': current})
    reference = read('C5_reference_build')
    source = reference['binary']
    assert sha(source) == reference['sha256'] == runtime[source]['sha256']
    binaries.append({'report': 'C5_reference_build', 'source': source, 'member': runtime[source]['path'], 'sha256': reference['sha256']})
    authored = []
    for row in read('C4_AUDIT')['rtl']:
        path = local(row['path']); assert sha(path) == row['sha256']
        authored.append({'path': path.relative_to(ROOT).as_posix(), 'sha256': row['sha256'], 'acceptance': ['reports/C4_AUDIT.json']})
    builds = read('C5_soc_build')['variants']
    files = [*sorted((ROOT/'C/C5/rtl').glob('*.sv')), *sorted((ROOT/'C/C5/rtl').glob('*.v')),
             *sorted((ROOT/'C/C5/perip').rglob('*.v')), *sorted((ROOT/'C/C5/sim').glob('*.cpp')),
             *sorted((ROOT/'C/C5/sim').glob('*.hpp'))]
    for path in files:
        digest = sha(path)
        accepted = [r['executable'] for r in builds if any(i['path'] == str(path) and i['sha256'] == digest for i in r['inputs'])]
        assert accepted, ('Current RTL/harness source has no accepted build binding', path)
        authored.append({'path': path.relative_to(ROOT).as_posix(), 'sha256': digest, 'build_executables': accepted})
    overlays = []
    for row in read('C5_am_setup')['files']:
        path = local(row['path']); target = row['destination']; digest = sha(path)
        assert digest == row['sha256'] == runtime[target]['sha256']
        overlays.append({'path': path.relative_to(ROOT).as_posix(), 'member': runtime[target]['path'], 'sha256': digest})
    for filename,relative in [('paddr.c','src/memory/paddr.c'),('ref.c','src/cpu/difftest/ref.c'),('inst.c','src/isa/riscv32/inst.c')]:
        path=ROOT/'C/C5/ref'/filename; target=str(WORK/'c5/nemu-ref'/relative); digest=sha(path)
        assert digest==runtime[target]['sha256']
        assert any(row['sha256']==digest for row in reference['inputs'])
        overlays.append({'path':path.relative_to(ROOT).as_posix(),'member':runtime[target]['path'],'sha256':digest})
    historical=[]
    for filename in ['context.c', 'interrupt.c', 'libc.c', 'acceptance.c']:
        path = ROOT/'C/C5/rtthread'/filename; digest = sha(path)
        for variant in ['rt-thread-am', 'rt-thread-interactive']:
            source = str(WORK/'c5'/variant/'bsp/abstract-machine/src'/filename)
            if runtime[source]['sha256']!=digest:
                assert filename=='acceptance.c' and variant=='rt-thread-am',source
                record_path=ROOT/'artifacts/C5/rtthread/sdram32/build/run.json';record=json.loads(record_path.read_text())
                assert any(r['path']==source and r['sha256']==runtime[source]['sha256'] for r in record['inputs'])
                historical.append({'member':runtime[source]['path'],'runtime_source':source,'sha256':runtime[source]['sha256'],
                    'accepted_build_record':record_path.relative_to(ROOT).as_posix(),'accepted_build_record_sha256':sha(record_path),
                    'reason':'Scripted RT boot has no integrated AM applications. Its accepted c5_done predates the later interactive application-failure guard; the original tested source is preserved.'})
            else:
                overlays.append({'path': path.relative_to(ROOT).as_posix(), 'member': runtime[source]['path'], 'sha256': digest})
    rt = read('C5_rtthread_apps_sdram128')
    rt_build_path=ROOT/rt['evidence']/'link/run.json'
    build_record = json.loads(rt_build_path.read_text())
    generated = str(WORK/'c5/rt-thread-interactive/bsp/abstract-machine/build/c5-am-apps.c')
    assert any(r['path'] == generated and r['sha256'] == runtime[generated]['sha256'] for r in build_record['inputs'])
    rt_inputs = []
    for row in build_record['inputs']:
        if row['path'] in runtime:
            assert row['sha256'] == runtime[row['path']]['sha256'], row['path']
            rt_inputs.append({'member': runtime[row['path']]['path'], 'sha256': row['sha256']})
    for key in ['image', 'elf']:
        assert rt[key+'_sha256'] == runtime[rt[key]]['sha256']
    dump(output/'C_final_bindings.json', {'status': 'PASS_LIVE_PREVIEW_NOT_FROZEN' if args.live_preview else 'PASS', 'archive_sha256': frozen['sha256'],
        'binaries': binaries, 'authored_hardware_sources': authored, 'software_overlays': overlays,'historical_software_sources':historical,
        'rtthread_final_build_inputs': rt_inputs, 'rtthread_build_record':rt_build_path.relative_to(ROOT).as_posix(),'rtthread_build_record_sha256': sha(rt_build_path),
        'scope': 'Current C4 RTL matches its final audit. Each current C5 RTL/model/harness file occurs byte-identically in at least one accepted build input. All recorded C4/C5 simulator binaries and the C5 reference match frozen members. Current AM/RT overlays and the integrated RT application generated C match the final frozen workbench and accepted build. Earlier profile inputs remain in per-command snapshots; a later shared harness does not retroactively rebuild an older binary.'})

    candidates = []
    for row in read('C_PREFLIGHT')['tools']:
        candidates.append({**row, 'accepted_by': 'reports/C_PREFLIGHT.json'})
    for row in read('C5_toolchain')['binaries']:
        candidates.append({**row, 'accepted_by': 'reports/C5_toolchain.json'})
    sta = read('C4_opensta_toolchain')
    candidates.append({'path': sta['binary'], 'sha256': sta['sha256'], 'version': sta['version'], 'accepted_by': 'reports/C4_opensta_toolchain.json'})
    for report in ['C1_experiment', 'C3_experiment']:
        for row in read(report)['tools']:
            candidates.append({**row, 'accepted_by': 'reports/'+report+'.json'})
    locks = {}
    for row in candidates:
        path = local(row['path']); assert sha(path) == row['sha256'], path
        entry = locks.setdefault(str(path), {'path': str(path), 'sha256': row['sha256'], 'version': row.get('version'), 'accepted_by': []})
        assert entry['sha256'] == row['sha256']
        if row['accepted_by'] not in entry['accepted_by']: entry['accepted_by'].append(row['accepted_by'])
    # Launchers and Python modules are separately fingerprinted; no global install.
    scons = read('C5_rtthread_setup')['scons']
    extras = [Path('/usr/bin/python3').resolve(), Path('/usr/bin/g++').resolve(), Path(scons['wrapper']),
              Path('/home/USER/tools/scons-4.0.1/usr/lib/python3/dist-packages/SCons/Script/__init__.py')]
    for path in extras:
        locks.setdefault(str(path), {'path': str(path), 'sha256': sha(path), 'accepted_by': ['Current fingerprint; acceptance use recorded in build/preflight commands']})
    libraries = []
    for row in read('C4_synthesis_inputs')['libraries']:
        assert sha(local(row['path'])) == row['sha256']; libraries.append(row)
    nangate = read('C4_nangate_library')
    assert sha(local(nangate['local_file'])) == nangate['local_sha256']
    libraries.append({'path': str(local(nangate['local_file'])), 'sha256': nangate['local_sha256']})
    dependencies=[];system_libraries={}
    for source,row in runtime.items():
        if row.get('role')!='binary':continue
        with Path(source).open('rb') as stream:magic=stream.read(4)
        if magic!=b'\x7fELF':continue
        command=['ldd',source];result=subprocess.run(command,capture_output=True,text=True,timeout=30)
        output_text=result.stdout+result.stderr
        static='not a dynamic executable' in output_text or 'statically linked' in output_text
        assert (result.returncode==0 or static) and 'not found' not in output_text,(source,output_text)
        resolved=[]
        for name in re.findall(r'(/[^\s]+)\s+\(',output_text):
            path=Path(name).resolve();assert path.is_file();resolved.append(str(path))
            if str(path) not in system_libraries:system_libraries[str(path)]={'path':str(path),'sha256':sha(path)}
        dependencies.append({'member':row['path'],'command':command,'exit_code':result.returncode,'static':static,
            'stdout':result.stdout,'stderr':result.stderr,'resolved_libraries':sorted(set(resolved))})
    dump(output/'C_toolchain_final.json', {'status': 'PASS_LIVE_PREVIEW_NOT_FROZEN' if args.live_preview else 'PASS_RECHECKED_LOCKED_FILES',
        'tools': list(locks.values()), 'timing_libraries': libraries,
        'binary_dependencies':dependencies,'system_libraries':list(system_libraries.values()),'os_release':Path('/etc/os-release').read_text(),
        'observed_linux_memory': {line.split(':')[0]: line.split(':')[1].strip() for line in Path('/proc/meminfo').read_text().splitlines() if line.startswith(('MemTotal:', 'MemAvailable:', 'SwapTotal:', 'SwapFree:'))},
        'active_policy': load_policy(), 'resource_policy_report': 'reports/C_memory_policy.json',
        'parallel_validation_profile':read('C_performance_policy')['profile'],'parallel_validation_acceptance':'reports/C5_parallel_sdram_pilot.json',
        'scope': 'Existing accepted tool files, timing libraries and resolved shared libraries of frozen ELF binaries are fingerprinted; per-command snapshots record usage and functional positive/negative controls. Installed OS libraries, portable tool installations and Maven/JDK caches remain external dependencies. ldd inspection and a fingerprint match are not a new clean-machine rebuild, tool-feature test or physical-PPA qualification.'})
    print('C_LIVE_BINDING_PREVIEW_PASS' if args.live_preview else 'C_FINAL_BINDINGS_PASS', len(binaries), 'binaries', len(authored), 'hardware files', len(locks), 'tools', flush=True)


if __name__ == '__main__':
    main()
