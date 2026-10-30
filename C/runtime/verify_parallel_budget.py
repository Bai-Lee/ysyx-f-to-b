"""Prove that a batch is limited by combined PSS, not a limit per worker."""
from common import *
rows=[]
for name,limit in [('positive',160),('aggregate-over-budget',48)]:
    folder=ROOT/'artifacts/C/parallel-budget'/name;folder.mkdir(parents=True,exist_ok=True)
    pidfile=folder/'children.json'
    child='import time; a=bytearray(32*1024**2); time.sleep(4)'
    code='import subprocess,sys,json; from pathlib import Path; ps=[subprocess.Popen([sys.executable,"-c",'+repr(child)+']) for _ in range(2)]; Path('+repr(str(pidfile))+').write_text(json.dumps([p.pid for p in ps])); [p.wait() for p in ps]'
    expected=0 if name=='positive' else 125
    run('C/parallel-budget/'+name+'/run',['python3',ROOT/'C/runtime/budget_exec.py','--rss-mib',str(limit),'--report',folder/'resources.json','--','python3','-c',code],
        inputs=[Path(__file__),ROOT/'C/runtime/budget_exec.py',ROOT/'C/runtime/resource_policy.py'],outputs=[folder/'resources.json',pidfile],expected=(expected,),timeout=30)
    data=json.loads((folder/'resources.json').read_text());assert data['peak_group_pss_bytes']>64*1024**2
    assert data['status']==('PASS' if expected==0 else 'RESOURCE_LIMIT')
    if expected:
        assert data['reason']=='PROCESS_GROUP_MEMORY'
        for pid in json.loads(pidfile.read_text()):
            stat=Path('/proc',str(pid),'stat')
            assert not stat.exists() or stat.read_text().rsplit(')',1)[1].split()[0]=='Z'
    rows.append({'name':name,'status':'PASS','expected_exit':expected,'limit_MiB':limit,'peak_pss_bytes':data['peak_group_pss_bytes'],'evidence':folder.relative_to(ROOT).as_posix()})
dump(ROOT/'reports/C_parallel_resource_controls.json',{'status':'PASS','controls':rows,'scope':'Two actual child allocators each below48MiB together exceed48MiB; the whole shared process group is stopped. A160MiB aggregate budget accepts both. No multi-GiB allocation used just to test the guard.'})
print('PARALLEL_PSS_CONTROLS_PASS',flush=True)
