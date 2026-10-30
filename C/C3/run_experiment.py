"""Small reproducible debugging exercise: same assertion, real watchpoint."""
from pathlib import Path
import sys,re,signal
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
recorded_run=run
def run(*args,**kwargs):
    kwargs.setdefault('resume',True)
    return recorded_run(*args,**kwargs)

def main():
    d=ROOT/'C/C3';out=d/'results';out.mkdir(exist_ok=True)
    slide=ARCHIVE/'slides/markdown/2306/1dbf54f914088a36.md'
    toolrows=[]
    for name in ['gcc','gdb']:
        p=Path(shutil.which(name));o,e,_=run('C3/tools/'+name,[p,'--version'],inputs=[p],cwd=out)
        toolrows.append({'name':name,'path':str(p),'sha256':sha(p),'version':(o+e).splitlines()[0]})
    dump(ROOT/'reports/C3_PREFLIGHT.json',{'status':'READY_FOR_BOUNDED_BACKGROUND_EXPERIMENT','core_tasks':0,'tools':toolrows,'capabilities':['debug-symbol compilation','batch GDB watchpoint/backtrace'],'budget':'Sequential light native jobs; no large NEMU/RTL build. Core dumps disabled for the deliberately rejected mutant.','source':str(slide),'source_sha256':sha(slide)})
    executables={}
    for kind,flag in [('correct',0),('mutant',1)]:
        exe=out/kind;executables[kind]=exe
        run('C3/debug/build-'+kind,['gcc','-std=c11','-O0','-g3','-fno-omit-frame-pointer','-Wall','-Wextra','-Werror','-DINJECT_FAULT='+str(flag),d/'sum_debug.c','-o',exe],inputs=[d/'sum_debug.c'],outputs=[exe],cwd=out)
    o,_,_=run('C3/debug/correct',[executables['correct']],inputs=[executables['correct']],cwd=out);assert o=='SUM_RESULT=15 expected=15\n'
    o,e,negative=run('C3/debug/mutant',[executables['mutant']],inputs=[executables['mutant']],expected=(-signal.SIGABRT,),cwd=out)
    assert 'SUM_RESULT=16 expected=15' in o and 'result == 15' in e
    o,e,_=run('C3/debug/gdb-watchpoint',['gdb','-nx','-nh','-q','-batch','-x',d/'watch_mutant.gdb','--args',executables['mutant']],inputs=[executables['mutant'],d/'watch_mutant.gdb',d/'sum_debug.c'],cwd=out,timeout=45)
    assert 'FIRST_BAD_PREFIX=11 INDEX=3 DELTA=5' in o
    changes=re.findall(r'New value = (\d+)',o);assert changes[:4]==['1','3','6','11'],changes
    assert 'SIGABRT' in o and 'sum_sequence' in o and 'main' in o and 'result == 15' in e
    (out/'watchpoint-transcript.txt').write_text(o+e)
    dump(ROOT/'reports/C3_experiment.json',{'status':'PASS_BOUNDED_BACKGROUND_EXPERIMENT','course_record':'C3-O001','core_tasks':0,'source':str(slide),'source_sha256':sha(slide),'expected_prefix_sums':[1,3,6,10,15],'observed_mutant_watch_values':list(map(int,changes[:4])),'first_divergence':{'zero_based_index':3,'expected_prefix':10,'actual_prefix':11,'observed_increment':5},'correct_result':15,'mutant_result':16,'mutant_exit':negative['exit_code'],'gdb_observed_SIGABRT':True,'tools':toolrows,'evidence':['artifacts/C3/debug','C/C3/results/watchpoint-transcript.txt'],'limits':['One deterministic native host defect with -O0 debug variables; not a claim all GDB/RTL/optimized-variable scenarios are covered.','No perf sampling, reverse execution, multithread race analysis or new large CPU regression.','Initial watchpoint script tried to read a block-local term outside its debug scope; failure preserved. Final script observes the actual state delta and mixed source disassembly.']})
    print('C3_BACKGROUND_EXPERIMENT_PASS',flush=True)

if __name__=='__main__':main()
