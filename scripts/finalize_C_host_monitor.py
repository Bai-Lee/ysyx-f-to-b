"""Stop the task-owned Windows sampler after all guarded replay jobs finish."""
from evidence import *
import time

assert json.loads((ROOT/'reports/C_offline_replay.json').read_text('utf8'))['status']=='PASS'
assert json.loads((ROOT/'artifacts/C5/parallel-full128-job/status.json').read_text('utf8'))['status']=='PASS'
controls=json.loads((ROOT/'reports/C_host_memory_controls.json').read_text('utf8'));session=controls['session']
folder=ROOT/'artifacts/C/host-memory-monitor'/session;started=json.loads((folder/'started.json').read_text('utf8'))
stop=Path(started['stop_file']).resolve();assert stop.is_relative_to((ROOT/'temp/host-memory').resolve())
stop.write_text('All guarded C validation and offline replay jobs completed.\n',encoding='utf8')
deadline=time.monotonic()+10
while not (folder/'result.json').exists() and time.monotonic()<deadline:time.sleep(.2)
result=json.loads((folder/'result.json').read_text('utf8'));assert result['status']=='STOPPED_BY_REQUEST' and result['error'] is None
samples=[json.loads(line) for line in (folder/'samples.jsonl').read_text('utf8').splitlines()]
assert len(samples)==result['samples'] and len(samples)>=3
assert all(r['schema']==1 and r['source']=='GlobalMemoryStatusEx.ullAvailPhys' and 0<r['available_bytes']<=r['total_bytes'] for r in samples)
assert min(r['available_bytes'] for r in samples)==result['minimum_available_bytes']
prior=[]
for old in (ROOT/'artifacts/C/host-memory-monitor').glob('*/result.json'):
    if old.parent==folder:continue
    entry=json.loads(old.read_text('utf8'));prior.append({'path':old.relative_to(ROOT).as_posix(),'sha256':sha(old),'status':entry['status'],'error':entry.get('error')})
dump(ROOT/'reports/C_host_memory_monitor.json',{'status':'PASS_STOPPED_AFTER_VALIDATION','session':session,'sampler_pid':result['pid'],
    'samples':len(samples),'minimum_available_bytes':result['minimum_available_bytes'],'elapsed_seconds':result['elapsed_seconds'],
    'files':[{'path':(folder/name).relative_to(ROOT).as_posix(),'sha256':sha(folder/name)} for name in ['launch.json','started.json','samples.jsonl','result.json']],
    'controls_sha256':sha(ROOT/'reports/C_host_memory_controls.json'),
    'io_controls_sha256':sha(ROOT/'reports/C_host_memory_io_controls.json'),'prior_sessions':prior,
    'scope':'Bounded task-owned Windows process used the native physical-memory API and appended newline-framed telemetry for detached WSL guards. Readers select the latest complete record. Stale/missing telemetry fails closed. Sampler stopped normally before the delivery manifest is made; no service/scheduled task/system setting was created.'})
print('HOST_MEMORY_MONITOR_STOPPED_AND_FROZEN',len(samples),flush=True)
