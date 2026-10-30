from pathlib import Path
import sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    p=argparse.ArgumentParser();p.add_argument('--modes',default='1,2,3,4,5,6');p.add_argument('--mutant',action='store_true');a=p.parse_args()
    d=ROOT/'C/C4';sim=d/'sim';cap=BENCH/'nemu/tools/capstone/repo'
    for script in ('make_sim_top.py','make_runner.py'):subprocess.run(['python3',str(d/script)],check=True)
    objects=[];base=WORK/'c4/build/common';base.mkdir(parents=True,exist_ok=True)
    for name in ('debug_core','trace_core'):
        source=ROOT/'C/runtime'/(name+'.c');obj=base/(name+'.o')
        run('C4/build/'+name,['gcc','-std=c11','-O3','-g','-Wall','-Wextra','-Werror','-I',ROOT/'C/runtime','-c',source,'-o',obj],inputs=[source,ROOT/'C/runtime'/(name+'.h')],outputs=[obj],resume=True);objects.append(obj)
    rows=[];report=ROOT/'reports/C4_sim_build.json'
    if report.exists():rows=json.loads(report.read_text())['variants']
    rtl=sorted((d/'rtl').glob('*.sv'))
    for mode in map(int,a.modes.split(',')):
        assert 1<=mode<=6;tag=f'mode{mode}'+('-mutant' if a.mutant else '');out=WORK/'c4/build'/tag;out.mkdir(parents=True,exist_ok=True);exe=out/'sim'
        cmd=[VERILATOR,'--cc','--exe','--build','-j','1','--assert','-Wall','-Wno-UNUSEDSIGNAL','-Wno-PINCONNECTEMPTY','--top-module','c4_sim','--timescale','1ns/1ns','-GMODE='+str(mode),'-GFAULT_ADDI='+str(int(a.mutant)),'--Mdir',out,'-o','sim','-CFLAGS',f'-O3 -g -Wall -Wextra -Werror -DC4_MODE={mode} -I{sim} -I{ROOT/"C/runtime"} -I{cap/"include"}','-LDFLAGS',f'-L{cap} -l:libcapstone.so.5 -Wl,-rpath,{cap} -ldl',*rtl,sim/'c4_sim.sv',sim/'runner.cpp',*objects]
        inputs=[*rtl,*sim.glob('*'),*objects,cap/'libcapstone.so.5']
        run('C4/build/'+tag,cmd,inputs=inputs,outputs=[exe],timeout=300,resume=True)
        row={'tag':tag,'mode':mode,'mutant':a.mutant,'executable':str(exe),'sha256':sha(exe),'inputs':[{'path':str(x),'sha256':sha(x)} for x in inputs]}
        rows=[x for x in rows if x['tag']!=tag]+[row]
        dump(report,{'status':'BUILT_NOT_YET_QUALIFIED','variants':rows})
    print('C4_SIM_BUILD_FINISHED',flush=True)

if __name__=='__main__':main()
