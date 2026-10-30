from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    n=BENCH/'nemu';exe=n/'build/riscv32-nemu-interpreter';ref=n/'tools/spike-diff/build/riscv32-spike-so';env=json.loads((ROOT/'reports/D7_build.json').read_text())['environment'];old=json.loads((ROOT/'reports/D3_official_tests.json').read_text());rows=[]
    out=ROOT/'D/D7/results/regression';out.mkdir(parents=True,exist_ok=True)
    for prior in old['programs']:
        suite=BENCH/('riscv-tests' if prior['suite']=='riscv' else 'am-kernels/tests/cpu-tests');image=suite/'build'/(prior['name']+'-riscv32-nemu.bin');assert sha(image)==prior['image_sha256']
        report=out/(prior['suite']+'-'+prior['name']+'.json')
        o,e,r=run('D7/regression/'+prior['suite']+'/'+prior['name'],[exe,'-b','-d',ref,'--report',report,image],cwd=n,env=env,inputs=[exe,ref,image],outputs=[report],timeout=180,resume=True)
        got=json.loads(report.read_text());expected=prior['simulation'];assert got['result']=='GOOD_TRAP' and got['gpr']==expected['gpr'] and got['instructions']==expected['instructions'] and got['diff_checked']+got['diff_skipped']==got['instructions']
        rows.append({'suite':prior['suite'],'name':prior['name'],'status':'PASS','result':got,'seconds':r['elapsed_seconds']})
        dump(ROOT/'reports/D7_regression.json',{'status':'IN_PROGRESS','rows':rows})
    dump(ROOT/'reports/D7_regression.json',{'status':'PASS','program_count':len(rows),'nemu_sha256':sha(exe),'spike_sha256':sha(ref),'rows':rows,'scope':'Re-executed every D3 official image after trace integration; exact final registers and instruction counts checked against earlier results, each ordinary instruction compared with Spike.'})

if __name__=='__main__':main()
