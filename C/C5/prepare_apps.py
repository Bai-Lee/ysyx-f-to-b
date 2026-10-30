from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *


def main():
    base=WORK/'c5/workbench';jobs={}
    for relative in ['kernels/hello','kernels/typing-game','kernels/snake','benchmarks/microbench','tests/am-tests']:
        origin=BENCH/'am-kernels'/relative;target=base/'am-kernels'/relative
        if not target.exists():shutil.copytree(origin,target,ignore=shutil.ignore_patterns('build','.git','__pycache__'))
        jobs[Path(relative).name]={'source':str(origin),'destination':str(target)}
    fceux=base/'fceux-am';origin=BENCH/'fceux-am'
    def ignore(path,names):
        excluded={'.git','build','__pycache__'}
        if Path(path).name=='nes':excluded|={'rom','gen'}
        return [n for n in names if n in excluded]
    if not fceux.exists():shutil.copytree(origin,fceux,ignore=ignore)
    rom=fceux/'nes/rom/interaction.nes';rom.parent.mkdir(exist_ok=True);shutil.copyfile(ROOT/'C/C2/homebrew/interaction.nes',rom)
    config=fceux/'src/config.h';text=config.read_text();text=text.replace('//#define HAS_GUI','#define HAS_GUI');config.write_text(text)
    jobs['fceux']={'source':str(origin),'destination':str(fceux),'rom':str(rom),'rom_sha256':sha(rom),'scope':'CC0 project interaction ROM only. Inherited C2 source includes Escape/Q exit; GUI enabled in this private C5 copy.'}
    gpio=base/'gpio-demo';gpio.mkdir(exist_ok=True);shutil.copyfile(ROOT/'C/C5/programs/gpio-demo.c',gpio/'main.c')
    (gpio/'Makefile').write_text('NAME = gpio-demo\nSRCS = main.c\ninclude $(AM_HOME)/Makefile\n')
    jobs['gpio-demo']={'source':str(ROOT/'C/C5/programs/gpio-demo.c'),'destination':str(gpio)}
    manifests={}
    for name,job in jobs.items():
        folder=Path(job['destination']);manifests[name]=[{'path':str(p.relative_to(folder)),'sha256':sha(p)} for p in sorted(folder.rglob('*')) if p.is_file() and not any(x in p.relative_to(folder).parts for x in ['build','.git','__pycache__'])]
    dump(ROOT/'reports/C5_app_setup.json',{'status':'PREPARED_NOT_EXECUTED','jobs':jobs,'files':manifests,'scope':'Selected original/C2-qualified app sources copied into C5. No prior project modified. No commercial game ROM copied into this runtime.'})
    print('C5_APPS_PREPARED',flush=True)


if __name__=='__main__':main()
