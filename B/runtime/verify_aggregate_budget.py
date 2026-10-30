from common import *
from resource_policy import windows_available_bytes

def main():
    assert windows_available_bytes()>3*1024**3,'Run this small control when host headroom exceeds3GiB'
    lease_dir=WORK/'budget-tests'/str(time.time_ns());lease_dir.mkdir(parents=True)
    env={'YSYX_B_RESOURCE_LEASES':str(lease_dir)};guard=ROOT/'B/runtime/budget_exec.py'
    out=ROOT/'artifacts/B/resource-aggregate';out.mkdir(parents=True,exist_ok=True)
    code='import time; x=bytearray(120*1024*1024); time.sleep(5)'
    processes=[]
    for i in range(2):
        report=out/f'limit-{i}.json'
        command=['python3',str(guard),'--kind','simulation','--rss-mib','192','--report',str(report),'--','python3','-c',code]
        processes.append(subprocess.Popen(command,env={**os.environ,**env},stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True))
    codes=[p.wait(timeout=25) for p in processes];reports=[json.loads((out/f'limit-{i}.json').read_text()) for i in range(2)]
    assert any(r['status']=='RESOURCE_LIMIT' and r['reason']=='AGGREGATE_B_PROCESS_GROUP_MEMORY' for r in reports),reports
    assert all(r['peak_group_pss_bytes']<192*1024**2 for r in reports)
    assert max(r['peak_aggregate_B_group_pss_bytes'] for r in reports)>192*1024**2
    positive=out/'positive.json'
    run('B/resource-aggregate/positive',['python3',guard,'--kind','simulation','--rss-mib','512','--report',positive,'--','python3','-c','import time; x=bytearray(24*1024*1024); time.sleep(1)'],env=env,inputs=[guard,ROOT/'B/runtime/resource_leases.py'],outputs=[positive])
    assert json.loads(positive.read_text())['status']=='PASS'
    dump(ROOT/'reports/B_resource_aggregate.json',{'status':'PASS','negative_exit_codes':codes,'negative_reports':reports,'positive':json.loads(positive.read_text()),'scope':'Two120MiB processes are each below192MiB but their combined PSS exceeds it; aggregate guard rejects the overlap. Separate24MiB control passes. Test uses an isolated task-local lease directory; production budget remains6GiB.'})
    print('B_AGGREGATE_BUDGET_PASS')

if __name__=='__main__':main()
