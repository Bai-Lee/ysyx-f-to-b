"""Recheck saved C inputs/tools and current resources before resuming."""
from common import *
from resource_policy import load_policy

def main():
    rows=[]
    for name,key in [('C_PREFLIGHT','tools'),('C5_toolchain','binaries')]:
        data=json.loads((ROOT/'reports'/f'{name}.json').read_text())
        for row in data[key]:
            actual=sha(row['path']);assert actual==row['sha256'],row['path']
            rows.append({'path':row['path'],'sha256':actual})
    command=['/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe','-NoProfile','-NonInteractive','-Command','(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory']
    windows_free=int(subprocess.check_output(command,text=True).strip())
    memory={}
    for line in Path('/proc/meminfo').read_text().splitlines():
        key,value=line.split(':',1)
        if key in ['MemTotal','MemAvailable','SwapTotal','SwapFree']:memory[key+'_KiB']=int(value.split()[0])
    p=ROOT/'reports/C_resume_check.json'
    if p.exists():
        archive=ROOT/'artifacts/C/resume'/str(time.time_ns());archive.mkdir(parents=True);shutil.copyfile(p,archive/p.name)
    dump(p,{'status':'PASS_FINGERPRINTS','timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tools':rows,'windows_free_kib':windows_free,'linux_memory':memory,'generation_process_group_pss_limit_mib':load_policy()['process_group_limit_mib'],'resource_policy':load_policy(),'scope':'Actual VM capacity is observed, not assumed from the historical 4GiB setting. Existing positive/negative tool evidence remains applicable because binaries match. New functional C work still requires its own tests. No WSL/global settings changed.'})
    print('C_RESUME_FINGERPRINTS_PASS',windows_free,memory,flush=True)

if __name__=='__main__':main()
