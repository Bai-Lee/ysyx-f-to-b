"""Task-local admission and aggregate accounting across owned B process groups."""
from pathlib import Path
from contextlib import contextmanager
import fcntl,json,os,time

WORK=Path('/home/USER/b-stage')
DIRECTORY=Path(os.environ.get('YSYX_B_RESOURCE_LEASES',str(WORK/'resource-leases'))).resolve()
assert DIRECTORY.is_relative_to(WORK.resolve()),'Lease directory must stay in the B workbench'
DIRECTORY.mkdir(parents=True,exist_ok=True)
BOOT=Path('/proc/sys/kernel/random/boot_id').read_text().strip()

def identity(pid):
    try:
        fields=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()
        return int(fields[19]) if fields[0]!='Z' else None
    except (FileNotFoundError,ProcessLookupError):return None

@contextmanager
def locked():
    with (DIRECTORY/'lock').open('a+') as handle:
        fcntl.flock(handle,fcntl.LOCK_EX)
        try:yield
        finally:fcntl.flock(handle,fcntl.LOCK_UN)

def active():
    rows=[]
    for p in DIRECTORY.glob('lease-*.json'):
        row=json.loads(p.read_text())
        if row['boot']==BOOT and identity(row['owner_pid'])==row['owner_start']:
            rows.append(row)
    return rows

def admit(kind,slots,maximum_simulators):
    rows=active()
    if kind=='heavy' and any(r['kind']=='heavy' for r in rows):return 'HEAVY_SLOT_BUSY'
    if kind=='simulation' and slots+sum(r['slots'] for r in rows if r['kind']=='simulation')>maximum_simulators:return 'SIMULATOR_SLOT_LIMIT'
    return None

def register(pgid,kind,slots):
    row={'schema':1,'boot':BOOT,'owner_pid':os.getpid(),'owner_start':identity(os.getpid()),'process_group':pgid,'kind':kind,'slots':slots,'created':time.time()}
    path=DIRECTORY/f'lease-{os.getpid()}-{time.time_ns()}.json';path.write_text(json.dumps(row))
    return path

def release(path):
    if path is not None:
        assert path.parent==DIRECTORY
        path.unlink(missing_ok=True)
