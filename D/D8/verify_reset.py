from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
d=ROOT/'D/D8';iv=Path('/home/USER/tools/e-stage/oss-20261022/oss-cad-suite/bin');rtl=d/'rv32e_core.sv';tb=d/'reset_tb.sv'
for name,source,expected in [('normal',rtl,0),('mutant',d/'results/bad_reset.sv',1)]:
    if name=='mutant':source.write_text(rtl.read_text().replace('r[j]<=0;','r[j]<=1;'))
    exe=WORK/'build'/('rv32e-reset-'+name)
    run('D8/reset/'+name+'-build',[iv/'iverilog','-g2012','-s','tb','-o',exe,source,tb],inputs=[source,tb],outputs=[exe])
    o,e,_=run('D8/reset/'+name,[iv/'vvp',exe],inputs=[exe],expected=(expected,))
    assert ('RESET_PASS' in o) if not expected else ('RESET_REGISTER' in o)
dump(ROOT/'reports/D8_reset.json',{'status':'PASS','scope':'Actual four-state Icarus simulation of initial and warm reset, clearing dirty registers, halted state and fault, plus wrong-reset-value negative control. No analog metastability claim.','rtl_sha256':sha(rtl),'testbench_sha256':sha(tb)})
