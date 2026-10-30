"""Active workspace memory policy; historical run reports are never policy inputs."""
import json
import subprocess
import os,time
from pathlib import Path

POLICY_PATH = Path(__file__).resolve().parents[4] / 'config/toolchain.lock.json'


def load_policy():
    limits = json.loads(POLICY_PATH.read_text(encoding='utf-8'))['limits']
    return {
        'source': str(POLICY_PATH),
        'revision': limits['memory_policy_revision'],
        'heavy_jobs': limits['heavy_parallelism'],
        'compile_jobs': limits['compile_jobs_default'],
        'process_group_limit_mib': int(limits['soft_process_tree_rss_GiB'] * 1024),
        'windows_start_available_mib': int(limits['minimum_free_ram_before_heavy_GiB'] * 1024),
        'windows_running_available_mib': int(limits['minimum_free_ram_during_heavy_GiB'] * 1024),
        'linux_running_available_mib': limits['minimum_wsl_available_MiB'],
        'jvm_heap_mib': limits['B_jvm_heap_MiB'],
        'max_simulators':limits['B_parallel_validation']['max_simulators'],
        'estimated_simulator_mib':limits['B_parallel_validation']['estimated_worker_MiB'],
        'windows_simulator_reserve_mib':limits['B_parallel_validation']['windows_reserve_MiB'],
    }


def read_host_sample(sample):
    sample=Path(sample)
    if sample.is_dir():
        pointers=sorted(sample.glob('pointer-*.json'))
        if not pointers:raise FileNotFoundError('No host sampler pointer')
        sample=pointers[-1]
    data=json.loads(sample.read_text(encoding='utf8'))
    if data['schema']==2:
        project=POLICY_PATH.parent.parent/'projects/ysyx_f_to_b'
        stream=(project/data['stream']).resolve()
        if not stream.is_relative_to(project.resolve()):raise ValueError('Host stream outside project')
        with stream.open('rb') as handle:
            handle.seek(0,2);size=handle.tell();handle.seek(max(0,size-8192));tail=handle.read()
        complete=tail.rsplit(b'\n',1)[0] if b'\n' in tail else b''
        if not complete:raise ValueError('No complete host sample')
        latest=json.loads(complete.splitlines()[-1])
        if latest['pid']!=data['pid'] or latest['session']!=data['session']:raise ValueError('Host sample owner mismatch')
        data=latest
    return data


def windows_available_bytes():
    sample=Path(os.environ.get('YSYX_HOST_MEMORY_SAMPLE',str(POLICY_PATH.parent.parent/'projects/ysyx_f_to_b/temp/host-memory')))
    required=os.environ.get('YSYX_REQUIRE_HOST_MEMORY_SAMPLE')=='1'
    if sample.exists():
        try:
            data=read_host_sample(sample);age=time.time()-data['timestamp']
            if data['schema']!=1 or data['source']!='GlobalMemoryStatusEx.ullAvailPhys' or not -2<=age<=15 or not 0<data['available_bytes']<=data['total_bytes']:
                raise ValueError('Invalid or stale sample')
            return int(data['available_bytes'])
        except (ValueError,KeyError,OSError,TypeError,IndexError) as exc:
            if required:raise RuntimeError('HOST_MEMORY_SAMPLE_INVALID_OR_STALE: '+repr(exc)) from exc
    elif required:raise RuntimeError('HOST_MEMORY_SAMPLE_MISSING')
    command = ['/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe',
               '-NoProfile', '-NonInteractive', '-Command',
               '(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory']
    return int(subprocess.check_output(command, text=True, timeout=10).strip()) * 1024


def linux_memory():
    return {key: int(value.split()[0]) * 1024
            for line in Path('/proc/meminfo').read_text().splitlines()
            for key, value in [line.split(':', 1)]
            if key in ('MemTotal', 'MemAvailable', 'SwapTotal', 'SwapFree')}


def generation_environment(environment):
    """Retain accepted JVM/TLS settings while applying the active heap budget."""
    import re
    result = dict(environment)
    for key in ('MILL_JVM_OPTS', 'JAVA_OPTS', 'JDK_JAVA_OPTIONS', '_JAVA_OPTIONS', 'JAVA_TOOL_OPTIONS'):
        if key in result:
            result[key] = re.sub(r'-Xmx\S+', '-Xmx%dm' % load_policy()['jvm_heap_mib'], result[key])
    return result
