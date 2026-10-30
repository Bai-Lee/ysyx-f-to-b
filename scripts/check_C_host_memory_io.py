"""Exercise Windows sharing semantics and complete-record telemetry framing."""
from evidence import *
import ctypes,tempfile
sys.path.insert(0,str(ROOT/'C/runtime'))
from resource_policy import read_host_sample

kernel=ctypes.WinDLL('kernel32',use_last_error=True)
kernel.CreateFileW.argtypes=[ctypes.c_wchar_p,ctypes.c_ulong,ctypes.c_ulong,ctypes.c_void_p,ctypes.c_ulong,ctypes.c_ulong,ctypes.c_void_p]
kernel.CreateFileW.restype=ctypes.c_void_p
kernel.CloseHandle.argtypes=[ctypes.c_void_p];kernel.CloseHandle.restype=ctypes.c_int
def hold(path):
    handle=kernel.CreateFileW(str(path),0x80000000,3,None,3,0x80,None)
    if handle==ctypes.c_void_p(-1).value:raise ctypes.WinError(ctypes.get_last_error())
    return handle

control=ROOT/'temp/host-memory';pointer=sorted(control.glob('pointer-*.json'))[-1]
metadata=json.loads(pointer.read_text('utf8'));stream=ROOT/metadata['stream'];first=read_host_sample(pointer)
handle=hold(stream)
try:time.sleep(5);second=read_host_sample(pointer);assert second['timestamp']>first['timestamp']
finally:kernel.CloseHandle(handle)
with tempfile.TemporaryDirectory(prefix='host-memory-io-',dir=ROOT/'temp') as temp:
    folder=Path(temp).resolve();assert folder.is_relative_to((ROOT/'temp').resolve())
    old=folder/'old.txt';replacement=folder/'replacement.txt';old.write_text('old\n');replacement.write_text('replacement\n')
    handle=hold(old)
    try:
        try:os.replace(replacement,old)
        except PermissionError:replace_rejected=True
        else:raise AssertionError('The fixture failed to deny replacement')
        with old.open('a') as output:output.write('appended\n')
        assert old.read_text()=='old\nappended\n'
    finally:kernel.CloseHandle(handle)
    fixture=folder/'samples.jsonl';fixture.write_bytes((json.dumps(second)+'\n').encode()+b'{"unfinished":')
    fixture_pointer=folder/'pointer.json';fixture_pointer.write_text(json.dumps({**metadata,'stream':fixture.relative_to(ROOT).as_posix()}))
    assert read_host_sample(fixture_pointer)==second
    fixture.write_text(json.dumps(second)+'\nnot-json\n')
    try:read_host_sample(fixture_pointer)
    except ValueError:malformed_rejected=True
    else:raise AssertionError('Malformed complete record was silently ignored')
dump(ROOT/'reports/C_host_memory_io_controls.json',{'status':'PASS_WINDOWS_SHARING_AND_FRAMING',
    'replace_rejected_under_read_handle':replace_rejected,'append_while_read_handle':True,'live_stream_advanced_while_held':True,
    'partial_tail_uses_previous_complete_record':True,'malformed_complete_record_rejected':malformed_rejected,
    'first_sample':first,'second_sample':second,'reader_sha256':sha(ROOT/'C/runtime/resource_policy.py'),
    'sampler_sha256':sha(ROOT/'scripts/host_memory_monitor.py'),
    'scope':'Actual Windows read handle permits reading/writing but denies deletion. Replacement is rejected, appending succeeds, and the actual sampler keeps appending. A partial trailing record is not parsed; a malformed complete record is rejected.'})
print('HOST_MEMORY_SHARING_AND_FRAMING_PASS',flush=True)
