#include <unistd.h>
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
