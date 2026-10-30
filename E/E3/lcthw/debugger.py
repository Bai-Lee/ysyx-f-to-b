from native import *
import subprocess,time,shutil
def main():
    original=write('ex31_original.c',block(31));exe,_,_=build('ex31_original',files=[original])
    line=next(i+1 for i,s in enumerate(original.read_text().splitlines()) if 'usleep(3000)' in s)
    args=['gdb','--batch','-q','-ex','set pagination off','-ex',f'break {original}:{line}','-ex','run','-ex','print i','-ex','continue','-ex','print i','-ex','set var i=200','-ex','print i','-ex','delete breakpoints','-ex','continue',str(exe)]
    o,e,r=run('debugger/launched',args,inputs=[original,exe],timeout=20)
    assert re.findall(r'\$\d+ = (\d+)',o)==['0','0','200'] and 'exited normally' in o
    verdict(['LCT-31-BASE'],'PASS',['debugger/launched'],'Original nonprogress loop observed twice in actual GDB; setting i200 causes normal exit. Source is not incorrectly called a normally terminating program.')
    # Authorize only the particular debugger PID, without changing ptrace_scope.
    attachsrc=write('ex31_attach.c',r'''#include <unistd.h>
#include <sys/prctl.h>
#include <stdio.h>
#include <errno.h>
int main(int argc,char **argv){
    int debugger_pid;if(argc!=2||scanf("%d",&debugger_pid)!=1)return 2;
    if(prctl(PR_SET_PTRACER,debugger_pid,0,0,0)){
        if(errno!=EINVAL || access("/proc/sys/kernel/yama/ptrace_scope",F_OK)==0)return 3;
    }
    FILE *ready=fopen(argv[1],"w");if(!ready)return 4;fputs("ready",ready);fclose(ready);
    int i=0;
    while(i<100){
        usleep(3000);
    }
    return 0;
}
''')
    ax,_,_=build('ex31_attach',files=[attachsrc]);ready=common.LAB/'attach.ready'
    if ready.exists():ready.unlink()
    target=subprocess.Popen([str(ax),str(ready)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    line=next(i+1 for i,s in enumerate(attachsrc.read_text().splitlines()) if 'usleep(3000)' in s)
    commands=write('attach.gdb',f'''set pagination off
shell while [ ! -f {ready} ]; do sleep 0.01; done
attach {target.pid}
break {attachsrc}:{line}
continue
print i
set var i=200
print i
delete breakpoints
continue
quit
''')
    outpath=common.OUT/'debugger/attached';outpath.mkdir(parents=True,exist_ok=True)
    try:
        with (outpath/'stdout.log').open('wb') as out,(outpath/'stderr.log').open('wb') as err:
            debug_env=os.environ.copy();debug_env.update(SHELL='/bin/bash',LC_ALL='C')
            debugger=subprocess.Popen(['gdb','--batch','-q',str(ax),'-x',str(commands)],stdout=out,stderr=err,env=debug_env,start_new_session=True)
            target.stdin.write((str(debugger.pid)+'\n').encode());target.stdin.flush();target.stdin.close()
            rc=debugger.wait(timeout=20);assert rc==0
            assert target.wait(timeout=5)==0
        text=(outpath/'stdout.log').read_text()
        assert re.findall(r'\$\d+ = (\d+)',text)==['0','200'] and 'exited normally' in text
        dump(outpath/'run.json',{'status':'PASS','command':['gdb','--batch','-q',str(ax),'-x',str(commands)],'target_started_before_debugger':True,'target_pid':target.pid,'debugger_pid':debugger.pid,'yama_present':Path('/proc/sys/kernel/yama/ptrace_scope').exists(),'ptrace_permission':'Specific debugger PID opt-in where Yama exists; standard same-user policy when kernel has no Yama. No global policy change.','source_sha256':sha(attachsrc),'binary_sha256':sha(ax),'command_file_sha256':sha(commands),'stdout_sha256':sha(outpath/'stdout.log'),'stderr_sha256':sha(outpath/'stderr.log')})
    finally:
        if target.poll() is None:target.terminate();target.wait(timeout=5)
        if 'debugger' in locals() and debugger.poll() is None:os.killpg(debugger.pid,9);debugger.wait(timeout=5)
    verdict(['LCT-31-X01'],'PASS_ADAPTED',['debugger/attached'],'Actual attach to an already-running target; no global ptrace changes. Current kernel lacks Yama, so ordinary same-user permission applies; portable test supports per-debugger opt-in when present.')
    crash=write('ex31_crash.c',r'''#include <unistd.h>
int main(void){
    int i=0;
    while(i<10){
        usleep(3000);
        if(i==5){*(volatile int *)0=7;}
        ++i;
    }
    return 0;
}
''')
    cx,_,_=build('ex31_crash',files=[crash]);core=common.OUT/'debugger/controlled.core'
    o,e,r=run('debugger/core_generate',['gdb','--batch','-q','-ex','set pagination off','-ex','set exec-wrapper env -i PATH=/usr/bin:/bin LC_ALL=C','-ex','run','-ex','print i','-ex','generate-core-file '+str(core),str(cx)],inputs=[crash,cx],timeout=30)
    assert 'SIGSEGV' in o and re.search(r'\$1 = 5\b',o) and core.exists()
    o,e,r=run('debugger/core_analyze',['gdb','--batch','-q',str(cx),str(core),'-ex','bt','-ex','frame 0','-ex','print i'],inputs=[crash,cx,core],timeout=30)
    assert 'SIGSEGV' in o and re.search(r'\$1 = 5\b',o)
    verdict(['LCT-31-X03'],'PASS_ADAPTED',['debugger/core_generate','debugger/core_analyze'],'Actual crash at iteration5, real ELF core generated from stopped inferior and analyzed separately. Debugger-generated core avoids changing global core_pattern; inferior environment cleared of unrelated credentials.')
    verdict(['LCT-31-X02'],'PASS_DOCUMENTED',[],'VS Code C/C++ graphical debugger identified from official documentation; comparison with actual CLI GDB in notes. GUI capabilities are documentation-based, not falsely labeled as GUI runtime-tested.')
    print('DEBUGGER_EXERCISE_DONE',flush=True)
if __name__=='__main__':main()
