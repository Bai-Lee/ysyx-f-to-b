from pathlib import Path
import sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--build',action='store_true');args=parser.parse_args()
    origin=ARCHIVE/'repos/NJU-ProjectN__nvboard__master';commit=(origin/'.git/HEAD').read_text().strip();assert commit=='b5f49b68a85f4a1a185086cbd6532fff3ecda454'
    target=WORK/'c5/nvboard'
    if not target.exists():shutil.copytree(origin,target,ignore=shutil.ignore_patterns('.git','build','__pycache__'))
    event=(origin/'src/event.cpp').read_text();assert event.count('exit(0);')==2
    event='static bool c5_close_requested=false;\nbool c5_nvboard_should_close(){return c5_close_requested;}\n'+event.replace('exit(0);','c5_close_requested=true; return;')
    (target/'src/event.cpp').write_text(event)
    uart=(origin/'src/uart.cpp').read_text();assert 'divisor(16)' in uart
    observers='''#include <cstdio>
#include <cstdlib>
static FILE *c5_open_log(const char *name){
  const char *path=std::getenv(name);if(!path)return nullptr;
  FILE *f=std::fopen(path,"wb");if(!f){std::perror(name);std::abort();}return f;
}
static void c5_uart_decoded(unsigned char value){
  static FILE *f=c5_open_log("C5_NVBOARD_TX_LOG");if(f){if(std::fwrite(&value,1,1,f)!=1)std::abort();std::fflush(f);}
}
static void c5_uart_input(unsigned char value){
  static FILE *f=c5_open_log("C5_NVBOARD_RX_LOG");if(f){if(std::fwrite(&value,1,1,f)!=1)std::abort();std::fflush(f);}
}
'''
    uart=observers+uart.replace('term->feed_ch(tx_data);','term->feed_ch(tx_data);\n      c5_uart_decoded(tx_data);').replace('rx_sending_str += ch;','c5_uart_input(ch);\n  rx_sending_str += ch;')
    (target/'src/uart.cpp').write_text(uart)
    bind=WORK/'c5/nvboard_bind.cpp';constraints=ROOT/'C/C5/constr/soc.nxdc'
    run('C5/nvboard/bind',['python3',target/'scripts/auto_pin_bind.py',constraints,bind],inputs=[constraints,target/'scripts/auto_pin_bind.py'],outputs=[bind],env={'NVBOARD_HOME':str(target)})
    files=[p for p in sorted(target.rglob('*')) if p.is_file() and not any(x in p.relative_to(target).parts for x in ['build','.git','__pycache__'])]
    if args.build:
        run('C5/nvboard/build',['make','-f',target/'scripts/nvboard.mk','-j1','nvboard-archive'],cwd=WORK,env={'NVBOARD_HOME':str(target)},inputs=files,outputs=[target/'build/nvboard.a'],timeout=240,resume=True)
    dump(ROOT/'reports/C5_nvboard_setup.json',{'status':'LIBRARY_BUILT_NOT_GUI_ACCEPTED' if args.build else 'SOURCES_PREPARED_NOT_BUILT','source':str(origin),'source_commit':commit,'workbench':str(target),'uart_cycles_per_bit':16,'uart16550_dll':1,'patch_scope':'Original NVBoard decoding/rendering. Passive binary logs after actualTXdecode and beforeRXqueue insertion. Native window close requests return to the host for evidence finalization instead of exit(0). No synthetic keyboard/UART data injected by these patches.','files':[{'path':str(p.relative_to(target)),'sha256':sha(p)} for p in files],'binding':{'path':str(bind),'sha256':sha(bind)},'constraint_sha256':sha(constraints)})
    print('C5_NVBOARD_PREPARED',flush=True)


if __name__=='__main__':main()
