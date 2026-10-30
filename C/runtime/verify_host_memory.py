"""Accept fresh Windows telemetry and reject stale/missing telemetry without IPC."""
from common import *
from unittest.mock import patch
import resource_policy,tempfile

live=ROOT/'temp/host-memory'
os.environ['YSYX_HOST_MEMORY_SAMPLE']=str(live);os.environ['YSYX_REQUIRE_HOST_MEMORY_SAMPLE']='1'
first=resource_policy.read_host_sample(live);time.sleep(3);second=resource_policy.read_host_sample(live);assert second['timestamp']>first['timestamp']
with patch.object(resource_policy.subprocess,'check_output',side_effect=AssertionError('WSL interop must not be used')):
    observed=resource_policy.windows_available_bytes();assert 0<observed<=second['total_bytes']
    with tempfile.TemporaryDirectory() as temp:
        path=Path(temp)/'stale.json';path.write_text(json.dumps({**second,'timestamp':time.time()-120}));os.environ['YSYX_HOST_MEMORY_SAMPLE']=str(path)
        try:resource_policy.windows_available_bytes()
        except RuntimeError as error:assert 'STALE' in str(error)
        else:raise AssertionError('Stale sample was accepted')
        os.environ['YSYX_HOST_MEMORY_SAMPLE']=str(path.with_name('missing.json'))
        try:resource_policy.windows_available_bytes()
        except RuntimeError as error:assert 'MISSING' in str(error)
        else:raise AssertionError('Missing sample was accepted')
dump(ROOT/'reports/C_host_memory_controls.json',{'status':'PASS_FRESH_AND_FAIL_CLOSED_CONTROLS','first_sample':first,'second_sample':second,
    'sampler_pid':second['pid'],'session':second['session'],'observed_available_bytes':observed,'stale_rejected':True,'missing_rejected':True,'no_interop_calls':True,
    'reader_sha256':sha(ROOT/'C/runtime/resource_policy.py'),'sampler_sha256':sha(ROOT/'scripts/host_memory_monitor.py'),
    'scope':'Actual fresh Windows append-only physical-memory samples advance after the launching shell exits. Only complete newline-terminated records are read. Required missing/stale telemetry raises an error. Native interop invocation was explicitly prohibited during this control.'})
print('HOST_MEMORY_CHANNEL_CONTROLS_PASS',flush=True)
