from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *


def main():
    builds=json.loads((ROOT/'reports/C5_soc_build.json').read_text())['variants']
    ref_report=json.loads((ROOT/'reports/C5_reference_build.json').read_text());assert ref_report['status'].startswith('PASS')
    ref=Path(ref_report['binary']);assert sha(ref)==ref_report['sha256']
    boot=json.loads((ROOT/'reports/C5_boot.json').read_text());rows=[]
    good=next(r for r in builds if r['reset_pc']==0x20000000 and not r.get('mutant',False) and not r.get('psram_qpi',False) and r.get('psram_bytes',4096)==4096 and not r.get('fast_flash',False) and not r.get('cycle_sim',False))
    bad=next(r for r in builds if r['reset_pc']==0x20000000 and r.get('mutant',False) and not r.get('fast_flash',False) and not r.get('cycle_sim',False))
    for name,program,build,extra,expected in [('first-ebreak','first-ebreak',good,[],0),('char-halt','char-halt',good,[],0),
            ('corrupt-reference-first-MROM','char-halt',good,['--corrupt-reference-rom'],1),('actual-RTL-ADDI-mutant','char-halt',bad,[],1)]:
        exe=Path(build['executable']);assert sha(exe)==build['sha256'];image=Path(boot['programs'][program]['binary']);assert sha(image)==boot['programs'][program]['binary_sha256']
        output=ROOT/'artifacts/C5/diff'/name;output.mkdir(parents=True,exist_ok=True);report=output/'simulation.json';trace=output/'events.log'
        text,err,_=run('C5/diff/'+name,[exe,'--mrom',image,'--ref',ref,'--report',report,'--trace',trace,*extra],inputs=[exe,image,ref],outputs=[report,trace],expected=(expected,))
        result=json.loads(report.read_text());assert result['diff_enabled'] and result['diff_checked']+result['device_sync_checked']==result['instructions']
        if expected==0:assert result['result']=='GOOD_TRAP' and result['diff_checked']>0
        else:
            assert result['result']=='DIFF_FAIL' and 'DIFF_GPR' in err and result['device_sync_checked']==0
            assert result['instructions']==(1 if extra else 2)
        rows.append({'name':name,'status':'PASS','result':result,'evidence':'artifacts/C5/diff/'+name})
    dump(ROOT/'reports/C5_diff.json',{'status':'PASS_RESTORED_MROM_DIFFERENTIAL_EXECUTION','runs':rows,
         'scope':'Every non-MMIO retired instruction executes in independently built NEMU; MMIO instruction effect is independently decoded and checked before reference state synchronization. No whole MROM/SRAM range skip. First-instruction reference ROM corruption and actual RTL arithmetic mutation are both rejected. SRAM program suite follows separately.'})
    print('C5_MROM_DIFF_RESTORED_WITH_BOTH_MUTANTS',flush=True)


if __name__=='__main__':main()
