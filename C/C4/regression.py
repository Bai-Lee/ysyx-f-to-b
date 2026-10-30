from pathlib import Path
import sys,json,zipfile,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    p=argparse.ArgumentParser();p.add_argument('--modes',default='1,2,3,4,5,6');a=p.parse_args()
    builds=json.loads((ROOT/'reports/C4_sim_build.json').read_text())['variants'];ref=WORK/'nemu-ref/build/riscv32-nemu-interpreter-so';fixtures=WORK/'c4/fixtures';fixtures.mkdir(parents=True,exist_ok=True)
    old=json.loads((ROOT/'reports/D8_official_tests.json').read_text());cases=[]
    for row in old['programs']:
        base=fixtures/row['suite']/row['name'];base.mkdir(parents=True,exist_ok=True)
        snapshot=ROOT/row['evidence']/'output_snapshot.zip'
        with zipfile.ZipFile(snapshot) as z:
            for ext in ('bin','elf'):
                member=next(n for n in z.namelist() if n.endswith('.'+ext));dest=base/('program.'+ext)
                payload=z.read(member)
                if dest.exists():assert dest.read_bytes()==payload
                else:dest.write_bytes(payload)
        assert sha(base/'program.bin')==row['image_sha256'] and sha(base/'program.elf')==row['elf_sha256']
        cases.append((row['suite']+'-'+row['name'],base/'program.bin',base/'program.elf',row))
    # The independent 1758-check RV32E boundary program also has its own NEMU oracle.
    isa=json.loads((ROOT/'reports/D8_isa.json').read_text());d8=ROOT/'D/D8/results'
    image=next(p for p in d8.rglob('*.bin') if sha(p)==isa['binary_sha256'])
    elf=next(p for p in d8.rglob('*.elf') if sha(p)==isa['elf_sha256'])
    selected=list(map(int,a.modes.split(',')))
    prior_report=ROOT/'reports/C4_regression.json'
    rows=[r for r in json.loads(prior_report.read_text()).get('runs',[]) if r['mode'] not in selected] if prior_report.exists() else []
    for mode in map(int,a.modes.split(',')):
        build=next(b for b in builds if b['mode']==mode and not b['mutant']);exe=Path(build['executable']);assert sha(exe)==build['sha256']
        extras=['--random-delay','--core-delays','7','--backpressure'] if mode in (4,6) else []
        for name,binary,symbols,prior in [('boundaries1758',image,elf,None),*cases]:
            path=ROOT/'artifacts/C4/regression'/f'mode{mode}'/name;path.mkdir(parents=True,exist_ok=True);report=path/'result.json'
            _,_,r=run(f'C4/regression/mode{mode}/'+name,[exe,'--image',binary,'--elf',symbols,'--ref',ref,'--report',report,'--max-cycles','5000000000',*extras],inputs=[exe,ref,binary,symbols],outputs=[report],timeout=600,resume=True)
            result=json.loads(report.read_text());assert result['result']=='GOOD_TRAP' and result['diff_enabled'] and result['diff_checked']+result['device_sync_checked']==result['instructions'] and result['ebreak_calls']==1
            if prior:
                assert result['gpr']==prior['simulation']['gpr'] and result['pc']==prior['simulation']['pc'] and result['instructions']==prior['simulation']['instructions'],(name,mode)
            rows.append({'mode':mode,'name':name,'status':'PASS','image_sha256':sha(binary),'elf_sha256':sha(symbols),'simulation':result,'seconds':r['elapsed_seconds']})
            dump(ROOT/'reports/C4_regression.json',{'status':'IN_PROGRESS','runs':rows})
    dump(ROOT/'reports/C4_regression.json',{'status':'PASS_SELECTED_MODES','modes':sorted({r['mode'] for r in rows}),'programs_per_mode':74,'independent_boundary_checks':1758,'official_programs':73,'runs':rows,'source_scope':'Exact accepted RV32E ELF/binary bytes recovered from D output snapshots, whose original source/ABI hashes remain locked. C4 changes bus timing, not application semantics. MicroBench train is rebuilt separately for performance. Modes4/6 include random memory/core delays and backpressure.'})
    print('C4_REGRESSION_PASS',len(rows),flush=True)

if __name__=='__main__':main()
