from pathlib import Path
import sys,json,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    p=argparse.ArgumentParser();p.add_argument('--modes',default='1,2,3,4,5,6');a=p.parse_args()
    lock=json.loads((ROOT/'reports/C4_sim_build.json').read_text());prior_report=ROOT/'reports/C4_front.json';selected=list(map(int,a.modes.split(',')));rows=[r for r in json.loads(prior_report.read_text()).get('runs',[]) if r['mode'] not in selected] if prior_report.exists() else [];ref=WORK/'nemu-ref/build/riscv32-nemu-interpreter-so'
    image=ROOT/'D/D8/results/trace-rv32e.bin';elf=ROOT/'D/D8/results/trace-rv32e.elf'
    for mode in map(int,a.modes.split(',')):
        build=next(r for r in lock['variants'] if r['mode']==mode and not r['mutant']);exe=Path(build['executable']);assert sha(exe)==build['sha256']
        configs=[('normal',[])]
        if mode>=3:configs += [(f'latency{n}',['--latency',str(n)]) for n in (5,10,20)]
        if mode>=3:configs += [('random',['--random-delay','--core-delays','3'])]
        if mode>=4:configs += [('pressure',['--random-delay','--core-delays','7','--backpressure'])]
        for name,options in configs:
            d=ROOT/'artifacts/C4/front'/f'mode{mode}'/name;d.mkdir(parents=True,exist_ok=True);report=d/'result.json';trace=d/'commit.trace'
            run(f'C4/front/mode{mode}/'+name,[exe,'--image',image,'--elf',elf,'--ref',ref,'--report',report,'--trace',trace,'--trace-modes','imf','--max-cycles','10000',*options],inputs=[exe,ref,image,elf],outputs=[report,trace],timeout=30)
            r=json.loads(report.read_text());assert r['result']=='GOOD_TRAP' and r['instructions']==18 and r['diff_checked']==18 and r['device_sync_checked']==0 and r['ebreak_calls']==1
            assert r['gpr'][7]==43
            if mode==1 and name=='normal':assert r['cycles']==40,r # 18*2 + four post-halt checks
            if mode==2 and name=='normal':assert r['cycles']==44,r # four memory instructions add one each
            text=trace.read_text().splitlines();assert sum(s.startswith('I ') for s in text)==18 and sum(s.startswith('M ') for s in text)==4
            rows.append({'mode':mode,'config':name,'status':'PASS','simulation':r,'evidence':str(d.relative_to(ROOT))})
    dump(ROOT/'reports/C4_front.json',{'status':'PASS_SELECTED_MODES','modes':sorted({r['mode'] for r in rows}),'runs':rows,'scope':'Actual full RV32E control-flow/data program against independent NEMU. Backend separately validates observed bus transactions, not only RTL commit assertions. Full ISA/apps and interconnect units remain separate.'})
    print('C4_FRONT_PASS',len(rows),flush=True)

if __name__=='__main__':main()
