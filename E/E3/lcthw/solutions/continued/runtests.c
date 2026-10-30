#include <dirent.h>
#include <stdio.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
int main(void){DIR*d=opendir("tests");if(!d)return 2;struct dirent*e;int found=0;while((e=readdir(d))){size_t n=strlen(e->d_name);if(n<6||strcmp(e->d_name+n-6,"_tests"))continue;char p[512];if(snprintf(p,sizeof p,"tests/%s",e->d_name)>=(int)sizeof p){closedir(d);return 2;}found=1;pid_t child=fork();if(child<0){closedir(d);return 2;}if(!child){execl(p,p,(char*)0);_exit(127);}int status;if(waitpid(child,&status,0)<0||!WIFEXITED(status)||WEXITSTATUS(status)!=0){closedir(d);return 1;}}closedir(d);return found?0:1;}
