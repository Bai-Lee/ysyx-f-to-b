"""Bounded Windows physical-memory sampler for detached WSL validation jobs."""
from pathlib import Path
import argparse,ctypes,hashlib,json,msvcrt,os,sys,time,traceback
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[1]


class MemoryStatus(ctypes.Structure):
    _fields_=[('length',ctypes.c_ulong),('load',ctypes.c_ulong),('total_phys',ctypes.c_ulonglong),
              ('available_phys',ctypes.c_ulonglong),('total_pagefile',ctypes.c_ulonglong),('available_pagefile',ctypes.c_ulonglong),
              ('total_virtual',ctypes.c_ulonglong),('available_virtual',ctypes.c_ulonglong),('available_extended_virtual',ctypes.c_ulonglong)]


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--session',required=True);parser.add_argument('--max-seconds',type=int,default=21600);args=parser.parse_args()
    assert __import__('re').fullmatch('[0-9T]+',args.session) and 10<=args.max_seconds<=43200
    control=ROOT/'temp/host-memory';control.mkdir(parents=True,exist_ok=True)
    evidence=ROOT/'artifacts/B/host-memory-monitor'/args.session;evidence.mkdir(parents=True,exist_ok=True)
    started=time.time();minimum=None;samples=0;status='UNKNOWN';error=None;error_traceback=None
    kernel=ctypes.WinDLL('kernel32',use_last_error=True);kernel.GlobalMemoryStatusEx.argtypes=[ctypes.POINTER(MemoryStatus)];kernel.GlobalMemoryStatusEx.restype=ctypes.c_int
    lock=(control/'sampler.lock').open('a+b');lock.seek(0);lock.write(b'1');lock.flush();lock.seek(0)
    try:msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
    except OSError:raise SystemExit('Another memory sampler owns the lock')
    metadata={'pid':os.getpid(),'session':args.session,'source':'GlobalMemoryStatusEx.ullAvailPhys','started_utc':datetime.now(timezone.utc).isoformat(),
        'command':sys.argv,'python':sys.executable,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'stop_file':str(control/('stop-'+args.session)),'max_seconds':args.max_seconds,'purpose':'Read-only memory telemetry; no service, scheduled task, system configuration or process manipulation.'}
    (evidence/'started.json').write_text(json.dumps(metadata,indent=2),encoding='utf8')
    try:
        pointer={'schema':2,'source':metadata['source'],'pid':os.getpid(),'session':args.session,
                 'stream':(evidence/'samples.jsonl').relative_to(ROOT).as_posix()}
        # Each pointer is written once under a new name. The journal is append
        # only, so a reader denying FILE_SHARE_DELETE cannot disrupt sampling.
        (control/('pointer-'+args.session+'.json')).write_text(json.dumps(pointer),encoding='utf8')
        with (evidence/'samples.jsonl').open('a',encoding='utf8') as journal:
            while time.time()-started<args.max_seconds and not (control/('stop-'+args.session)).exists():
                memory=MemoryStatus();memory.length=ctypes.sizeof(memory)
                if not kernel.GlobalMemoryStatusEx(ctypes.byref(memory)):raise ctypes.WinError(ctypes.get_last_error())
                now=time.time();row={'schema':1,'source':metadata['source'],'pid':os.getpid(),'session':args.session,'timestamp':now,
                    'available_bytes':memory.available_phys,'total_bytes':memory.total_phys,'load_percent':memory.load}
                assert 0<row['available_bytes']<=row['total_bytes']
                minimum=row['available_bytes'] if minimum is None else min(minimum,row['available_bytes']);samples+=1
                payload=json.dumps(row,separators=(',',':'))
                journal.write(payload+'\n');journal.flush();time.sleep(2)
        status='STOPPED_BY_REQUEST' if (control/('stop-'+args.session)).exists() else 'STOPPED_TIME_LIMIT'
    except Exception as exc:status='FAIL';error=repr(exc);error_traceback=traceback.format_exc()
    finally:
        (evidence/'result.json').write_text(json.dumps({**metadata,'status':status,'error':error,'error_traceback':error_traceback,'samples':samples,'minimum_available_bytes':minimum,
            'elapsed_seconds':time.time()-started,'completed_utc':datetime.now(timezone.utc).isoformat()},indent=2),encoding='utf8')
        lock.close()


if __name__=='__main__':main()
