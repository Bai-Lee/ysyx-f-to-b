from common import *
import argparse

def main():
    parser=argparse.ArgumentParser();parser.add_argument('component',choices=['capstone','spike']);args=parser.parse_args()
    if args.component=='capstone':
        source=BENCH/'nemu/tools/capstone/repo'
        run('D/dependencies/capstone_build',['make','-j1','CAPSTONE_ARCHS=riscv','CAPSTONE_BUILD_CORE_ONLY=yes','CAPSTONE_SHARED=yes'],cwd=source,inputs=[source/'Makefile'],outputs=[source/'libcapstone.so.5'],timeout=600)
        c=WORK/'capstone_smoke.c';c.write_text('#include <capstone/capstone.h>\n#include <assert.h>\n#include <string.h>\nint main(void){csh h;assert(cs_open(CS_ARCH_RISCV,CS_MODE_RISCV32,&h)==CS_ERR_OK);unsigned char good[]={0x13,0x05,0x10,0};cs_insn *i;size_t n=cs_disasm(h,good,4,0x80000000,1,&i);assert(n==1);assert(!strcmp(i[0].mnemonic,"addi")||!strcmp(i[0].mnemonic,"li"));cs_free(i,n);unsigned char bad[]={0xff,0xff,0xff,0xff};assert(cs_disasm(h,bad,4,0,1,&i)==0);cs_close(&h);return 0;}\n')
        exe=WORK/'capstone_smoke';run('D/dependencies/capstone_smoke_build',['gcc','-Wall','-Wextra','-Werror','-I'+str(source/'include'),c,'-L'+str(source),'-lcapstone','-Wl,-rpath,'+str(source),'-o',exe],inputs=[c,source/'libcapstone.so.5'],outputs=[exe])
        run('D/dependencies/capstone_smoke',[exe],inputs=[exe,source/'libcapstone.so.5'])
        dump(ROOT/'reports/D_capstone.json',{'status':'PASS','version':'5.0.6','commit':'accf4df62f1fba6f92cae692985d27063552601c','library':str(source/'libcapstone.so.5'),'sha256':sha(source/'libcapstone.so.5'),'architectures':['riscv'],'evidence':'artifacts/D/dependencies'})
    else:
        source=BENCH/'nemu/tools/spike-diff/repo';build=source/'build';build.mkdir(exist_ok=True)
        env={'CFLAGS':'-O2 -fPIC -fvisibility=hidden','CXXFLAGS':'-O2 -fPIC -fvisibility=hidden','MAKEFLAGS':'-j1'}
        env.update(json.loads((ROOT/'reports/D_spike_support.json').read_text())['env'])
        run('D/dependencies/spike_configure',[source/'configure','--prefix=/home/USER/tools/d-stage/spike','--without-boost'],cwd=build,env=env,inputs=[source/'configure'],timeout=180)
        names=['libspike_main.a','libriscv.a','libdisasm.a','libsoftfloat.a','libfesvr.a','libfdt.a']
        run('D/dependencies/spike_libraries',['make','-j1',*names],cwd=build,env=env,inputs=[build/'Makefile',source/'configure'],outputs=[build/x for x in names],timeout=7200)
        dump(ROOT/'reports/D_spike_build.json',{'status':'PASS_LIBRARIES_NOT_YET_API_TESTED','source':str(source),'commit':'b3cb1ef52ba0cb1bce84135febef1c4941c5455b','libraries':[{'path':str(build/x),'sha256':sha(build/x)} for x in names],'threads':1,'evidence':'artifacts/D/dependencies/spike_libraries'})

if __name__=='__main__':main()
