from pathlib import Path
import sys,urllib.request,re,os,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--interactive',action='store_true');args=parser.parse_args()
    source=ROOT/'C/C5/rtthread';tool=Path('/home/USER/tools/scons-4.0.1');package=Path('/workspace/downloads/scons_4.0.1+dfsg-2_all.deb')
    url='https://archive.ubuntu.com/ubuntu/pool/universe/s/scons/scons_4.0.1+dfsg-2_all.deb'
    digest='d451de7060ea2f2eed75fb8ac55a37df680a678ffaeaa2e8be44ce36ad575f6d'
    text,_,_=run('C5/rtthread/scons-package-metadata',['apt-cache','show','scons=4.0.1+dfsg-2'])
    assert 'SHA256: '+digest in text
    if not package.exists():
        with urllib.request.urlopen(url,timeout=60) as response,package.open('wb') as output:shutil.copyfileobj(response,output)
    assert sha(package)==digest
    if not (tool/'usr/lib/python3/dist-packages/SCons').exists():
        tool.mkdir(parents=True,exist_ok=True)
        run('C5/rtthread/scons-extract',['dpkg-deb','-x',package,tool],inputs=[package])
    (tool/'bin').mkdir(exist_ok=True)
    wrapper=tool/'bin/scons';wrapper.write_text('#!/usr/bin/python3\nimport sys\nsys.path.insert(0,"'+str(tool/'usr/lib/python3/dist-packages')+'")\nimport SCons.Script\nSCons.Script.main()\n');wrapper.chmod(0o755)
    run('C5/rtthread/scons-version',[wrapper,'--version'],inputs=[wrapper,package])
    origin=ARCHIVE/'repos/NJU-ProjectN__rt-thread-am__master';destination=WORK/'c5'/('rt-thread-interactive' if args.interactive else 'rt-thread-am')
    # The archive is a detached, locked checkout. Read its recorded HEAD without changing Git trust settings.
    commit=(origin/'.git/HEAD').read_text()
    assert commit.strip()=='72ba231bb79db53f1c07920f2642ef20679faeff'
    if not destination.exists():shutil.copytree(origin,destination,ignore=shutil.ignore_patterns('.git','build','__pycache__'))
    bsp=destination/'bsp/abstract-machine'
    for name in ['context.c','interrupt.c','libc.c','acceptance.c']:shutil.copyfile(source/name,bsp/'src'/name)
    uart=(origin/'bsp/abstract-machine/src/uart.c').read_text()
    if args.interactive:
        uart=uart.replace("return (*p != '\\0' ? *(p ++) : -1);","if (*p != '\\0') return *(p++);\n  unsigned char value=io_read(AM_UART_RX).data;\n  return value==255 ? -1 : value;")
        assert 'io_read(AM_UART_RX)' in uart
    else:
        uart=uart.replace('memcheck\\nutest_list\\n','memcheck\\nutest_list\\nc5_context_test\\nc5_done\\n')
        assert 'c5_context_test' in uart
    (bsp/'src/uart.c').write_text(uart)
    # These tables are inside the copy/zero spans of the C5 linker script.
    (bsp/'extra.ld').write_text('/* RT-Thread tables and AM-app sections are integrated in the C5 relocation linker script. */\n')
    # The upstream loop halves size even after a successful allocation; retain its actual size.
    init=(origin/'bsp/abstract-machine/src/init.c').read_text()
    init=init.replace('for (; p == NULL && size != 0; size /= 2) { p = rt_malloc(size); }','while (size != 0 && (p = rt_malloc(size)) == NULL) { size /= 2; }\n  assert(p != NULL);')
    (bsp/'src/init.c').write_text(init)
    arch='riscv32e-ysyxsoc-psram';build=bsp/'build'/arch;build.mkdir(parents=True,exist_ok=True)
    if not (build/'am-apps.mk').exists():(build/'am-apps.mk').write_text('# Boot/context acceptance profile; AM applications are integrated in a later profile.\n')
    base=WORK/'c5/workbench';am=base/'abstract-machine'
    environment={'AM_HOME':str(am),'NPC_HOME':str(base/'npc'),'PATH':str(tool/'bin')+':'+os.environ['PATH']}
    subprocess.run(['python3',str(ROOT/'C/C5/prepare_am.py')],check=True)
    inputs=[p for p in sorted((bsp/'src').glob('*')) if p.is_file()]+[bsp/'Makefile',bsp/'SConstruct',bsp/'.config',bsp/'extra.ld']
    run('C5/rtthread/make-init',['make','-j1','ARCH='+arch,'init'],cwd=bsp,env=environment,inputs=inputs,outputs=[bsp/'files.mk',bsp/'rtconfig.h'],timeout=180)
    dump(ROOT/('reports/C5_rtthread_interactive_setup.json' if args.interactive else 'reports/C5_rtthread_setup.json'),{'status':'PREPARED_NOT_EXECUTED','source_commit':commit.strip(),'source':str(origin),'workbench':str(destination),
        'scons':{'version':'4.0.1+dfsg-2','url':url,'package':str(package),'sha256':digest,'verification':'Compared with SHA256 in the installed Ubuntu apt package index. Portable extraction; no system install.','wrapper':str(wrapper)},
        'patches':[{'path':str(p),'sha256':sha(p)} for p in inputs],
        'scope':'Original RT-Thread kernel and built-in scripted shell commands. Added real single-CPU synchronous context switching, interrupt state restoration, thread-return validation. Polling without asynchronous interrupts; integrated AM applications not yet tested.'})
    print('C5_RTTHREAD_PREPARED',flush=True)


if __name__=='__main__':main()
