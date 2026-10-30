"""Prove the generated lint normalization preserves the sequential design."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    folder=ROOT/'B/B5/export';raw=folder/'unsanitized.sv';final=ROOT/'B/soc/build/ysyx_00000000.sv'
    script=folder/'equivalence.ys';body=''
    for name,source in [('gold',raw),('gate',final)]:
        body+='read_verilog -sv '+str(source)+'\nprep -top ysyx_00000000 -flatten\nmemory_map\nopt\nrename ysyx_00000000 '+name+'\ndesign -stash '+name+'\n'
    body+='design -copy-from gold -as gold gold\ndesign -copy-from gate -as gate gate\nequiv_make gold gate equiv\nhierarchy -top equiv\nequiv_simple\nequiv_induct -seq 2\nequiv_status -assert\n'
    script.write_text(body)
    yosys=Path('/home/USER/tools/e-stage/oss-20260821/oss-cad-suite/bin/yosys');budget=ROOT/'artifacts/B5/export/equivalence/budget.json'
    output,error,_=run('B5/export/equivalence',['python3',ROOT/'B/runtime/budget_exec.py','--report',budget,'--',yosys,'-s',script],inputs=[yosys,raw,final,script],outputs=[budget],timeout=600)
    assert 'Equivalence successfully proven!' in output
    dump(ROOT/'reports/B5_export_equivalence.json',{'status':'PASS','raw_rtl_sha256':sha(raw),'exported_rtl_sha256':sha(final),'scope':'Yosys equiv_make/equiv_simple/equiv_induct proves all equivalence cells between preprocessed accepted RTL and lint-normalized export. Same input ports and paired sequential states; temporal induction proves they remain aligned after matching observable states. Common-reset simulations check startup. This is translation equivalence, not a proof of the CPU ISA or independent end-to-end correctness.','evidence':'artifacts/B5/export/equivalence'})
    print('B5_EXPORT_EQUIVALENCE_PASS')

if __name__=='__main__':main()
