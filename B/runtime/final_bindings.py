"""Bind final live source/tool fingerprints to accepted builds and frozen members."""
from common import *
import argparse
from resource_policy import POLICY_PATH,linux_memory,windows_available_bytes

def read(name):return json.loads((ROOT/'reports'/f'{name}.json').read_text())

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--live-preview',action='store_true');args=parser.parse_args()
    soc=next(r for r in read('B_soc_soc_build')['variants'] if r['variant']=='b5-release')
    standalone=next(r for r in read('B_standalone_builds')['variants'] if r['label']=='release')
    timing=read('B5_final_timing');exported=read('B5_export')
    synthesis=json.loads((ROOT/'artifacts/B3/synthesis/b5-release-cpu/run.json').read_text())
    synthesized={r['path']:r['sha256'] for r in synthesis['inputs']};build={r['path']:r['sha256'] for r in soc['inputs']}
    authored=[]
    for row in exported['sources']:
        path=ROOT/row['path'];value=sha(path)
        assert value==row['sha256']==synthesized[str(path)]==build[str(path)],path
        authored.append({'path':row['path'],'sha256':value})
    policy_metadata_changes=[]
    for row in soc['inputs']:
        path=Path(row['path']);current=sha(path)
        if current==row['sha256']:continue
        assert path==POLICY_PATH,'Functional build input changed: '+str(path)
        record=json.loads((ROOT/'artifacts/B/soc/build/b5-release/run.json').read_text());index=next(i for i,r in enumerate(record['inputs']) if r['path']==str(path))
        with zipfile.ZipFile(ROOT/'artifacts/B/soc/build/b5-release/input_snapshot.zip') as archive:
            payload=archive.read(archive.namelist()[index]);assert hashlib.sha256(payload).hexdigest()==row['sha256'];prior=json.loads(payload)
        after=json.loads(path.read_text());assert prior['limits']==after['limits']
        for key in set(prior)|set(after):
            if key not in ['workspace_state','project_toolchains','last_updated_utc']:assert prior.get(key)==after.get(key),key
        policy_metadata_changes.append({'path':str(path),'build_sha256':row['sha256'],'current_sha256':current,'scope':'Only completed-stage/audit-pointer/timestamp metadata changed; numeric resource limits and installed-tool fields identical.'})
    for row in [soc,standalone]:assert sha(Path(row['executable']))==row['sha256']
    binaries=[{'role':'final_soc','source':soc['executable'],'sha256':soc['sha256']},
              {'role':'final_standalone','source':standalone['executable'],'sha256':standalone['sha256']}]
    for name in ['nemu-ref/build/riscv32-nemu-interpreter-so','fast-nemu-ref/build/riscv32-nemu-interpreter-so','workbench/nemu/build/riscv32-nemu-interpreter','workbench/nemu/tools/spike-diff/build/riscv32-spike-so']:
        path=WORK/name;assert path.is_file();binaries.append({'role':'reference_or_native','source':str(path),'sha256':sha(path)})
    frozen=read('B_runtime_export') if not args.live_preview else None
    if frozen:
        assert sha(ROOT/frozen['archive'])==frozen['sha256'];members={r['source']:r for r in frozen['members'] if r['kind']=='file'}
        for row in binaries:assert members[row['source']]['sha256']==row['sha256'];row['member']=members[row['source']]['path']
    tools=[]
    for row in read('B_PREFLIGHT')['tools']:
        path=Path(row['path']);assert sha(path)==row['sha256'];tools.append({**row,'acceptance':'B_PREFLIGHT and actual B build/runtime evidence'})
    suite=Path('/home/USER/tools/e-stage/oss-20260821/oss-cad-suite');sta=read('C4_opensta_toolchain')
    for name,path,flag in [('yosys',suite/'bin/yosys','-V'),('iverilog',suite/'bin/iverilog','-V'),('vvp',suite/'bin/vvp','-V'),('opensta',Path(sta['binary']),'-version')]:
        output,error,_=run('B/toolchain-final/'+name,[path,flag],inputs=[path])
        tools.append({'name':name,'path':str(path),'sha256':sha(path),'version':(output+error).strip(),'acceptance':'Actual final synthesis/four-state/STA evidence; version call alone is not acceptance'})
    executables=[]
    for path in [suite/'libexec/yosys',suite/'libexec/iverilog',suite/'libexec/vvp',suite/'lib/ld-linux-x86-64.so.2',Path('/home/USER/tools/verilator-stable-src/bin/verilator_bin'),Path('/usr/bin/python3').resolve(),Path('/usr/bin/g++').resolve()]:
        if path.is_file():executables.append({'path':str(path),'sha256':sha(path)})
    toolchain={'status':'PASS_CURRENT_FINGERPRINTS','tools':tools,'launch_support':executables,
        'library':{'path':'B/models/nangate45/lib/Nangate45_typ.lib','sha256':sha(ROOT/'B/models/nangate45/lib/Nangate45_typ.lib')},
        'cell_models':{'path':'B/models/nangate45/sim/cells.v','sha256':sha(ROOT/'B/models/nangate45/sim/cells.v')},
        'memory_observed':{'linux_bytes':linux_memory(),'windows_available_bytes':windows_available_bytes()},'active_limits':load_policy(),
        'scope':'Windows base Python/venv kept separate from Linux EDA/runtime tools. Current hashes rechecked against accepted source/build evidence; no installs or global environment changes.'}
    result={'status':'PASS_LIVE_PREVIEW' if args.live_preview else 'PASS','authored_rtl':authored,'binaries':binaries,
        'soc_build_sha256':sha(ROOT/'artifacts/B/soc/build/b5-release/run.json'),'standalone_build_index_sha256':sha(ROOT/'reports/B_standalone_builds.json'),
        'mapped_netlist_sha256':timing['netlist_sha256'],'exported_rtl_sha256':exported['sha256'],'archive_sha256':frozen['sha256'] if frozen else None,
        'policy_metadata_changes':policy_metadata_changes,
        'scope':'Every final RTL source byte belongs to both the accepted full-SoC build and original fixed-address synthesis. Two drive substitutions and export normalization are separately checked. Final binaries and references match the frozen runtime when not in preview mode.'}
    output=ROOT/'temp' if args.live_preview else ROOT/'reports';dump(output/'B_final_bindings.json',result);dump(output/'B_toolchain_final.json',toolchain)
    print('B_FINAL_BINDINGS_PASS',args.live_preview,len(authored),len(binaries),flush=True)

if __name__=='__main__':main()
