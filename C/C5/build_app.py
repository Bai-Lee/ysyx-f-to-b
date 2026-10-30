from pathlib import Path
import sys,argparse,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *


def compile_app(name,memory='sdram32',arguments=''):
    jobs=json.loads((ROOT/'reports/C5_app_setup.json').read_text())['jobs'];app=Path(jobs[name]['destination'])
    base=WORK/'c5/workbench';am=base/'abstract-machine';arch='riscv32e-ysyxsoc-'+memory
    product={'am-tests':'amtest','typing-game':'typing-game','fceux':'fceux'}.get(name,name)
    image=app/'build'/(product+'-'+arch+'.bin');elf=image.with_suffix('.elf');tag='C5/apps-build/'+name+'-'+memory
    inputs=[p for p in sorted(app.rglob('*')) if p.is_file() and not any(part in p.relative_to(app).parts for part in ['build','.git','__pycache__','gen'])]
    inputs += [*sorted((am/'am/src/riscv/ysyxsoc').glob('*')),am/'scripts'/('ysyxsoc-code-'+memory+'.ld')]
    run(tag,['make','-j1','ARCH='+arch,'mainargs='+arguments,'insert-arg'],cwd=app,env={'AM_HOME':str(am),'NPC_HOME':str(base/'npc')},inputs=inputs,outputs=[image,elf],timeout=600)
    assert image.is_file() and elf.is_file(),(name,product,list((app/'build').glob('*.bin')))
    text,_,_=run(tag+'-symbols',['riscv64-linux-gnu-nm','-n',elf],inputs=[elf]);symbols={v[2]:int(v[0],16) for line in text.splitlines() if len(v:=line.split())==3 and re.fullmatch('[0-9a-fA-F]+',v[0])}
    assert symbols['_start']==0x30000000 and 0xa0000000<=symbols['main']<0xa8000000 and symbols['_stack_pointer']==0x0f002000
    row={'name':name,'memory':memory,'arguments':arguments,'image':str(image),'elf':str(elf),'image_sha256':sha(image),'elf_sha256':sha(elf),'image_bytes':image.stat().st_size,'symbols':symbols,'evidence':'artifacts/'+tag}
    p=ROOT/'reports/C5_app_builds.json';rows=json.loads(p.read_text()).get('builds',[]) if p.exists() else []
    # Exact argument variants keep immutable images for later interaction/replay.
    frozen=WORK/'c5/app-images'/name/memory/(arguments.replace(' ','_') or 'empty');frozen.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(image,frozen/'image.bin');shutil.copyfile(elf,frozen/'image.elf');row['image']=str(frozen/'image.bin');row['elf']=str(frozen/'image.elf')
    rows=[r for r in rows if (r['name'],r['memory'],r['arguments'])!=(name,memory,arguments)]+[row]
    dump(p,{'status':'BUILT_NOT_RUNTIME_ACCEPTED','builds':rows})
    return row


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('name');parser.add_argument('--memory',choices=['sdram32','sdram64','sdram128'],default='sdram32');parser.add_argument('--arguments',default='');args=parser.parse_args()
    result=compile_app(args.name,args.memory,args.arguments)
    print('C5_APP_BUILT',result['name'],result['memory'],result['image_bytes'],result['image_sha256'],flush=True)
