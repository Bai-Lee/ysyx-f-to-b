"""Sample a Linux process group and host headroom using the active workspace policy."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time

from resource_policy import POLICY_PATH, linux_memory, load_policy, windows_available_bytes
import resource_leases


def group_memory(pgid):
    rss = pss = 0
    for proc in Path('/proc').glob('[0-9]*'):
        try:
            fields = (proc / 'stat').read_text().rsplit(')', 1)[1].split()
            if int(fields[2]) != pgid:
                continue
            current = int(fields[21]) * os.sysconf('SC_PAGE_SIZE')
            rss += current
            try:
                pss += int(next(line.split()[1] for line in (proc / 'smaps_rollup').read_text().splitlines()
                                if line.startswith('Pss:'))) * 1024
            except (FileNotFoundError, ProcessLookupError, PermissionError, StopIteration):
                pss += current
        except (FileNotFoundError, ProcessLookupError, PermissionError, ValueError):
            pass
    return rss, pss


def main():
    policy = load_policy()
    parser = argparse.ArgumentParser()
    parser.add_argument('--rss-mib', type=int, default=policy['process_group_limit_mib'])
    parser.add_argument('--metric', choices=['rss', 'pss'], default='pss')
    parser.add_argument('--report', required=True)
    parser.add_argument('--kind',choices=['heavy','simulation'],default='heavy')
    parser.add_argument('--slots',type=int,default=1)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command or not 0 < args.rss_mib <= policy['process_group_limit_mib'] or not 1<=args.slots<=policy['max_simulators']:
        parser.error('Command required; memory override must be positive and within the active policy.')
    start = time.monotonic()
    child = None
    reason = detail = error = None
    peak = peak_pss = 0
    peak_aggregate_pss=0
    lease=None
    minimum_available = minimum_windows = None
    timeline = []
    rc = None

    def terminate(signum, frame):
        nonlocal reason, detail
        reason, detail = 'PARENT_TERMINATED', signal.Signals(signum).name

    def stop_group():
        if child is None:
            return
        try:
            os.killpg(child.pid, signal.SIGTERM)
        except ProcessLookupError:
            return
        try:
            child.wait(timeout=5)
        except subprocess.TimeoutExpired:
            pass
        try:
            os.killpg(child.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        child.wait()

    signal.signal(signal.SIGTERM, terminate)
    signal.signal(signal.SIGINT, terminate)
    try:
        host = windows_available_bytes()
        available = linux_memory()['MemAvailable']
        minimum_windows, minimum_available = host, available
        if host < policy['windows_start_available_mib'] * 1024**2:
            reason, detail = 'RESOURCE_LIMIT', 'WINDOWS_START_HEADROOM'
        elif available < policy['linux_running_available_mib'] * 1024**2:
            reason, detail = 'RESOURCE_LIMIT', 'LINUX_START_HEADROOM'
        else:
            with resource_leases.locked():
                admission=resource_leases.admit(args.kind,args.slots,policy['max_simulators'])
                if admission:reason,detail='RESOURCE_LIMIT',admission
                else:
                    child = subprocess.Popen(command, start_new_session=True)
                    lease=resource_leases.register(child.pid,args.kind,args.slots)
            last_host_check = time.monotonic()
            over = 0
            while child is not None and child.poll() is None and reason is None:
                rss, pss = group_memory(child.pid)
                peak, peak_pss = max(peak, rss), max(peak_pss, pss)
                with resource_leases.locked():
                    groups={row['process_group'] for row in resource_leases.active()}
                aggregate_pss=sum(group_memory(group)[1] for group in groups)
                peak_aggregate_pss=max(peak_aggregate_pss,aggregate_pss)
                available = linux_memory()['MemAvailable']
                minimum_available = min(minimum_available, available)
                if time.monotonic() - last_host_check >= 5:
                    host = windows_available_bytes()
                    minimum_windows = min(minimum_windows, host)
                    last_host_check = time.monotonic()
                measured = rss if args.metric == 'rss' else pss
                over = over + 1 if max(measured,aggregate_pss) > args.rss_mib * 1024**2 else 0
                if not timeline or time.monotonic() - start - timeline[-1]['elapsed_seconds'] >= 5:
                    timeline.append({'elapsed_seconds': time.monotonic() - start,
                                     'rss_bytes': rss, 'pss_bytes': pss, 'available_bytes': available,
                                     'windows_available_bytes': host,'aggregate_B_group_pss_bytes':aggregate_pss,'active_B_groups':len(groups)})
                if over >= 3:
                    reason, detail = 'RESOURCE_LIMIT', 'AGGREGATE_B_PROCESS_GROUP_MEMORY' if aggregate_pss>args.rss_mib*1024**2 else 'PROCESS_GROUP_MEMORY'
                elif available < policy['linux_running_available_mib'] * 1024**2:
                    reason, detail = 'RESOURCE_LIMIT', 'LINUX_RUNNING_HEADROOM'
                elif host < policy['windows_running_available_mib'] * 1024**2:
                    reason, detail = 'RESOURCE_LIMIT', 'WINDOWS_RUNNING_HEADROOM'
                if reason is None:
                    time.sleep(.5)
            if reason:
                stop_group()
            if child is not None:rc = child.wait()
    except Exception as exc:
        reason, error = 'MONITOR_ERROR', repr(exc)
        stop_group()
        if child is not None:
            rc = child.returncode
    with resource_leases.locked():resource_leases.release(lease)
    record = {'status': reason or ('PASS' if rc == 0 else 'CHILD_FAILURE'),
              'reason': detail, 'error': error, 'exit_code': rc,
              'elapsed_seconds': time.monotonic() - start,
              'peak_group_rss_bytes': peak, 'peak_group_pss_bytes': peak_pss,
              'peak_aggregate_B_group_pss_bytes':peak_aggregate_pss,'job_kind':args.kind,'simulation_slots':args.slots if args.kind=='simulation' else 0,
              'guard_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'lease_module_sha256':hashlib.sha256(Path(resource_leases.__file__).read_bytes()).hexdigest(),
              'metric': args.metric, 'memory_limit_bytes': args.rss_mib * 1024**2,
              'minimum_system_available_bytes': minimum_available,
              'minimum_windows_available_bytes': minimum_windows,
              'policy': policy, 'policy_sha256': hashlib.sha256(POLICY_PATH.read_bytes()).hexdigest(),
              'timeline': timeline, 'command': command,
              'sampling': 'Owned group and all active B job groups every0.5s, Windows every5s. At most one heavy job; up to8 verified simulator slots. All share the6GiB PSS budget. Sampled soft limit, no OS hard cap; no unrelated process is terminated.'}
    path = Path(args.report)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        history = path.parent / 'budget_history'
        history.mkdir(exist_ok=True)
        (history / (str(time.time_ns()) + '.json')).write_bytes(path.read_bytes())
    path.write_text(json.dumps(record, indent=2), encoding='utf-8')
    return 125 if reason == 'RESOURCE_LIMIT' else 143 if reason == 'PARENT_TERMINATED' else 126 if reason else rc


if __name__ == '__main__':
    raise SystemExit(main())
