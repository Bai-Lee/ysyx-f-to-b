"""Execute selected tests using only runtime inputs extracted from the frozen tar."""
from common import *
from pathlib import PurePosixPath
import tarfile,argparse

CASES={'context':'B4/release-soc/context','rtthread':'B4/release-soc/rtthread',
       'microbench':'B3/perf/b5-release-test-pad24/run','wrong-original':'B4/final-cpu/wrong/run',
       'memory4k':'B4/parallel-sdram/release-pilot4k/phase-6','four-state-gate-hello':'B5/design/netlist/hello'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--demo',action='store_true',help='Write fresh demonstration evidence without changing frozen acceptance reports');args=parser.parse_args()
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f');base_tag='B/demo/'+stamp if args.demo else 'B/offline-replay'
    frozen=json.loads((ROOT/'reports/B_runtime_export.json').read_text());archive=ROOT/frozen['archive'];assert sha(archive)==frozen['sha256']
    by_source={r['source']:r for r in frozen['members'] if r['kind']=='file'};members={r['path']:r for r in frozen['members']};selected=set();originals={}
    vvp=Path('/home/USER/tools/e-stage/oss-20260821/oss-cad-suite/bin/vvp')
    tools=json.loads((ROOT/'reports/B_toolchain_final.json').read_text());assert any(r['path']==str(vvp) and r['sha256']==sha(vvp) for r in tools['tools'])
    for case,evidence in CASES.items():
        record=json.loads((ROOT/'artifacts'/evidence/'run.json').read_text());assert record['status']=='PASS'
        command=list(record['command']);command=command[command.index('--')+1:] if '--' in command else command
        for index,arg in enumerate(command):
            if index and command[index-1] in ['--report','--perf-trace']:continue
            value=arg.split('=',1)[1] if arg.startswith('+IMAGE=') else arg
            if value.startswith('/'):
                if value==str(vvp):continue
                assert value in by_source,('Input not frozen',value);selected.add(by_source[value]['path'])
        originals[case]=(record,command)
    destination=WORK/'offline-replay'/stamp;destination.mkdir(parents=True,exist_ok=False);seen=set()
    with tarfile.open(archive,'r|gz') as tar:
        for item in tar:
            path=PurePosixPath(item.name);assert not path.is_absolute() and '..' not in path.parts and '\\' not in item.name
            if item.name not in selected:continue
            assert item.isfile() and item.name not in seen;seen.add(item.name);target=destination/item.name;target.parent.mkdir(parents=True,exist_ok=True)
            with tar.extractfile(item) as source,target.open('xb') as output:shutil.copyfileobj(source,output,1048576)
            target.chmod(item.mode&0o777);assert sha(target)==members[item.name]['sha256']
    assert seen==selected;rows=[]
    for case,evidence in CASES.items():
        original,command=originals[case];folder=ROOT/'artifacts'/base_tag/case;folder.mkdir(parents=True,exist_ok=True);inputs=[]
        for index,arg in enumerate(command):
            if index and command[index-1]=='--report':command[index]=str(folder/'simulation.json');continue
            if index and command[index-1]=='--perf-trace':command[index]=str(folder/'retired.bin');continue
            prefix='+IMAGE=' if arg.startswith('+IMAGE=') else '';value=arg[len(prefix):]
            if value in by_source:
                path=destination/by_source[value]['path'];command[index]=prefix+str(path);inputs.append(path)
        assert inputs and all(p.is_relative_to(destination) for p in inputs)
        budget=folder/'budget.json';outputs=[budget]+([] if case=='four-state-gate-hello' else [folder/'simulation.json'])+([folder/'retired.bin'] if '--perf-trace' in command else [])
        output,error,record=run(base_tag+'/'+case,['python3',ROOT/'B/runtime/budget_exec.py','--kind','simulation','--report',budget,'--',*command],inputs=inputs+([vvp] if case=='four-state-gate-hello' else []),outputs=outputs,expected=(1 if case=='wrong-original' else 0,),timeout=600)
        if case=='four-state-gate-hello':assert 'B5_PROGRAM_PASS' in output and 'B_FAST_HELLO_PASS' in output;result='B5_PROGRAM_PASS'
        else:
            data=json.loads((folder/'simulation.json').read_text());assert data['result']==('BAD_TRAP' if case=='wrong-original' else 'GOOD_TRAP')
            assert data['diff_enabled'] and data['diff_checked']+data['device_sync_checked']==data['instructions'];result=data['result']
            previous=json.loads((ROOT/'artifacts'/evidence/'simulation.json').read_text()) if (ROOT/'artifacts'/evidence/'simulation.json').exists() else json.loads((ROOT/'artifacts'/evidence).parent.joinpath('simulation.json').read_text())
            for key in ['cycles','instructions','gpr','uart','coverage']:
                if key in previous:assert data[key]==previous[key],(case,key)
            if '--perf-trace' in command:
                original_command=original['command'];old_trace=Path(original_command[original_command.index('--perf-trace')+1]);assert sha(folder/'retired.bin')==sha(old_trace)
        rows.append({'case':case,'status':'PASS_EXPECTED_NEGATIVE' if case=='wrong-original' else 'PASS','result':result,'evidence':'artifacts/'+base_tag+'/'+case,'inputs':[{'member':p.relative_to(destination).as_posix(),'sha256':sha(p)} for p in inputs]})
    output_path=ROOT/'artifacts'/base_tag/'summary.json' if args.demo else ROOT/'reports/B_offline_replay.json'
    dump(output_path,{'status':'PASS','archive_sha256':frozen['sha256'],'extracted_members':len(selected),'runs':rows,
        'scope':'All replayed simulator/reference/firmware or Icarus bytecode/image inputs came from the frozen runtime in a fresh directory. No build/download or original live workbench binary. Installed Linux loader/libraries, locked Icarus executable and project resource guard remain external runtime dependencies. Full128 evidence is hash-verified, not redundantly rerun by this short replay.'})
    print('B_OFFLINE_REPLAY_PASS',len(rows),len(selected),flush=True)

if __name__=='__main__':main()
