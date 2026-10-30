from pathlib import Path
import sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    p=argparse.ArgumentParser();p.add_argument('--label',default='multicycle-cache128');p.add_argument('--mutant',action='store_true');p.add_argument('--fault-fence',action='store_true');p.add_argument('--cache-lines',type=int,default=4);p.add_argument('--cache-words',type=int,default=8);p.add_argument('--cache-ways',type=int,default=2)
    p.add_argument('--pipeline',action='store_true');p.add_argument('--forward',action='store_true');p.add_argument('--predict',action='store_true');p.add_argument('--predict-jal',action='store_true');p.add_argument('--stream-fetch',action='store_true');p.add_argument('--fault-fence-flush',action='store_true');p.add_argument('--fault-raw',action='store_true');a=p.parse_args()
    assert not(a.predict and a.predict_jal)
    out=WORK/'standalone/build'/a.label;out.mkdir(parents=True,exist_ok=True);exe=out/'sim';cpp=ROOT/'B/standalone/runner.cpp'
    sources=[*sorted((ROOT/'B/soc/rtl').glob('*.sv')),*sorted((ROOT/'B/soc/rtl').glob('*.v'))]
    headers=[ROOT/'B/soc/sim/reference.hpp',ROOT/'B/soc/sim/performance.hpp']
    cmd=[VERILATOR,'--cc','--exe','--build','-j','4','--assert','-Wall','-Wno-fatal','--top-module','ysyx_00000000','--Mdir',out,'-o','sim',"-DC5_RESET_PC=32'h80000000",f'-DC5_FAULT_ADDI={int(a.mutant)}',f'-DB_FAULT_FENCE={int(a.fault_fence)}',f'-DB_ICACHE_ENABLE={int(a.cache_lines>0)}',f'-DB_ICACHE_LINES={a.cache_lines or 16}',f'-DB_ICACHE_WORDS={a.cache_words}',f'-DB_ICACHE_WAYS={a.cache_ways}',f'-DB_PIPELINE={int(a.pipeline)}',f'-DB_FORWARD={int(a.forward)}',f'-DB_PREDICT={int(a.predict)}',f'-DB_FAULT_FENCE_FLUSH={int(a.fault_fence_flush)}',f'-DB_FAULT_RAW={int(a.fault_raw)}','-CFLAGS','-O3 -DB_STANDALONE=1','-LDFLAGS','-ldl',*sources,cpp]
    budget=ROOT/'artifacts/B/standalone/build'/a.label/'budget.json'
    cmd.insert(1,f'-DB_FETCH_PIPELINED={int(a.stream_fetch)}')
    cmd=[f'-DB_PREDICT={2 if a.predict_jal else int(a.predict)}' if str(x).startswith('-DB_PREDICT=') else x for x in cmd]
    run('B/standalone/build/'+a.label,['python3',ROOT/'B/runtime/budget_exec.py','--report',budget,'--',*cmd],inputs=[VERILATOR,cpp,*headers,*sources],outputs=[exe,budget],timeout=300,resume=True)
    report=ROOT/'reports/B_standalone_builds.json';rows=json.loads(report.read_text())['variants'] if report.exists() else [];rows=[r for r in rows if r['label']!=a.label]+[{'label':a.label,'executable':str(exe),'sha256':sha(exe),'cache_lines':a.cache_lines,'cache_words':a.cache_words,'cache_ways':a.cache_ways,'mutant':a.mutant,'fault_fence':a.fault_fence,'pipeline':a.pipeline,'forward':a.forward,'predict':a.predict,'predict_jal':a.predict_jal,'predict_mode':2 if a.predict_jal else int(a.predict),'stream_fetch':a.stream_fetch,'fault_fence_flush':a.fault_fence_flush,'fault_raw':a.fault_raw}];dump(report,{'status':'BUILT_NOT_FUNCTIONALLY_ACCEPTED','variants':rows});print('B_STANDALONE_BUILT',a.label)

if __name__=='__main__':main()
