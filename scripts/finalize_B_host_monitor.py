"""Freeze task-owned Windows telemetry after all guarded validation/replay ends."""
from evidence import *
import time

def main():
    for name in ['B_offline_replay','B5_ACCEPTANCE','B4_full128','B_final_regressions']:
        assert json.loads((ROOT/'reports'/f'{name}.json').read_text('utf8'))['status'].startswith('PASS'),name
    pointers=sorted((ROOT/'temp/host-memory').glob('pointer-*.json'));assert pointers
    pointer=json.loads(pointers[-1].read_text('utf8'));folder=ROOT/pointer['stream'];assert folder.name=='samples.jsonl';folder=folder.parent
    assert folder.is_relative_to(ROOT/'artifacts/B/host-memory-monitor')
    started=json.loads((folder/'started.json').read_text('utf8'));stop=Path(started['stop_file']).resolve();assert stop.is_relative_to((ROOT/'temp/host-memory').resolve())
    stop.write_text('All guarded B validation and frozen-runtime replay completed.\n',encoding='utf8')
    deadline=time.monotonic()+10
    while not (folder/'result.json').exists() and time.monotonic()<deadline:time.sleep(.2)
    current=json.loads((folder/'result.json').read_text('utf8'));assert current['status']=='STOPPED_BY_REQUEST' and current['error'] is None
    baseline=json.loads((ROOT/'reports/B_baseline.json').read_text('utf8'));sessions=[]
    for base in [ROOT/'artifacts/B/host-memory-monitor',ROOT/'artifacts/C/host-memory-monitor']:
        if not base.exists():continue
        for directory in sorted(base.iterdir()):
            if not directory.is_dir() or directory.name<baseline['timestamp']:continue
            result_file=directory/'result.json';assert result_file.exists(),directory
            result=json.loads(result_file.read_text('utf8'));samples=[json.loads(line) for line in (directory/'samples.jsonl').read_text('utf8').splitlines()]
            assert len(samples)==result['samples'] and samples
            assert all(r['schema']==1 and r['source']=='GlobalMemoryStatusEx.ullAvailPhys' and 0<r['available_bytes']<=r['total_bytes'] for r in samples)
            assert min(r['available_bytes'] for r in samples)==result['minimum_available_bytes']
            files=[directory/name for name in ['started.json','samples.jsonl','result.json','launch.json'] if (directory/name).is_file()]
            sessions.append({'path':directory.relative_to(ROOT).as_posix(),'status':result['status'],'error':result.get('error'),'samples':len(samples),'minimum_available_bytes':result['minimum_available_bytes'],
                'files':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in files]})
    assert sessions
    dump(ROOT/'reports/B_host_memory_monitor.json',{'status':'PASS_FINAL_SESSION_STOPPED','session':pointer['session'],'sessions':sessions,
        'scope':'Task-local native Windows physical-memory sampling. Early B sessions added under the historical C telemetry directory are explicitly listed; previously delivered C files remain unchanged. Final B session stopped normally before the delivery manifest. No service, automation or global system change.'})
    print('B_HOST_MONITOR_FROZEN',len(sessions),sum(r['samples'] for r in sessions),flush=True)

if __name__=='__main__':main()
