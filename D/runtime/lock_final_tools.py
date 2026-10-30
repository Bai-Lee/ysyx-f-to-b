"""Read final fingerprints and memory state; no installation or configuration changes."""
from common import *

def main():
    initial=json.loads((ROOT/'reports/D_PREFLIGHT.json').read_text());rows=[]
    for row in initial['tools']:
        p=Path(row['path']);assert sha(p)==row['sha256'],p
        rows.append({**row,'rechecked_final':True})
    extras=[Path(json.loads((ROOT/'reports/D_clang.json').read_text())['compiler']),WORK.parent/'tools/d-stage/support/usr/bin/dtc']
    binaries=json.loads((ROOT/'reports/D_final_bindings.json').read_text())['binaries']
    extras += [Path(x['source']) for x in binaries]
    fingerprints=[{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in extras]
    pdk=json.loads((ROOT/'reports/D6_pdk.json').read_text())['inputs']
    for row in pdk:assert sha(row['path'])==row['sha256']
    memory={}
    for line in Path('/proc/meminfo').read_text().splitlines():
        k,v=line.split(':',1)
        if k in ['MemTotal','MemAvailable','SwapTotal','SwapFree']:memory[k+'_KiB']=int(v.split()[0])
    dump(ROOT/'reports/D_toolchain_final.json',{'status':'PASS_LOCKED_AFTER_RUNS','captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inherited_tools':rows,'additional_fingerprints':fingerprints,'pdk_inputs_rechecked':pdk,'memory_observation':memory,'dependency_acceptance':['reports/D_clang.json','reports/D_spike_support.json','reports/D_capstone.json','reports/D8_reference.json'],'scope':'Actual paths/fingerprints verified after runs. This is not a new functional simulation; previous positive/negative acceptance remains attached. No global configuration changed.'})
    print('D_FINAL_TOOL_FINGERPRINTS_PASS',flush=True)

if __name__=='__main__':main()
